from django import forms
class DingGroupForm(forms.ModelForm):
    def clean(self):
        
            
        SNcode = self.cleaned_data['SNcode']
        print(SNcode) 
