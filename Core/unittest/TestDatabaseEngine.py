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
            result = self.db.getPhoneFromDB(brand=self.phone.getBrand(),
                                            model=self.phone.getModel(), vendor=self.phone.getVendor())
            self.assertEqual(result.getPrice(), self.phone.getPrice())
            self.assertEqual(result.getInfo().get("currency"), self.phone.getInfo().get("currency"))
        except ClientError as e:
            self.fail("update Data failed")
        # Delete
        self.db.deleteItemFromDB(self.phone)
        temp = self.db.getPhoneFromDB(brand=self.phone.getBrand(),
                                                 model=self.phone.getModel(), vendor=self.phone.getVendor())
        self.assertIsNone(temp)

if __name__ == '__main__':
    unittest.main()
