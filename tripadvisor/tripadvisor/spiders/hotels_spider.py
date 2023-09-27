import scrapy
  
  
class HotelsSpider(scrapy.Spider):
    
    # name of variable should be 'name' only
    name = "hotels" 
  
    # urls from which will be used to extract information
    # list should be named 'start_urls' only
    start_urls = [
        'https://www.tripadvisor.es/Hotels',
        #'https://www.tripadvisor.es/Search?searchSessionId=000c5c686c7b20a0.ssid&ssrc=h&q=Espa%C3%B1a&sid=485E16AFF3684177A1546710A6AF00A31695664100074&blockRedirect=true&geo=1&rf=2',
        #'https://www.tripadvisor.es/Search?searchSessionId=000c5c686c7b20a0.ssid&ssrc=h&q=Espa%C3%B1a&sid=485E16AFF3684177A1546710A6AF00A31695664100074&blockRedirect=true&geo=1&rf=3&o=30',
        #'https://www.tripadvisor.es/Search?searchSessionId=000c5c686c7b20a0.ssid&ssrc=h&q=Espa%C3%B1a&sid=485E16AFF3684177A1546710A6AF00A31695664100074&blockRedirect=true&geo=1&rf=4&o=60',
    ]
  
    def parse(self, response):

        for hotel in response.css('div.ui_shelf_item_detail'):

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
            }

    #scrapy crawl hotels -O hotels.json