from django.contrib.auth.models import User
from rest_framework import serializers

from helpers.serializers import CitySerializer, ProvinceSerializer, CountrySerializer
from scholarship.models import Scholarship
from userprofile.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'userprofile', 'username', 'email')
        read_only_fields = ('userprofile', 'username')


class UserProfileSerializer(serializers.ModelSerializer):
    # city = serializers.MultipleChoiceField(choices=CITY_CHOICES)
    # province = serializers.MultipleChoiceField(choices=PROVINCE_CHOICES)
    education_level = serializers.ListField(child=serializers.CharField(max_length=200, allow_blank=True))
    education_field = serializers.ListField(child=serializers.CharField(max_length=200, allow_blank=True))

    saved_scholarships = serializers.PrimaryKeyRelatedField(queryset=Scholarship.objects.all(), many=True,
                                                            allow_null=True)
    city = CitySerializer(many=True)
    province = ProvinceSerializer(many=True)
    country = CountrySerializer(many=True)
    street_address = serializers.CharField(required=False, max_length=300, allow_blank=True)
    postal_code = serializers.CharField(required=False, max_length=300, allow_blank=True)

    # def update(self, instance, validated_data):
    #     print('inside userProfileSerializer.update(): validated_date =', validated_data)
    #     city = validated_data.pop('city')
    #     province = validated_data.pop('province')
    #     country = validated_data.pop('country')
    #     user_id = validated_data.pop('user')
    #
    #     # For now, user's can only have 1 city todo change this to give users more freedom
    #     city = city[0]
    #     province = province[0]
    #     country = country[0]
    #
    #     country = Country.objects.get_or_create(name=country)
    #     province = Province.objects.get_or_create(name=province, country__name=country)
    #     city = City.objects.get_or_create(name=city, province__name=province, country__name=country)
    #
    #     instance.city.add(city)
    #     instance.province.add(province)
    #     instance.country.add(country)
    #
    #     instance.save()
    #
    #     return instance

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('user', 'username')

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class UserProfilePublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'first_name', 'last_name', 'username', 'profile_pic_url', 'title', 'profile_description',
                  'secondary_school', 'post_secondary_school', 'public_metadata')
