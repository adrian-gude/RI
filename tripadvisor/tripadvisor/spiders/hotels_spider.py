import scrapy
from bs4 import BeautifulSoup
  
  
class HotelsSpider(scrapy.Spider):
    
    # name of variable should be 'name' only
    name = "hotels" 
  
    # urls from which will be used to extract information
    # list should be named 'start_urls' only
    start_urls = [
        #'https://www.tripadvisor.es/Hotels',
        #'https://www.tripadvisor.es/Hotels-g187506-Galicia-Hotels.html',
        #'https://www.tripadvisor.es/Hotels-g187506-oa30-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotel_Review-g187508-d231702-Reviews-Gran_Hotel_Los_Abetos-Santiago_de_Compostela_Province_of_A_Coruna_Galicia.html?spAttributionToken=MjE4OTkxNTM'
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        #lista_hoteles = soup.find_all('div', class_='NXAUb _T')

        #Coger nombre y precio de un hotel:
        datos_hotel = soup.find_all(class_='page')
        if len(datos_hotel) > 0:
            hotel = datos_hotel[0]
            nombre = hotel.find('h1', class_='QdLfr b d Pn', id='HEADING')
            precio = soup.find_all('div', class_='hhlrH w')
            if len(precio) > 0:
                precio = precio[0].get_text()
                precio = precio.replace('€', '')
                precio = precio.replace(',', '.')
                precio = float(precio)

            yield {
                'Comunidad': 'Galicia',
                'nombre': nombre.get_text(),
                'precio': str(precio),
                'ubicacion': '',
                'opiniones': '',
                'puntuacion': '',
            }

        #Coger nombre de un hotel de la url 'https://www.tripadvisor.es/Hotels' (creo)
        """for hotel in lista_hoteles:
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
                    'name': hotel.get_text(),
                    'ratings': "",
                    'address': "",
                }
            }"""
        
        #yield {'data': hotel}


    #scrapy crawl hotels -O hotels.json

    #https://www.tripadvisor.es/Hotels-g187506-oa330-Galicia-Hotels.html