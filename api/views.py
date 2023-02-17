import imp
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from .models import *
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend,FilterSet
from .serializers import *
from .paginations import CustomPagination
from django_filters import CharFilter, NumberFilter, BooleanFilter

# Create your views here.
class UserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoadUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                user.data,
                status=status.HTTP_200_OK
            )


        except:
            return Response(
                {'error':'Something went wrong when trying to load user'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    def post(self, request):
       return Response('true')

class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    
class UserFilter(FilterSet):
    # categories = CharFilter(field_name='categories__slug', lookup_expr='iexact')
    role = CharFilter(field_name='role', lookup_expr='iexact')
    # name = CharFilter(field_name='name', lookup_expr='icontains')
    # shop_id = NumberFilter(field_name='shop_id', lookup_expr='exact')

    class Meta:
        model = User
        fields = []

class ProjectFilter(FilterSet):
    owner_id = NumberFilter(field_name='owner__id', lookup_expr='exact')

    class Meta:
        model = Project
        fields = []

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['role',]
    filterset_class = UserFilter

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['owner__id',]
    filterset_class = ProjectFilter

class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    pagination_class = CustomPagination

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    pagination_class = CustomPagination