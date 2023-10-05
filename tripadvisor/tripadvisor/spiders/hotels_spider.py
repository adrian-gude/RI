import scrapy
from bs4 import BeautifulSoup

class HotelsSpider(scrapy.Spider):
    name = "hotels" 
    start_urls = [
        'https://www.tripadvisor.es/Hotels-g187506-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa30-Galicia-Hotels.html'
    ]

    def __init__(self):
        super().__init__()
        self.visited_urls = set()  # Conjunto para almacenar las URLs visitadas

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Obtén los enlaces a los hoteles en la página inicial
        hotel_links = soup.select('div[data-automation="hotel-card-title"] a')
        
        for link in hotel_links:
            hotel_url = link.get('href')
            # Comprueba si el enlace es relativo y construye la URL completa
            if not hotel_url.startswith('http'):
                hotel_url = response.urljoin(hotel_url)
            
            # Verifica si la URL ya ha sido visitada
            if hotel_url not in self.visited_urls:
                self.visited_urls.add(hotel_url)  # Agrega la URL al conjunto de URLs visitadas
                # Realiza la solicitud a la página del hotel y llama a una función de devolución de llamada para extraer datos
                yield scrapy.Request(url=hotel_url, callback=self.parse_hotel)

    def parse_hotel(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Aquí puedes extraer los datos del hotel, por ejemplo:
        hotel_name = soup.find('h1', class_='QdLfr b d Pn', id='HEADING').get_text()
        hotel_price = soup.find('div', class_='hhlrH w').get_text()
        
        # Puedes seguir extrayendo más datos según tus necesidades
        
        yield {
            'Comunidad': 'Galicia',
            'nombre': hotel_name,
            'precio': hotel_price,
            'ubicacion': '',
            'opiniones': '',
            'puntuacion': '',
        }

    

        #yield {'data': hotel}


    #scrapy crawl hotels -O hotels.json

    #https://www.tripadvisor.es/Hotels-g187506-oa330-Galicia-Hotels.html