from Core.scraping.PhoneData import PhoneData



class PhoneCollection:
    def __init__(self, firstPhone: PhoneData):
        self.brand = firstPhone.getBrand()
        self.model = firstPhone.getModel()
        self.name = firstPhone.getName()
        self.minPrice = firstPhone.getPrice()
        self.phoneList = [firstPhone]

    def addIfBelongToCollection(self, phone: PhoneData):
        if self.brand == phone.getBrand() and self.model == phone.getModel():
            self.phoneList.append(phone)
            self.minPrice = min(self.minPrice, phone.getPrice())
            return True
        else:
            return False
