from django.db import models
from django.utils import timezone
from pantry.models import Item

GENDER = (
    ('M', 'Male'),
    ('F', 'Female')
)

class Customer(models.Model):
    first_name = models.CharField(max_length=50,verbose_name="First Name")
    last_name = models.CharField(max_length=50,verbose_name="Last Name")
    gender = models.CharField(max_length=10,verbose_name="Gender", choices=GENDER)
    birth_date = models.DateField(verbose_name="Birth date")
    address = models.CharField(max_length=100,verbose_name="Mailing Address")
    city = models.CharField(max_length=50, verbose_name="City")
    zipcode = models.CharField(max_length=20, verbose_name="Zipcode")
    phone = models.CharField(max_length=10,verbose_name="Phone number")
    is_employed = models.BooleanField(verbose_name="Are you Employed?")
    employer = models.CharField(max_length=50,verbose_name="If currently employed then who is your current employer?", blank=True)
    family_size = models.IntegerField(verbose_name="How many members in the family including you?")
    items_needed = models.TextField(max_length=200,verbose_name="What items do you need today?")
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()
    def __str__(self):
        return 'Name: %s %s - ZIP-Code:%s' % (self.first_name, self.last_name, self.zipcode)

class Visit(models.Model):
    client = models.ForeignKey(Customer,
                                 related_name='client',
                                 on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)
    picked_up = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_date',)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return '{}'.format(self.id)

class VisitItems(models.Model):
    visit = models.ForeignKey(Visit,
                               related_name='items',
                               on_delete=models.CASCADE)
    item = models.ForeignKey(Item,
                               related_name='visit_items',
                               on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{}'.format(self.id)




