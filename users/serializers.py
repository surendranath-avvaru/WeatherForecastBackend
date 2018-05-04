from rest_framework import serializers
from django.core.mail import send_mail
from django.contrib.auth.models import User

from users.utils import generate_password
from users.settings import (
							FIELD_REQUIRED,
							EMAIL_EXISTS_ERROR,
							NOT_REGISTERED_MAIL,
							PASSWORD_NOT_MATCHED_ERROR,
							RESET_PASSWORD_SUBJECT,
							RESET_PASSWORD_BODY,
							DEFAULT_FROM_EMAIL
							)


class UserListSerializer(serializers.ModelSerializer):
	is_superuser = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ['id', 'first_name', 'last_name', 'username', 'email', 'is_superuser']

	def get_is_superuser(self, obj):
		return obj.is_superuser

class UserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField()
	password = serializers.CharField(min_length=8, write_only=True, required=False)
	confirm_password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

	def create(self, validated_data):
		validated_data.pop('confirm_password')
		return User.objects.create_user(**validated_data)

	def validate(self, data):
		if data.get('password') != data.get('confirm_password'):
			raise serializers.ValidationError(PASSWORD_NOT_MATCHED_ERROR)
		return data

	def validate_email(self, email):
		if self.instance != None:
			if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
				raise serializers.ValidationError(EMAIL_EXISTS_ERROR)
		else:
			if User.objects.filter(email=email).exists():
				raise serializers.ValidationError(EMAIL_EXISTS_ERROR)
		return email


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=8, required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def is_valid(self):
        self._errors = {}
        if self.initial_data.get('email',False):
            if not User.objects.filter(email=self.initial_data.get('email')).exists():
                self._errors = {"email": [ NOT_REGISTERED_MAIL ]}
                return
            return True
        self._errors = {"email": [ FIELD_REQUIRED ]}
        return

    def save(self):
        email = self.initial_data.get('email')
        user = User.objects.get(email=email)
        new_password = generate_password()
        user.set_password(new_password)
        send_mail(RESET_PASSWORD_SUBJECT, RESET_PASSWORD_BODY + new_password, DEFAULT_FROM_EMAIL, [email], fail_silently=True)
        user.save()