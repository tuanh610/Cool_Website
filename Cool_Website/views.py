from django.shortcuts import render, redirect
from .forms import UserRegisterForm
import Core.constant as constants

def register(request):
    """
    This page allow user to register for an account for admin related thing
    :param request: The request of page
    :return:
    Render register.html
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('request_result_ok', f'Account created for {username}!', permanent=True)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def request_result(request, status=None, error=None):
    """
    Show result after add/edit/delete operation

    Return
    ----------
    If status exist:
    -> render request_result.html with status parameter

    If error exist:
    -> render request_result.html with error parameter

    Else:
    -> render request_result.html with error parameter as "unknown error"
    """
    if status is not None:
        return render(request, template_name='request_result.html',
                      context={"status": status})
    elif error is not None:
        return render(request, template_name='request_result.html',
                      context={"error": error})
    else:
        return render(request, template_name='request_result.html',
                      context={"error": "Unknown error"})

def home(request):
    return render(request, 'home.html', {'sources': constants.scrapingSources})

def about(request):
    return render(request, 'about.html')