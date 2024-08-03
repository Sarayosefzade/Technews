from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    source = models.URLField()
    tags = models.ManyToManyField(Tag, related_name='news')

    def __str__(self):
        return f"{self.title} - {self.description} - {', '.join(tag.name for tag in self.tags.all())} - {self.source}"
