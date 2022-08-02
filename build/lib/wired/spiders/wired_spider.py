from unicodedata import category
import scrapy
from ..items import WiredItem

class WiredSpider(scrapy.Spider):
    """ Wired Spider"""
    name = 'wired'
    start_urls = [] 

    def __init__(self,*args, **kwargs):
        super(WiredSpider, self).__init__(*args, **kwargs)
        self.number_of_articles = kwargs.get('number_of_articles', None)
        self.author = kwargs.get('author', None)
        self.start_date = kwargs.get('strat_date')
        self.end_date = kwargs.get('end_date')
        self.search = kwargs.get('search', None)
        self.url = "https://www.wired.com/"
        if self.search is not None:
            self.url = "https://www.wired.com/search/?q="+ self.search +"&sort=score+desc"

        self.start_urls.append(self.url)
    

    def parse(self, response):
        self.items = WiredItem()       
        all_articles = response.css('div.SummaryItemContent-gXUSWx.lnJXfO.summary-item__content')
        if self.number_of_articles:
            all_articles = all_articles[0:int(self.number_of_articles)]
             
        for article in all_articles:
            category = article.css('span.RubricName-eYuXtr.drMtl::text').get()
            title = article.css('h3.SummaryItemHedBase-dZRVRw.JMeoG.summary-item__hed::text').get()
            summary = article.css("div.BaseWrap-sc-UABmB::text").get()
            author = article.css("div.summary-item__byline__content").css('span::text').extract()
            author = ','.join(author[1:])

            date = article.css('div.SummaryItemContent-gXUSWx.lnJXfO.summary-item__content').css("time::text").get()

            self.items['category']=category
            self.items['title']=title
            self.items['summary']=summary
            self.items['author']=author
            self.items['date']=date

            yield self.items

            if self.author is not None and self.author == self.items['author']:
                print(self.items)
                 

            
             