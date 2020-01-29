from django import forms
from Core.database.phoneDBEngine import phoneDBEngine
import Core.constant as constants
import Core.utilityHelper as helper
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.urls import reverse

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
        self.helper.form_action = reverse('frontend:search_result')
        self.helper.layout = Layout(
            Row(
                Column('brand', css_class='col s6'),
                Column('model', css_class='col s6'),
                css_class='row'
            ),
            Row(
                Column('type', css_class='col s12'),
                css_class='row'),
            Row(
                Column('lowPrice', css_class='col s6'),
                Column('highPrice', css_class='col s6'),
            ),
            Submit('submit', "Submit", css_class="waves-effect waves-light")
        )
