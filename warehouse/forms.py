from django import forms
from .models import Item, Order,Stock, Category,User,MaterialRequest
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm

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
    first_name = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Required.',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    user_name = forms.CharField(
        max_length=200,
        required=True,
        help_text='Required.',
        widget=forms.TextInput(attrs={'placeholder': 'User name'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Retype password'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'user_name',  'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['user_name', 'password']

class UserEditForm(UserChangeForm):
    class Meta:
        model =User
        fields = ['user_type']
        
class materialrequestForm(forms.ModelForm):
    class Meta:
        model = MaterialRequest
        fields = ['quantity_requested','item']

class EditmaterialrequestForm(forms.ModelForm):
    class Meta:
        model = MaterialRequest
        fields = ['status']
