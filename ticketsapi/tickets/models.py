from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
import uuid

STATUS_CHOICES = (
    ('IN_PROGRESS', 'in progress'), ('COMPLETED', 'resolved',),
    ('NEW', 'newly logged',),
)
TICKET_CATEGORY_CHOICES = (('IT', 'IT'), ('SALES', 'SALES'), ('ACCOUNTS', 'ACCOUNTS'))
PERMISSION_CHOICES = (('OWNER', 'owner'),
                          ('MAINTAINER', 'maintainer'), ('VIEWER', 'viewer'))
PERMISSIONS_LEVELS = {'viewer': 0, 'maintainer': 1, 'owner': 2}

class User(AbstractUser):
    """Create a custom user model which uses email as username"""
    username = models.CharField(max_length=55, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        """Field to be returned when this class is called"""
        return "{}".format(self.email)


class UserGroup(models.Model):
    """User group model to store the groups."""

    name = models.TextField(max_length=50, null=False, blank=False, default='')
    description = models.TextField(max_length=80, null=False, blank=False, default='')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_group')
    add_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class UserProfile(models.Model):
    """Standard Profile Model, stores information not used in authentication."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='user_profile', blank=True)
    company = models.CharField(max_length=255, null=True)
    logged_in = models.NullBooleanField(default=False)
    accepted_conditions = models.NullBooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=5)
    user_type = models.TextField(null=True)
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)
    tickets = models.TextField(null=True)


def generate_ticket_id():
    return str(uuid.uuid4()).split("-")[-1]


class Ticket(models.Model):
    """Model to store details of a ticket."""

    subject = models.TextField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    ticket_assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                        related_name='owner', null=True)
    ticket_id = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=20, choices=TICKET_CATEGORY_CHOICES, default='IT')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='IN_PROGRESS', null=True)
    date_logged = models.DateTimeField(auto_now=True, null=False)
    date_updated = models.DateTimeField(auto_now=True, null=False)
    slug = models.SlugField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        if len(self.ticket_id.strip(" ")) == 0:
            self.ticket_id = generate_ticket_id()

        super(Ticket, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-date_logged", "status"]


class Notification(models.Model):
    """Model to store the notification information."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_notification',
                             blank=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,
                                related_name='ticket_notification',
                                blank=False)
    receive_notifications = models.BooleanField(default=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    added_at = models.DateTimeField(auto_now_add=True)
