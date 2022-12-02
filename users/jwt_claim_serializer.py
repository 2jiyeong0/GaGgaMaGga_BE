from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework import serializers, exceptions

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import User, LoggedIn

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD
    token_class = RefreshToken

    default_error_messages = {"no_active_account": _("아이디와 비밀번호를 확인해주세요. ")}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()
    
    def validate(self, attrs):
        authenticate_kwargs = {self.username_field: attrs[self.username_field], "password": attrs["password"],}
        
        try:
            authenticate_kwargs["request"] = self.context["request"]
            
        except KeyError:
            pass
            
        self.user = authenticate(**authenticate_kwargs)\
            
        try:
            username = attrs[self.username_field]
            self.target_user =  User.objects.get(username=username)
            self.is_active = self.target_user.is_active
            self.withdraw = self.target_user.withdraw
            
            account_lock_count = self.target_user.account_lock_count
            
            #로그인 제한 횟수 counting
            if self.user == None:
                self.target_user.account_lock_count += 1
                self.target_user.save()

            #로그인 제한 횟수 counting이 5이면 잠금
            if account_lock_count == 4:
                self.target_user.is_active = False   
                self.target_user.account_lock_time = timezone.now()
                self.target_user.save()
                
            #회원 상태 S이면 제한 시간 확인 후 N으로 변경
            self.now_today_time = timezone.now()

            if self.is_active == False:
                target_user_lock_time = self.target_user.lock_time + timezone.timedelta(minutes=5)
                
                if self.now_today_time >= target_user_lock_time:
                    self.target_user.is_active = True
                    self.target_user.lock_count = 0
                    self.target_user.save()

            #회원상태 비활성화이면 로그인 시 비활성화 해제
            if self.withdraw == True:
                self.target_user.withdraw = False
                self.target_user.save()
            
        except:
            pass
        
        #회원 상태 에러 발생
        if User.objects.filter(username=username).exists():
            
            #회원 상태 S이면 계정잠금 에러
            if self.is_active == False:
                raise serializers.ValidationError("계정이 잠금이 되었습니다. 잠시 후 다시 시도해주시길 바랍니다. ")
        
        #로그인 실패 에러
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(self.error_messages["no_active_account"],"no_active_account",)
        
        #로그인 로그
        LoggedIn.objects.create(user=self.target_user, created_at=self.now_today_time)
        
        #로그인 토큰 발행
        refresh = self.get_token(self.user)

        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return {"access":attrs["access"], "refresh":attrs["refresh"]}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["username"] = user.username
        
        return token