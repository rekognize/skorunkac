from django.db import models


class City(models.Model):
    name = models.CharField('ad', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'il'
        verbose_name_plural = 'iller'


class District(models.Model):
    city = models.ForeignKey(City, verbose_name='il', on_delete=models.CASCADE)
    name = models.CharField('ad', max_length=50)

    def __str__(self):
        return f"{self.name} / {self.city.name}"

    class Meta:
        verbose_name = 'il / ilçe'
        verbose_name_plural = 'il / ilçe'
