from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from photoapp.models import Like,Contest,PhotoUpload
from google_social_auth.models import AccessToken
from .serializers import ContestSerializer,MyContestSerializer


class ContestView(APIView):

      def get(self, request, *args, **kwargs):
          contests=Contest.objects.filter(end_date__gt=timezone.now())
          contest_serializer=ContestSerializer(contests,many=True)
          print(contest_serializer.data)
          #contest_json = JSONRenderer().render(contest_serializer.data)

          return Response(data=contest_serializer.data,status=status.HTTP_200_OK)




class MyContestView(APIView):

      def post(self, request, *args, **kwargs):
          print('token'+request.data.get('token'))
          try:                 
             access_token=AccessToken.objects.get(token=request.data.get('token'))
             user=access_token.user

          except AccessToken.DoesNotExist:
             return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

          contests=Contest.objects.filter(user=user,end_date__gt=timezone.now())
          contest_serializer=MyContestSerializer(contests,many=True,context={'user': user})
          print(contest_serializer.data)
          #contest_json = JSONRenderer().render(contest_serializer.data)

          return Response(data=contest_serializer.data,status=status.HTTP_200_OK)




          
