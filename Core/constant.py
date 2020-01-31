from Core.database.DatabaseEngine import DynamoElement, DynamoGSI
from Core.scraping.SourceData import SourceData, SourceInfo

phonePrimaryElements = [DynamoElement('BRAND', 'HASH', 'S'), DynamoElement('MODEL', 'RANGE', 'S')]
phoneSecondaryElements = [DynamoGSI("TypeIndex",
                                    [DynamoElement('TYPE', 'HASH', 'S'), DynamoElement('PRICE', 'RANGE', 'N')])]
dynamoDBTableName = "WebScraperDB"
dynamoDBAllBrandPK = "all_brands"
dynamoDBAllBrandRK = "dummy1"

scrapingSources = [
    SourceData(url="https://www.thegioididong.com/dtdd", name="thegioididong", info=SourceInfo(param="viewmore", ignoreTerm=["Chính hãng", "Chính Hãng", "-"])),
    SourceData(url="https://hoanghamobile.com/dien-thoai-di-dong-c14.html", name="hoanghaMobile", info=SourceInfo(param="?sort=0&p=", ignoreTerm=["Chính hãng", "Chính Hãng", "-"]))
]

priceRange = [(0, 2000000), (2000000, 5000000), (5000000, 10000000), (1000000, 20000000)]

currencyCode = ["₫", "SGD", "USD", "EUR", "INR", "VND", "JPY"]