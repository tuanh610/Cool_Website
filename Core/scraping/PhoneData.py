import Core.constant as constants
class PhoneDataInvalidException(Exception):
    pass


class PhoneData:
    def __init__(self, brand: str, model: str, price, vendor: str, name=None, info=None):
        if info is None:
            self.info = {}
        else:
            self.info = info
        if model != "":
            self.brand = brand
            self.model = model
        else:
            idx = brand.find(" ")
            temp1 = brand[:idx] if idx >= 0 else brand
            temp2 = brand[idx+1:] if len(brand) > idx+1 > 0 else ""
            for i in range(len(temp1)):
                if temp1[i].isdigit():
                    temp2 = temp1[i:] + (" " + temp2 if temp2 != "" else "")
                    temp1 = temp1[:i]
                    break
            self.brand = temp1
            self.model = temp2

        self.vendor = vendor

        if name is not None:
            self.name = name
        else:
            self.name = self.brand + ' ' + self.model

        self.brand = self.brand.lower()
        self.model = self.model.lower()

        if isinstance(price, str):
            self.price = 0
            self.processPriceString(price)
        else:
            try:
                self.price = float(price)
                if price < 0:
                    raise PhoneDataInvalidException
            except Exception as e:
                raise PhoneDataInvalidException

    def __eq__(self, other):
        if self.brand == other.brand and self.model == other.model and self.vendor == other.vendor:
            return True
        else:
            return False

    def __str__(self):
        return self.getName() + " from " + self.getVendor() + ": " + str(self.getPrice())

    def checkPriceChange(self, oldData):
        if self == oldData and self.price != oldData.price:
            return True
        else:
            return False

    def checkInfoChange(self, oldData):
        if self == oldData and self.info != oldData.info:
            return True
        else:
            return False

    def processPriceString(self, priceStr: str):
        #find currency symbol
        temp = self.batchRemove(priceStr, ["$", ".", ","])
        splited = temp.split(sep=' ')
        splited_len = len(splited)
        try:
            if splited_len >= 2:
                if (not splited[0].isdecimal()) and (not splited[1].isdecimal()):
                    raise PhoneDataInvalidException
                elif splited[0].isdecimal():
                    self.price = int(splited[0])
                    self.info["currency"] = splited[1]
                else:
                    self.price = int(splited[1])
                    self.info["currency"] = splited[0]
            elif splited_len == 1:
                if splited[0].isdecimal():
                    self.price = int(splited[0])
                    self.info["currency"] = "NA"
                else:
                    for currency in constants.currencyCode:
                        if splited[0].startswith(currency):
                            self.price = int(splited[0][len(currency):])
                            self.info["currency"] = currency
                            return
                        elif splited[0].endswith(currency):
                            self.price = int(splited[0][:-len(currency)])
                            self.info["currency"] = currency
                            return
                    raise PhoneDataInvalidException

        except Exception as e:
            print(str(e))
            raise PhoneDataInvalidException

    def batchRemove(self, a: str, lst: [str]):
        temp = a
        for item in lst:
            temp = temp.replace(item, "")
        return temp

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getInfo(self):
        return self.info

    def getBrand(self):
        return self.brand

    def getModel(self):
        return self.model

    def getVendor(self):
        return self.vendor

    def getDBModel(self):
        return self.model + "_" + self.vendor

    def getPriceString(self):
        return ("{:,}".format(self.price)) + " " + self.info.get("currency", "")
