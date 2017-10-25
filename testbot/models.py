from django.db import models

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        return self.name


class Intent(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        return self.name


class Example(models.Model):
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    text = models.CharField(max_length=2048)

    def __str__(self):
        return self.text


class EntityTypes(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    payload = models.CharField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return self.name


class IntentEntities(models.Model):
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    entity = models.ForeignKey(EntityTypes, on_delete=models.CASCADE)
    payload = models.CharField(max_length=2048, blank=True, null=True)
