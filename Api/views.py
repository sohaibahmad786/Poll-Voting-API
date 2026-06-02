from django.shortcuts import render
import jwt
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework import permissions
from rest_framework import generics,filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from datetime import datetime, timedelta
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from rest_framework .viewsets import ModelViewSet


from .models import Register
from .serializer import Register_serializer
from .models import Poll,Option,Vote
from .serializer import Poll_serializer,Option_serializer,Vote_serializer

    
class Register_view(generics.ListCreateAPIView):
    serializer_class=Register_serializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        login_user=self.request.user

        if not login_user.is_authenticated:
            return Register.objects.none()

        if login_user.Role=='admin':
            return Register.objects.all()
        else:
            return Register.objects.filter(id=login_user.id)
    
class Register_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Register.objects.all()
    serializer_class=Register_serializer
    authentication_classes=[JWTAuthentication,SessionAuthentication]
    permission_classes=[IsAuthenticated]


class PollView(ModelViewSet):
    queryset=Poll.objects.all()
    serializer_class=Poll_serializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class OptionView(ModelViewSet):
    queryset=Option.objects.all()
    serializer_class=Option_serializer
    permission_classes=[IsAuthenticated]

class VoteView(ModelViewSet):
    queryset=Vote.objects.all()
    serializer_class=Vote_serializer
    permission_classes=[IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user=request.user
        poll_id=request.data.get('poll')
        option_id=request.data.get('option')

        already_created=Vote.objects.filter(
            user=user,
            poll_id=poll_id
        ).exists()

        if already_created:
            return Response({'message':'you already voted'})
        
        option=Option.objects.get(id=option_id)
        option.votes+=1
        option.save()

        Vote.objects.create(
            user=user,
            poll_id=poll_id,
            option=option
        )

        return Response({
            'message':'Vote Submitted Successfully'
        })

# Create your views here.





