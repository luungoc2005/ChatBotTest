from django.db import models

# Create your models here.

class Intent(models.Model):
  name = models.CharField(max_length=128, blank=False, null=False)

  def __str__(self):
    return self.name

class Example(models.Model):
  intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
  text = models.CharField(max_length=500)

  def __str__(self):
    return self.text
