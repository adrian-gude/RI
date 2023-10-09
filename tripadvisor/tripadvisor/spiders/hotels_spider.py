import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst


MOSTRAR_WARNINGS = False # Establece en True para mostrar advertencias de campos no encontrados
SERVICIOS = ['Aparcamiento público de pago cerca', 'Wifi', 'Gimnasio / Sala de entrenamiento', 'Restaurante', 'Sauna', 'Habitaciones de no fumadores', 'Hotel de no fumadores'] # Servicios que se van a identificar en la página
IDIOMAS = ['Español', 'Inglés', 'Francés', 'Italiano', 'Portugués'] # Idiomas que se van a identificar en la página

class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    
    comunidad = scrapy.Field(output_processor = TakeFirst())
    name = scrapy.Field(output_processor = TakeFirst())
    precio = scrapy.Field(output_processor = TakeFirst())
    comunidad = scrapy.Field(output_processor = TakeFirst())
    localizacion = scrapy.Field(output_processor = TakeFirst())
    n_opiniones = scrapy.Field(output_processor = TakeFirst())
    puntuacion = scrapy.Field(output_processor = TakeFirst())
    categoria = scrapy.Field(output_processor = TakeFirst())
    idiomas = scrapy.Field()
    servicios = scrapy.Field()
   



class HotelsSpider(scrapy.Spider):
    name = "hotels" 
    start_urls = [
        'https://www.tripadvisor.es/Hotels-g187506-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-Asturias-Hotels.html'
        # 'https://www.tripadvisor.es/Hotels-g187453-Basque_Country-Hotels.html'
        # 'https://www.tripadvisor.es/Hotels-g187506-oa30-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa60-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa90-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa120-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa150-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa180-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa210-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa240-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa270-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa300-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa330-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa360-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa390-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa420-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa450-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa480-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa510-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa30-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa60-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa90-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa120-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa150-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa180-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa210-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa240-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa270-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa300-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa330-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa360-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa390-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa420-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa450-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187449-oa480-Asturias-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187506-oa510-Galicia-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187453-oa30-Basque_Country-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187453-oa60-Basque_Country-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187453-oa90-Basque_Country-Hotels.html',
        # 'https://www.tripadvisor.es/Hotels-g187453-oa120-Basque_Country-Hotels.html',
    ]


    custom_settings = {
        #'DOWNLOAD_DELAY':0.1,  # Establece un retraso entre solicitudes para evitar ser bloqueado
        'LOG_LEVEL': 'INFO'
    }

    def __init__(self):
        super().__init__()
        self.visited_urls = set()  # Conjunto para almacenar las URLs visitadas

    def parse(self, response):
        item = HotelItem()
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
                if 'Galicia' in hotel_url : 
                    yield scrapy.Request(url=hotel_url, callback=self.parse_hotel, cb_kwargs=dict(comunidad='Galicia'))
                if 'Asturias' in hotel_url : 
                    yield scrapy.Request(url=hotel_url, callback=self.parse_hotel, cb_kwargs=dict(comunidad='Asturias'))
                if 'Basque_Country' in hotel_url : 
                    yield scrapy.Request(url=hotel_url, callback=self.parse_hotel, cb_kwargs=dict(comunidad='País Vasco'))


    def parse_hotel(self, response,comunidad):
        sel = Selector(response)
        item = ItemLoader(HotelItem(),sel)


        fields = ['nombre', 'precio', 'localizacion', 'n_opiniones', 'puntuacion', 'categoria', 'idiomas', 'servicios']
        field_count = 0

        soup = BeautifulSoup(response.text, 'html.parser')
        
        try: #Intentamos extraer los datos del hotel
            nombre = soup.find('h1', class_='QdLfr b d Pn', id='HEADING').get_text()

            field_count += 1
            precio = None
            clases_posibles_precio = ['DJRuD Z1 _U', 'DJRuD Z1 _U sGyzo', 'JPNOn JPNOn']
            # Recorre las clases posibles
            for clase in clases_posibles_precio:
                span_element = soup.find('span', class_=clase)
                if span_element:
                    # Extrae el contenido del span (que debería contener el precio)
                    precio = span_element#.text.strip()
                    break  # Detén la búsqueda si se encuentra el elemento
            precio = precio.get_text()

            field_count += 1
            localizacion = soup.find('span', class_='fHvkI PTrfg').get_text()

            field_count += 1
            n_opiniones = soup.find('span', class_='qqniT').get_text()
            n_opiniones = int(n_opiniones.replace('.', '').split(' ')[0])  # Extracción del número de opiniones

            field_count += 1
            puntuacion = soup.find('span', class_='uwJeR P').get_text()

            field_count += 1
            try:
                categoria = soup.find('svg', class_='JXZuC d H0')['aria-label'][0] # Extracción de la categoría que es el número de estrellas
            except:
                categoria = None

            field_count += 1
            posible_div_idiomas = soup.find_all('div', class_='euDRl _R MC S4 _a H') # Existen varios div's con la misma clase
            idiomas = []
            for div in posible_div_idiomas:
                texto = div.get_text()
                texto = texto.replace('y 1 más', '').replace(' ', '').split(',')
                for idioma in texto:
                    if idioma in IDIOMAS:
                        idiomas.append(idioma)


            field_count += 1
            lista_servicios = soup.find_all('div', class_='yplav f ME H3 _c')
            servicios = []
            for servicio in lista_servicios:
                servicio = servicio.get_text()
                if servicio in SERVICIOS:
                    servicios.append(servicio)

            item.add_value('comunidad',comunidad)
            item.add_value('name', nombre)
            item.add_value('precio', precio)
            item.add_value('comunidad', 'Galicia') #TODO: Extraer comunidad
            item.add_value('localizacion',localizacion)
            item.add_value('n_opiniones',n_opiniones)
            item.add_value('puntuacion',puntuacion)
            item.add_value('categoria',categoria)
            item.add_value('idiomas',idiomas)
            item.add_value('servicios',servicios)
            

            yield item.load_item()
            
        except AttributeError:
            if MOSTRAR_WARNINGS:
                self.logger.warning(f'No se pudo encontrar información en {response.url} para el campo {fields[field_count]}')


    #scrapy crawl hotels -O hotels.json

    #https://www.tripadvisor.es/Hotels-g187506-oa330-Galicia-Hotels.html