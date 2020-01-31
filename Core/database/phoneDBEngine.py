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

    # region push and update
    def pushAllDataToDB(self, data: [PhoneData]):
        for phone in data:
            self.table.put_item(
                Item=phoneDBEngine.convertPhoneToDBData(phone)
            )
        #print("Data pushed completed")

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
            pass
            # print("UpdateItem succeeded:")

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
    # endregion

    def getItemWithBrandAndPriceAndType(self, devType: str, lowerLim, higherLim, brand: str = None):
        try:
            gsiElement = constant.phoneSecondaryElements[0]
            if brand is None:
                response = self.table.query(
                    IndexName=gsiElement.name,
                    KeyConditionExpression=Key(gsiElement.elements[0].name).eq(devType) &
                                           Key(gsiElement.elements[1].name).between(lowerLim, higherLim)
                )
            else:
                response = self.table.query(
                    IndexName=gsiElement.name,
                    KeyConditionExpression=Key(gsiElement.elements[0].name).eq(devType) &
                                           Key(gsiElement.elements[1].name).between(lowerLim, higherLim),
                    FilterExpression=Key(constant.phonePrimaryElements[0].name).eq(brand),
                )
            return response['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])

    def getAllDataFromTable(self):
        try:

            response = self.table.scan(
                FilterExpression=Attr('PRICE').gt(0)
            )
            return response['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])

    def getSpecificItemFromDB(self, brand: str, model: str, vendor: str):
        try:
            response = self.table.get_item(
                Key={
                    'BRAND': brand,
                    'MODEL': model + "_" + vendor
                }
            )
            return response['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ClientError
        except KeyError as e:
            print("Data is empty. No Item found")
            return None

    def getItemsWithBrandAndModel(self, brand, model=None):
        try:
            if model is None:
                condition = Key('BRAND').eq(brand)
            else:
                condition = Key('BRAND').eq(brand) & Key('MODEL').begins_with(model)

            response = self.table.query(
                KeyConditionExpression=condition
            )
            return response['Items']
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ClientError
        except KeyError as e:
            print("Data is empty. No Item found")
            return None

    def getPhonesInPriceRange(self, lowerLim, upperLim):
        try:
            gsiElement = constant.phoneSecondaryElements[0]
            response = self.table.query(
                IndexName=gsiElement.name,
                KeyConditionExpression=Key(gsiElement.elements[0].name).eq('Mobile') &
                                       Key(gsiElement.elements[1].name).between(lowerLim, upperLim),
            )
            result = []
            for item in response['Items']:
                phone = phoneDBEngine.convertDBDataToPhone(item)
                if phone is not None:
                    result.append(phone)
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])


    def getAllPhones(self):
        try:
            gsiElement = constant.phoneSecondaryElements[0]
            response = self.table.query(
                IndexName=gsiElement.name,
                KeyConditionExpression=Key(gsiElement.elements[0].name).eq('Mobile'),
            )
            result = []
            for item in response['Items']:
                phone = phoneDBEngine.convertDBDataToPhone(item)
                if phone is not None:
                    result.append(phone)
            return result
        except ClientError as e:
            print(e.response['Error']['Message'])

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
            pass
            #print("DeleteItem succeeded:")

    def filterItemsWithConditions(self, brand, model, devType, lowPrice, highPrice):
        if model != '' and brand != '':
            temp = self.getItemsWithBrandAndModel(brand, model)
            results = phoneDBEngine.convertAllDataToPhone(temp)
        elif model == '' and brand != '':
            if lowPrice is None or highPrice is None or devType == '':
                temp = self.getItemsWithBrandAndModel(brand=brand)
                results = phoneDBEngine.convertAllDataToPhone(temp)
            else:
                temp = self.getItemWithBrandAndPriceAndType(devType=devType, brand=brand,
                                                            lowerLim=int(lowPrice), higherLim=int(highPrice))
                results = phoneDBEngine.convertAllDataToPhone(temp)
        else:
            results = self.getPhonesInPriceRange(int(lowPrice), int(highPrice))
        return results

    # region Static Methods
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
                             price=item['PRICE'], vendor=item['VENDOR'], name=item['NAME'], info=item['INFO'])
        except PhoneDataInvalidException as error:
            print("Phone data invalid: " + item['NAME'] + ": " + item['PRICE'])

    @staticmethod
    def convertPhoneToDBData(phone: PhoneData):
        return {
            'BRAND': phone.getBrand(),
            'MODEL': phone.getDBModel(),
            'NAME': phone.getName(),
            'TYPE': 'Mobile',
            'PRICE': phone.getPrice(),
            'VENDOR': phone.getVendor(),
            'INFO': phone.getInfo()
        }

    @staticmethod
    def convertAllDataToPhone(items):
        result = []
        for item in items:
            temp = phoneDBEngine.convertDBDataToPhone(item)
            if temp is not None:
                result.append(temp)
        return result
    # endregion


