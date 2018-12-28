import re

from django.db import models


# Steps to follow when adding a new model
# 1. Migrate your changes: python manage.py makemigrations && python manage.py migrate && python manage.py runserver
# 2. Register the new view, serializer and URL
# 3. Register the model to admin.
# helper methods
class HelperMethods:
    @staticmethod
    def any_default():
        return ["Any"]

    @staticmethod
    def empty_list():
        return []

    @staticmethod
    def any_default_dict():
        return {"Any": "Any"}

    @staticmethod
    def empty_dict():
        return {}

    default_profile_pic_url = "https://firebasestorage.googleapis.com/v0/b/atila-7.appspot.com/o/user-profiles%2Fgeneral-data%2Fdefault-profile-pic.png?alt=media&token=455c59f7-3a05-43f1-a79e-89abff1eae57"

    @staticmethod
    def title_case(s):
        print('BEFORE title_except():', s)
        articles = ['a', 'an', 'of', 'the', 'is']
        word_list = re.split(' ', s)  # re.split behaves as expected
        final = [word_list[0].capitalize()]
        for word in word_list[1:]:
            final.append(word if word in articles else word.capitalize())

        print('AFTER title_except():', " ".join(final))
        return " ".join(final)


class Country(models.Model):
    name = models.CharField(max_length=128, primary_key=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        obj_as_str = self.name
        return obj_as_str

    def save(self, *args, **kwargs):
        self.name = HelperMethods.title_case(self.name)

        super(Country, self).save(*args, **kwargs)


class ProvinceManager(models.Manager):
    def get_by_natural_key(self, name, country):
        return self.get(name=name, country=country)


class Province(models.Model):
    objects = ProvinceManager()

    name = models.CharField(max_length=128, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def natural_key(self):
        return (self.name, self.country.name,)

    natural_key.dependencies = ['dante.country']

    class Meta:
        unique_together = (('name', 'country'),)

    def __str__(self):
        # different front end stuff require the province to just be a single name, so we can't include country in string,
        # obj_as_str = self.name + ", " + str(self.country)
        obj_as_str = self.name
        return obj_as_str

    def save(self, *args, **kwargs):
        self.name = HelperMethods.title_case(self.name)

        super(Province, self).save(*args, **kwargs)


class CityManager(models.Manager):
    def get_by_natural_key(self, name, province, country):
        return self.get(name=name, province__name=province, country=country)


class City(models.Model):
    objects = CityManager()

    name = models.CharField(max_length=128, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def natural_key(self):
        return (self.name, self.province.name, self.country.name,)

    natural_key.dependencies = ['dante.province', 'dante.country']

    class Meta:
        verbose_name_plural = "Cities"
        unique_together = (('name', 'province', 'country'),)

    def __str__(self):
        # different front end stuff require the city to just be a single name,
        #  so we can't include country/province in string,

        # obj_as_str = self.name + ", " + str(self.province)
        # method below is confusing if trying to debug same city and province with diff spelling
        # or same city name but diff provinces
        # obj_as_str = self.name + self.province
        return self.name

    def save(self, *args, **kwargs):
        self.name = HelperMethods.title_case(self.name)

        super(City, self).save(*args, **kwargs)
