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
from body.models import Blood_pressure,Weight,Blood_sugar
from friend.models import Friend,Friend_data
# Create your views here.
@csrf_exempt #修飾器,一定要加不然會出問題的樣子
def register(request):#def後面就接跟功能相關的單字之類
	if request.method == "POST":#防呆 這邊用到POST,API文件上面有
		data=request.body#這2行是把接收到的格式轉成json格式
		data=str(data,encoding="UTF-8")
		data=json.loads(data)#因為postman需要用json格式才這樣寫
		try:
			account = data["account"]#這邊格式是json格式,postman在用的時候要用raw來測試
			phone = data["phone"]
			password = data["password"]
			email = data["email"]
			uid = uuid.uuid3(uuid.NAMESPACE_DNS,'account')
			invite_code = ''.join(random.sample("0123456789",6))#隨機生成0~9的6位隨機整數
			if UserProfile.objects.get(uid=uid):
				return JsonResponse({'status':'0'})
			else:
				UserProfile.objects.create(uid=uid,account=account,password=password,phone=phone,email=email,invite_code=invite_code)
				Medical_Information.objects.create(uid=uid)
				UserSet.objects.create(uid=uid,must_change_password=0)#後來新增change還沒測
				druginformation.objects.create(uid=uid)
				Blood_pressure.objects.create(uid=uid)
				Weight.objects.create(uid=uid)
				Blood_sugar.objects.create(uid=uid)
				Friend.objects.create(uid=uid,invite_code=invite_code)
				Friend_data.objects.create(uid=uid)
				UserCare.objects.create(uid=uid)
				Share.objects.create(uid=uid)
				Notification.objects.create(uid=uid)
			message={
				"status":"0"
			}
		except:
			message={
				"status":"1"
			}
		return JsonResponse(message)
@csrf_exempt
def login(request): # 登入 #測試成功    
	if request.method == "POST":
		account=request.POST.get('account')#這兩行讀使用者輸入的帳號和密碼
		password=request.POST.get('password')
		try:
			user = UserProfile.objects.get(account=account)
			auth_obj = auth.authenticate(request,account=account,password=password)
			if auth_obj:
				request.session.create()
				auth.login(request, auth_obj)
			message = {"status": "0",
			"token":request.session.session_key
			}
			return JsonResponse(message)	
		except:
			return JsonResponse({'status':'1'})	

@csrf_exempt
def logout(request): # 登出
	if request.method == "POST":
		auth.logout(request)
		return HttpResponseRedirect('api/login')

@csrf_exempt
def send(request):  # 傳送驗證信 #測試成功
	if request.method == "POST":
		emaildata=request.POST.get('email')
		profile = UserProfile.objects.get(email=emaildata)
		code = ''.join(random.sample("0123456789",6)) #隨機生成0~9的6位隨機整數
		profile.code = code
		profile.save()
		content = "歡迎使用普元血糖app:\n請點選下列連結完成註冊:\n127.0.0.1:8000/api/check\n驗證碼:{}".format(code)#此行到下面server.close都是寄信的標準格式
		msg = email.message.EmailMessage()
		msg["From"] = "nihandsomeni@gmail.com"
		msg["To"] = request.POST.get('email')
		msg["Subject"] = "普元認證"
		print(msg["To"])
		msg.set_content(content)
		server = smtplib.SMTP_SSL("smtp.gmail.com",465)
		server.login("nihandsomeni@gmail.com","ni123456ni")#這邊是以這組帳號密碼登入發送訊息，一開始要去google帳戶裡面設定>安全性>低安全性應用程式存權設定打開
		server.send_message(msg)
		server.close()
		return JsonResponse({'status':'0'})	

@csrf_exempt
def check(request):  #測試成功
	if request.method == "POST":
		try:
			code=request.POST.get('code')#使用者輸入的認證碼為code
			phonedata=request.POST.get('phone')
			profile = UserProfile.objects.get(phone=phonedata)#profile來接收 phonedata那一整列
			if profile.code==code:
				return JsonResponse({'status':'0'})
		except:
			return JsonResponse({'status':'1'})

