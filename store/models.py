from django.db import models
from django.utils import timezone
# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length = 20, blank=True, null=True)
    email = models.EmailField(max_length = 100, unique = True, blank = True, null = True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'category'
    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length = 100)
    percent_off = models.DecimalField(max_digits = 5, decimal_places = 2)
    start_date = models.DateField()
    end_date = models.DateField()


    class Meta:
        constraints = [
            models.CheckConstraint(
                check = models.Q(percent_off__gte = 0) & models.Q(percent_off__lte = 100), name = "discount_percent_off_range"
            ),
            models.CheckConstraint(
                check = models.Q(end_date__gte = models.F("start_date")), name = "discount_end_after_Start"
            )
        ]
    def __str__(self):
        return self.name