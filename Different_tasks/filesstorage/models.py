from django.db import models


class MyFiles(models.Model):
    myfile = models.FileField("Файл")
