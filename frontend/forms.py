from django import forms
from Core.database.phoneDBEngine import phoneDBEngine
import Core.constant as constants


class SearchForm(forms.Form):
    phoneDBAdapter = phoneDBEngine(tableName=constants.dynamoDBTableName)
    brands = phoneDBAdapter.getAllBrandData()
    allChoices = [(x, x) for x in brands]
    brand = forms.ChoiceField(choices=allChoices, label="Brands")
    model = forms.CharField(label="Models")
    type = forms.ChoiceField(choices=[("Mobiles", "Mobiles")])
    lowPrice = forms.IntegerField(min_value=0)
    highPrice = forms.IntegerField(min_value=0)
