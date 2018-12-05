from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('pantry:item_list_by_category',
                           args=[self.slug])


class Item(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='items',
                                 on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('item_name',)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.item_name)