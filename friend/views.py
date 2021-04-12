from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse
import json
from user.models import UserSet,UserProfile,druginformation,Medical_Information
# Create your views here.
@csrf_exempt
def friend_code(request):
	if request.method == 'GET':  #獲取空糖團邀請碼
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Friend.objects.get(uid=uid)
			message = { 
			"status":"0",
			'invite_code':user.invite_code
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def friend_list(request):
	if request.method == 'GET':  #空糖團列表
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = UserSet.objects.get(uid=uid)
			user1 = UserProfile.objects.get(uid=uid)
			user2 = Friend_data.objects.get(uid=uid)
			message = {
			"status":"0",
			"friends":
			{"id": user.id,
			"name": user.name,
			"account": user1.account,
			"email": user.email,
			"phone": user.phone,
			"fb_id": user1.fb_id,
			"status": user2.status,
			"group": "null",
			"birthday": user.birthday,
			"height": user.height,
			"gender": user.gender,
			"verified": "1",
			"privacy_policy": "1",
			"must_change_password": user.must_change_password,
			"badge": "87",
			"created_at": user1.created_at,
			"updated_at": user1.updated_at,
			"relation_type": "1"}
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def friend_requests(request):#測試完成
	if request.method == 'GET':  #獲取空糖團邀請碼
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = UserSet.objects.get(uid=uid)
			user1 = UserProfile.objects.get(uid=uid)
			user2 = Friend_data.objects.get(uid=uid)
			user3 = druginformation.objects.get(uid=uid)
			user4 = Medical_Information.objects.get(uid=uid)
			message = { 
			"status":"0",
			"requests":
			{
			"id":user.id,
			"user_id":user4.user_id,
			"relation_id":"1",
			"type":user3.drugtype,
			"created_at": user1.created_at,
			"updated_at": user1.updated_at},
			"user":
			{
			"id":user.id,
			"name": user.name,
			"account":user1.account,
			"email": user.email,
			"phone": user.phone,
			"fb_id": user1.fb_id,
			"status": "Normal",
			"group": "???",
			"birthday": user.birthday,
			"height": user.height,
			"gender": user.gender,
			"verified": "1",
			"privacy_policy": "1",
			"must_change_password": user.must_change_password,
			"badge": "87",
			"created_at": user1.created_at,
			"updated_at": user1.updated_at,}
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def friend_send(request):#測試完成
	if request.method == 'POST':  #送出控糖團邀請
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			# uid = request.user.uid #(在app上測試)
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)			
			user = Friend.objects.get(uid=uid)
			try:
				invite_code = data['invite_code']
				profile = Friend.objects.get(invite_code=invite_code)
				print("123")
				if profile.invite_code==invite_code:
					user.invite_code = data['invite_code']
					user.type = data['type']
					user.save()
					message = {"status":"0"}
			except:
				message = {"status":"1"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def friend_accept(request,friend_data_id):
	if request.method == 'GET':  #接受控糖團邀請
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			check = Friend_data.objects.get(id=friend_data_id, status=0)
			Friend_data.objects.create(uid=uid, relation_id=check.uid, status=1, read=True, imread=True, friend_type=check.friend_type, updated_at=nowtime)
			check.read = True
			check.status = 1
			check.updated_at = nowtime
			check.save()
		except:
			output = {"status":"1"}
		else:
			output = {"status":"0"}
		return JsonResponse(output,safe=False)

@csrf_exempt
def friend_refuse(request,friend_data_id): # 拒絕控糖團邀請
	if request.method == 'GET':
		uid = request.user.id
		nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		try:
			check = Friend_data.objects.get(id=friend_data_id, status=0)
			check.read = True
			check.status = 2
			check.updated_at = nowtime
			check.save()
		except:
			output = {"status":"1"}
		else:
			output = {"status":"0"}
		return JsonResponse(output,safe=False)

@csrf_exempt
def friend_remove(request,friend_data_id): # 刪除控糖團邀請
	uid = request.user.id
	if request.method == 'GET':
		try:
			Friend_data.objects.filter(id=friend_data_id, status=0).delete()
		except:
			message = {"status":"1"}
		else:
			message = {"status":"0"}
		return JsonResponse(message)

@csrf_exempt
def friend_results(request,friend_data_id): # 控糖團結果
	if request.method == 'GET':
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			check = Friend_data.objects.get(id=friend_data_id, status=0)
			check.read = True
			check.status = 2
			check.updated_at = nowtime
			check.save()
		except:
			message = {"status":"1"}
		else:
			message = {"status":"0"}
		return JsonResponse(message)

@csrf_exempt
def friend_remove_more(request): # 刪除更多好友!
	uid = request.user.id
	if request.method == 'DELETE':
		Friend_data.objects.get(uid=ids, relation_id=uid, status=1).delete()
		Friend_data.objects.get(uid=uid, relation_id=ids, status=1).delete()
		message = {"status":"1"}
	else:
		message = {"status":"0"}
	return JsonResponse(message)