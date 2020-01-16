import unittest
import Core.constant as constant
import os

class TestHoangHaMobileScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ignoreTerm = ["Chính hãng", "Chính Hãng", "-"]
        url = "https://hoanghamobile.com/dien-thoai-di-dong-c14.html"
        param = '?sort=0&p='
        cls.scraper = constant.parser.get('hoanghaMobile')(ignoreTerm=ignoreTerm, url=url, param=param)

    def test_ParsePage(self):
        result = self.scraper.getOnePage(os.path.dirname(os.path.realpath(__file__)) + "/../testdata/testWebsite.html")
        self.assertEqual(20, len(result))
        self.assertEqual(result[0].getName(), "Samsung Galaxy A50  6GB/128GB")
        self.assertEqual(result[0].getBrand(), "Samsung")
        self.assertEqual(result[0].getModel(), "Galaxy A50  6GB/128GB")
        self.assertEqual(result[0].getPrice(), 5550000)
        self.assertEqual(result[0].getInfo().get("url"), "https://hoanghamobile.com/samsung-galaxy-a50-6gb128gb-chinh-hang-p14862.html")
        self.assertEqual(result[0].getInfo().get("img"), "./testWebsite_files/201912161609127044_A500.png")

    def test_getAllPages(self):
        result = self.scraper.getAllPages()
        self.assertGreater(len(result), 30)

if __name__ == '__main__':
    unittest.main()
