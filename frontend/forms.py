from django import forms
from Core.database.phoneDBEngine import phoneDBEngine
import Core.constant as constants
import Core.utilityHelper as helper
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div
#from crispy_forms.layout import Layout, Submit, Row, Column
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Photo

class SearchForm(forms.Form):
    phoneDBAdapter = phoneDBEngine(tableName=constants.dynamoDBTableName)
    brands = phoneDBAdapter.getAllBrandData()
    if brands is None:
        brands = helper.readBrandsFromFile()
    allChoices = [(x, x) for x in brands]
    brand = forms.ChoiceField(choices=allChoices, label="Brands")
    model = forms.CharField(label="Models", required=False)
    type = forms.ChoiceField(choices=[("Mobile", "Mobile")])
    lowPrice = forms.IntegerField(min_value=0, required=False)
    highPrice = forms.IntegerField(min_value=0, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('frontend:new_search')
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('brand', css_class='col col-md-6'),
                    Column('model', css_class='col col-md-6'),
                    css_class='row mt-3'
                ),
                Row(
                    Column('type', css_class='col col-md-12'),
                    css_class='row'),
                Row(
                    Column('lowPrice', css_class='col col-md-6'),
                    Column('highPrice', css_class='col col-md-6'),
                    css_class='row mb-3'
                ),
                css_class="container border border-info rounded"
            ),
            Div(
                Row(
                    Column(
                        Submit('submit', "Submit", css_class="btn btn-primary"),
                        css_class="col-2"
                    ),
                    Column(
                        Submit('cancel', "Cancel", css_class="btn btn-danger", formnovalidate='formnovalidate'),
                        css_class="col-2"
                    )
                ),
                css_class="container pt-3"
            )
        )

class PhotoSubmitForm(forms.ModelForm):
    """
    A Form used to request the photos submission
    """
    class Meta:
        model = Photo
        fields = ('title', 'tags', 'draft', 'photo')
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'multiple': True})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('frontend:submit_photo')
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('title', css_class='col'),
                    css_class="pt-3",
                ),
                Row(
                    Column('tags', css_class='col'),
                ),
                Row(
                    Column('draft', css_class='col'),
                ),
                Row(
                    Column('photo', css_class='col'),
                    css_class="pb-3",
                ),
                css_class= "container border border-info rounded"
            ),
            Div(
                Row(
                    Column(
                        Submit('submit', "Submit", css_class="btn btn-primary"),
                        css_class="col-2"
                    ),
                    Column(
                        Submit('cancel', "Cancel", css_class="btn btn-danger", formnovalidate='formnovalidate'),
                        css_class="col-2"
                    )
                ),
                css_class= "container pt-3"
            )
        )