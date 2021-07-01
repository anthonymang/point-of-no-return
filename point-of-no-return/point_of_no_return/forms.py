from django import forms

class SearchForm(forms.Form):
    URI = forms.CharField(label='URI', max_length=100)
    search_type = forms.ChoiceField(label = 'Music Type', choices = (
        ('Album', 'Album'),
        ('Track', 'Track'),
        ('Artist', 'Artist')
    ))