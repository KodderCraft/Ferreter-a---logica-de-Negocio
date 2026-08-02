from django import forms

class CSVForm(forms.Form):
    archivo = forms.FileField()