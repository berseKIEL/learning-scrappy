import sqlite3
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        availability_string = adapter.get('availability')
        split_spring_array = availability_string.split('(')
        if len(split_spring_array) < 2:
            adapter['availability'] = 0
        else:
            availabity_array = split_spring_array[1].split(' ')
            adapter['availability'] = int(availabity_array[0])

        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        star_string = adapter.get('stars')
        split_stars_array = star_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        number_mapping = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5
        }

        if stars_text_value in number_mapping:
            adapter['stars'] = number_mapping[stars_text_value]

        return item


class SaveSQLITE:

    def __init__(self):
        self.con = sqlite3.connect('sqlite.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT_NULL AUTO_INCREMENT,
            url VARCHAR(255),
            title TEXT,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description TEXT,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute("""
            INSERT INTO books (url, title, upc,
                    product_type, price_excl_tax, price_incl_tax,
                    tax, price, availability,
                    num_reviews, stars, category,
                    description)
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item['url'],
            item['title'],
            item['upc'],
            item['product_type'],
            item['price_excl_tax'],
            item['price_incl_tax'],
            item['tax'],
            item['price'],
            item['availability'],
            item['num_reviews'],
            item['stars'],
            item['category'],
            str(item['description'][0])
        ))

        self.con.commit()
        return item
