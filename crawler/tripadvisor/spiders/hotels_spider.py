import scrapy
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
import re
import random

MOSTRAR_WARNINGS = False

# Servicios que se capturarán si el hotel los tiene
SERVICIOS = ['Aparcamiento público de pago cerca', 'Wifi', 'Gimnasio / Sala de entrenamiento', 'Restaurante', 'Sauna', 'Habitaciones de no fumadores', 'Hotel de no fumadores']
# Idiomas que se capturarán si el hotel los tiene
IDIOMAS = ['Español', 'Inglés', 'Francés', 'Italiano', 'Portugués']

class HotelItem(scrapy.Item):
    nombre = scrapy.Field(output_processor=TakeFirst())
    comunidad = scrapy.Field(output_processor=TakeFirst())
    precio = scrapy.Field(output_processor=TakeFirst())
    comunidad = scrapy.Field(output_processor=TakeFirst())
    localizacion = scrapy.Field(output_processor=TakeFirst())
    n_opiniones = scrapy.Field(output_processor=TakeFirst())
    puntuacion = scrapy.Field(output_processor=TakeFirst())
    categoria = scrapy.Field(output_processor=TakeFirst())
    idiomas = scrapy.Field()
    servicios = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    imageUrl = scrapy.Field(output_processor=TakeFirst())

