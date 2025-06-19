# Scrapy-парсер сайта alkoteka.com
- Доступен выбор города, укажите его в START_CITY в файле с пауком по пути `alko_parser/alko_parser/spiders/alkoteka_spider.py`
- Реализован мидлварь для парсинга с прокси, настройки указаны в файле по пути `alko_parser/alko_parser/settings.py`
- Были использованы бесплатные прокси, они находятся по пути `alko_parser/proxies.txt`
- Три категории уже спаршены, результат можно увидеть по пути `alko_parser/result.json`

## Этапы запуска проекта
- Клонируйте репозиторий
    ```
    git clone https://github.com/akatsukiHell/alkoteka-scrapy-parser.git
    ```

- Установите зависимости
    ```
    pip install -r requirements.txt
    ```

- Перейдите в папку проекта
    ```
    cd alkoteka-parser/alko_parser
    ```

- Запустите паука
    ```
    scrapy crawl alko -O result.json
    ```
