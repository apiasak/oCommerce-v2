from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = (
        ("IT", "IT & Gadget"),
        ("EL", "Electronics"),
        ("FA", "Fashion")
    )
    
    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=500)
    price = models.FloatField()
    photo = models.ImageField(upload_to='products')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name