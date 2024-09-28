from django.db import models

class ScrapedData(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
