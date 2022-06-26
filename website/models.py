from django.db import models, transaction


class Banner(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='uploads/banner')


# Create your models here.
class Services(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    service_image = models.ImageField(upload_to='uploads/services')

    class Meta:
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name


class Contact(models.Model):
    phone = models.CharField(max_length=13)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=80)


class ContactUs(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=13)
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

    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} {}'.format(self.first_name, self.last_name)


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
