from django.db import models
from django.conf import settings


class Laboratory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nomi")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Ikonka")
    image = models.ImageField(upload_to='labs/', blank=True, null=True, verbose_name="Rasm")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Laboratoriya"
        verbose_name_plural = "Laboratoriyalar"

    def __str__(self):
        return self.name


class Program(models.Model):
    LEVEL_CHOICES = (
        ('beginner', "Boshlang'ich"),
        ('advanced', "Ilg'or"),
    )
    FORMAT_CHOICES = (
        ('offline', 'Offline'),
        ('online', 'Online'),
        ('hybrid', 'Gibrid'),
    )
    name = models.CharField(max_length=200, verbose_name="Nomi")
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True, blank=True, related_name='programs', verbose_name="Laboratoriya")
    image = models.ImageField(upload_to='programs/', blank=True, null=True, verbose_name="Rasm")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name="Daraja")
    age_min = models.PositiveIntegerField(default=10, verbose_name="Minimal yosh")
    age_max = models.PositiveIntegerField(default=25, verbose_name="Maksimal yosh")
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='offline', verbose_name="Format")
    duration = models.CharField(max_length=100, blank=True, verbose_name="Davomiylik")
    start_date = models.DateField(blank=True, null=True, verbose_name="Boshlanish sanasi")
    end_date = models.DateField(blank=True, null=True, verbose_name="Tugash sanasi")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Dastur"
        verbose_name_plural = "Dasturlar"

    def __str__(self):
        return self.name


class Event(models.Model):
    TYPE_CHOICES = (
        ('masterclass', 'Master-klass'),
        ('hackathon', 'Xakaton'),
        ('lecture', "Ma'ruza"),
        ('competition', 'Tanlov'),
    )
    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='masterclass', verbose_name="Turi")
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Rasm")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    date = models.DateTimeField(verbose_name="Sana va vaqt")
    location = models.CharField(max_length=300, blank=True, verbose_name="Joy")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Tadbir"
        verbose_name_plural = "Tadbirlar"

    def __str__(self):
        return self.title


class Project(models.Model):
    STAGE_CHOICES = (
        ('idea', "G'oya"),
        ('prototype', 'Prototip'),
        ('mvp', 'MVP'),
    )
    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects', verbose_name="Muallif")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="Rasm")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='idea', verbose_name="Bosqich")
    team_members = models.TextField(blank=True, verbose_name="Jamoa a'zolari")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Loyiha"
        verbose_name_plural = "Loyihalar"

    def __str__(self):
        return self.title


class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nomi")
    logo = models.ImageField(upload_to='partners/', blank=True, null=True, verbose_name="Logotip")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Hamkor"
        verbose_name_plural = "Hamkorlar"

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('approved', 'Tasdiqlangan'),
        ('rejected', 'Rad etilgan'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications', verbose_name="Foydalanuvchi")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='applications', verbose_name="Dastur")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    message = models.TextField(blank=True, verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Ariza"
        verbose_name_plural = "Arizalar"

    def __str__(self):
        return f"{self.user} - {self.program}"


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates', verbose_name="Foydalanuvchi")
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='certificates', verbose_name="Dastur")
    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    certificate_id = models.CharField(max_length=50, unique=True, verbose_name="Sertifikat ID")
    issued_date = models.DateField(verbose_name="Berilgan sana")
    pdf_file = models.FileField(upload_to='certificates/', blank=True, null=True, verbose_name="PDF fayl")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_date']
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"

    def __str__(self):
        return f"{self.title} - {self.user}"


class News(models.Model):
    title = models.CharField(max_length=300, verbose_name="Sarlavha")
    slug = models.SlugField(max_length=300, unique=True, verbose_name="Slug")
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Rasm")
    content = models.TextField(verbose_name="Kontent")
    is_published = models.BooleanField(default=False, verbose_name="Chop etilgan")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Chop etilgan sana")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def __str__(self):
        return self.title


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, default="Yoshlar innovatsiya markazi", verbose_name="Sayt nomi")
    site_logo = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name="Logotip")
    site_favicon = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name="Favicon")
    slogan = models.CharField(max_length=300, default="Kelajak texnologiyalari — yoshlar qo'lida", verbose_name="Slogan")
    about_text = models.TextField(blank=True, verbose_name="Markaz haqida matn")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Manzil")
    telegram_link = models.URLField(blank=True, verbose_name="Telegram havola")
    instagram_link = models.URLField(blank=True, verbose_name="Instagram havola")
    youtube_link = models.URLField(blank=True, verbose_name="YouTube havola")
    map_embed = models.TextField(blank=True, verbose_name="Xarita embed kodi")
    working_hours = models.CharField(max_length=200, blank=True, verbose_name="Ish vaqti")

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