@csrf_exempt
def ForgetPwd(request): #測試成功
	if request.method == "POST":
		try:
			newpassword = ''.join(random.sample("0123456789",8)) #newpassword #隨機生成0~9的8位隨機整數
			content = "這是您的新密碼:{}".format(newpassword)
			emaildata=request.POST.get('email')#emaildata接收使用者輸入的email
			profile = UserProfile.objects.get(email=emaildata)#找到使用者輸入的EAMIL對應到資料庫那一列
			profile.password = newpassword#將隨機產生8位數密碼更新到那一列的密碼
			profile.save()
			msg = email.message.EmailMessage()
			msg["From"] = "nihandsomeni@gmail.com"
			msg["To"] = request.POST.get('email')
			msg["Subject"] = "普元認證"
			print(msg["To"])
			msg.set_content(content)
			server = smtplib.SMTP_SSL("smtp.gmail.com",465)
			server.login("nihandsomeni@gmail.com","ni123456ni")
			server.send_message(msg)
			server.close()
			return JsonResponse({'status':'0'})
		except:
			return JsonResponse({'status':'1'})

@csrf_exempt
def ResetPwd(request):  #測試成功
	if request.method == "POST":
		try:
			passworddata = request.POST.get('password')#使用者輸入忘記密碼產生的新密碼8位數
			newpassword = request.POST.get('newpassword')#設定新密碼
			profile = UserProfile.objects.get(password=passworddata)#找到使用者新密碼的那一列
			profile.password = newpassword#使用者自己訂的密碼更新到那一列的密碼
			profile.save()
			return JsonResponse({'status':'0'})
		except:
			return JsonResponse({'status':'1'})

@csrf_exempt
def recheck(request): #註冊確認uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
	if request.method == 'GET':
		user_ck = request.GET["account"]
		try:
			user = UserProfile.objects.get(username=user_ck)
			message = {'status':'1'}
		except:
			message = {'status':'0'}
		return JsonResponse(message)

def privacy_policy(request): # 隱私權聲明 FBLogin
	result = '1'
	try:
		if request.method == 'POST':
			result = '0'
	except:
		pass
	return JsonResponse({'status': result})


# @csrf_exempt
# def user_set(request):  
# 	# data=request.body #這2行是把接收到的格式轉成json格式
# 	# data=str(data,encoding="UTF-8")
# 	if request.method == "PATCH":
# 		try:
# 			name=request.POST('name')
			# birthday=request.POST.get('birthday')
			# height=request.POST.get('height')
			# gender=request.POST.get('gender')
			# address=request.POST.get('address')
			# weight=request.POST.get('weight')
			# phone=request.POST.get('phone')
			# email=request.POST.get('email')
			# UserSet.objects.create(name=name)
# 			user.save()
# 			return JsonResponse({'status':'0'})
# 		except:
# 			return JsonResponse({'status':'1'})	

