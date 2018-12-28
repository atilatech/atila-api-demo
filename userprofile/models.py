from django.db import models

# Create your models here.

class UserProfile(models.Model):
    """ Profiles created by SMB and sponsors."""

    objects = UserProfileManager()

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=128, unique=True, default='DEFAULTUSER')
    email = models.EmailField(max_length=128, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=128, blank=True, null=True)
    firebase_token = models.TextField(blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True, null=True)
    is_atila_admin = models.BooleanField(default=False)
    is_debug_mode = models.BooleanField(default=False)

    atila_points = models.DecimalField(max_digits=19, decimal_places=4, default=Decimal('0'))

    # https://stackoverflow.com/questions/31412377/non-primary-foreign-keys-in-django
    # https://stackoverflow.com/questions/30100553/multiple-foreign-keys-to-the-same-id-django-design-patterns
    referred_by = models.ForeignKey('UserProfile', to_field="username", db_column="userprofile_username", default=None,
                                    null=True, blank=True)

    saved_scholarships = models.ManyToManyField('Scholarship', blank=True)
    saved_scholarships_metadata = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)

    scholarships_not_interested = models.ManyToManyField('Scholarship',
                                                         blank=True, related_name='user_scholarships_not_interested')

    scholarships_match_score = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    birth_date = models.DateField(blank=True, null=True)

    gender = models.CharField(blank=True, null=True, max_length=1000, choices=GENDERS, default='')

    profile_pic_url = models.URLField(blank=True,
                                      default=HelperMethods.default_profile_pic_url, max_length=700)
    title = models.CharField(max_length=128, blank=True)
    profile_description = models.CharField(max_length=140, blank=True)

    is_sponsor = models.BooleanField(default=False)
    is_international_student = models.BooleanField(default=False)

    phone_number = models.BigIntegerField(blank=True, null=True)
    street_address = models.CharField(max_length=500, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)

    city = models.ManyToManyField(City, blank=True)
    province = models.ManyToManyField(Province, blank=True)
    country = models.ManyToManyField(Country, blank=True)

    country_extra = models.ManyToManyField(Country, blank=True, related_name='country_extra')

    secondary_school = models.CharField(max_length=200, blank=True, )
    post_secondary_school = models.CharField(max_length=200, blank=True, )
    academic_average = models.BigIntegerField(blank=True, null=True)
    major = models.CharField(max_length=200, blank=True, )
    degree = models.CharField(max_length=200, blank=True, )

    financial_need = models.BooleanField(default=False)

    ethnicity = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('ETHNICITY')),
                           default=list, blank=True, null=True)
    heritage = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('COUNTRIES')),
                          default=list, blank=True, null=True)
    citizenship = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('COUNTRIES')),
                             default=list, blank=True, null=True)
    religion = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('RELIGION')),
                          default=list, blank=True, null=True)
    activities = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('ACTIVITIES')),
                            default=list, blank=True, null=True)
    sports = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('SPORTS')),
                        default=list, blank=True, null=True)
    disability = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('DISABILITY')),
                            default=list, blank=True, null=True)

    language = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=get_tuple('LANGUAGE')),
                          default=list, blank=True, null=True)

    eligible_schools = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                                  default=list, blank=True, null=True)

    eligible_programs = ArrayField(models.CharField(blank=True, null=True, max_length=1000),
                                   default=list, blank=True, null=True)

    education_field = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=EDUCATION_FIELDS),
                                 default=list, blank=True, null=True)
    education_level = ArrayField(models.CharField(blank=True, null=True, max_length=1000, choices=EDUCATION_LEVELS),
                                 default=list, blank=True, null=True)
    grade_level = models.CharField(blank=True, null=True, max_length=1000)
    # todo ability to add multiple, resume, transcripts and reference letters
    resume = models.URLField(blank=True, null=True, max_length=1000)
    transcript = models.URLField(blank=True, null=True, max_length=1000)
    reference_letter = models.URLField(blank=True, null=True, max_length=1000)
    reference_letter_alternate = models.URLField(blank=True, null=True, max_length=1000)
    enrollment_proof = models.URLField(blank=True, null=True, max_length=1000)
    cover_letter = models.URLField(blank=True, null=True, max_length=1000)

    extracurricular_description = models.TextField(blank=True)
    academic_career_goals = models.TextField(blank=True)

    date_created = models.DateField(auto_now_add=True)
    date_time_created = models.DateTimeField(default=timezone.now)
    website_url = models.URLField(blank=True, null=True, max_length=500)
    linkedin_url = models.URLField(blank=True, null=True, max_length=500)

    extra_information = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    preferences = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    metadata = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)
    public_metadata = JSONField(default=HelperMethods.empty_dict, blank=True, null=True)

    email_digest_sent_date = models.DateTimeField(default=datetime(2018, 1, 1, tzinfo=pytz.UTC))
    email_digest_status = models.CharField(null=True, blank=True, max_length=500)

    # 'tomiwa' means, referred by tomiwa, don't send Digest as often

    class Meta:
        ordering = ['last_name', 'first_name']
        # unique_together = ('username',)

    def natural_key(self):
        return (self.username,)

    def __str__(self):
        obj_as_str = self.last_name + ", " + self.first_name
        return obj_as_str

    def get_full_name(self):
        full_name = self.last_name + ", " + self.first_name
        return full_name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = self.user.username
            self.email = self.user.email

        if self.user.email != self.email:
            logger.warning(
                'Warning emails Not Matching! userProfile email: %s, user email:%s' % (self.email, self.user.email))
            print('Warning emails Not Matching! userProfile email: %s, user email:%s' % (self.email, self.user.email))
            self.user.email = self.email
            self.user.save()

        super(UserProfile, self).save(*args, **kwargs)

    def guess_city(self) -> City:
        city = None
        if self.metadata.get('registration_location'):
            city = self.metadata['registration_location'].get('city', '')
            city = City.objects.filter(name__icontains=city).first()
        return city

    def guess_province(self) -> Province:
        province = None
        if self.metadata.get('registration_location'):
            province = self.metadata['registration_location'].get('region', '')
            province = Province.objects.filter(name__icontains=province).first()
        return province