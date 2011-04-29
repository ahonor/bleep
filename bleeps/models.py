from django.db import models
from django.forms import ModelForm
from django import forms
import datetime
from django.contrib.auth.models import User

class Bleep(models.Model):
    bleep_message = models.TextField()
    bleep_client = models.CharField('client name',max_length=200, blank=True, null=True)
    bleep_service = models.CharField(max_length=200)
    bleep_pub_date = models.DateTimeField('date published', blank=True, null=True)
    bleep_get_data = models.TextField('GET data',blank=True, null=True)
    bleep_post_data = models.TextField('POST data',blank=True,null=True)

    CONTENTTYPE_CHOICES = (
        ('application/xml', 'xml'),
        ('application/json','json'),
        ('text/html','html'),
        ('text/plain','txt'),
        ('text/csv','csv'),
        ('text/yaml','yaml'),
        )
    bleep_content_type = models.CharField('POST data content-type',
                                                   max_length=100,
                                                   blank=True, null=True)
    
    STATUS_CHOICES = (
        ('rcvd','Received'),
        ('qued','Queued'),
        ('dspd','Dispatched'),
        ('comp','Completed'),
        ('fail','Failed'),
        )
    bleep_status = models.CharField('Bleep status',
                                    max_length=4, 
                                    choices=STATUS_CHOICES, 
                                    blank=True, null=True)

    def was_published_today(self):
        return self.bleep_pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'

    def is_sendable(self):
        return self.bleep_status == 'qued'

    def add_comment(self, msg, cat="", stat=""):
        """
        Add a comment to the bleep
        """
        return Comment.objects.create(timestamp=datetime.datetime.now(),
                                  category=cat, message=msg, status=stat, 
                                  bleep=self)

    def as_dict(self, prefix=""):
        """
        return dictionary containing the bleep instance data.
        todo: use a dynamic way to dump this !
        """
        bleep_dict = {}
        bleep_dict[prefix+'bleep_message']=self.bleep_message
        bleep_dict[prefix+'bleep_content_type']=self.bleep_content_type
        bleep_dict[prefix+'bleep_service']=self.bleep_service
        bleep_dict[prefix+'bleep_client']=self.bleep_client
        bleep_dict[prefix+'bleep_status']=self.bleep_status
        bleep_dict[prefix+'bleep_pub_date']=str(self.bleep_pub_date)
        bleep_dict[prefix+'bleep_url']=self.get_absolute_url()
        return bleep_dict

    def last_log(self):
        return self.log_set.latest( "timestamp" )

    def get_absolute_url(self):
        return "/bleeps/%i/" % self.id

class Comment(models.Model):
    bleep = models.ForeignKey(Bleep, editable=False)
    timestamp = models.DateTimeField('timestamp', blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    message = models.CharField(max_length=200)
    user = models.ForeignKey(User, null=True, blank=True, editable=False)

    def __str__(self):
        return "%s" % self.message

class BleepForm(ModelForm):
    class Meta:
        model = Bleep

class BleepSearchForm(forms.Form):
    """
    Search form
    """
    keyword = forms.CharField(max_length=100)


class CommentForm(ModelForm):
    class Meta:
        model = Comment


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, editable=True, )
    url = models.URLField("Website", blank=True, verify_exists=False)
    organization = models.CharField(max_length=50, blank=True)
    daily_digest_subscription = models.BooleanField()

    def __str__(self):
        return "%s" % self.user.username

    def add_auth_token(self, description):
        """
        Add an API key to the user profile
        """
        return UserAuthToken.objects.create(timestamp=datetime.datetime.now(),
                                         description=description,
                                         token=UserAuthToken.generate_token(),
                                         user_profile=self)
    def has_auth_token(self, key):
        """
        Check if this profile contains specified auth token
        """
        for token in self.userauthtoken_set.all():
            if key == token.token:
                return True
        return False
    
# Have the profile created automatically when referenced
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile

import random
import hashlib
import base64
class UserAuthToken(models.Model):
    user_profile = models.ForeignKey(UserProfile, unique=False, editable=True)    
    timestamp = models.DateTimeField('timestamp', blank=True, null=True)
    description = models.CharField(max_length=200)
    token = models.CharField(max_length=50, editable=True,  blank=True, null=True)

    def __str__(self):
        return "%s" % self.description
 
    @classmethod
    def generate_token(cls):
        """
        Generate a simple API key, a 38 character alphanumeric string
        """
        # 256bit number generated by the Mersenne Twister Pseudo Random Number Generator (PRNG)
        key = str(random.getrandbits(256))
        # Hash it with SHA-256
        hashed_key = hashlib.sha224(key).digest()
        # Base64 encode and substitute (salt) the non alpha chars
        encoded_key = base64.b64encode(
            hashed_key,
            random.choice(['rA','aZ','gQ','hH','hG','aR','DD'])).rstrip('==')
        return encoded_key

class UserAuthTokenForm(ModelForm):
    class Meta:
        model = UserAuthToken
