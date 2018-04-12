from django.http import Http404
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import permission_classes
from rest_framework import generics

from root.response import GenericResponse, CustomResponse
from users.serializers import UserListSerializer, UserSerializer


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserListSerializer


class UserSignupView(generics.CreateAPIView):

	def post(self, request):
		serializer = UserSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return GenericResponse(serializer.data, status=status.HTTP_201_CREATED)
		return GenericResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(instance=user)
        return GenericResponse(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return GenericResponse(serializer.data, status=status.HTTP_200_OK)
        return GenericResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return GenericResponse(status=status.HTTP_200_OK)