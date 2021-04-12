from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import auth
from django.core.mail import send_mail, send_mass_mail
import uuid,email.message,smtplib,hashlib,random
from django.contrib.sessions.models import Session
import uuid
from friend.models import Friend_data
# Create your views here.

@csrf_exempt
def b_pressure(request):#上傳成功,但是終端機會報錯
	if request.method == 'POST':  #上傳血壓測量結果
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			# uid = request.user.uid #(在app上測試)
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)			
			# recorded_at = auto_now
			# recorded_at = data['recorded_at']
			# recorded_at = recorded_at.replace("%20", " ")
			# recorded_at = recorded_at.replace("%3A", ":")
			user = Blood_pressure.objects.get(uid=uid)
			user.systolic = data['systolic']
			user.diastolic = data['diastolic']
			user.pulse = data['pulse']
			# user.recorded_at=recorded_at
			user.save()
			return JsonResponse({"status":"0"})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def weight(request):#上傳成功,但是終端機會報錯
	if request.method == 'POST':#上傳體重測量結果
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Weight.objects.get(uid=uid)
			user.weight=data['weight']
			user.body_fat=data['body_fat']
			user.bmi=data['bmi']
			# user.recorded_at=data['recorded_at']
			user.save()
			return JsonResponse({"status":"0"})
		except:
			return JsonResponse({"status":"1"})
			
@csrf_exempt
def b_sugar(request):#上傳成功,但是終端機會報錯
	if request.method == 'POST':#上傳體重測量結果
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Blood_sugar.objects.get(uid=uid)
			user.sugar=data['sugar']
			user.timeperiod=data['timeperiod']
			# user.recorded_at=data['recorded_at']
			user.save()
			return JsonResponse({"status":"0"})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def last_upload(request):#測試成功
	if request.method == 'GET':#最後上傳時間
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		# uid = request.user.uid #(在app上測試)
		uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
		user = Weight.objects.get(uid=uid)
		user1 = Blood_sugar.objects.get(uid=uid)
		user2 = Blood_pressure.objects.get(uid=uid)
		try:
			user.save()
			return JsonResponse({
			"status": "0",
			"last_upload": {
			"blood_pressure": user2.pulse,
			"weight": user.weight,
			"blood_sugar": user1.sugar
			# "diet": user1.date
			}
			})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def records(request):#測試成功
	uid = request.user.id
	if request.method == 'POST':#上一筆紀錄資訊
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data) #少一個input "diets"
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Blood_sugar.objects.get(uid=uid)
			user1 = Blood_pressure.objects.get(uid=uid)
			user2 = Weight.objects.get(uid=uid)
			return JsonResponse({
			"status":"0",
			"blood_sugars":{
			"id":user.id,
			"user_id":user.user_id,
			"sugar":user.sugar,
			"timeperiod":user.timeperiod,
			"recorded_at":user.recorded_at
			},
			"blood_pressures":{
			"id":user1.id,
			"user_id":user1.user_id,
			"systolic":user1.systolic,
			"diastolic":user1.diastolic,
			"pulse":user1.pulse,
			"recorded_at":user1.recorded_at
			},
			"weights":{
			"id":user2.id,
			"user_id":user2.user_id,
			"weight":user2.weight,
			"body_fat":user2.body_fat,
			"bmi":user2.bmi,
			"recorded_at":user2.recorded_at
			}
			})
		except:
			return JsonResponse({"status":"1"})
	if request.method == 'DELETE':#刪除日記記錄
		# data = request.body
		# data = str(data, encoding="utf-8")
		# data=json.loads(data) 
		try:
			user = Blood_sugar.objects.get(uid=uid)
			user.delete()
			user1 = Blood_pressure.objects.get(uid=uid)
			user1.delete()
			user2 = Weight.objects.get(uid=uid)
			user2.delete()
			return JsonResponse({"status":"0"})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def diary(request):
	if request.method == 'GET':#日記列表資料
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		# uid = request.user.uid #(在app上測試)
		uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
		user = Blood_sugar.objects.get(uid=uid)
		user1 = Blood_pressure.objects.get(uid=uid)
		user2= Weight.objects.get(uid=uid)
		try:
			return JsonResponse({
			"status": "0",
			"blood_sugars":{
			"id":user.id,
			"user_id":user.user_id,
			"sugar":user.sugar,
			"timeperiod":user.timeperiod,
			"recorded_at":user.recorded_at,
			},
			"blood_pressures":{
			"id":user1.id,
			"user_id":user1.user_id,
			"systolic":user1.systolic,
			"diastolic":user1.diastolic,
			"pulse":user1.pulse,
			"recorded_at":user1.recorded_at
			},
			"weights":{
			"id":user2.id,
			"user_id":user2.user_id,
			"weight":user2.weight,
			"body_fat":user2.body_fat,
			"bmi":user2.bmi,
			"recorded_at":user2.recorded_at
			}
			})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def Diary_diet(request):
	if request.method == 'POST':#飲食日記
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Diary_diet.objects.get(uid=uid)
			user.description=data['description']
			user.meal=data['meal']
			user.tag=data['tag']
			user.image=data['image']
			user.lat=data['lat']
			user.lng=data['lng']
			user.recorded_at=data['recorded_at']
			user.save()
			return JsonResponse({"status":"0"})
		except:
			return JsonResponse({"status":"1"})

@csrf_exempt
def care(request):  
	if request.method == 'POST':  #發送關懷諮詢 #測試完成
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			# uid = request.user.uid #(在app上測試)
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)			
			user = UserCare.objects.get(uid=uid)
			user.message = data['message']
			user.save()
			return JsonResponse({"status":"0"})
		except:
			return JsonResponse({"status":"1"})
	if request.method == 'GET':#獲取關懷諮詢 #測試完成
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		# uid = request.user.uid #(在app上測試)
		uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
		user = UserCare.objects.get(uid=uid)
		try:
			return JsonResponse(
			{
			"status": "0",
			"cares":
			{
			"id":user.id,
			"user_id":user.uid, 
			"member_id": user.member_id,
			"reply_id": user.reply_id,
			"message": user.message, 
			"created_at": user.created_at,
			"updated_at": user.updated_at
			}
			}
			)
		except:
			return JsonResponse({"status":"1"})
			