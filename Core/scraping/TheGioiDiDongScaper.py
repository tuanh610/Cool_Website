import os.path
import Core.scraping.ScrapEngine as ScrapEngine
from Core.scraping.PhoneData import PhoneData, PhoneDataInvalidException
from urllib.parse import urljoin

class NoProductFoundException(Exception):
    pass

class TheGioiDiDongScraper:
    def __init__(self, ignoreTerm, url, param):
        self.url = url
        self.ignoreTerm = ignoreTerm
        self.param = param

    def parseData(self, content, url):
        listMobile = []
        listProduct = content.find('ul', attrs={'class': 'homeproduct'})
        temp = listProduct.findAll('li')
        allProducts = [x.find('a', href=True) for x in temp]
        if len(allProducts) == 0:
            raise NoProductFoundException
        for a in allProducts:
            try:
                image_html = ScrapEngine.hideInvalidTag(a.find('img'), ['strike'])
                name_html = ScrapEngine.hideInvalidTag(a.find('h3'), ['strike'])
                price_html = ScrapEngine.hideInvalidTag(a.find('div', attrs={'class': 'price'}), ['strike', 'span'])
                image_src = "NA"
                if 'src' in image_html.attrs:
                    image_src = image_html['src']
                elif 'data-original' in image_html.attrs:
                    image_src = image_html['data-original']
                name = ScrapEngine.processString(name_html.getText(), self.ignoreTerm)
                name_idx = name.find(" ")

                price = ScrapEngine.processString(price_html.getText(), self.ignoreTerm)
                href = "n.a"
                href = urljoin(url, a['href'])
                try:
                    listMobile.append(PhoneData(brand=name, model="", price=price, vendor="thegioididong",
                                                info={"url": href, "img": image_src}))
                except PhoneDataInvalidException as error:
                    print("Unable to parse: " + name + ": " + price + ". Error:" + str(error))
                    pass
            except Exception as e:
                print("Error: " + str(e))
                pass
        print("Done with: " + url)
        return listMobile

    def getAllPages(self):
        return self.parseData(ScrapEngine.connectToWebsiteWithBtnClick(self.url, self.param), self.url)
