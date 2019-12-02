from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='towns')

    def __str__(self):
        return self.name


class Address(models.Model):
    address = models.CharField(max_length=100)
    hint = models.TextField(max_length=200, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='addresses')

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.address
