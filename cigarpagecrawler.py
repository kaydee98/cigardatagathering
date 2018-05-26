import json

import productlistpage
import productdetailspage

product_list_page = productlistpage.ProductListPageCrawler('https://www.neptunecigar.com/cigars')
last_page = product_list_page.get_max_page()

cigarjsonfile = open("cigars.json", "w")

for i in range(1, last_page + 1):
    print(f"Scapping Page #{i} of {last_page}")
    for product_item in product_list_page.get_product_items(i):

        print('Writing Product Name: %s, Url: %s to file' % (product_item["name"], product_item["url"]))
        product_details = productdetailspage.ProductDetailsPage()
        json.dump(product_details.get_product_details(product_item["url"]), cigarjsonfile, ensure_ascii=False)
        cigarjsonfile.write("\n")

cigarjsonfile.close()

