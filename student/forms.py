from django import forms
from accounts.models import User
from dashboard.models import Application, Project


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 4
            field.widget.attrs.update({
                'class': css_class,
            })


class StudentLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Foydalanuvchi nomi',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Parol',
        })
    )


class StudentRegisterForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Parol")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Parolni tasdiqlang")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password_confirm'):
            raise forms.ValidationError("Parollar mos kelmadi!")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'student'
        if commit:
            user.save()
        return user


class StudentProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'bio', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': "Nima uchun bu dasturga qiziqasiz? O'zingiz haqingizda qisqacha yozing...",
                'rows': 5,
            }),
        }
        labels = {
            'message': "Xabar (ixtiyoriy)",
        }


class StudentProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description', 'stage', 'team_members']
        labels = {
            'title': 'Loyiha nomi',
            'image': 'Rasm',
            'description': 'Tavsif',
            'stage': 'Bosqich',
            'team_members': "Jamoa a'zolari",
        }
