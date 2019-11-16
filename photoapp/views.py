from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status
from photoapp.models import Like,Contest,PhotoUpload
from .serializers import ContestSerializer


class ContestView(APIView):

      def get(self, request, *args, **kwargs):
          contests=Contest.objects.all()
          contest_serializer=ContestSerializer(contests,many=True)
          contest_json = JSONRenderer().render(contest_serializer.data)
          return Response(data=contest_json,status=status.HTTP_200_OK)




          
