import scrapy
import html2text


class WikiSpider(scrapy.Spider):
    name = "wikiita"
    allowed_domains = [
        'it.wikipedia.org'
    ]
    start_urls = [
        'https://it.wikipedia.org/wiki/Pagina_principale',
    ]

    def parse(self, response):
        title = response.css('h1.firstHeading::text').get()
        if title:
            print(title)
            filename = "".join(x for x in title if x.isalnum())
            with open(f'./data/{filename}.txt', 'w') as f:
                converter = html2text.HTML2Text()
                converter.ignore_links = True
                f.write(converter.handle(''.join(response.css('p').getall())))

        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse)


class WikiSpider2(scrapy.Spider):
    name = "wikieng"
    allowed_domains = [
        'en.wikipedia.org'
    ]
    start_urls = [
        'https://en.wikipedia.org/wiki/Main_Page',
    ]

    def parse(self, response):
        title = response.css('h1.firstHeading::text').get()
        if title:
            print(title)
            filename = "".join(x for x in title if x.isalnum())
            with open(f'./data/{filename}.txt', 'w') as f:
                converter = html2text.HTML2Text()
                converter.ignore_links = True
                f.write(converter.handle(''.join(response.css('p').getall())))

        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse)
