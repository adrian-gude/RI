import scrapy
from bs4 import BeautifulSoup
  
  
class HotelsSpider(scrapy.Spider):
    
    # name of variable should be 'name' only
    name = "hotels" 
  
    # urls from which will be used to extract information
    # list should be named 'start_urls' only
    start_urls = [
        'https://www.tripadvisor.es/Hotels',
        #'https://www.tripadvisor.es/Hotels-g187506-Galicia-Hotels.html',
        #'https://www.tripadvisor.es/Hotels-g187506-oa30-Galicia-Hotels.html',
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        lista_hoteles = soup.find_all('div', class_='ui_shelf_item_detail')

        for hotel in lista_hoteles:
            #Coger el nombre del hotel
            name = hotel.find('a').get_text()

            #Coger el número de ratings
            ratingsNumberString = hotel.find_all('span', class_='reviewCount')
            rating = ""
            if len(ratingsNumberString) > 0:
                rating = ratingsNumberString[0].get_text()
                rating = rating.replace('.', '')
                rating = rating.split(' ')
                for ratingString in rating:
                    if ratingString.isnumeric():
                        rating = int(ratingString)
                        break

            #Coger la dirección del hotel
            address = hotel.find_all('div', class_='item tags')
            if len(address) > 0:
                address = address[0].get_text()
                

            yield {
                'dataType': 'spainHotels',
                'data': {
                    'name': name,
                    'ratings': rating,
                    'address': address,
                }
            }

        """for hotel in response.css('div.ui_shelf_item_detail'):

            #Se obtiene el número de ratings
            ratingsNumberString = hotel.css('span.reviewCount::text').get()
                #Se quitan los puntos para que números como 1.001 se detecten como 1001 (mil uno)
            ratingsNumberString = ratingsNumberString.replace('.', '')
            ratingsNumberStrings = ratingsNumberString.split(' ')
            for ratingString in ratingsNumberStrings:
                if ratingString.isnumeric():
                    ratingsNumber = int(ratingString)
                    break

            yield {
                'dataType': 'spainHotels',
                'data': {
                    'name': hotel.css('a::text').get(),
                    'ratings': ratingsNumber,
                    'address': hotel.css('div.item.tags::text').get(),
                }
            }"""

    #scrapy crawl hotels -O hotels.json

    #https://www.tripadvisor.es/Hotels-g187506-oa330-Galicia-Hotels.html