from django import forms
from django.forms import ModelForm
from .models import Menu, MenuCategory

 
class MenuForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(MenuForm, self).__init__(*args, **kwargs)
    self.fields['img'].widget.attrs.update({
      'id':'menu_img',
      'name':'img',
      'class':'form-control'
    })
    self.fields["name"].widget.attrs.update({
      'required':'',
      'id':'menu_name',
      'name':'name',
      'class':'form-control'
    })
    self.fields["category"].widget.attrs.update({
      'id':'menu_category',
      'name':'category',
      'class':'form-control p-2'
    })
    self.fields["detail"].widget.attrs.update({
      'id':'menu_detail',
      'name':'detail',
      'rows': '3',
      'class':'form-control',
    })
    self.fields["price"].widget.attrs.update({
      'id':'menu_detail',
      'name':'detail',
      'class':'form-control',
    })
    self.fields["discount"].widget.attrs.update({
      'id':'menu_discount',
      'name':'discount',
      'class':'form-control',
    })
    self.fields["qty"].widget.attrs.update({
      'id':'menu_qty',
      'name':'qty',
      'class':'form-control',
    })
  class Meta:
    model = Menu
    fields = (  "img", "name", "category", "detail", "price", "discount", "qty", "added_by", "updated_by"
)


class MenuCategorytForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(MenuForm, self).__init__(*args, **kwargs)
    self.fields['name'].widget.attrs.update({
      'id':'menu_cat_name',
      'name':'name',
      'class':'form-control'
    })
  
    self.fields['description'].widget.attrs.update({
      'id':'menu_cat_description',
      'name':'description',
      'rows':'4',
      'class':'form-control'
    })
  
  class Meta:
    model = MenuCategory
    fields = ("name", "description", "added_by", "updated_by")