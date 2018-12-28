import time
from datetime import date, datetime
from decimal import Decimal

import pytz
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from multiselectfield import MultiSelectField

from helpers.constants import get_tuple, FILTER_TYPES, FUNDING_TYPES
# Create your models here.
from helpers.models import HelperMethods, City, Province, Country
from userprofile.models import UserProfile

DEFAULT_SCHOLARSHIP_IMAGE = "https://ucarecdn.com/f9a8fb7d-e7c2-43bc-8177-47638c801fb3/"


class Scholarship(models.Model):
    owner = models.ForeignKey(UserProfile, null=True, blank=True,
                              related_name='scholarship_owner',
                              on_delete=models.SET_NULL, )  # one-to-many, each scholarship is owned by one UserProfile

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200, default='NO-SLUG')
    description = models.TextField(max_length=10000)
    criteria_info = models.TextField(blank=True)
    date_created = models.DateField(default=date.today)  # todo should we change the default deadline?
    date_time_created = models.DateTimeField(default=timezone.now)

    # https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
    # RuntimeWarning: DateTimeField Scholarship.deadline received a naive datetime (2019-01-01 00:00:00) while time zone support is active.
    deadline = models.DateTimeField(
        default=datetime(2019, 1, 1, tzinfo=pytz.UTC))  # Default deadline is January 1, 2019

    open_date = models.DateField(null=True, blank=True)

    base_match_score = models.FloatField(default=0)

    form_url = models.URLField(blank=True, max_length=2000)
    local_form_location = models.URLField(blank=True, max_length=2000)

    # scholarship_img_url = models.URLField(default="http://www.brockpress.com/wp-content/uploads/2015/08/GIRL_studying.jpg",
    #                                 max_length=300)

    img_url = models.URLField(
        default="https://ucarecdn.com/f9a8fb7d-e7c2-43bc-8177-47638c801fb3/")

    scholarship_url = models.URLField(blank=True, max_length=500)

    funding_amount = models.DecimalField(max_digits=19, decimal_places=2, default=Decimal('0.00'))
    # better than float field because of exactness, and more human intuitive arithmetic

    funding_type = MultiSelectField(choices=get_tuple('FUNDING_TYPES'), default=FUNDING_TYPES[0][0], blank=True,
                                    null=True)

    city = models.ManyToManyField(City, blank=True)
    # The following 2 fields may be redundant once we already have city,
    province = models.ManyToManyField(Province, blank=True)
    country = models.ManyToManyField(Country, blank=True)

    keywords = models.TextField(blank=True)

    ethnicity = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                           default=list, blank=True, null=True, choices=get_tuple('ETHNICITY'))
    heritage = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                          default=list, blank=True, null=True, choices=get_tuple('COUNTRIES'))
    citizenship = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                             default=list, blank=True, null=True, choices=get_tuple('COUNTRIES'))
    religion = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                          default=list, blank=True, null=True, choices=get_tuple('RELIGION'))
    activities = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                            default=list, blank=True, null=True, choices=get_tuple('ACTIVITIES'))
    sports = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                        default=list, blank=True, null=True, choices=get_tuple('SPORTS'))
    disability = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                            default=list, blank=True, null=True, choices=get_tuple('DISABILITY'))

    language = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('LANGUAGE')),
                          default=list, blank=True, null=True)

    eligible_schools = ArrayField(models.CharField(blank=True, null=True, max_length=1000), default=list,
                                  blank=True, null=True)
    eligible_programs = ArrayField(models.CharField(blank=True, null=True, max_length=1000), default=list,
                                   blank=True, null=True)
    education_field = ArrayField(
        models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('EDUCATION_FIELDS')),
        default=list, blank=True, null=True)
    education_level = ArrayField(
        models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('EDUCATION_LEVELS')),
        default=list, blank=True, null=True)

    academic_average = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    submission_info = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    extra_questions = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    extra_criteria = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)

    is_automated = models.BooleanField(
        default=False)  # todo Should we make an integer field, for different automation levels
    bot_created = models.BooleanField(default=False)
    renewable_years = models.IntegerField(default=0)
    financial_need = models.BooleanField(default=False)
    no_essay_required = models.BooleanField(default=False)
    female_only = models.BooleanField(default=False)
    international_students_eligible = models.BooleanField(default=False)
    number_available_scholarships = models.IntegerField(default=1)

    resume_required = models.BooleanField(default=False)
    cover_letter_required = models.BooleanField(default=False)
    transcript_required = models.BooleanField(default=False)
    reference_letter_required = models.IntegerField(default=0)
    enrollment_proof_required = models.BooleanField(default=False)
    document_details = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)

    applicants = models.ManyToManyField(UserProfile, through='Application', related_name='scholarship_applicants')
    metadata = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    metadata_private = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)

    class Meta:
        ordering = ['-date_created', 'name']
        # unique_together = ('slug',)

    # temporarily disable natural key when dumping scholarship and userprofile in same command due to
    # RuntimeError: Can't resolve dependencies for dante.Scholarship, dante.UserProfile in serialized app list.
    # def natural_key(self):
    #     return (self.slug,)
    #
    # natural_key.dependencies = ('dante.userprofile',)

    def __str__(self):
        return '#%s: %s ' % (self.pk, self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

            # If a scholarship with that URL already exists, then append timestamp to the end
            if Scholarship.objects.filter(slug=self.slug).exists():
                time_int = int(time.time() * 100)
                time_str = str(time_int)[4:]
                time_int = int(time_str)
                self.slug = '%s-%d' % (self.slug, time_int)

            if self.img_url == DEFAULT_SCHOLARSHIP_IMAGE:
                self.img_url = self.img_url + self.slug + '.jpg'

        if not self.scholarship_url:
            self.scholarship_url = 'https://atila.ca/scholarship/' + self.slug + '/'

        self.save_keywords(skip_save=True)

        super(Scholarship, self).save(*args, **kwargs)

    def save_keywords(self, *args, **kwargs):
        self.keywords = ""
        keyword_sources = FILTER_TYPES
        location_types = ['city', 'province', 'country']

        for keyword_source in keyword_sources:

            if keyword_source not in location_types and hasattr(self, keyword_source):
                keyword = getattr(self, keyword_source)
                if len(keyword) > 0:
                    self.keywords = self.keywords + " " + " ".join(keyword)

        if self.female_only:
            self.keywords += " female"

        if self.international_students_eligible:
            self.keywords += " international student"

        locations = []

        if self.id:  # need id before you can use related fields
            for location_type in location_types:
                location = getattr(self, location_type)
                location = location.all()
                location = [location_str.name for location_str in location]
                locations.extend(location)

            location_keywords = " ".join(locations)
            self.keywords = self.keywords + " " + location_keywords
        self.keywords = self.keywords.strip()

        if not kwargs.get('skip_save', False):
            self.save()

        return self.keywords


# https://docs.djangoproject.com/en/1.11/topics/db/models/#intermediary-manytomany
class Application(models.Model):
    """ Intermediary model (association table) linking applicants (UserProfile) and scholarships."""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)

    # todo how should we handle on_delete, will be models.CASCADE by default
    # https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models
    # https://stackoverflow.com/a/8543956

    app_url = models.URLField(blank=True, max_length=500)
    date_created = models.DateTimeField(default=timezone.now)

    responses = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    userprofile_responses = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    document_urls = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        obj_as_str = "Applicant: " + str(self.user) \
                     + " | Scholarship: " + str(self.scholarship)
        return obj_as_str

    class Meta:
        ordering = ['scholarship', '-date_created']

    metadata = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
