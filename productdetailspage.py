import urllib3
from bs4 import BeautifulSoup

class ProductDetailsPage(object):

    product_details = {}

    def __init__(self):
        urllib3.disable_warnings()
        self.http_pool = urllib3.PoolManager()

    def get_key(self, content):
        return {
            'Brands': 'brand',
            'Cigar Shape': 'shape',
            'Cigar Section': 'section',
            'Origin': 'origin',
            'Cigar Length': 'length',
            'Strength': 'strength',
            'Cigar Ring Gauge': 'gauge',
            'Wrapper Color': 'color',
            'Cigar Manufacturer': 'manufacturer',
            'Cigar Wrapper': 'wrapper',
            'Cigar Binder': 'binder',
            'Cigar Filler': 'filler'
        }.get(content, content)

    def get_value(self, content):

        try:
            value = content.contents[0].text
        except:
            value = content.text
        return value.strip()



    def get_product_details(self, page_details_url):

        response = self.http_pool.request('GET', page_details_url)
        soup = BeautifulSoup(response.data, 'html.parser')

        product_spec = soup.find_all("li", {"class": "pr_pItem"})

        # get product attributes/specification on the page
        for item in product_spec:
            contents = item.find_all('div')
            self.product_details[self.get_key(contents[0].text)] = self.get_value(contents[1])
        return self.product_details