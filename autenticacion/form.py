from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# Obtener el modelo de usuario activo
User = get_user_model()

class RegistroUsuarioForm(UserCreationForm):
    #
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder':'Nombre',
        }))
    
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder':'Apellido',
        }))

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                    'placeholder':'Correo Electrónico',
        }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado")
        return email  

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está registrado")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user


        