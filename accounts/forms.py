from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth import get_user_model


class UserCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.pop('autofocus', None)
        self.fields['first_name'].widget.attrs['autofocus'] = 'true'

        # To add extra stuff to rendered element 👇
        # self.fields['email'].widget.attrs['style'] = 'color: red;'

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2',)
