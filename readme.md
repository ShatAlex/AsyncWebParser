# Async Web Parser

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beautifulsoup4)
![PyPI](https://img.shields.io/pypi/v/beautifulsoup4?label=beautifulsoup4&color=purple)
![PyPI](https://img.shields.io/pypi/v/aiohttp?label=aiohttp&color=yellow)
![PyPI](https://img.shields.io/pypi/v/asyncio?label=asyncio&color=green)

### Actual business benefit

A small project designed to get data from the hotels website. It can be useful for aggregator sites, data analysis, or database formation.

___

### Input parsing object

The hotel aggregator site [tury.ru](https://www.tury.ru/hotel/) was chosen as the object for parsing.The site includes detailed pages about each of the 1.5 million hotels in the world.

![Site page](https://github.com/ShatAlex/AsyncWebParser/blob/master/ReadMeImages/site_page.png)

___

### Parser Output parameters

For each hotel, the program receives:
+ name
+ rating
+ size of the hotel
+ description
+ location. 

Provides the received data in **_csv_** and **_json_** format.
