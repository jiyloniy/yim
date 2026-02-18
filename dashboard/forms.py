from django import forms
from accounts.models import User
from .models import (
    Laboratory, Program, Event, Project,
    Partner, Application, Certificate, News, SiteSetting
)


class StyledFormMixin:
    """Mixin to add consistent styling to form fields"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            css_class = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            elif isinstance(field.widget, forms.FileInput):
                css_class = 'form-control'
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows'] = 4
            field.widget.attrs.update({
                'class': css_class,
                'placeholder': field.label or field_name.replace('_', ' ').title(),
            })


class LoginForm(forms.Form):
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


class LaboratoryForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ['name', 'icon', 'image', 'description', 'order', 'is_active']


class ProgramForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'name', 'laboratory', 'image', 'description', 'level',
            'age_min', 'age_max', 'format', 'duration',
            'start_date', 'end_date', 'is_active'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EventForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'image', 'description', 'date', 'location', 'is_active']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'author', 'image', 'description', 'stage', 'team_members', 'is_approved', 'is_active']


class PartnerForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'website', 'order', 'is_active']


class CertificateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['user', 'program', 'title', 'certificate_id', 'issued_date', 'pdf_file']
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
        }


class NewsForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'slug', 'image', 'content', 'is_published', 'published_at']
        widgets = {
            'published_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class UserForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Parol (bo'sh qoldiring o'zgartirmaslik uchun)"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'avatar', 'bio', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class UserCreateForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Parol")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'role', 'avatar', 'bio', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class SiteSettingForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = [
            'site_name', 'site_logo', 'site_favicon', 'slogan', 'about_text',
            'phone', 'email', 'address', 'telegram_link', 'instagram_link',
            'youtube_link', 'map_embed', 'working_hours'
        ]
