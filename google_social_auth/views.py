from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from django.conf import settings
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from google.oauth2 import id_token
from google.auth.transport import requests
from .forms import RequestTokeForm
from google_social_auth.models import AccessToken,Application
from . import common
from django.utils import timezone
from datetime import timedelta
import datetime

class TokenUtils():
      
      def create_id_token_response(self,token,application):
          try:
             GOOGLE_CLIENT_ID='407408718192.apps.googleusercontent.com'
             idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
             if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
             #valid id token 
          
     
          
             user, _created = User.objects.get_or_create(
                    email=idinfo['email'])
             if _created:
                 user.username=idinfo['sub']
                 user.first_name=idinfo['name']
                 user.last_name=idinfo['family_name']
                 user.save()
                 access_token = AccessToken(
                    user=user,
                    expires=datetime.datetime.now() + datetime.timedelta(days=1),
                    token=common.generate_token(),
                    application=application
                    )
                 access_token.save()
             else:
                  try:
                    access_token=user.access_token
                    access_token.token=common.generate_token()
                    expires=datetime.datetime.now() + datetime.timedelta(days=1)
                    access_token.save()
                  except AccessToken.DoesNotExist:
                    access_token = AccessToken(
                    user=user,
                    expires=datetime.datetime.now() + datetime.timedelta(days=1),
                    token=common.generate_token(),
                    application=application
                    )
                    
                    access_token.save()
                 
             return access_token
          except ValueError:
             return None






class ConvertTokenView(TokenUtils,APIView):
    """
    Implements an endpoint to convert a provider token to an access token
    The endpoint is used in the following flows:
    * Authorization code
    * Client credentials
    """ 

    def post(self, request, *args, **kwargs):
             
            
            client_secret = request.data.get('client_secret')
            client_id =request.data.get('client_id')
            token = request.data.get('token')
            print(request.POST)
            
            application = Application.objects.get(client_id=client_id)
            
            if application.client_secret==client_secret:
                access_token=self.create_id_token_response(token,application)
                if not access_token:
                   
                    return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            
                
                return Response(data={'access_token':access_token.token}, status=status.HTTP_200_OK)



class RevokeTokenView(APIView):
    """
    Implements an endpoint to convert a provider token to an access token
    The endpoint is used in the following flows:
    * Authorization code
    * Client credentials
    """ 

    def post(self, request, *args, **kwargs):
             
            
            access_token = request.data.get('token')
            acsess_token.revoke()
            return Response(status=status.HTTP_200_OK)
















       


    


