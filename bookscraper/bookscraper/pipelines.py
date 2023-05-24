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