@csrf_exempt
def User_set(request):#測試成功
	if request.method == 'PATCH':  #個人資訊上傳
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			user = UserSet.objects.get(uid=uid)
			user.name = data['name']
			user.birthday=data['birthday']
			user.height=data['height']
			user.gender=data['gender']
			user.address=data['address']
			user.weight=data['weight']
			user.phone=data['phone']
			user.email=data['email']
			user.save()
			message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

	if request.method == 'GET':  #個人資訊 #測試成功
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		uid = data['token']
		# uid = request.user.uid #(在app上測試)
		uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
		user = UserProfile.objects.get(uid=uid)
		user_set = UserSet.objects.get(uid=uid)
		try:
			message = {
			"status":"0",
			"user":{
			"id":user.id,   
			"name":user_set.name,
			"account":user.account,
			"email":user.email,
			"phone":user_set.phone,
			# "fb_id":user_set.fb_id,
			# "status":user_set.status,
			# "group":user_set.group,
			"birthday":user_set.birthday,
			"height":user_set.height,
			"weight":user_set.weight,
			"gender":user_set.gender,
			"address":user_set.address}
			}
			# "unread_records":[int(UserSetdata.unread_records_one),UserSetdata.unread_records_two,int(UserSetdata.unread_records_three)],
			# "verified":int(UserSetdata.verified),
			# "privacy_policy":UserSetdata.privacy_policy,
			# "must_change_password":1 if UserSetdata.must_change_password else 0,
			# "fcm_id":UserSetdata.fcm_id,
			# "badge":int(UserSetdata.badge),
			# "login_time":int(UserSetdata.login_times),
			# "created_at": datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
			# "updated_at": datetime.strftime(UserProfiledata.updated_at,"%Y-%m-%d %H:%M:%S")},
			# "default":{
			# "id": UserProfiledata.id,
			# "user_id": Userdeflat.uid,
			# "sugar_delta_max": int(Userdeflat.sugar_dalta_max),
			# "sugar_delta_min":int(Userdeflat.sugar_delta_min),
			# "sugar_morning_max": int(Userdeflat.sugar_morning_max),
			# "sugar_morning_min": int(Userdeflat.sugar_morning_min),
			# "sugar_evening_max": int(Userdeflat.sugar_evening_max),
			# "sugar_evening_min": int(Userdeflat.sugar_evening_min),
			# "sugar_before_max": int(Userdeflat.sugar_before_max),
			# "sugar_before_min": int(Userdeflat.sugar_before_min),
			# "sugar_after_max": int(Userdeflat.sugar_after_max),
			# "sugar_after_min":int(Userdeflat.sugar_after_min),
			# "systolic_max": int(Userdeflat.systolic_max),
			# "systolic_min": int(Userdeflat.systolic_min),
			# "diastolic_max": int(Userdeflat.diastolic_max),
			# "diastolic_min":int(Userdeflat.diastolic_min),
			# "pulse_max": int(Userdeflat.pulse_max),
			# "pulse_min":int(Userdeflat.pulse_min),
			# "weight_max": int(Userdeflat.weight_max),
			# "weight_min": int(Userdeflat.weight_min),
			# "bmi_max": int(Userdeflat.bmi_max),
			# "bmi_min": int(Userdeflat.bmi_min),
			# "body_fat_max": int(Userdeflat.body_fat_max),
			# "body_fat_min": int(Userdeflat.body_fat_min),
			# "created_at": datetime.strftime(UserProfiledata.created_at ,"%Y-%m-%d %H:%M:%S"),
			# "updated_at": datetime.strftime(UserProfiledata.updated_at,"%Y-%m-%d %H:%M:%S")}
			# "setting":{
			# "id": UserProfiledata.id,
			# "user_id":Userdeflat.uid,
			# "after_recording": int(UserSetdata.after_recording),
			# "no_recording_for_a_day": int(UserSetdata.no_recording_for_a_day),
			# "over_max_or_under_min": int(UserSetdata.over_max_or_under_min),
			# "after_meal":int(UserSetdata.after_mael),
			# "unit_of_sugar": int(UserSetdata.unit_of_sugar),
			# "unit_of_weight": int(UserSetdata.unit_of_weight),
			# "unit_of_height": int(UserSetdata.unit_of_height),
			# "created_at":datetime.strftime(UserSetdata.created_at ,"%Y-%m-%d %H:%M:%S"),
			# "updated_at": datetime.strftime(UserSetdata.updated_at ,"%Y-%m-%d %H:%M:%S")}
			# }
			# message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def User_defult(request):#測試成功
	if request.method == 'PATCH':  #個人資訊預設值
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = data['token']
			user = UserSet.objects.get(uid=uid)
			# uid = request.user.uid #(在app上測試)
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
			user.sugar_delta_max = data['sugar_delta_max']
			user.sugar_delta_min = data['sugar_delta_min']
			user.sugar_morning_max=data['sugar_morning_max']
			user.sugar_morning_min=data['sugar_morning_min']
			user.sugar_evening_max=data['sugar_evening_max']
			user.sugar_evening_min=data['sugar_evening_min']
			user.sugar_before_max=data['sugar_before_max']
			user.sugar_before_min=data['sugar_before_min']
			user.sugar_after_max = data['sugar_after_max']
			user.sugar_after_min = data['sugar_after_min']
			user.systolic_max=data['systolic_max']
			user.systolic_min=data['systolic_min']
			user.diastolic_max=data['diastolic_max']
			user.diastolic_min=data['diastolic_min']
			user.pulse_max=data['pulse_max']
			user.pulse_min=data['pulse_min']
			user.weight_max=data['weight_max']
			user.weight_min=data['weight_min']
			user.bmi_max=data['bmi_max']
			user.bmi_min=data['bmi_min']
			user.body_fat_max=data['body_fat_max']
			user.body_fat_min=data['body_fat_min']
			user.save()
			message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def User_setting(request):#測試成功
	if request.method == 'PATCH':  #個人設定
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = data['token']
			user = UserSet.objects.get(uid=uid)
			# uid = request.user.uid #(在app上測試)
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)
			user.after_recording = data['after_recording']
			user.no_recording_for_a_day = data['no_recording_for_a_day']
			user.over_max_or_under_min = data['over_max_or_under_min']
			user.after_meal = data['after_meal']
			user.unit_of_sugar = data['unit_of_sugar']
			user.unit_of_weight = data['unit_of_weight']
			user.unit_of_height = data['unit_of_height']
			message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)


