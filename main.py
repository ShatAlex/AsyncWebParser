import csv
import datetime
import time

from bs4 import BeautifulSoup
import asyncio
import aiohttp
import json

hotels_lst = []
open('hotels.txt', 'w').close()

async def get_hotels_urls(session, page):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 YaBrowser/23.1.4.778 Yowser/2.5 Safari/537.36',
        "accept": "*/*"
    }
    url = f'https://www.tury.ru/hotel/?cn=0&ct=0&cat=0&txt_geo=&srch=&s={page}'
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        cards = soup.find_all('div', class_='reviews-travel__item')
        with open(f'hotels.txt', 'a') as file:
            for card in cards:
                link = card.find('a').get('href')
                file.write(link + '\n')
        print(f'[INFO] Обработано {page} ссылок')


async def gather_urls():
    async with aiohttp.ClientSession() as session:
        tasks = []

        for page in range(0, 200, 20):  # 1595460
            task = asyncio.create_task(get_hotels_urls(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_hotels_data(session, url, sch):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/108.0.0.0 YaBrowser/23.1.4.778 Yowser/2.5 Safari/537.36',
        "accept": "*/*"
    }

    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')

        try:
            hotel_name = soup.find('div', class_='h1').text.strip()
        except Exception as ex:
            hotel_name = None

        try:
            hotel_rank = soup.find('div', class_='hotel-rating__wrapp').find('span').text
        except Exception as ex:
            hotel_rank = None

        try:
            hotel_location = soup.find('img', src="/_img2/icon/marker-map.svg").find_next().text.strip()
        except Exception as ex:
            hotel_location = None

        try:
            hotel_description = soup.find_all('div', class_='hotel__text')[0].text.strip()
        except Exception as ex:
            hotel_description = None

        try:
            hotel_area = soup.find('b', string='Размер объекта').find_next().text.strip()
        except Exception as ex:
            hotel_area = None

        try:
            in_rooms = ''
            things = soup.find('b', string='В номерах').find_previous().find_previous().find_all('span')
            for thing in things:
                in_rooms += thing.text.strip() + ', '
            in_rooms = in_rooms[:-2]
        except Exception as ex:
            in_rooms = None

        hotels_lst.append(
            {
                'hotel_name': hotel_name,
                'hotel_rank': hotel_rank,
                'hotel_location': hotel_location,
                'hotel_description': hotel_description,
                'hotel_area': hotel_area,
                'in_rooms': in_rooms
            }
        )
        print(f'[INFO] Отель №{sch} записан. URL: {url}')


async def gather_data():
    async with aiohttp.ClientSession() as session:
        tasks = []
        sch = 1
        with open(f'hotels.txt') as file:
            url_lst = [url.strip() for url in file.readlines()]
        for url in url_lst:
            task = asyncio.create_task(get_hotels_data(session, url, sch))
            tasks.append(task)
            sch += 1
        await asyncio.gather(*tasks)


def main():
    start_time = time.time()
    asyncio.run(gather_urls())
    asyncio.run(gather_data())

    cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')

    with open(f'hotels_{cur_time}.json', 'w', encoding='utf-8') as file:
        json.dump(hotels_lst, file, indent=4, ensure_ascii=False)

    for hotel in hotels_lst:
        with open(f'hotels_{cur_time}.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    hotel['hotel_name'],
                    hotel['hotel_rank'],
                    hotel['hotel_location'],
                    hotel['hotel_description'],
                    hotel['hotel_area'],
                    hotel['in_rooms'],
                )
            )
    finish_time = time.time() - start_time
    print(f'Затраченное время: {finish_time}')


if __name__ == '__main__':
    main()
