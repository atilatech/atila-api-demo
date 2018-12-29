from rest_framework import serializers

from helpers.models import Country, Province, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = '__all__'
