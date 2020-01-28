from django.shortcuts import render
from Core.database.phoneDBEngine import phoneDBEngine
from django.core.paginator import Paginator
import Core.constant as constants
import Core.utilityHelper as helper
import Core.constant as constant
from .forms import SearchForm
# Create your views here.

def home(request):
    return render(request, 'home.html', {'sources': constants.scrapingSources})


def about(request):
    return render(request, 'about.html')


def new_search(request):
    searchform = SearchForm()
    return render(request, template_name='mobile/new_search.html', context={"form": searchform})

def search_result(request):
    try:
        phoneDBAdapter = phoneDBEngine(tableName=constant.dynamoDBTableName)
        devType = request.POST['TYPE']
        brand = request.POST['BRAND']
        model = request.POST['MODEL']
        lowerLim = request.POST['LOWER_LIM']
        higherLim = request.POST['HIGHER_LIM']
    except KeyError:
        return render(request, 'mobile/search_result.html', {
            'error_message': "You didn't select any filter conditions"
        })
    else:
        if model != "NONE" and brand != "NONE":
            temp = phoneDBAdapter.getItemsWithBrandAndModel(brand, model)
            results = phoneDBEngine.convertAllDataToPhone(temp)
        elif model == "NONE" and brand != "NONE":
            if lowerLim == "NONE" or higherLim == "NONE" or devType == "NONE":
                temp = phoneDBAdapter.getItemsWithBrandAndModel(brand)
                results = phoneDBEngine.convertAllDataToPhone(temp)
            else:
                temp = phoneDBAdapter.getItemWithBrandAndPriceAndType(devType=devType, brand=brand,
                                                                      lowerLim=int(lowerLim), higherLim=int(higherLim))
                results = phoneDBEngine.convertAllDataToPhone(temp)
        else:
            results = phoneDBAdapter.getPhonesInPriceRange(int(lowerLim), int(higherLim))
        return render(request, 'mobile/search_result.html', {'allData': results})




def all_mobiles(request, page):
    # Retrieve all data from amazonDB
    phoneDB = phoneDBEngine(tableName=constants.dynamoDBTableName)
    phones = phoneDB.getAllPhones()
    processedList = helper.getLowestPriceList(phones)
    paginator = Paginator(list(processedList.values()), 12)
    allData = paginator.get_page(page)

    return render(request, 'mobile/all_mobiles.html',
                  {'allData': allData})
