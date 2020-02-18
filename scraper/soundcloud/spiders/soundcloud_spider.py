import scrapy
import json

class SCSpider(scrapy.Spider):
    name = 'sc'

    start_urls = [
        'https://api-v2.soundcloud.com/me/play-history/tracks?client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&limit=25&offset=0&linked_partitioning=1&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?representation=&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&limit=20&offset=0&linked_partitioning=1&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2018-08-31T00%3A09%3A23.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2017-08-05T21%3A05%3A12.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2017-03-10T00%3A57%3A36.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2016-12-02T21%3A30%3A27.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2016-08-12T00%3A00%3A00.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2015-11-30T14%3A54%3A35.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2015-02-17T02%3A59%3A36.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2014-01-30T17%3A35%3A40.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
        'https://api-v2.soundcloud.com/users/892605/tracks?offset=2012-11-23T18%3A32%3A50.000Z&representation=&limit=20&client_id=qeWb21nmKO1VUDsY88W1341i7kO1JXeK&app_version=1581677269&app_locale=en',
    ]


    def parse(self, response):

        if response.request.url.startswith('https://soundcloud.com'):

            yield {
                'title': response.css('header h1 a::text').get(),
                'image': response.css('img::attr(src)').get()
            }

        data = json.loads(response.body)

        
        for x in range(len(data['collection'])):

            song_page = data['collection'][x]['permalink_url']
            yield scrapy.Request(song_page, callback=self.parse)

            yield {
                'title': data['collection'][x]['title'],
                'thumbnail': data['collection'][x]['artwork_url'],
                'audio_request_url': data['collection'][x]['media']['transcodings'][1]['url'],
                'desc': data['collection'][x]['description'],
                'created_at': data['collection'][x]['created_at'],
                'permalink_url': data['collection'][x]['permalink_url']
            }

            
            

        # response.css('h2 a::attr(href)').getall()