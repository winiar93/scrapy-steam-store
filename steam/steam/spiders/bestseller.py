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
            steam_item['game_image'] = game.xpath(".//div[@class='col search_capsule']/img/@src").get()
            steam_item['game_name'] = game.xpath(".//span[@class='title']/text()").get()
            steam_item['release_date'] = game.xpath(".//div[@class='col search_released "
                                                    "responsive_secondrow']/text()").get()

            raw_platfrom_list = game.xpath(".//span[contains(@class,'platform_img') or @class='vr_supported']"
                                           " /@class").getall()
            platform_list = []
            for plat in raw_platfrom_list:
                if " " in plat:
                    plat = plat.split(" ")[-1]
                    platform_list.append(plat)
                else:
                    platform_list.append(plat)

            steam_item['platform'] = platform_list

            yield steam_item
