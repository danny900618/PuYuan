
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    uid= models.CharField(max_length=100, blank=True)
    account = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)
    fb_id = models.CharField(max_length=100, blank=False)
    invite_code = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100, blank=True)
    emailck = models.BooleanField(default=True)
    FBck = models.BooleanField(default=True)#unuse
    
    def __str__(self):
        data = dict()
        data = {
            'id':self.id,
            'uid':self.uid,
            'account':self.account,
            'password':self.password,
            'phone':self.phone,
            'email':self.email,
            'created_at':self.created_at,
            'updated_at':self.updated_at,
            'fb_id':self.fb_id,
            "invite_code":self.invite_code,
            "code":self.code,
            "emailck" :self.emailck
        }
        return str(data)

   
class UserSet(models.Model):
    uid= models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=30, blank=True)
    birthday =models.DateField(max_length=8, blank=True)#models.DateField()
    height = models.DecimalField(max_length=30,max_digits=2,decimal_places=1, blank=True)#models.DecimalField(max_digits=3,decimal_places=1)
    gender = models.BooleanField(default=True)
    fcm_id = models.CharField(max_length=30, blank=False)
    address = models.CharField(max_length=50, blank=True)
    weight = models.DecimalField(max_length=30,max_digits=2,decimal_places=2, blank=True)#models.DecimalField(max_digits=3,decimal_places=2)
    phone = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    must_change_password = models.BooleanField(default=True)	
    pushed_at = models.DateTimeField(auto_now=True)             #news最新資料時間
    sugar_delta_max = models.IntegerField( blank=True, default=0)
    sugar_delta_min = models.IntegerField( blank=True, default=0)
    sugar_morning_max = models.IntegerField( blank=True, default=0)
    sugar_morning_min = models.IntegerField( blank=True, default=0) 
    sugar_evening_max = models.IntegerField( blank=True, default=0)
    sugar_evening_min = models.IntegerField( blank=True, default=0)
    sugar_before_max = models.IntegerField( blank=True, default=0)
    sugar_before_min = models.IntegerField( blank=True, default=0)
    sugar_after_max = models.IntegerField( blank=True, default=0)
    sugar_after_min= models.IntegerField( blank=True, default=0)  
    systolic_max = models.IntegerField( blank=True, default=0)  
    systolic_min = models.IntegerField( blank=True, default=0)    
    diastolic_max = models.IntegerField( blank=True, default=0)   
    diastolic_min = models.IntegerField( blank=True, default=0) 
    pulse_max = models.IntegerField( blank=True, default=0)         
    pulse_min = models.IntegerField( blank=True, default=0)         
    weight_max = models.IntegerField( blank=True, default=0)        
    weight_min = models.IntegerField( blank=True, default=0)    
    bmi_max = models.IntegerField( blank=True, default=0)           
    bmi_min = models.IntegerField( blank=True, default=0)      
    body_fat_max = models.IntegerField( blank=True, default=0)    
    body_fat_min = models.IntegerField( blank=True, default=0)

    after_recording = models.BooleanField(default=True)        
    no_recording_for_a_day = models.BooleanField(default=True)  
    over_max_or_under_min = models.BooleanField(default=True)  
    after_meal = models.BooleanField(default=True)             
    unit_of_sugar = models.BooleanField(default=True)            
    unit_of_weight = models.BooleanField(default=True)          
    unit_of_height = models.BooleanField(default=True)      

    badge = models.DecimalField(max_digits=15,decimal_places=0,default="0") 
    group = models.CharField(max_length=100,blank=True) 
    def __str__(self):
        data = dict()
        data = {
            'uid':self.uid,
            'name' :self.name,
            'birthday' :self.birthday,
            'height' :self.height,
            'gender' :self.gender,
            'fcm_id' :self.fcm_id,
            'address' :self.address,
            'weight' :self.weight,
            'phone' :self.phone,
            'email' :self.email,
            'must_change_password' :self.must_change_password,

            'sugar_delta_max' :self.sugar_delta_max,
            'sugar_delta_min' :self.sugar_delta_min,
            'sugar_morning_max' :self.sugar_morning_max,
            'sugar_morning_min' :self.sugar_morning_min,
            'sugar_evening_max' :self.sugar_evening_max,
            'sugar_before_max' :self.sugar_before_max,
            '"sugar_before_min' :self.sugar_before_min,
            'sugar_after_max' :self.sugar_after_max,
            'sugar_after_min' :self.sugar_after_min,
            'systolic_max' :self.systolic_max,
            'systolic_min' :self.systolic_min,
            'diastolic_max' :self.diastolic_max,
            'diastolic_min' :self.diastolic_min,
            'pulse_max' :self.pulse_max,
            'pulse_min' :self.pulse_min,
            'weight_max' :self.weight_max,
            'weight_min' :self.weight_min,
            'bmi_max' :self.bmi_max,
            'bmi_min' :self.bmi_min,
            'body_fat_max' :self.body_fat_max,
            'body_fat_min' :self.body_fat_min,

            'after_recording' :self.after_recording,
            'no_recording_for_a_day' :self.no_recording_for_a_day,
            'over_max_or_under_min' :self.over_max_or_under_min,
            'after_meal' :self.after_meal,
            'unit_of_sugar' :self.unit_of_sugar,
            'unit_of_weight' :self.unit_of_weight,
            'unit_of_height' :self.unit_of_height,
            'badge':self.badge,
            'group':self.group
        }
        return str(data)



        
class Medical_Information(models.Model):
    uid= models.CharField(max_length=100, blank=True)
    a1c = models.DecimalField(max_digits=2,decimal_places=1, default=0)
    user_id =  models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    diabetes_type =  models.DecimalField(max_digits=15,decimal_places=0,default=0)
    oad = models.BooleanField(default=True)  
    insulin = models.BooleanField(default=True) 
    anti_hypertensives = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        data = dict()
        data = {
            'uid':self.uid,
            'a1c':self.a1c,
            'user_id':self.user_id,
            'diabetes_type':self.diabetes_type,
            'oad':self.oad,
            'insulin':self.insulin,
            'anti_hypertensives':self.anti_hypertensives,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(data)

class druginformation(models.Model):
    uid= models.CharField(max_length=100, blank=True)
    drugtype = models.BooleanField(default=True)#Boolean
    drugname = models.CharField(max_length=50, blank=True)
    recorded_at= models.DateTimeField(auto_now=True, auto_now_add=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        data = dict()
        data = {
            'uid':self.uid,
            'drugtype':self.drugtype,
            'drugname':self.drugname,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(data)

class Notification(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    member_id = models.CharField(max_length = 100,blank=True)
    reply_id = models.CharField(max_length = 100,blank=True)
    message = models.CharField(max_length = 100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        data = dict()
        data = {
            'uid':self.uid,
            'member_id':self.member_id,
            'reply_id':self.reply_id,
            'message':self.message,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(data)

class Share(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    fid = models.CharField(max_length = 100,blank=True)
    data_type = models.CharField(max_length = 100,blank=True)
    relation_type = models.CharField(max_length = 100,blank=True)
    def __str__(self):
        message = dict()
        message = {
            'uid':self.uid,
            'fid':self.fid,
            'data_type':self.data_type,
            'relation_type':self.relation_type
        }
        return str(message)