@csrf_exempt
def hba1c(request):
	if request.method == 'GET':  #糖化血色素  #a1c已經移動到藥物資訊欄
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Medical_Information.objects.get(uid=uid)
			message = {
			"status":"0",
			'uid':uid,
			"a1cs":
			{'a1c':a1c,
			'created_at':created_at,
			'updated_at':updated_at,
			'after_recording':after_recording,
			'no_recording_for_a_day':no_recording_for_a_day,
			'over_max_or_under_min':over_max_or_under_min,
			'after_meal':after_meal,
			'unit_of_sugar':unit_of_sugar,
			'unit_of_weight':unit_of_weight,
			"unit_of_height":unit_of_height}
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)
	if request.method == 'POST':  #送糖化血色素
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Medical_Information.objects.get(uid=uid)
			user.a1c = data['a1c']
			user.save()
		except:
			message = {"status":"1"}
		return JsonResponse(message)
	
	if request.method == 'DELETE':  #刪除糖化血色素
		uid = request.user.uid
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		user = Medical_Information.objects.get(uid=uid)
		try:
			deletedwho = data['ids']
			if deletedwho == '1':
				user.user_id =''
				user.save()
				message = {'status':'0'}
			elif deletedwho == '2':
				user.a1c = 0
				user.save()
				message = {'status':'0'}
		except:
			message = {'status':'1'}
		return JsonResponse(message)


@csrf_exempt
def med_inf(request):
	if request.method == 'GET': #就醫資訊  #測試成功
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Medical_Information.objects.get(uid=uid)
			message = {
			"status":"0",
			"medical_info": {
			"id":user.id,
			"user_id":user.user_id,
			"diabetes_type":user.diabetes_type,
			"oad":user.oad,
			"insulin":user.insulin,
			"anti_hypertensives":user.anti_hypertensives,
			"created_at":user.created_at,
			"updated_at":user.updated_at 
			}
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)
	if request.method == 'PATCH':  #更新就醫資訊 #測試成功
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = Medical_Information.objects.get(uid=uid)
			user.diabetes_type = data['diabetes_type']
			user.oad = data['oad']
			user.insulin = data['insulin']
			user.anti_hypertensives = data['anti_hypertensives']
			user.save()
			message = {"status":"0"}
		except:
			message = {"status":"1"}
		return JsonResponse(message)
@csrf_exempt
def drug_inf(request):
	if request.method == 'GET':  # 藥物資訊展示  測試完成
		# uid = request.user.uid
		data = request.body
		data = str(data, encoding="utf-8")
		uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
		druginformationdata = druginformation.objects.get(uid=uid)
		UserProfiledata = UserProfile.objects.get(uid=uid)
		UserSetdata = UserSet.objects.get(uid=uid)
		try:
			type1 = "0"
			if type1 == '0':
				message = {
					"status": "0",
					"drug_useds": {
						"id": UserProfiledata.id,
						"user_id": UserSetdata.name,
						"type": druginformationdata.drugtype,
						"name": druginformationdata.drugname,
						"recorded_at": druginformationdata.recorded_at
					}
				}
		except:
			message = {'status': '1'}
		return JsonResponse(message, safe=False)
	if request.method == 'POST':  #藥物資訊 上傳 #測試完成
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1"
			# uid = request.user.uid #(在app上測試)
			user = druginformation.objects.get(uid=uid)
			user.drugname = data['name']
			user.drugtype = data['Type']

			user.save()
			message = {
			"status":"0"
			}
		except:
	 		message = {"status":"1"}
		return JsonResponse(message)
	if request.method == 'DELETE':  #刪除藥物資訊
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			deletedwho = data['ids']
			if deletedwho == 'drugname':
				user.drugname = []
				user.save()
				message = {'status':'0'}
			elif deletedwho == 'drugtype':
				user.drugtype  = []
				user.save()
				message = {'status':'0'}
		except:
			message = {'status':'1'}
		return JsonResponse(message)

