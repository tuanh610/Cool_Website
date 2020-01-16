import unittest
from bs4 import BeautifulSoup
import os
import Core.scraping.ScrapEngine as ScrapEngine

class TestScrapEngine(unittest.TestCase):

    def test_connecttoWebsite(self):
        url = os.path.dirname(os.path.realpath(__file__)) + "/../testdata/testWebsite.html"
        ignoreTerm = ["Chính hãng", "Chính Hãng", "-"]
        try:
            result = ScrapEngine.connectToWebSite(url, ignoreTerm)
            self.assertIsNotNone(result, "Beautiful soup result is none")
        except:
            self.fail("Unable to connect to website")


    def test_processString(self):
        test = "     hello world 213 #$%@*^)@    "
        ignore = ["!", "@", "#", "$", "%", "^", "&", "*", ")", "("]
        output = "hello world 213"
        self.assertEqual(output, ScrapEngine.processString(test, ignore))

    def test_hideTag(self):
        tag = ['a', 'li', 'strike']
        url = os.path.dirname(os.path.realpath(__file__)) + "/../testdata/testWebsite.html"
        content = open(url, encoding='utf8')
        soup = BeautifulSoup(content.read(), features="html.parser")
        result = ScrapEngine.hideInvalidTag(soup, tag)
        temp1 = result.findAll('a')
        temp2 = result.findAll('li')
        temp3 = result.findAll('div')
        self.assertEqual(0, len(temp1))
        self.assertEqual(0, len(temp2))
        self.assertNotEqual(0, len(temp3))

        temp = "<div class=\"product-price\"><strike>33.990.000 ₫</strike> 29.890.000 ₫</div>"
        soup = BeautifulSoup(temp, features="html.parser")
        temp1 = soup.findAll('strike')
        self.assertEqual(1, len(temp1))
        result = ScrapEngine.hideInvalidTag(soup, tag)
        temp1 = result.findAll('strike')
        self.assertEqual(0, len(temp1))

if __name__ == '__main__':
    unittest.main()
