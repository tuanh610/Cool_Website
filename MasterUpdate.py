from Core.mail.mailingModule import mailModule
import Core.constant as constant
from Core.database.phoneDBEngine import phoneDBEngine

def masterUpdate():
    ChangesToNotify = {}
    phoneDBAdaper = phoneDBEngine(constant.dynamoDBTableName)
    all_brands = set()
    # Loop through each source to update information
    data = []
    # region ScrapData
    for src in constant.scrapingSources:
        if src.name in constant.parser:
            parser = constant.parser[src.name](src.info.ignoreTerm, src.url, src.info.param)
            data += parser.getAllPages()
        else:
            print("Parser for " + src.name + " is not available. Skip")
    # endregion

    # region UpdateDatabase
    dataFromDB = phoneDBAdaper.getAllPhones()
    updateNeeded = []
    newItem = []
    # Update data
    for item in data:
        all_brands.add(item.getBrand())
        existed = False
        for phone in dataFromDB:
            if item == phone:
                if item.needUpdate(oldData=phone):
                    updateNeeded.append((item, phone))
                existed = True
                break
        if not existed:
            newItem.append(item)
    # Delete old items that not there anymore
    toDelete = []
    for phone in dataFromDB:
        existed = False
        for item in data:
            if item == phone:
                existed = True
                break
        if not existed:
            toDelete.append(phone)

    # push new data to database
    for item, _ in updateNeeded:
        phoneDBAdaper.updateItemToDB(item)

    for item in toDelete:
        phoneDBAdaper.deleteItemFromDB(item)

    if len(newItem) > 0:
        phoneDBAdaper.pushAllDataToDB(newItem)

    # Add changes to notify list
    ChangesToNotify[src.name] = (newItem, updateNeeded, toDelete)

    # Update all brands
    phoneDBAdaper.updateAllBrandData(list(all_brands))
    f = open("Core/brands.txt", "+w")
    f.write(', '.join(list(all_brands)))
    f.close()
    # endregion
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

        if content == "":
            content = "No update needed"
        content += "================================================================\n"

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


