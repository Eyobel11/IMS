from django import forms
from .models import Item, Order,Stock, Category,User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['item', 'quantity', 'order_date', 'status']

    item = forms.ModelChoiceField(queryset=Item.objects.all(), label="Select Item")
    quantity = forms.IntegerField(min_value=1, label="Quantity", required=True)
    order_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date", required=True)
    status = forms.ChoiceField(choices=[('shipped', 'Shipped'), ('pending', 'Pending')], label="Select Status")

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'description', 'stock']

    name = forms.CharField(label="Name", required=True)
    stock = forms.ModelChoiceField(queryset=Stock.objects.all(), label="Select stock", required=True)
    price = forms.DecimalField(min_value=1, max_digits=10, decimal_places=2, label="Price", required=True)
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")

class catForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description',]

    name = forms.CharField(label="Name", required=True)
    description = forms.CharField(widget=forms.Textarea, required=False, label="Description")
   

class stockform(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['current_level','stock_no','description','category']

   
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_name', 'email', 'user_type', 'password1', 'password2']
    

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['user_name', 'password']