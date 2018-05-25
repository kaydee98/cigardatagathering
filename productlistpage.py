import urllib3
from bs4 import BeautifulSoup

class ProductListPageCrawler(object):

    def __init__(self, base_url):
        self.base_url = base_url
        urllib3.disable_warnings()
        self.http_pool = urllib3.PoolManager()

    def get_soup(self, page):
        site_url = self.base_url + '?pg=' + str(page) + '&nb=48&sort=BeS'
        response = self.http_pool.request('GET', site_url)
        soup = BeautifulSoup(response.data, 'html.parser')

        return soup

    def get_product_info(self, product_page_tag):

        product_page_item = {"name": product_page_tag.find(itemprop="name").contents[0],
                             "url": product_page_tag.find(itemprop="url").get("content")}

        return product_page_item


    def get_max_page(self):

        soup = self.get_soup(1)
        page_navigation = soup.find("ul", {"class": "paging_section_inner_bar"})
        page_items = []

        for child in page_navigation.children:

            try:
                page_items.append(int(str(child.string)))
            except:
                pass

        return max(page_items)



    def get_product_items(self, page):

        soup = self.get_soup(page)

        product_page_items = []
        product_list = soup.find_all("div", {"class": "product_item"})

        for product_info_tag in product_list:
            product_page_items.append(self.get_product_info(product_info_tag))

        return product_page_items
