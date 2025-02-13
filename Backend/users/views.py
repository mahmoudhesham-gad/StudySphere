from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from . import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
import logging 


# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        # Validate and create the new user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate token pair for the newly created user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'user': user.id,
        }
        response = Response(response_data, status=status.HTTP_201_CREATED)

        # Set tokens as HttpOnly cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,      
            samesite='Lax'     
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response

class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'user': user.id,
        }
        response = Response(response_data, status=status.HTTP_200_OK)

        # Set tokens as HttpOnly cookies
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
        Handles user logout by blacklisting the refresh token and clearing cookies.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        print(refresh_token)
        if not refresh_token:
            return Response(
                {"error": "No refresh token found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {"error": "An error occurred while logging out"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(
            {"message": "Logged out successfully"},
            status=status.HTTP_205_RESET_CONTENT
        )
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response

class VerifyTokenView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
        Handles token verification.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "No refresh token found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.check_blacklist()
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {"error": "An error occurred while verifying the token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Token is valid"},
            status=status.HTTP_200_OK
        )
    
class RefreshTokenView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """
        Handles token refresh.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"error": "No refresh token found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {"error": "An error occurred while refreshing the token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = Response(
            status=status.HTTP_200_OK
        )
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response