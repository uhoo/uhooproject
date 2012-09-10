from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from account.choices import GENDER_CHOICES
from locality.models import Point
from sorl.thumbnail import ImageField
from gallery.choices import POINTS_GROUP_ACTION

import re, datetime


from django.db.models import permalink
from dateutil import relativedelta
#from communication.models import Notification
#from gamification.models import Championship



"""
User Profile
"""
class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    gender = models.PositiveSmallIntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    address1 = models.CharField(_('address1'), blank=True, max_length=100)
    address2 = models.CharField(_('address2'), blank=True, max_length=100)
    city = models.CharField(_('city'), blank=True, max_length=100)
    state = models.CharField(_('state'), blank=True, max_length=100, help_text='or Province')
    zip = models.CharField(_('zip'), blank=True, max_length=10)
    country = models.CharField(_('country'), blank=True, max_length=100)
    mobile_provider = models.ForeignKey('MobileProvider', blank=True, null=True)
    accepted_communication = models.NullBooleanField()
    picture = ImageField(upload_to='upload/profile', null=True, blank=True)
    phone_number = models.CharField(_('Phone Number'), max_length = 20, null=True, blank=True)
    phone_area_code = models.CharField(_('Phone Area Code'), max_length = 4, null=True, blank=True)
    nickname = models.CharField(_('nickname'), blank=True, max_length=100)
    
    @property
    def picture_mobile(self):
        if not self.picture:
            return None
        else:
            from sorl.thumbnail import get_thumbnail
            return get_thumbnail(self.picture, '80x80').url    
    
#    @property
#    def notifications(self):
#        return Notification.objects.filter(user_to=self.user, active=True)
    
    def to_json(self):
        return  {
                    "first_name" : self.user.first_name,
                    "last_name" : self.user.last_name,
                    "email" : self.user.email,
                    "picture_mobile" : self.picture_mobile,
                    }
    
    def __unicode__(self):
        return self.user.get_full_name()
    
    class Meta:
        db_table = 'user_profile'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        


    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.birth_date:
            return u"%s" % relativedelta.relativedelta(TODAY, self.birth_date).years
        else:
            return None

    @permalink
    def get_absolute_url(self):
        return ('profile_detail', None, { 'username': self.user.username })

    @property
    def sms_address(self):
        if (self.mobile and self.mobile_provider):
            return u"%s@%s" % (re.sub('-', '', self.mobile), self.mobile_provider.domain)
        
        
            
    
#class Team(models.Model):
#    name = models.CharField(max_length=128)
    #members = models.ManyToManyField(User, related_name='team_members')
#    championships = models.ManyToManyField(Championship, related_name='team_championship')

    # reference objects
#    owner = models.ForeignKey(User, related_name='team_owner')
    
    # control fields
#    active = models.BooleanField(default=True)
#    created = models.DateTimeField(auto_now_add = True)
#    updated = models.DateTimeField(auto_now = True)
#    ip_created = models.IPAddressField(null=True, blank=True)    
#    ip_updated = models.IPAddressField(null=True, blank=True)
#    picture = models.ImageField(upload_to='upload/team', null=True, blank=True)
    
#    @property
#    def members(self):
#        return UserProfile.objects.filter(team__id=self.id)
    
#    @property
#    def championship(self):
#        return TeamChampionship.objects.get(team__id=self.id, active=True)
#        
#    def __unicode__(self):
#        return self.name
#    
#    class Meta:
#        db_table = 'team'    
#
#"""
#
#"""        
#class TeamChampionship(models.Model):
#    # refrence object
#    team = models.ForeignKey(Team)
#    championship = models.ForeignKey(Championship)
#    institution = models.ForeignKey(Institution)
#    
#    # specialized fields
#    started = models.DateTimeField(auto_now_add = True)    
#    finished = models.DateTimeField(null=True, blank=True)
#    active = models.BooleanField(default=True)
#    position = models.IntegerField(default=0)
#    points  = models.IntegerField(default=0)
#    
#
#    class Meta:
#        db_table = 'team_championship'       
#    
#    
         
class MobileProvider(models.Model):
    """MobileProvider model"""
    title = models.CharField(_('title'), max_length=25)
    domain = models.CharField(_('domain'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('mobile provider')
        verbose_name_plural = _('mobile providers')
        db_table = 'user_mobile_providers'

    def __unicode__(self):
        return u"%s" % self.title
        
          







#Gerenciador de pontuacao        
class action_points(models.Model):
    datapoint = models.DateTimeField(auto_now = True)
    action_exec = models.IntegerField(choices = POINTS_GROUP_ACTION)
    onwer = models.ForeignKey(User) 
    
    class Meta:
        db_table = 'action_points'  

"""
Create object user profile
"""
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)