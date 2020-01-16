import boto3
from Core.scraping.PhoneData import PhoneData, PhoneDataInvalidException
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError
import Core.database.DatabaseEngine as DatabaseEngine
import Core.constant as constant


class phoneDBEngine:
    def __init__(self, tableName: str):
        DatabaseEngine.createTable(tableName=tableName, primaryElemens=constant.phonePrimaryElements,
                                   secondaryElements=constant.phoneSecondaryElements)
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
        self.tableName = tableName
        self.table = self.dynamodb.Table(self.tableName)

    def pushAllDataToDB(self, data: [PhoneData]):
        for phone in data:
            self.table.put_item(
                Item=phoneDBEngine.convertPhoneToDBData(phone)
            )
        print("Data pushed completed")

    def getAllDataFromTable(self):
        try:

            response = self.table.scan(
                FilterExpression=Attr('PRICE').gt(0)
            )
            result = []
            for item in response['Items']:
                phone = phoneDBEngine.convertDBDataToPhone(item)
                if phone is not None:
                    result.append(phone)
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])

    def getPhoneFromDB(self, brand: str, model: str, vendor: str):
        try:
            response = self.table.get_item(
                Key={
                    'BRAND': brand,
                    'MODEL': model + "_" + vendor
                }
            )
            item = phoneDBEngine.convertDBDataToPhone(response['Item'])
            if item is not None:
                print("Get item successfully")
            else:
                print("No record for " + brand + " " + model + " from " + vendor)
            return item
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ClientError
        except KeyError as e:
            print("Data is empty. No Item found")
            return None

    def getPhonesFromDB(self, brand: str, model: str = None):
        try:
            if model is None:
                condition = Key('BRAND').eq(brand)
            else:
                condition = Key('BRAND').eq(brand) & Key('MODEL').begins_with(model)

            response = self.table.query(
                KeyConditionExpression=condition
            )
            result = []
            for item in response['Item']:
                phone = phoneDBEngine.convertDBDataToPhone(item)
                if phone is not None:
                    result.append(phone)
            print("Get items successfully")
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ClientError
        except KeyError as e:
            print("Data is empty. No Item found")
            return None

    def getItemsWithPrimaryKey(self, keyCondition, filterCondition):
        try:
            response = self.table.query(
                KeyConditionExpression=keyCondition,
                FilterExpression=filterCondition
            )
            result = []
            for item in response['Items']:
                phone = phoneDBEngine.convertDBDataToPhone(item)
                if phone is not None:
                    result.append(phone)
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])

    def getPhonesInPriceRange(self, lowerLim, upperLim):
        try:
            gsiElement = constant.phoneSecondaryElements[0]
            response = self.table.query(
                IndexName=gsiElement.name,
                KeyConditionExpression=Key(gsiElement.elements[0].name).eq('Mobile') &
                                       Key(gsiElement.elements[1].name).between(lowerLim, upperLim),
            )
            result = []
            for item in response['Item']:
                phone = phoneDBEngine.convertDBDataToPhone(item)
                if phone is not None:
                    result.append(phone)
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])

    def updateItemToDB(self, item: PhoneData):
        try:
            response = self.table.update_item(
                Key={
                    'BRAND': item.getBrand(),
                    'MODEL': item.getDBModel()
                },
                UpdateExpression="set INFO = :i, PRICE = :p",
                ExpressionAttributeValues={
                    ':p': item.getPrice(),
                    ':i': item.getInfo()
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("UpdateItem succeeded:")

    def updateAllBrandData(self, all_brands):
        try:
            response = self.table.update_item(
                Key={
                    'BRAND': constant.dynamoDBAllBrandPK,
                    'MODEL': constant.dynamoDBAllBrandRK,
                },
                UpdateExpression="set BRAND_NAMES = :n",
                ExpressionAttributeValues={
                    ':n': all_brands,
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("All brands list updated succeeded:")

    def getAllBrandData(self):
        try:
            response = self.table.get_item(
                Key={
                    'BRAND': constant.dynamoDBAllBrandPK,
                    'MODEL': constant.dynamoDBAllBrandRK,
                }
            )
            result = []
            for brand in response['Item']['BRAND_NAMES']:
                result.append(brand.strip())
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])


    def deleteItemFromDB(self, item: PhoneData):
        try:
            response = self.table.delete_item(
                Key={
                    'BRAND': item.getBrand(),
                    'MODEL': item.getDBModel()
                },
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("DeleteItem succeeded:")

    @staticmethod
    def convertDBDataToPhone(item):
        try:
            temp = item['MODEL']
            idx = temp.find('_')
            if idx < 0:
                phone_model = temp
            else:
                phone_model = temp[:idx]
            return PhoneData(brand=item['BRAND'], model=phone_model,
                             price=item['PRICE'], vendor=item['VENDOR'], info=item['INFO'])
        except PhoneDataInvalidException as error:
            print("Phone data invalid: " + item['NAME'] + ": " + item['PRICE'])

    @staticmethod
    def convertPhoneToDBData(phone: PhoneData):
        return {
            'BRAND': phone.getBrand(),
            'MODEL': phone.getDBModel(),
            'TYPE': 'Mobile',
            'PRICE': phone.getPrice(),
            'VENDOR': phone.getVendor(),
            'INFO': phone.getInfo()
        }
