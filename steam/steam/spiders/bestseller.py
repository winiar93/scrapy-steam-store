import scrapy
from ..items import SteamItem


class BestsellerSpider(scrapy.Spider):
    name = 'bestseller'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/?filter=topsellers/']

    def parse(self, response):
        steam_item = SteamItem()
        games = response.xpath("//div[@id='search_resultsRows']/a")
        for game in games:
            steam_item['game_url'] = game.xpath(".//@href").get()
            

