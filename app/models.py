from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="user_image/")
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.first_name


class Blog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_blogs")
    title = models.CharField(max_length=100, null=False, blank=True)
    description = RichTextField()
    image = models.ImageField(upload_to="blog_image/")
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title} created by {self.user}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_images")
    image = models.ImageField(upload_to="blog_images/")
    is_main = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.image.url}"

    class Meta:
        verbose_name = "BlogImage"
        verbose_name_plural = "BlogImages"

class BlogComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_blog_comments")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_comments")
    comment = models.CharField(max_length=150, null=False, blank=False)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.comment}"


    class Meta:
        ordering = ["created_at"]
        verbose_name = "BlogComment"
        verbose_name_plural = "BlogComments"


