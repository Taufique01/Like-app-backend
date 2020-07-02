from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import requests
import zillow
from zillowAPI import zillow
from zillowAPI import ZillowDataType
from zillowAPI import ZillowAPI
from zillowAPI import ZillowError
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
# Create your views here.
class GetZillowSearch(APIView):
     
      def post(self, request, *args, **kwargs):
          print('ggggg')
          print(request.data)
          address = request.data.get('address')#"3400 Pacific Ave"
          postal_code =request.data.get('zip')# "90292"
          key='X1-ZWz1hkfgcy337v_55f1z'
          data=zillow().GetSearchResults(key, address, postal_code,True)
          def obj_dict(obj):
            return obj.__dict__
          json_string = json.dumps(data.results, default=obj_dict)

          print(json_string)
          return Response(data=json_string, status=status.HTTP_200_OK)

