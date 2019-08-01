import re


def parse(product, soup):
    if 'gymgrossisten' in product.url:
        return gg_parse(product, soup)


def gg_parse(product, soup):
    price_tag = soup.find(id=product.tag_id)
    if price_tag is not None:
        match = re.search(r'.*?(\d+[.,]?\d+).*', price_tag.contents[0])
        if match is None:
            match = re.search(r'.*?(\d+[.,]?\d+).*', price_tag.contents[0].contents[0])
        price = match.group(1)
        return float(price.replace(',', '.'))
    else:
        raise Exception('Parse exception')
