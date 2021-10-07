import scrapy
from ..items import SteamItem
from w3lib.html import remove_tags


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
            raw_platform_list = game.xpath(".//span[contains(@class,'platform_img') or @class='vr_supported']"
                                           " /@class").getall()
            platform_list = []
            for plat in raw_platform_list:
                if " " in plat:
                    plat = plat.split(" ")[-1]
                    platform_list.append(plat)
                else:
                    platform_list.append(plat)

            steam_item['platform'] = platform_list
            summar_reviews = game.xpath(".//span[contains(@class,'search_review_summary')]/@data-tooltip-html").get()
            if summar_reviews:
                steam_item['reviews'] = remove_tags(summar_reviews)
            else:
                steam_item['reviews'] = None

            actual_price = game.xpath(".//div[@class='col search_price  responsive_secondrow'] /text()").get()
            if actual_price:
                steam_item['actual_price'] = actual_price.strip()
            else:
                steam_item['actual_price'] = \
                    game.xpath(".//div[contains(@class, 'search_price discounted')]/text()").getall()[-1].strip()

            discount_rate = game.xpath(".//div[@class='col search_discount responsive_secondrow']"
                                       "/span/text()").get()
            steam_item['discount_rate'] = discount_rate

            if discount_rate:
                steam_item['original_price'] = game.xpath(".//span[@style='color: #888888;']/strike/text()").get()
            else:
                steam_item['original_price'] = steam_item['actual_price']

            yield steam_item
