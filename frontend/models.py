from django.db import models

# Create your models here.


class Query(models.Model):
    query_text = models.CharField(max_length=500)
    query_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.query_text)

    class Meta:
        verbose_name_plural = "Queries"
