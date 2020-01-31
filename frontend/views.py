from django.shortcuts import render, redirect
from Core.database.phoneDBEngine import phoneDBEngine
from django.core.paginator import Paginator
import Core.constant as constants
import Core.utilityHelper as helper
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
        if request.method == "POST":
            searchform = SearchForm(request.POST)
            if searchform.is_valid():
                devType = str(searchform.cleaned_data.get('type'))
                brand = str(searchform.cleaned_data.get('brand'))
                model = str(searchform.cleaned_data.get('model'))
                lowPrice = searchform.cleaned_data.get('lowPrice')
                highPrice = searchform.cleaned_data.get('highPrice')
                print(devType, brand, model, lowPrice, highPrice)

                phoneAdapter = phoneDBEngine(tableName=constants.dynamoDBTableName)
                phones = phoneAdapter.filterItemsWithConditions(brand, model.lower(), devType, lowPrice, highPrice)
                phones.sort(key=lambda phone: phone.price)
                collections = phoneDBEngine.orderPhonesToCollections(phones)
                return render(request, 'mobile/search_result.html', {'allData': collections})
            else:
                render(request, 'mobile/search_result.html', {
                    'error_message': "Filter Conditions are wrong"
                })
        else:
            return redirect('frontend:new_search')
    except KeyError:
        return render(request, 'mobile/search_result.html', {
            'error_message': "You didn't select any filter conditions"
        })


def search_PriceRange(request, dev, low, high):
    phoneDB = phoneDBEngine(tableName=constants.dynamoDBTableName)
    phones = phoneDBEngine.convertAllDataToPhone(phoneDB.getItemWithBrandAndPriceAndType(devType=dev, lowerLim=low, higherLim=high))
    phones.sort(key=lambda phone: phone.price)
    collections = phoneDBEngine.orderPhonesToCollections(phones)

    return render(request, 'mobile/search_result.html',
                  {'allData': collections})

def all_mobiles(request, page):
    # Retrieve all data from amazonDB
    phoneDB = phoneDBEngine(tableName=constants.dynamoDBTableName)
    data = phoneDB.getAllDevicesWithType('Mobile')
    phones = phoneDBEngine.convertAllDataToPhone(data)
    collections = phoneDBEngine.orderPhonesToCollections(phones)
    paginator = Paginator(collections, 12)
    allData = paginator.get_page(page)

    return render(request, 'mobile/all_mobiles.html',
                  {'allData': allData})
