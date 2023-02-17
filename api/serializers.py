from email.policy import default
from pkg_resources import require
from rest_framework import serializers, viewsets
from .models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# class UserAddressSerializer(WritableNestedModelSerializer):
#     address = AddressSerializer(many=False)    

#     class Meta:
#         model = UserAddress
#         fields = ('title', 'type', 'default','user', 'address', 'customer_id', 'created_at', 'updated_at')



class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ('id', 'name', 'guard_name', 'created_at', 'updated_at')

class UserSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    # address = UserAddressSerializer(many=True, required=False)
    permissions = PermissionsSerializer(many=True, required=False)
    # profile = ProfileSerializer(many=False, required=False)
    password = serializers.CharField(required=False, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField()
    avatar = serializers.ImageField(max_length=None, use_url=True)

    def validate_email(self, email):
        User = self.Meta.model
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already registered to a user.')
        return email

    def validate_username(self, username):
        User = self.Meta.model
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already taken. Try another one.')
        return username
    
    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data

    class Meta:
        model =  User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}, 'tokens':{}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        user = self.Meta.model.objects.create(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
    

class SponsorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Sponsor
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    sponsors = SponsorSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

class BeneficiarySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Beneficiary
        fields = '__all__'

class SponsorSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Sponsor
        fields = '__all__'