from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style = {'input_type':'password'},write_only = True)
    class Meta:
        model  = User
        fields =  ['email','username','first_name','last_name','password','confirm_password'] #'__all__'
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        UserData = User.objects.create_user(**validated_data)
        return UserData
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        return super().validate(attrs)

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length = 255)
    class Meta:
        model = User
        fields = ['username','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style = {"input_type" : "password"},write_only = True)
    confirm_password = serializers.CharField(max_length = 255,style = {"input_type" : "password"},write_only = True)
    class Meta:
        fields = ['password','confirm_password']
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')
        if password != confirm_password:
            raise serializers.ValidationError("Password and confirm password doesn't match")
        user.set_password(password)
        user.save()
        return super().validate(attrs)

class SendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if  User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = 'http://127.0.0.1:8000/accounts/ResetPassword/'+uid+'/'+token
            body = 'Click Following Link to Reset Your Password' + link
            data = {
                'subject' : 'Reset Your Password',
                'body' : body,
                'to_email' : user.email
            }
            Util.send_email(data)
            return super().validate(attrs)
        else:
            raise serializers.ValidationError("you are not a registered user")

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style = {"input_type" : "password"},write_only = True)
    confirm_password = serializers.CharField(max_length = 255,style = {"input_type" : "password"},write_only = True)
    class Meta:
        fields = ['password','confirm_password']
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != confirm_password:
                raise serializers.ValidationError("Password and confirm password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("token is not valid or expired")
            user.set_password(password)
            user.save()
            return super().validate(attrs)
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator.check_token(user, token)
            raise serializers.ValidationError("token is not valid or expired")
            

        