from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phoneno = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.ImageField(
        upload_to="uploads/avatar", blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)

    @staticmethod
    def get_user_by_id(username):
        try:
            print(username)
            return User.objects.get(username=username)

        except:
            return False

    def isuserExist(self):
        if User.objects.filter(username=self.username):
            return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    service_image = models.ImageField(upload_to='uploads/services')

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project_image = models.ImageField(upload_to='uploads/projects')

    def __str__(self):
        return self.name


class Contact(models.Model):
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    status = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/team')

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    class Meta:
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.email


class Blog(models.Model):
    blog_title = models.CharField(max_length=50)
    blog_description = models.TextField()
    blog_image = models.ImageField(upload_to='uploads/blogs')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.blog_title


class Comment(MPTTModel):
    content = models.TextField()
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name="children", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return 'Comment by {}'.format(self.user.username)


class About(models.Model):
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    company_image = models.ImageField(upload_to='uploads/about')
    company_logo = models.ImageField(upload_to='uploads/about')
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.is_active:
            return super().save(*args, **kwargs)
        with transaction.atomic():
            About.objects.filter(is_active=True).update(is_active=False)
            return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "About"


def user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(user_created_signal, sender=User)


class Banner(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/banner')
    is_active = models.BooleanField(default=False)


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/testomonial')
    saying = models.TextField()

    def __str__(self):
        return 'Testimonial by {}'.format(self.customer_name)
