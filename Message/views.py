from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework import mixins, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from Message.serializers import SignupSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from .models import MessageModel
from .serializers import UserSerializer, MessageSerializer
from django.db.models import Q
import datetime







class SignupViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
	permission_classes = [AllowAny]
	queryset = User.objects.all()
	serializer_class = SignupSerializer



class LoginView(APIView):
	permission_classes = [AllowAny]

	def post(self,request):
		serializer = LoginSerializer(data=request.data)
		if serializer.is_valid():
			try:
				user = User.objects.get(username=serializer.data['username'])
			except BaseException as e:
				raise ValidationError({"message":"user does not exist."})
			if user:
				if user.check_password(serializer.data['password']):
					token = Token.objects.get(user=user)
					return Response({'token':str(token)})
				return Response({"message":"incorrect password."})
			return Response({"message":"User does not exist."})
		return Response({'message':serializer.errors})



class MessageView(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request):
		serializer = MessageSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			user_data = User.objects.get(id=serializer.data['user'])
			messages = MessageModel.objects.filter(Q(user=serializer.data['user']) & Q(created_at__hour=datetime.datetime.now().hour))
			if len(messages) < 10:
				res = {
					'msg' :serializer.data,
					'created_by'  : {
						'id': user_data.id,
						'username': user_data.username,
						'email' : user_data.email
						}
					}
				return Response({"result":res}, status=status.HTTP_201_CREATED)
			return Response({"message":"You have exceeded the limit of 10 messages in an hour."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
		return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
