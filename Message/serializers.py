from django.contrib.auth import get_user_model
from Message.models import MessageModel
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import  Serializer,ModelSerializer
from django.contrib.auth.models import User


class SignupSerializer(serializers.ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ['username','email','password']
		extra_kwargs = {
			'password':{'write_only':True}
		}


	def validate_password(self,value):
		validate_password(value)
		return value


	def create(self,validate_data):
		user = get_user_model()(**validate_data)
		user.set_password(validate_data['password'])
		user.save()
		return user



class LoginSerializer(Serializer):
	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True)




class UserSerializer(ModelSerializer):
	class Meta:
		model = get_user_model()
		fields = ['id','username','email']



class MessageSerializer(ModelSerializer):
    # created_by = UserSerializer(read_only=True)

    class Meta:
        model = MessageModel
        fields = ['id', 'message', 'created_at', 'updated_at','user']


