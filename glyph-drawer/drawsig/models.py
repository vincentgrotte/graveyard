from django.db import models

class Sigil(models.Model):
    intent = models.CharField(max_length=250, default="")
    shape = models.CharField(max_length=4, default="")

    def __str__(self):
    	return self.intent