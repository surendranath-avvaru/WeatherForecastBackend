from rest_framework import serializers
from django.contrib.auth.models import User

from users.settings import (
							EMAIL_EXISTS_ERROR,
							PASSWORD_NOT_MATCHED_ERROR
							)


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


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