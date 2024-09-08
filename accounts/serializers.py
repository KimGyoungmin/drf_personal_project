from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from rest_framework.exceptions import AuthenticationFailed, ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'nickname', 'birthday',
                  'gender', 'bio', "date_joined", "password", "password2",)
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'nickname': {'required': True},
            'birthday': {'required': True},
        }
    # 추가 유효성 검사 로직

    def validate(self, valid_user):
        # 비밀번호 일치 확인
        if valid_user['password'] != valid_user['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        # 이메일 유일성 확인
        if CustomUser.objects.filter(email=valid_user['email']).exists():
            raise serializers.ValidationError({"email": "이미 사용 중인 이메일입니다."})

        return valid_user

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            birthday=validated_data['birthday'],
            gender=validated_data['gender'],
            bio=validated_data['bio'],
        )
        # 비밀번호는 해시화 해서 저장
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'nickname', 'birthday', 'gender', 'bio',)
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'nickname': {'required': True},
            'birthday': {'required': True},
        }

    def validate(self, attrs):
        instance = self.instance
        # 수정된 이메일은 기존 다른 사용자의 이메일과 username은 중복되면 안됨
        if CustomUser.objects.filter(email=attrs['email']).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"email": "이미 사용중인 이메일입니다."})
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.name = validated_data['name']
        instance.nickname = validated_data['nickname']
        instance.birthday = validated_data['birthday']
        instance.gender = validated_data['gender']
        instance.bio = validated_data['bio']
        instance.save()

        return instance


# 로그인 실패시 응답 변경
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id

        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            user = self.user
            data['user_id'] = user.id

        except AuthenticationFailed:
            # 인증 실패 시 커스텀 응답
            raise AuthenticationFailed({
                'error': '아이디 또는 비밀번호가 틀렸습니다.'
            })
        return data


# 비밀번호 변경
class UserChangePasswordSerializer(serializers.Serializer):
    prev_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate_prev_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError({"error": "현재 비밀번호가 일치하지않습니다"})
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "변경할 비밀번호가 서로 일치하지 않습니다"})
        if attrs["prev_password"] == attrs["password"]:
            raise serializers.ValidationError(
                {"password": "기존비밀번호와 일치합니다."}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
