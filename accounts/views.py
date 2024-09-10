from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegisterSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer, UserChangePasswordSerializer
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError


# 로그인시 응답 수정
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 회원가입 클래스
class UserRegisterationView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]
    # 회원가입
    # - **조건**: username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
    # - **검증**: username과 이메일은 유일해야 하며, 이메일 중복 검증(선택 기능).
    # - **구현**: 데이터 검증 후 저장.

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "회원가입이 성공적으로 이루어졌습니다.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.name,
                    "date_joined": user.date_joined}, "refresh": str(refresh),
                "access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED)

    # 회원탈퇴
    # - **조건**: 로그인 상태, 비밀번호 재입력 필요.
    # - **검증**: 입력된 비밀번호가 기존 비밀번호와 일치해야 함.
    # - **구현**: 비밀번호 확인 후 계정 삭제.
    def delete(self, request):
        user = request.user
        password = request.data.get('password')
        if user.check_password(password):
            # 회원탈퇴시 해당 유저의 모든 토큰에대한 블랙리스트 추가
            try:
                for token in user.outstandingtoken_set.all():
                    try:
                        RefreshToken(token.token).blacklist()
                    except TokenError:
                        pass
                user.delete()
                return Response({"message": "계정이 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"message": f"계정 삭제 중 오류가 발생했습니다.: {str(e)}"})
        else:
            return Response({"message": "비밀번호가 일치하지 않습니다."}, status = status.HTTP_401_UNAUTHORIZED)

# - **조건**: 로그인 상태 필요.
# - **구현**: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    # - **조건**: 로그인 상태 필요.
    # - **구현**: 토큰 무효화 또는 다른 방법으로 로그아웃 처리 가능.
    # 회원 로그아웃

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃 성공"})
        except Exception as e:
            return Response({"error": str(e)})


# 프로필 클래스
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    # - **조건**: 로그인 상태 필요.
    # - **검증**: 로그인 한 사용자만 프로필 조회 가능
    # - **구현**: 로그인한 사용자의 정보를 JSON 형태로 반환.
    # 프로필 확인
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        serializer = UserRegisterSerializer(user)
        if request.user == user:  # 다른 사용자의 프로필
            return Response(serializer.data)
        else:
            return Response({"message": "해당 프로필을 볼 권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)

# - **조건**: 이메일, 이름, 닉네임, 생일 입력 필요하며, 성별, 자기소개 생략 가능
# - **검증**: 로그인 한 사용자만 본인 프로필 수정 가능. 수정된 이메일은 기존 다른 사용자의 이메일과 username은 중복되면 안 됨.
# - **구현**: 입력된 정보를 검증 후 데이터베이스를 업데이트.
    # 회원 정보 수정
    def put(self, request, username):
        user = request.user
        if user.username != username:
            return Response({"error": "수정할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):

            serializer.save()
            return Response(serializer.data)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
# - 조건: 기존 패스워드와 변경할 패스워드는 상이해야 함
# - 검증: 패스워드 규칙 검증
# - 구현: 패스워드 검증 후 데이터베이스에 업데이트.
    # 유저 비밀번호 변경

    def put(self, request):

        serializer = UserChangePasswordSerializer(instance=request.user,
                                                  data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "비밀번호 변경 완료"})
