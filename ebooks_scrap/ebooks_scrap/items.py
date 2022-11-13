from scrapy import Field, Item
from itemloaders.processors import MapCompose, TakeFirst


def convert_to_int(txt):
    return (float(txt.replace('£', '')))


def get_quantity(txt):
    return int(
        txt.replace('(', '').split()[0]
    )

class EbooksScrapItem(Item):
    title = Field(
        output_processor=TakeFirst()
    )
    price = Field(
        input_processor=MapCompose(convert_to_int),
        output_processor=TakeFirst()
    )
    in_stock = Field(
        input_processor=MapCompose(get_quantity),
        output_processor=TakeFirst()
    )
    product_information = Field(
        output_processor=TakeFirst()
    )

