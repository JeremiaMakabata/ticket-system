from rest_framework import serializers
from .models import (
    Notification,
    UserProfile, Ticket, User, UserGroup,
    TICKET_CATEGORY_CHOICES, STATUS_CHOICES)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("company", "address", "country", "city", "postal_code", "user_type",
                  "first_name", "last_name", "tickets")


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user_profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'password', 'user_profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('user_profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('user_profile')
        user_profile = instance.user_profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()
        user_profile.first_name = profile_data.get('first_name', user_profile.first_name)
        user_profile.last_name = user_profile.get('last_name', user_profile.last_name)
        user_profile.company = profile_data.get('company',  user_profile.company)
        user_profile.address = profile_data.get('address', user_profile.address)
        user_profile.country = profile_data.get('country', user_profile.country)
        user_profile.city = profile_data.get('city', user_profile.city)
        user_profile.postal_code = profile_data.get('zip', user_profile.zip)
        user_profile.tickets = profile_data.get('tickets', user_profile.tickets)
        user_profile.save()

        return instance

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ("ticket", "receive_notifications")



class TicketSerializer(serializers.HyperlinkedModelSerializer):
    ticket_notification = NotificationSerializer(required=True)


    class Meta:
        model = Ticket
        fields = ("subject", "description", "status", "category",
                  "slug", "ticket_notification")
        extra_kwargs = {"ticket_assignee": {"read_only": True}}

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ticket_notification = validated_data.get('ticket_notification', instance.ticket_notification)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance














