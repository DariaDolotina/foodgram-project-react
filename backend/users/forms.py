from recipes.models import CustomUser
from django.contrib.auth.forms import UserCreationForm



class CreationForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ("first_name", "last_name", "username", "email")
