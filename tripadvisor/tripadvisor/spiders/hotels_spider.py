import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

MOSTRAR_WARNINGS = False

# Servicios que se capturarán si el hotel los tiene
SERVICIOS = ['Aparcamiento público de pago cerca', 'Wifi', 'Gimnasio / Sala de entrenamiento', 'Restaurante', 'Sauna', 'Habitaciones de no fumadores', 'Hotel de no fumadores']
# Idiomas que se capturarán si el hotel los tiene
IDIOMAS = ['Español', 'Inglés', 'Francés', 'Italiano', 'Portugués']

class HotelItem(scrapy.Item):
    comunidad = scrapy.Field(output_processor=TakeFirst())
    nombre = scrapy.Field(output_processor=TakeFirst())
    precio = scrapy.Field(output_processor=TakeFirst())
    comunidad = scrapy.Field(output_processor=TakeFirst())
    localizacion = scrapy.Field(output_processor=TakeFirst())
    n_opiniones = scrapy.Field(output_processor=TakeFirst())
    puntuacion = scrapy.Field(output_processor=TakeFirst())
    categoria = scrapy.Field(output_processor=TakeFirst())
    idiomas = scrapy.Field()
    servicios = scrapy.Field()

class HotelsSpider(scrapy.Spider):
    name = "hotels" 
    custom_settings = {
        'LOG_LEVEL': 'INFO'
    }

    BASE_URL = 'https://www.tripadvisor.es/Hotels-g{}-{}-Hotels.html'
    COMUNIDADES = [
       ('187506', 'Galicia'),
       ('187449', 'Asturias'),
       ('187483', 'Cantabria'),
       ('187453', 'Basque_Country'),
       ('187519', 'Navarra'),
       ('187444', 'Aragon'),
       #('187496', 'Catalonia'),
       ('187490', 'Castile_and_Leon'),
       ('187511', 'La_Rioja'),
       ('187514', 'Madrid'),
       ('187505', 'Extremadura'),
       ('187485', 'Castile_La_Mancha'),
       ('187521', 'Valencian_Community'),
       ('187518', 'Murcia'),
       #('187428', 'Andalucia'),
       ('187459', 'Balearic_Islands'),
       ('187466', 'Canary_Islands')
    ]
    PAGES_TO_SCRAPE = 14 # Número de páginas a scrapear por comunidad

    def start_requests(self):
        for code, comunidad in self.COMUNIDADES:
            start_url = self.BASE_URL.format(code, comunidad)
            yield scrapy.Request(start_url, callback=self.parse, cb_kwargs={'comunidad': comunidad})

    def parse(self, response, comunidad):
        for page in range(self.PAGES_TO_SCRAPE):
            url = response.url.replace(f'-Hotels.html', f'-oa{page * 30}-{comunidad}-Hotels.html')
            yield scrapy.Request(url, callback=self.parse_hotel, cb_kwargs={'comunidad': comunidad})

    def parse_hotel(self, response, comunidad):
        soup = BeautifulSoup(response.text, 'html.parser')

        # Obtén los enlaces a los hoteles en la página inicial
        hotel_links = soup.select('div[data-automation="hotel-card-title"] a')

        for link in hotel_links:
            hotel_url = link.get('href')
            if not hotel_url.startswith('http'):
                hotel_url = response.urljoin(hotel_url)

            if hotel_url:
                yield scrapy.Request(url=hotel_url, callback=self.parse_hotel_details, cb_kwargs={'comunidad': comunidad})

    def parse_hotel_details(self, response, comunidad):
        sel = Selector(response)
        item = ItemLoader(HotelItem(), sel)

        # Campos a capturar; utilizado para mostrar warnings
        fields = ['comunidad', 'nombre', 'precio', 'localizacion', 'n_opiniones', 'puntuacion', 'categoria', 'idiomas', 'servicios']
        field_count = 1

        soup = BeautifulSoup(response.text, 'html.parser')

        # Se usa un try para que si un campo no tiene valor se capture el error y no se registre dicho hotel
        try:
            # Se obtiene el valor del campo nombre
            nombre = soup.find('h1', class_='QdLfr b d Pn', id='HEADING').get_text()

            field_count += 1
            precio = None
            clases_posibles_precio = ['DJRuD Z1 _U', 'DJRuD Z1 _U sGyzo', 'JPNOn JPNOn']
            for clase in clases_posibles_precio:
                span_element = soup.find('span', class_=clase)
                if span_element:
                    precio = span_element
                    break
            precio = precio.get_text()
            if precio == '':
                raise AttributeError
            precio = precio.replace('€', '').replace(',', '.').replace(' ', '')
            precio = float(precio)

            field_count += 1
            localizacion = soup.find('span', class_='fHvkI PTrfg').get_text()

            field_count += 1
            n_opiniones = soup.find('span', class_='qqniT').get_text()
            n_opiniones = int(n_opiniones.replace('.', '').split(' ')[0])

            field_count += 1
            puntuacion = soup.find('span', class_='uwJeR P').get_text()
            if puntuacion is not None and puntuacion != '':
                puntuacion = float(puntuacion.replace(',', '.'))

            field_count += 1
            try:
                categoria = soup.find('svg', class_='JXZuC d H0')['aria-label'][0]
                if categoria is not None and categoria != '':
                    categoria = int(categoria)
            except:
                categoria = -1

            field_count += 1
            idiomas = []
            posible_div_idiomas = soup.find_all('div', class_='euDRl _R MC S4 _a H')
            for div in posible_div_idiomas:
                texto = div.get_text()
                texto = texto.replace('y 1 más', '').replace(' ', '').split(',')
                for idioma in texto:
                    if idioma in IDIOMAS:
                        idiomas.append(idioma)

            field_count += 1
            servicios = []
            lista_servicios = soup.find_all('div', class_='yplav f ME H3 _c')
            for servicio in lista_servicios:
                servicio = servicio.get_text()
                if servicio in SERVICIOS:
                    servicios.append(servicio)

            # Añade los valores a los campos
            item.add_value('comunidad', comunidad)
            item.add_value('nombre', nombre)
            item.add_value('precio', precio)
            item.add_value('localizacion', localizacion)
            item.add_value('n_opiniones', n_opiniones)
            item.add_value('puntuacion', puntuacion)
            item.add_value('categoria', categoria)
            item.add_value('idiomas', idiomas)
            item.add_value('servicios', servicios)

            # Obtiene los valores de los campos, o None si no existen
            comunidad = item.get_collected_values('comunidad')[0] if item.get_collected_values('comunidad') else None
            nombre = item.get_collected_values('nombre')[0] if item.get_collected_values('nombre') else None
            precio = item.get_collected_values('precio')[0] if item.get_collected_values('precio') else None
            localizacion = item.get_collected_values('localizacion')[0] if item.get_collected_values('localizacion') else None
            n_opiniones = item.get_collected_values('n_opiniones')[0] if item.get_collected_values('n_opiniones') else None
            puntuacion = item.get_collected_values('puntuacion')[0] if item.get_collected_values('puntuacion') else None
            categoria = item.get_collected_values('categoria')[0] if item.get_collected_values('categoria') else None
            idiomas = item.get_collected_values('idiomas')
            servicios = item.get_collected_values('servicios')

            # Crea un diccionario con los valores individuales
            hotel_data = {
                'comunidad': comunidad,
                'nombre': nombre,
                'precio': precio,
                'localizacion': localizacion,
                'n_opiniones': n_opiniones,
                'puntuacion': puntuacion,
                'categoria': categoria,
                'idiomas': idiomas,
                'servicios': servicios,
            }

            yield hotel_data # Devuelve el diccionario con los valores
            
        except AttributeError:
            # Si no se ha podido obtener un campo, se muestra un warning si la variable MOSTRAR_WARNINGS es True
            if MOSTRAR_WARNINGS:
                self.logger.warning(f'No se pudo encontrar información en {response.url} para el campo {fields[field_count]}')

    #scrapy crawl hotels -O hotels.json