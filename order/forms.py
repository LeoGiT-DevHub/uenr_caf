from django import forms

from finance.models import OrderPayment

from .models import Cart, Order


class OrderForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(OrderForm, self).__init__(*args, **kwargs)
    self.fields["customer_name"].widget.attrs.update({
      'id':'order_customer_name',
      'type':'text',
      'name':'customer_name',
      'placeholder':'Customer Name',
      'class':'form-control form-inline border-start-0 border-top-0 border-end-0 col-auto'
    })
    self.fields["customer_contact"].widget.attrs.update({
      'id':'order_customer_contact',
      'type':'text',
      'name':'customer_contact',
      'placeholder':'Customer Contact',
      'class':'form-control form-inline border-start-0 border-top-0 border-end-0 col-auto'
    })
    self.fields["customer_email"].widget.attrs.update({
      'id':'order_customer_email',
      'type':'email',
      'name':'customer_email',
      'placeholder':'Customer email',
      'class':'form-control form-inline border-start-0 border-top-0 border-end-0 col-12'
    })
    self.fields["delivery_address"].widget.attrs.update({
      'id':'order_delivery_address',
      'type':'text',
      'name':'delivery_address',
      'placeholder':'Delivery Address',
      'class':'form-control'
      })
    self.fields["address_description"].widget.attrs.update({
      'id':'order_address_description',
      'name':'address_description',
      'placeholder':'Address Description',
      'rows':'3',
      'class':'form-control h-100'
    })
    self.fields["payment_method"].widget.attrs.update({
      'id':'order_payment_method',
      'name':'payment_method',
      'class':'form-control'
    })
    self.fields["due_date"].widget.attrs.update({
      'id':'order_due_date',
      'name':'due_date',
      'class':'form-control w-50'
    })
    self.fields["served"].widget.attrs.update({
      'id':'order_served',
      'name':'served',
      'class':'form-check-input'
    })

  class Meta:
    model = Order
    fields = ("customer_name", "customer_contact", "customer_email", "delivery_address", "address_description", "due_date", "payment_method", "served"
  )
    

class CartForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(CartForm, self).__init__(*args, **kwargs)
    self.fields["qty"].widget.attrs.update({
      'id':'cart_qty',
      'name':'qty',
      'type': 'text',
      'style': 'width: 20px; text-align: center; background: transparent; border:none; outline: none; margin:2px;',
      'value': '4',
    })
  class Meta:
    model = Cart
    fields = ("ref", "user", "menu", "qty", "ordered")
    

