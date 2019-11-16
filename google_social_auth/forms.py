from django import forms
class RequestTokeForm(forms.Form):
   
    client_id = forms.CharField()
    client_secret = forms.CharField()
    id_token = forms.CharField()
    #client_type=forms.CharField(widget=forms.HiddenInput())
    
