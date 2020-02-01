from Core.mail.mailingModule import mailModule
import Core.constant as constant
from Core.database.phoneDBEngine import phoneDBEngine
from Core.scraping.ScrapEngine import parser as scrap_parser
import os

def masterUpdate():
    ChangesToNotify = {}
    phoneDBAdaper = phoneDBEngine(constant.dynamoDBTableName)
    all_brands = set()
    # Get all phones from DB
    dataFromDB = phoneDBAdaper.getAllDevicesWithType('Mobile')
    phonesFromDB = phoneDBEngine.convertAllDataToPhone(dataFromDB)

    # Loop through each source to update information
    for src in constant.scrapingSources:
        if src.name in scrap_parser:
            parser = scrap_parser[src.name](src.info.ignoreTerm, src.url, src.info.param)
            phonesFromScraper = parser.getAllPages()
            if phonesFromScraper is None or len(phonesFromScraper) == 0:
                continue
            # Update data for each source
            priceChange = []
            infoChange = []
            newItem = []
            # Update data
            for item in phonesFromScraper:
                all_brands.add(item.getBrand())
                existed = False
                for phone in phonesFromDB:
                    if item == phone:
                        if item.checkPriceChange(oldData=phone):
                            priceChange.append((item, phone))
                        elif item.checkInfoChange(oldData=phone):
                            infoChange.append((item, phone))
                        existed = True
                        break
                if not existed:
                    newItem.append(item)
            # Delete old items that not there anymore
            toDelete = []
            for phone in phonesFromDB:
                existed = False
                for item in phonesFromScraper:
                    if item == phone:
                        existed = True
                        break
                if not existed and phone.getVendor() == src.name:
                    toDelete.append(phone)

            # push new data to database
            for item, _ in priceChange:
                phoneDBAdaper.updateItemToDB(item)

            for item, _ in infoChange:
                phoneDBAdaper.updateItemToDB(item)

            for item in toDelete:
                phoneDBAdaper.deleteItemFromDB(item)

            if len(newItem) > 0:
                phoneDBAdaper.pushAllDataToDB(newItem)

            # Add changes to notify list
            ChangesToNotify[src.name] = (newItem, priceChange, toDelete)

        else:
            print("Parser for " + src.name + " is not available. Skip")

    # Update all brands
    if len(all_brands) > 0:
        phoneDBAdaper.updateAllBrandData(list(all_brands))
        fullpath = "{}/Core/brands.txt".format(os.path.dirname(os.path.realpath(__file__)))
        f = open(fullpath, "+w")
        f.write(', '.join(list(all_brands)))
        f.close()

    return ChangesToNotify


def notifyByEmail(changes):
    content = ""
    for src in changes:
        newItem, updateNeeded, toDelete = changes[src]
        if len(newItem) == 0 and len(updateNeeded) == 0 and len(toDelete)== 0:
            continue
        content += "Update for %s:\n" % src
        if len(newItem) > 0:
            content += "New Items:\n"
            for item in newItem:
                info = item.getInfo()
                content += "Name: %s. Price: %d %s\n" % (item.getName(), item.getPrice(), info["currency"])
                if "url" in info:
                    content += "URL: %s\n" % info["url"]
        if len(updateNeeded) > 0:
            content += "Price Change Items:\n"
            for item, oldItem in updateNeeded:
                info = item.getInfo()
                oldInfo = oldItem.getInfo()
                content += "Name: %s. Old price: %d %s. New Price: %d %s\n" % (item.getName(),
                                                                               oldItem.getPrice(),
                                                                               oldInfo["currency"],
                                                                               item.getPrice(), info["currency"])
        if len(toDelete) > 0:
            content += "Items Removed: "
            for item in toDelete:
                content += "Name: %s. From vendor: %s\n" % (item.getName(), item.getVendor())
        content += "==========================================================================\n"

    if content != "":
        mail = mailModule()
        service = mail.getCredential()
        message = mail.create_message("warmboy610@gmail.com", "tuanh.dang610@gmail.com", "Update Price", content)
        result = mail.send_message(service, message)
        print(result)
    else:
        print("Nothing new to notify users")


"""
NotifyByEmail is false as I do not include the credentials and tokens of my Gmail account here 
Once the project is pulled from the projects, please use the link in mailingModule to get your
credentials.json file. Then enable this code by set notifyByEmail to true
"""

notify = True
changeToSend = masterUpdate()
if notify:
    notifyByEmail(changeToSend)
print("done")


