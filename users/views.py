from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.contrib.auth import aauthenticate
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self , request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response({"detail":"Wrong old password"},status=400)
        
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status=204)


class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class ResetPasswordRequestView(APIView):
    def post(self , request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail":"Password reset link sent(mock)"} , status=200)


class ResetPasswordConfirmView(APIView):
    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.first()
            user.set_password(serializer.validated_data["new_password"])
            user.save()
        except ObjectDoesNotExist:
            pass
        return Response({"detail":"Password reset successful"}, status=200)