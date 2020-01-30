import unittest
from Core.database import DatabaseEngine
from Core.database.DatabaseEngine import ClientError, DynamoElement
from Core.database.phoneDBEngine import phoneDBEngine
from Core.scraping.PhoneData import PhoneData
import Core.constant as constants


class TestDatabaseCreation(unittest.TestCase):
    def test_dbCreation(self):
        tableName = "test_table"
        outputCreate = "Create table " + tableName + "successfully"
        outputDelete = "Delete table " + tableName + " successfully"
        self.pElements = constants.phonePrimaryElements
        self.sElements = constants.phoneSecondaryElements
        self.assertEqual(outputCreate, DatabaseEngine.createTable(tableName, self.pElements, self.sElements))
        self.assertEqual(outputDelete, DatabaseEngine.deleteTable(tableName))


class TestDatabaseFunctional(unittest.TestCase):

    def setUp(self) -> None:
        self.phone = PhoneData(brand="test", model="Megatron", price="500000 VND", vendor="unitTest")
        self.phone2 = PhoneData(brand="test", model="Megatron XL", price="1000000 VND", vendor="unitTest",
                                info={"url": "https:/testURL.com"})
        self.phone3 = PhoneData(brand="test 1", model="Decepticon", price="$SGD 300000", vendor="unitTest",
                                info={"url": "https:/testURL.com"})

        self.data = [self.phone, self.phone2, self.phone3]
        self.tableName = "test_table"
        self.pElements = constants.phonePrimaryElements
        self.sElements = constants.phoneSecondaryElements
        self.dynamoElements = [DynamoElement('DeviceName', 'HASH', 'S')]
        DatabaseEngine.createTable(self.tableName, self.pElements, self.sElements)
        self.db = phoneDBEngine(self.tableName)

    def tearDown(self) -> None:
        DatabaseEngine.deleteTable(self.tableName)
        
    def test_insert_update_deleteData(self):
        # Insert
        self.db.pushAllDataToDB(self.data)
        retriveData = self.db.getAllDataFromTable()
        ok = True
        for item in self.data:
            if item not in retriveData:
                ok = False
                break
        self.assertTrue(ok, "Push data failed")
        # Update
        self.phone.price = 12345
        self.phone.info["currency"] = "Yolo Dollar"
        self.db.updateItemToDB(self.phone)
        try:
            temp = self.db.getSpecificItemFromDB(brand=self.phone.getBrand(),
                                                   model=self.phone.getModel(), vendor=self.phone.getVendor())
            result = phoneDBEngine.convertAllDataToPhone(temp)
            self.assertEqual(result.getPrice(), self.phone.getPrice())
            self.assertEqual(result.getInfo().get("currency"), self.phone.getInfo().get("currency"))
        except ClientError as e:
            self.fail("update Data failed")
        # Delete
        self.db.deleteItemFromDB(self.phone)
        temp = self.db.getSpecificItemFromDB(brand=self.phone.getBrand(),
                                             model=self.phone.getModel(), vendor=self.phone.getVendor())
        self.assertIsNone(temp)

    def test_getAllPhones_withBrands(self):
        phoneAdapter = phoneDBEngine(constants.dynamoDBTableName)
        data = phoneAdapter.getItemsWithBrandAndModel(brand="Samsung")
        phoneData = phoneDBEngine.convertAllDataToPhone(data)
        for item in phoneData:
            if "Samsung" not in item.getBrand():
                self.fail("Phones not from correct brand." + str(item))

    def test_getAllPhones_withBrands_andModels(self):
        phoneAdapter = phoneDBEngine(constants.dynamoDBTableName)
        data = phoneAdapter.getItemsWithBrandAndModel(brand="Samsung", model="Galaxy A20s")
        phoneData = phoneDBEngine.convertAllDataToPhone(data)
        for item in phoneData:
            if "Samsung" not in item.getBrand():
                self.fail("Phones not from correct brand." + str(item))
            else:
                print(item)

    def test_getAllPhones(self):
        phoneAdapter = phoneDBEngine(constants.dynamoDBTableName)
        data = phoneAdapter.getAllPhones()
        self.assertGreater(len(data), 30)

    def test_getPhonesWithinPriceRange(self):
        lowerLim = 5000000
        higherLim = 10000000
        phoneAdapter = phoneDBEngine(constants.dynamoDBTableName)
        data = phoneAdapter.getPhonesInPriceRange(lowerLim, higherLim)
        self.assertGreater(len(data), 0)
        for item in data:
            if item.getPrice() < lowerLim or item.getPrice() > higherLim:
                self.fail("Price not within range. " + str(item))

    def test_getPhonesWithinPriceRangeWithBrand(self):
        lowerLim = 3000000
        higherLim = 10000000
        brand = "Samsung"
        phoneAdapter = phoneDBEngine(constants.dynamoDBTableName)
        data = phoneAdapter.getItemWithBrandAndPriceAndType(devType='Mobile', brand=brand,
                                                            lowerLim=lowerLim, higherLim=higherLim)
        self.assertGreater(len(data), 0)
        for item in data:
            phone = phoneDBEngine.convertDBDataToPhone(item)
            if phone.getPrice() < lowerLim or phone.getPrice() > higherLim or phone.getBrand() != brand:
                self.fail("Price not within range or Item not from from correct brand. " + str(item))

if __name__ == '__main__':
    unittest.main()
