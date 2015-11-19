import scrapy
from swedishblog.items import SwedishblogArticle
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class blogArticleSpider(CrawlSpider):
    name = "blogArticle"
    allowed_domains = ["swedish.org"]
    start_urls = [
        "http://www.swedish.org/blog/"
    ]
    rules = [
        Rule(LinkExtractor(
                allow=(r'/blog/\d{4}?page=\d+/')
            ),
             follow=True),
        Rule(LinkExtractor(
                allow=(r'/blog/\d{4}/')
            ),
             follow=True),
        Rule(LinkExtractor(
                allow=(r'/blog/\d{4}/\d{2}/.+')
            ),
             callback='parse_article',
             follow=False)
    ]
    def parse_article(self, response):
        title = response.xpath('//h1/text()').extract()[0].strip()
        date = response.xpath("//div[@class='module-bg-date']/text()")[0].extract().strip()
        # this is the highlighted author
        author1 = response.xpath("//div[@class='module-bg-detail-authors']/a/text()")[0].extract()
        # sometimes there is a secondary italic text showing the real author
        author2 = response.xpath("//div[@id='main_0_contentpanel_0_pnlDetail']/em/text()")
        if len(author2) > 1:
            author2 = author2[0].extract()
        else:
            author2 = None
        if "blogger" in author1.lower() and author2:
            author = author2
        else:
            author = author1
        # extract the contents. We basically collect the HTML below the div(id=main_0_contentpanel_0_UpdatePanel1) tag
        sibling_index = 1
        contents = []
        while True:
            content_html = response.xpath("//div[@id='main_0_contentpanel_0_UpdatePanel1']/following-sibling::*[" + str(sibling_index) + "]").extract()
            if len(content_html) == 0:
                break
            else:
                contents.append(content_html)
                sibling_index += 1
        article = SwedishblogArticle()
        article['title'] = title
        article['publishDate'] = date
        article['author'] = author
        article['url'] = response.url
        article['contents'] = contents

        return article
