import unittest
import Core.constant as constant
import os

class TestTheGioiDiDongScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        ignoreTerm = ["Chính hãng", "Chính Hãng", "-"]
        url = "https://www.thegioididong.com/dtdd"
        param = 'viewmore'
        cls.scraper = constant.parser.get('thegioididong')(ignoreTerm=ignoreTerm, url=url, param=param)

    def test_ParsePages(self):
        result = self.scraper.getAllPages()
        self.assertGreater(len(result), 30)
        self.assertEqual(result[0].getName(), "Samsung Galaxy Note 10+")
        self.assertEqual(result[0].getBrand(), "samsung")
        self.assertEqual(result[0].getModel(), "galaxy note 10+")
        self.assertEqual(result[0].getPrice(), 24990000)
        self.assertEqual(result[0].getInfo().get("url"), "https://www.thegioididong.com/dtdd/samsung-galaxy-note-10-plus")
        self.assertEqual(result[0].getInfo().get("img"), "https://cdn.tgdd.vn/Products/Images/42/206176/Feature/samsung-galaxy-note-10-plus-720x333-480x222.jpg")


if __name__ == '__main__':
    unittest.main()
