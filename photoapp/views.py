import json
import requests
from django.db.models import Count
from django.db.models.aggregates import Max
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from photoapp.models import Like,Contest,PhotoUpload,PaytmHistory
from google_social_auth.models import AccessToken
from .serializers import ContestSerializer,MyContestSerializer,ImageUploadForm,PhotoFeedSerializer,ContestHistorySerializer
from photoapp import Checksum
from django.core import serializers
class ContestView(APIView):

      def get(self, request, *args, **kwargs):
          contests=Contest.objects.filter(end_date__gt=timezone.now())
          contest_serializer=ContestSerializer(contests,many=True)
          print(contest_serializer.data)
          #contest_json = JSONRenderer().render(contest_serializer.data)filter(contest__end_date__lt=timezone.now())#.
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



class GetPhotoFeed(APIView):

      def post(self, request, *args, **kwargs):
          print('token'+request.data.get('token'))
          try:                 
             access_token=AccessToken.objects.get(token=request.data.get('token'))
             user=access_token.user

          except AccessToken.DoesNotExist:
             return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

          photo_up=PhotoUpload.objects.filter(contest__end_date__gt=timezone.now()).exclude(image__exact='')
          photo_up_serializer=PhotoFeedSerializer(photo_up,many=True,context={'user': user})
         
          #contest_json = JSONRenderer().render(contest_serializer.data)

          return Response(data=photo_up_serializer.data,status=status.HTTP_200_OK)


class PhotoLike(APIView):

      def post(self, request, *args, **kwargs):
          print('token'+request.data.get('token'))
          try:                 
             access_token=AccessToken.objects.get(token=request.data.get('token'))
             user=access_token.user

          except AccessToken.DoesNotExist:
             return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
          print(request.data)
          photo_id=request.data.get('id')
          isLiked=request.data.get('isLiked')
          photoUpload=PhotoUpload.objects.get(id=photo_id)
          try:
             like=Like.objects.get(user=user,photo=photoUpload)
          except Like.DoesNotExist:  
             like=Like.objects.create(user=user,photo=photoUpload)
          if isLiked=='true':          
             return Response(data={'isLiked':True},status=status.HTTP_200_OK)
          else:
             like.delete()
             return Response(data={'isLiked':False},status=status.HTTP_200_OK)
          
@csrf_exempt
def upload_pic(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            
          
            try:
               access_token = AccessToken.objects.get(token=form.cleaned_data['token'])
            except AccessToken.DoesNotExist:
               Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            user=access_token.user
            contest_id=form.cleaned_data['contest_id']
            image = form.cleaned_data['image']
            photo_upload=PhotoUpload.objects.get(user=user,contest__id=contest_id)
            photo_upload.image=image
            photo_upload.save()
            return JsonResponse({'img_url':photo_upload.image.url})
    return HttpResponseForbidden('allowed only via POST')


          
class ContestPayment(APIView):

     def post(self, request, *args, **kwargs):
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        MERCHANT_ID = settings.PAYTM_MERCHANT_ID
        CHANNEL_ID = settings.CHANNEL_ID
        WEBSITE=settings.WEBSITE
        INDUSTRY_TYPE_ID=settings.INDUSTRY_TYPE_ID
        print("gggg"+request.data.get('id'))
        ## Get token
        try:                 
            access_token=AccessToken.objects.get(token=request.data.get('token'))
            user=access_token.user
        except AccessToken.DoesNotExist:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        contest=Contest.objects.get(id=request.data.get('id'))
        bill_amount = str(contest.entry)
 
        ## Generating unique  ids
        order_id = Checksum.__id_generator__()
        CALLBACK_URL =settings.CALLBACK_URL + order_id
        

        data_dict = {
                'MERCHANT_ID':MERCHANT_ID,
                'ORDER_ID':order_id,
                'TXN_AMOUNT': bill_amount,
                'CUST_ID':user.username,
                'CALLBACK_URL':CALLBACK_URL,
                'CHANNEL_ID':CHANNEL_ID,
                'WEBSITE': WEBSITE,
                'INDUSTRY_TYPE_ID':INDUSTRY_TYPE_ID,
                 
        }
        param_dict = data_dict
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, MERCHANT_KEY)
        
        return JsonResponse(param_dict)
        
class VerifyPayment(APIView):

     def post(self, request, *args, **kwargs):
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        MERCHANT_ID = settings.PAYTM_MERCHANT_ID
        orderId=request.POST['ORDER_ID']
    

        ## Get token
        try:                 
            access_token=AccessToken.objects.get(token=request.data.get('token'))
            user=access_token.user
        except AccessToken.DoesNotExist:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        contest=Contest.objects.get(id=request.data.get('id'))
        bill_amount = str(contest.entry)
 
        ## initialize a dictionary
        paytmParams = dict()
        paytmParams["MID"] = MERCHANT_ID
        paytmParams["ORDERID"] = orderId
        ## Generate checksum by parameters we have in body
        checksum = Checksum.generate_checksum(paytmParams, MERCHANT_KEY)
        ## put generated checksum value here
        paytmParams["CHECKSUMHASH"] = checksum
        ## prepare JSON string for request
        post_data = json.dumps(paytmParams)

        url = settings.VERIFY_URL
        pay_res = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        
        if('ErrorMsg' in pay_res):
            return JsonResponse({'PAY_STATUS':pay_res['ErrorMsg']})

        status=pay_res['STATUS']
        back_response={
                'PAY_STATUS':status,
            }



        if status== 'TXN_SUCCESS':
            photo_upload=PhotoUpload(user=user,contest=contest)
           
            photo_upload.save()
            ## step 4 save the payment
            PaytmHistory.objects.create(user=user,photo_upload=photo_upload,**pay_res)
            return JsonResponse(back_response)
        return JsonResponse(back_response)
       

class ContestHistoryView(APIView):

      def get(self, request, *args, **kwargs):
          #print(contest_serializer.data)
          contest=Contest.objects.filter(end_date__lt=timezone.now())
          contest_history=ContestHistorySerializer(contest,many=True)
          
          return Response(data=contest_history.data,status=status.HTTP_200_OK)



class UserEarningView(APIView):

      def post(self, request, *args, **kwargs):
         try:                 
             access_token=AccessToken.objects.get(token=request.data.get('token'))
             user=access_token.user
         except AccessToken.DoesNotExist:
             return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

         profile=user.profile
         profile.refreshContestWon()
               
         return Response(data={'total_earning':profile.total_earning,'withdrawn':profile.withdrawn,'availabe':profile.availabeEarning()},status=status.HTTP_200_OK)




####################classes###########

      





