from django.db import models
from django.conf import settings
import uuid
from . import django_utility
# Create your models here.


class Query(models.Model):
    query_text = models.CharField(max_length=500)
    query_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.query_text)

    class Meta:
        verbose_name_plural = "Queries"

class Photo(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    tags = models.CharField(max_length=200)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 null=True)
    draft = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='images/',validators=[django_utility.validate_image_file])