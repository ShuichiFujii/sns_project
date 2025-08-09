from django.db import models

class Tag(models.Model):
    name = models.TextField(max_length=99, unique=True)
    
    def __str__(self):
        return self.name
        