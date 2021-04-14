import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import RrepublicbankbviItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class RrepublicbankbviSpider(scrapy.Spider):
	name = 'republicbankbvi'
	start_urls = ['https://republicbankbvi.com/news/']

	def parse(self, response):
		post_links = response.xpath('//a[contains(text(),"Continue reading")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		try:
			date = response.xpath('//p/em/strong/text()').get()
			date = re.findall(r'\w+\s\d+\,\s\d+', date)
		except:
			date = "Not stated in article"
		title = response.xpath('//h1/span[@property="schema:name"]/text()').get()
		content = response.xpath('//div[@class="content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=RrepublicbankbviItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
