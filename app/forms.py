from django import forms
from .models import ShippingAddress

class ContactShipping(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address','city','state','phone','quantity',]
        widgets = {
            'quantity': forms.HiddenInput()  # Sử dụng HiddenInput nếu không muốn người dùng chỉnh sửa
        }
   