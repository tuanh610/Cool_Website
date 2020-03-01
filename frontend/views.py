from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import SearchForm, PhotoSubmitForm
from .models import Photo
from Core.database.phoneDBEngine import phoneDBEngine
import Core.constant as constants
import Core.utilityHelper as helper
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def new_search(request):
    if request.method == "POST":
        #If cancel then go back to main page
        if "cancel" in request.POST:
            return redirect('home', permanent=True)

        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            devType = str(searchform.cleaned_data.get('type'))
            brand = str(searchform.cleaned_data.get('brand'))
            model = str(searchform.cleaned_data.get('model'))
            lowPrice = searchform.cleaned_data.get('lowPrice')
            highPrice = searchform.cleaned_data.get('highPrice')
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
        searchform = SearchForm()
        return render(request, template_name='mobile/new_search.html', context={"form": searchform})

def search_PriceRange(request, dev, low, high, page):
    phoneDB = phoneDBEngine(tableName=constants.dynamoDBTableName)
    phones = phoneDBEngine.convertAllDataToPhone(phoneDB.getItemWithBrandAndPriceAndType(devType=dev, lowerLim=low, higherLim=high))
    phones.sort(key=lambda phone: phone.price)
    collections = phoneDBEngine.orderPhonesToCollections(phones)

    paginator = Paginator(collections, 12)
    allData = paginator.get_page(page)

    return render(request, 'mobile/all_mobiles.html',
                  {'allData': allData, 'dev': dev, 'low': low, 'high': high})

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

def submit_photo(request):
    """
    View of the photos submit, can be multiple files
    :param request:
    :return:
    On success -> Photo uploaded success window
    On error -> Photo uploaded error window
    """
    if request.method == "POST":
        #if cancel then return to main page
        if "cancel" in request.POST:
            return redirect('home', permanent=True)

        submit_form = PhotoSubmitForm(request.POST, request.FILES)
        if submit_form.is_valid():
            files = request.FILES.getlist('photo')
            no_file = len(files)
            no_file_uploaded = 0
            for file in files:
                item = Photo(title=submit_form.cleaned_data.get('title'), tags=submit_form.cleaned_data.get('tags'), draft=submit_form.cleaned_data.get('draft'), photo=file, added_by=request.user)
                item.save()
                no_file_uploaded += 1
        return redirect('request_result_ok',
                            "{} photos added at {}.\n{} photos fail to upload".format(no_file_uploaded,helper.utcToLocal(item.created_at).strftime("%d %b %Y %H:%M:%S"), no_file-no_file_uploaded))
    else:
        submit_form = PhotoSubmitForm()
        response = render(request, template_name='photos/addPhoto.html', context={"form": submit_form})
        response['Cache-Control'] = 'no-cache'
        return response

def view_photos(request, mode, page, username=None):
    """
    This is the view to View all published photos
    :param request:
    :param mode: 0 - sort in time order, from latest to oldest, 1- oldest to latest, 2-by user
    :param page: page number to display
    :param username: view photos by users, only effective when mode set to 2
    :return: Render all photos
    """
    all_users = User.objects.all()
    #Grab normal photo
    if (mode == 0):
        all_photos = list(Photo.objects.filter(draft=False).order_by('-created_at'))
    elif (mode == 1):
        all_photos = list(Photo.objects.filter(draft=False).order_by('created_at'))
    else:
        if len(all_users) == 0:
            return redirect('request_result_error', "No user has been created", permanent=True)
        if username is None:
            user = all_users[0].username
        else:
            user = username
        all_photos = list(Photo.objects.filter(added_by__username=user).filter(draft=False).order_by('-created_at'))

    paginator = Paginator(all_photos, 12)
    allData = paginator.get_page(page)
    return render(request, template_name='photos/viewPhotos.html',
                  context={"allData": allData, "mode": mode, "all_users": all_users, "username":username})

def view_drafts(request, mode, page):
    """
    This is the view to View all draft photos of current user
    :param request:
    :param mode: 0 - sort in time order, from latest to oldest, 1- oldest to latest
    :param page: page number to display
    :return: Render all drafts
    """
    if not request.user.is_authenticated:
        return redirect('login')
    if (mode == 0):
        all_photos = list(Photo.objects.filter(added_by__username=request.user.username).filter(draft=True).order_by('-created_at'))
    else:
        all_photos = list(Photo.objects.filter(added_by__username=request.user.username).filter(draft=True).order_by('created_at'))

    paginator = Paginator(all_photos, 12)
    allData = paginator.get_page(page)
    return render(request, template_name='photos/viewDrafts.html',
                  context={"allData": allData, "mode": mode})


def photo_detail(request, pk):
    """
    Show the detail of each photo
    :param request:
    :param pk: primary key of the photo, in this case the uuid
    :return:
    render the detail view of each photo
    """
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, template_name='photos/photo_detail.html', context={"item": photo})

def publish_draft(request):
    """
    This view will handle changing the draft to False
    :param request:
    :return: Go to result view page
    """
    if request.method == "POST":
        if "id" in request.POST:
            try:
                photo_id = request.POST["id"]
                item = Photo.objects.get(pk=photo_id)
                item.draft = False
                item.save()
                return redirect('request_result_ok',
                                "Published successfully. Photo {} is available to public".format(item.title), permanent=True)
            except ObjectDoesNotExist:
                return redirect('request_result_error',
                                "Request ID incorrect. Cannot find request", permanent=True)
    else:
        return redirect('request_result_error',
                        "Invalid operation", permanent=True)

def delete_draft(request):
    """
    This view will handle deleting draft
    :param request:
    :return: Go to result view page
    """
    if request.method == "POST":
        if "id" in request.POST:
            try:
                photo_id = request.POST["id"]
                item = Photo.objects.get(pk=photo_id)
                photo_name = item.title
                item.delete()
                return redirect('request_result_ok',
                                "Delete successfully. Photo {} is available to public".format(photo_name), permanent=True)
            except ObjectDoesNotExist:
                return redirect('request_result_error',
                                "Request ID incorrect. Cannot find request", permanent=True)
    else:
        return redirect('request_result_error',
                        "Invalid operation", permanent=True)