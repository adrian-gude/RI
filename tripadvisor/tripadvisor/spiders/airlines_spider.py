import scrapy
  
  
class AirlinesSpider(scrapy.Spider):
    
    # name of variable should be 'name' only
    name = "airlines" 
  
    # urls from which will be used to extract information
    # list should be named 'start_urls' only
    start_urls = [
        'https://www.tripadvisor.es/Airlines',
    ]
  
    def parse(self, response):

        for airline in response.css('div.airlineData'):

            #Se obtienen los datos de cada review
            reviews = airline.css('p')
            reviewList = []
            for review in reviews:
                reviewList.append({
                    'review': review.css('p::text').get(),
                    'date': review.css('span.date::text').get(),
                })

            #Se obtiene el número de ratings
            ratingsNumberString = airline.css('div.airlineReviews::text').get()
                #Se quitan los puntos para que números como 1.001 se detecten como 1001 (mil uno)
            ratingsNumberString = ratingsNumberString.replace('.', '')
            ratingsNumberStrings = ratingsNumberString.split(' ')
            for ratingString in ratingsNumberStrings:
                if ratingString.isnumeric():
                    ratingsNumber = int(ratingString)
                    break

            yield {
                'dataType': 'airlines',
                'data': {
                    'name': airline.css('div.airlineName::text').get(),
                    'ratings': ratingsNumber,
                    'reviews': reviewList,
                }
            }

# Comando ejecución: scrapy crawl airlines -O airlines.json