class HotelsSpider(scrapy.Spider):
    name = "hotels" 
    custom_settings = {
        'LOG_LEVEL': 'INFO'
    }

    BASE_URL = 'https://www.tripadvisor.es/Hotels-g{}-{}-Hotels.html'
    COMUNIDADES = [
       ('187506', 'Galicia', 'Galicia'),
       ('187449', 'Asturias', 'Asturias'),
       ('187483', 'Cantabria', 'Cantabria'),
       ('187453', 'Basque_Country', 'Pais Vasco'),
       ('187519', 'Navarra', 'Navarra'),
       ('187444', 'Aragon', 'Aragon'),
       #('187496', 'Catalonia', 'Cataluña'),
       ('187490', 'Castile_and_Leon', 'Castilla y Leon'),
       ('187511', 'La_Rioja', 'La Rioja'),
       ('187514', 'Madrid', 'Madrid'),
       ('187505', 'Extremadura', 'Extremadura'),
       ('187485', 'Castile_La_Mancha', 'Castilla La Mancha'),
       ('187521', 'Valencian_Community', 'Comunidad Valenciana'),
       ('187518', 'Murcia', 'Murcia'),
       #('187428', 'Andalucia', 'Andalucia'),
       ('187459', 'Balearic_Islands', 'Islas Baleares'),
       ('187466', 'Canary_Islands', 'Islas Canarias')
    ]

    IMAGENES = [
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/24/dc/23/3e/berazadi-berri.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1d/82/fb/26/icon-malabar.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0e/e9/b1/af/piscina.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2a/b0/95/08/grand-deluxe-suite.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/15/37/f0/6d/categoria-de-habitacion.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/26/c3/2b/ee/guest-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/17/2f/7a/d7/parador-de-cordoba.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/9b/18/d7/terraza-barbacoa-de-lena.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/15/37/a3/13/hotel-the-serras.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/12/9c/93/ac/vue-du-rooftop.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/23/4f/ea/73/el-cel-bar.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1d/b0/24/34/superior-corner-bedroom.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0f/7c/ce/c5/suite-con-jacuzzi-xarello.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/19/ee/b4/79/axel-hotel-barcelona.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/14/e5/c0/bc/hotel-praktik-rambla.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/23/63/09/e4/rosellon-exterior-image.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/02/8b/7a/catalonia-magdalenes.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1c/eb/12/8a/property-amenity.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/12/88/db/08/hotel-jazz-pool.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/28/91/e7/84/terraza-el-cel-de-gaudi.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/0a/54/80/casa-marea-la-fosca-wehost.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-s/02/2a/37/7e/universal-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/09/32/a6/cc/sixtytwo-hotel.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2a/80/fb/95/500313-guest-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/09/27/dd/135718-guest-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/14/e9/cc/fa/easyhotel-barcelona.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/24/fe/ec/80/edificio.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1c/dd/da/ed/exterior-view.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/28/95/10/61/guest-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/27/68/d5/18/exterior-view.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/52/59/7f/500006-guest-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2a/c5/ba/87/caption.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/13/d1/6d/1e/deluxe-guest-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/10/0e/0b/aa/patio--v17122335.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/12/51/0f/2d/yeah-barcelona-hostel.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/1e/38/bb/75/sonder-casa-luz.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/26/52/e8/3c/fachada-catalonia-albinoni.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/09/21/a7/5a/junior-suite.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/13/a9/a7/b6/habitacion-doble.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/12/a0/5c/81/common-areas.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/18/dd/9e/8a/acta-voraport.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/23/af/99/9a/suite-frontal.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0f/72/04/5d/hotel-olivia-plaza.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/0a/54/80/casa-marea-la-fosca-wehost.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/04/63/45/ae/olivia-balmes-hotel.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/26/52/df/59/cataloniaavinyo-fachada.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/29/2f/6e/c6/comfort-room.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0a/16/d9/6e/suite-cama-matrimonio.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2a/b7/dc/a1/confort-estandard-silken.jpg?w=300&h=300&s=1",
        "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/2a/45/65/f3/hotel-cortes-rambla.jpg?w=300&h=300&s=1"
    ]

    PAGES_TO_SCRAPE = 15 # Número de páginas a scrapear por comunidad (-1)

    def start_requests(self):
        for code, comunidad, nombreComunidad in self.COMUNIDADES:
            start_url = self.BASE_URL.format(code, comunidad)
            yield scrapy.Request(start_url, callback=self.parse, cb_kwargs={'comunidad': comunidad, 'nombreComunidad': nombreComunidad})

    def parse(self, response, comunidad, nombreComunidad):
        for page in range(self.PAGES_TO_SCRAPE):
            url = response.url.replace(f'-{comunidad}-Hotels.html', f'-oa{page * 30}-{comunidad}-Hotels.html')
            yield scrapy.Request(url, callback=self.parse_hotel, cb_kwargs={'nombreComunidad': nombreComunidad})

    def parse_hotel(self, response, nombreComunidad):
        soup = BeautifulSoup(response.text, 'html.parser')
        hotel_divs = soup.find_all(lambda tag: tag.name == 'div' and tag.get('data-automation') and re.match(r'non-plus-hotel-offer-[1-9]|10$', tag.get('data-automation')))
        
        for div in hotel_divs:
            try:
                hotel_link = div.select('div[data-automation="hotel-card-title"] a')
                if len(hotel_link)>0:
                    hotel_link = hotel_link[0]
                    hotel_url = hotel_link.get('href')
                    if not hotel_url.startswith('http'):
                        hotel_url = response.urljoin(hotel_url)
        
                image_link = div.find_all(class_="_C")
                if image_link:
                    image_url = image_link[0].get('src')
                else:
                    image_url = random.choice(self.IMAGENES)


                yield scrapy.Request(url=hotel_url, callback=self.parse_hotel_details, cb_kwargs={'comunidad': nombreComunidad, 'imageUrl': image_url})
            except:
                # Si no se ha podido obtener un campo, se muestra un warning si la variable MOSTRAR_WARNINGS es True
                if MOSTRAR_WARNINGS:
                    self.logger.warning(f'No se pudo encontrar información de un hotel en {response.url}')

    def parse_hotel_details(self, response, comunidad, imageUrl):
        url = response.url
        sel = Selector(response)
        item = ItemLoader(HotelItem(), sel)

        # Campos a capturar; utilizado para mostrar warnings
        fields = ['comunidad', 'nombre', 'precio', 'localizacion', 'n_opiniones', 'puntuacion', 'categoria', 'idiomas', 'servicios', 'imageUrl']
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
            # Se elminar el símbolo de la moneda, los puntos de los miles y se reemplaza la coma decimal por un punto
            precio = precio.replace('€', '').replace('.','').replace(',', '.').replace(' ', '')
            precio = float(precio)
            precio = int(precio)

            field_count += 1
            localizacion = soup.find('span', class_='fHvkI PTrfg').get_text()

            field_count += 1
            n_opiniones = soup.find('span', class_='qqniT').get_text()
            n_opiniones = n_opiniones.replace('.', '').split(' ')[0]
            n_opiniones = int(n_opiniones)

            field_count += 1
            puntuacion = soup.find('span', class_='uwJeR P').get_text()
            if puntuacion is not None and puntuacion != '':
                puntuacion = puntuacion.replace(',', '.')
                puntuacion = float(puntuacion)

            field_count += 1
            try:
                categoria = soup.find('svg', class_='JXZuC d H0')['aria-label'][0]
                if categoria is not None and categoria != '':
                    categoria = int(categoria)
                if categoria is None or categoria == '':
                    raise AttributeError
            except:
                categoria = 0

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
            item.add_value('url', url)
            item.add_value('imageUrl', imageUrl)

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
            url = item.get_collected_values('url')[0] if item.get_collected_values('url') else None
            imageUrl = item.get_collected_values('imageUrl')[0] if item.get_collected_values('imageUrl') else None

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
                'url': url,
                'imageUrl': imageUrl,
            }

            yield hotel_data # Devuelve el diccionario con los valores
            
        except AttributeError:
            # Si no se ha podido obtener un campo, se muestra un warning si la variable MOSTRAR_WARNINGS es True
            if MOSTRAR_WARNINGS:
                self.logger.warning(f'No se pudo encontrar información en {response.url} para el campo {fields[field_count]}')
