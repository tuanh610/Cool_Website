import Core.scraping.PhoneData as PhoneData
import Core.database.phoneDBEngine as phoneDBEngine
import Core.constant as constant


def arrangePhonesToList(phones: [PhoneData]):
    data = {}
    for phone in phones:
        if phone.getName() in data:
            data[phone.getName()].append(phone)
        else:
            data[phone.getName()] = [phone]
    return data


def getLowestPriceList(phones: [PhoneData]):
    data = {}
    for phone in phones:
        if phone.getName() not in data or phone.getPrice() < data[phone.getName()].getPrice():
            data[phone.getName()] = phone
    return data


def initBrandsUsingTextFile():
    phoneDBAdaper = phoneDBEngine(constant.dynamoDBTableName)
    f = open("brands.txt", "r")
    content = f.read()
    f.close()
    brands = content.split(',')
    map(lambda x: x.strip(), brands)
    phoneDBAdaper.updateAllBrandData(brands)
