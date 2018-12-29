# https://stackoverflow.com/questions/41394761/the-create-method-does-not-support-writable-nested-fields-by-default
# https://stackoverflow.com/questions/30013284/django-rest-framework-writable-nested-field-using-create
# https://www.google.com/search?q=write+a+create+method+for+nestable+fields&oq=write+a+create+method+for+nestable+fields&aqs=chrome..69i57.6732j0j4&sourceid=chrome&ie=UTF-8
from rest_framework import serializers
from rest_framework.utils import model_meta

from helpers.constants import FUNDING_TYPES
from helpers.serializers import CitySerializer, ProvinceSerializer, CountrySerializer
from scholarship.models import Scholarship


class ScholarshipSerializer(serializers.ModelSerializer):
    # city = serializers.MultipleChoiceField(choices=CITY_CHOICES)
    # province = serializers.MultipleChoiceField(choices=PROVINCE_CHOICES)
    education_level = serializers.ListField(child=serializers.CharField(max_length=200, allow_blank=True))
    education_field = serializers.ListField(child=serializers.CharField(max_length=200, allow_blank=True))

    funding_type = serializers.MultipleChoiceField(choices=FUNDING_TYPES, required=False)
    extra_questions = serializers.JSONField(required=False)
    # applicants = serializers.PrimaryKeyRelatedField(many=True, read_only=True, allow_null=True, required=False)
    city = CitySerializer(many=True, required=False)
    province = ProvinceSerializer(many=True, required=False)
    country = CountrySerializer(many=True, required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    class Meta:
        model = Scholarship
        # fields = '__all__'
        exclude = ('applicants', 'metadata_private')

    def create(self, validated_data):
        city = validated_data.pop('city', None)
        province = validated_data.pop('province', None)
        country = validated_data.pop('country', None)
        instance = Scholarship.objects.create(**validated_data)

        instance.city = city if city else []
        instance.province = province if city else []
        instance.country = country if city else []

        instance.save()
        return instance
        # return super(ScholarshipSerializer, self).create(validated_data)

    def update(self, instance, validated_data):

        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                # todo check if this is right way to set attributes
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # super(ScholarshipSerializer, self).update(instance, validated_data)

        return instance
