import unittest
from Core.scraping.PhoneData import PhoneData
from Core.scraping.PhoneData import PhoneDataInvalidException

class TestPhoneData(unittest.TestCase):

    def test_init_string(self):
        phone = PhoneData(brand="test", model="Megatron", price="500000 VND", vendor="unitTest")
        self.assertEqual(phone.getPrice(), 500000)
        self.assertEqual(phone.getName(), "test Megatron")

        phone2 = PhoneData(brand="test", model="Megatron XL", price="1000000 VND", vendor="unitTest",
                           info={"url": "https:/testURL.com"})
        self.assertEqual(phone2.getPrice(), 1000000)
        self.assertEqual(phone2.getName(), "test Megatron XL")
        self.assertEqual(phone2.getInfo()["url"], "https:/testURL.com")

        phone3 = PhoneData(brand="test 1", model="Decepticon", price="$SGD 300000", vendor="unitTest",
                                info={"url": "https:/testURL.com"})
        self.assertEqual(phone3.getPrice(), 300000)
        self.assertEqual(phone3.getName(), "test 1 Decepticon")
        self.assertEqual(phone3.getInfo()["currency"], "SGD")

        with self.assertRaises(PhoneDataInvalidException):
            phone4 = PhoneData(brand="test 1", model="Decepticon", price="$SGD abc 300000 ", vendor="unitTest",
                                info={"url": "https:/testURL.com"})


    def test_init_decimal(self):
        phone = PhoneData(brand="test", model="Megatron", price=500000, vendor="unitTest", info={"currency": "SGD"})
        self.assertEqual(phone.getPrice(), 500000)
        self.assertEqual(phone.getName(), "test Megatron")

        phone2 = PhoneData(brand="test", model="Decepticon", price=300.123, vendor="unitTest",
                           info={"url": "https:/testURL.com", "currency": "VND"})
        self.assertEqual(phone2.getPrice(), 300.123)
        self.assertEqual(phone2.getName(), "test Decepticon")
        self.assertEqual(phone2.getInfo()["url"], "https:/testURL.com")
        self.assertEqual(phone2.getInfo()["currency"], "VND")

        with self.assertRaises(PhoneDataInvalidException):
            phone3 = PhoneData(brand="test", model="Decepticon", price=-300.123, vendor="unitTest",
                               info={"url": "https:/testURL.com", "currency": "VND"})

    def test_PhoneName(self):
        phone = PhoneData(brand="test Megatron", model="", price=500000, vendor="unitTest", info={"currency": "SGD"})
        self.assertEqual(phone.getBrand(), "test")
        self.assertEqual(phone.getModel(), "Megatron")

        phone = PhoneData(brand="iPhone6XR", model="", price=500000, vendor="unitTest", info={"currency": "SGD"})
        self.assertEqual(phone.getBrand(), "iPhone")
        self.assertEqual(phone.getModel(), "6XR")

        phone = PhoneData(brand="iPhone6 XR", model="", price=500000, vendor="unitTest", info={"currency": "SGD"})
        self.assertEqual(phone.getBrand(), "iPhone")
        self.assertEqual(phone.getModel(), "6 XR")

    def test_equal(self):
        phone1 = PhoneData(brand="test", model="Decepticon", price=300.123, vendor="unitTest",
                           info={"url": "https:/testURL.com", "currency": "VND"})
        phone2 = PhoneData(brand="test", model="Decepticon", price="300.123 VND", vendor="unitTest")
        self.assertEqual(phone1, phone2)

if __name__ == '__main__':
    unittest.main()