@csrf_exempt
def notification(request):
	if request.method == 'POST':  #親友團通知
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			# uid = request.user.uid #(在app上測試)
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)			
			user = Notification.objects.get(uid=uid)
			user.message = data['message']
			user.save()
			message = {
			"status":"0"
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)

@csrf_exempt
def share(request):
	if request.method == 'POST':  #分享
		data = request.body
		data = str(data, encoding="utf-8")
		data=json.loads(data)
		try:
			# uid = request.user.uid #(在app上測試)
			uid = "0f2541f1-8953-3ed4-9673-fb41519e21c1" #postman測試(直接將1代換成uid)			
			user = Share.objects.get(uid=uid)
			user.data_type = data['type']
			user.fid= data['id']
			user.relation_type = data['relation_type']
			user.save()
			message = {
			"status":"0"
			}
		except:
			message = {"status":"1"}
		return JsonResponse(message)
		
@csrf_exempt
def share_check(request,relation_type):
	if request.method == 'GET':  # 查看分享（含自己分享出去的）!
		uid = request.user.uid #(在app上測試)
		user_pro = UserProfile.objects.get(uid=uid)
		user = UserSet.objects.get(uid=uid)
		if share_check.data_type == '0' :
			share_data = Blood_pressure.objects.get(uid=share_check.uid, id=share_check.fid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"systolic":share_data.systolic,
				"diastolic":share_data.diastolic,
				"pulse":share_data.pulse,
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":0,
				"user":
					{
					"id":user_pro.uid,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		if share_check.data_type == '1' :
			share_data = Weight.objects.get(uid=share_check.uid, id=share_check.fid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"weight":float(share_data.weight),
				"body_fat":float(share_data.body_fat),
				"bmi":float(share_data.bmi),
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":1,
				"user":
					{
					"id":user_pro.uid,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		if share_check.data_type == '2' :
			share_data = Blood_sugar.objects.get(uid=share_check.uid, id=share_check.fid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"sugar":float(share_data.sugar),
				"timeperiod":int(share_data.timeperiod),
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":2,
				"user":
					{
					"id":user_pro.id,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		if share_check.data_type == '3' :
			share_data = Diary_diet.objects.get(uid=share_check.uid, id=share_check.fid)
			created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
			recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
			created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
			updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
			image = str(share_data.image)
			r = {
				"id":share_data.id,
				"user_id":share_data.uid,
				"description":share_data.description,
				"meal":int(share_data.meal),
				"tag":share_data.tag,
				"image":str(image),
				"lat":share_data.lat,
				"lng":share_data.lng,
				"recorded_at":recorded_at,
				"created_at":created_at,
				"type":3,
				"user":{
					"id":user_pro.uid,
					"name":user.name,
					"account":user.email,
					"email":user.email,
					"phone":user.phone,
					"fb_id":user_pro.fb_id,
					"status":user.status,
					"group":user.group,
					"birthday":user.birthday,
					"height":user.height,
					"gender":user.gender,
					"verified":user.verified,
					"privacy_policy":user.privacy_policy,
					"must_change_password":user.must_change_password,
					"badge":user.badge,
					"created_at":created_at_userfile,
					"updated_at":updated_at_userfile
					}
				}
		message = {"status":"0"}
	else:
		message = {"status":"1"}
	return JsonResponse(message)


@csrf_exempt
def newnews(request): #最新消息
	if request.method == 'GET':
		uid = request.user.uid #(在app上測試)
		user = UserProfile.objects.get(uid=uid)
		user1 = UserSet.objects.get(uid=uid)
		user2 = Notification.objects.get(uid=uid)
		try:
			message = {
			'status':'0',
			'news':{
				"id": user.id,
				"member_id": user2.member_id,
				"group": user1.group,
				"message": user2.message,
				"pushed_at": user1.pushed_at,
				"created_at": user.created_at,
				"updated_at": user1.updated_at
				}
			}
		except:
			message = {'status':'1'}
		return JsonResponse(message)