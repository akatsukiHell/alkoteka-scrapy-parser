from urllib.parse import urlencode
from typing import AsyncGenerator

from scrapy import Spider, Request

from alko_parser.utils import JsonParser

class Parser(Spider):
    name="alko"

    START_CITY = "Краснодар"
    START_URLS = [
        "https://alkoteka.com/catalog/slaboalkogolnye-napitki-2",
        "https://alkoteka.com/catalog/krepkiy-alkogol",
        "https://alkoteka.com/catalog/axioma-spirits",
    ]
    city_uuid = None
    
    product_api = "https://alkoteka.com/web-api/v1/product"
    city_api = "https://alkoteka.com/web-api/v1/city"

    base_product_link = "https://alkoteka.com/product/"

    async def start(self):
        yield Request(
            url=self.city_api,
            callback=self.get_city_uuid
        )
    
    async def get_city_uuid(self, response, page: int=1) -> AsyncGenerator[Request]:
        """
        Получает UUID города из списка API

        Args:
            response: Ответ от API с данными городов
            page (int): Номер страницы для пагинации
        
        Returns:
            Generator[Request]: Запросы для следующих категорий или перехода на следующую страницу
        """

        raw = response.json()
        for city in raw.get("results"):
            if city["name"] == self.START_CITY:
                self.city_uuid = city["uuid"]
                for categories_url in self.START_URLS:
                    root_category_slug = categories_url.split("/")[-1]
                    yield await self.get_catalog_api(root_category_slug)
                return
            
        if raw.get("meta").get("has_more_pages"):
            page += 1
            next_url = f"{self.city_api}?page={page}"
            yield response.follow(
                url=next_url,
                callback=self.get_city_uuid,
            )

    async def get_catalog_api(self, root_category_slug: str, page: int=1) -> AsyncGenerator[Request]:
        """
        Получаем API каталога для указанной категории и страницы

        Args:
            root_category_slug (str): Короткое название категории
            page (int): Номер страницы для пагинации

        Returns:
            Request: Запрос для получения товаров из API
        """
        querystring = {
            "city_uuid":self.city_uuid,
            "page":page,
            "per_page":40,
            "root_category_slug":root_category_slug
        }
        url = f"{self.product_api}?{urlencode(querystring)}"
        return Request(
            url=url,
            callback=self.parse_items,
            cb_kwargs={"root_category_slug": root_category_slug, "page": page}
        )

    async def parse_items(self, response, root_category_slug: str, page: int) -> AsyncGenerator[Request]:
        """
        Парсим API товаров из полученной API-страницы каталога

        Args:
            root_category_slug (str): Короткое название категории
            page (int): Номер страницы для пагинации

        Returns:
            Request: Запрос на парсинг JSON-API каждого товара
        """

        raw = response.json()
        results = raw.get("results")

        for product in results:
            slug = product.get("slug")
            category_slug = product.get("category_slug")
            product_url = f"{self.base_product_link}{category_slug}/{slug}"
            product_api = f"{self.product_api}/{slug}?city_uuid={self.city_uuid}"

            yield Request(
                url=product_api,
                callback=self.parse_result,
                meta={"original_urls": product_url}
            )

        if raw.get("meta").get("has_more_pages"):
            yield await self.get_catalog_api(root_category_slug, page + 1)
    

    async def parse_result(self, response) -> AsyncGenerator[dict]:
        """
        Вызываем отдельный класс для парсинга JSON

        Args:
            response: Ответ от Scrapy с данными оригинальных ссылок на товар

        Returns:
            dict: Словарь со спаршенными данными
        """
        raw = response.json().get("results")
        json_parser = JsonParser(raw, response.meta.get("original_urls"))
        yield json_parser.parse()