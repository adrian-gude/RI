import scrapy
import re
from bs4 import BeautifulSoup

class HotelsSpider(scrapy.Spider):
    name = "hotels" 
    start_urls = [
        'https://www.tripadvisor.es/Hotels-g187506-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187449-Asturias-Hotels.html'
        'https://www.tripadvisor.es/Hotels-g187453-Basque_Country-Hotels.html'
        'https://www.tripadvisor.es/Hotels-g187506-oa30-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa60-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa90-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa120-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa150-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa180-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa210-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa240-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa270-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa300-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa330-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa360-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa390-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa420-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa450-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa480-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187506-oa510-Galicia-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187449-oa30-Asturias-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187449-oa60-Asturias-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187449-oa90-Asturias-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187449-oa120-Asturias-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187453-oa30-Basque_Country-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187453-oa60-Basque_Country-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187453-oa90-Basque_Country-Hotels.html',
        'https://www.tripadvisor.es/Hotels-g187453-oa120-Basque_Country-Hotels.html',
    ]


    custom_settings = {
        #'DOWNLOAD_DELAY':0.1,  # Establece un retraso de 2 segundos entre solicitudes
        'LOG_LEVEL': 'INFO'
    }

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
        
        try:
            # Aquí puedes extraer los datos del hotel
            nombre = soup.find('h1', class_='QdLfr b d Pn', id='HEADING').get_text()
            precio = soup.find('span', class_='DJRuD Z1 _U').get_text()
            localizacion = soup.find('span', class_='fHvkI PTrfg').get_text()
            n_opiniones = soup.find('span', class_='qqniT').get_text()
            n_opiniones = int(n_opiniones.replace('.', '').split(' ')[0])  # Extracción del número de opiniones
            puntuacion = soup.find('span', class_='uwJeR P').get_text()
            try:
                categoria = soup.find('svg', class_='JXZuC d H0')['aria-label'][0]
            except:
                categoria = None

            yield {
                'nombre': nombre,
                'precio': precio,
                'Comunidad': 'Galicia',
                'localizacion': localizacion,
                'n_opiniones': n_opiniones,
                'puntuacion': puntuacion,
                'categoria': categoria
            }
        except AttributeError:
            self.logger.warning(f'No se pudo encontrar información en {response.url}')

        #yield {'data': hotel}


    #scrapy crawl hotels -O hotels.json

    #https://www.tripadvisor.es/Hotels-g187506-oa330-Galicia-Hotels.html