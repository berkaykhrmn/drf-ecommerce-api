from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth.models import User
from . import serializers as user_serializers

class LogoutSerializer(serializers.Serializer):
    pass

@extend_schema_view(
    post=extend_schema(
        summary="User Registration",
        description="Allows anyone to create a new user account. Returns user details upon successful registration.",
        tags=["Authentication"],
    )
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema_view(
    post=extend_schema(
        summary="User Login",
        description="Authenticates a user with username and password. Returns user information along with refresh and access JWT tokens.",
        tags=["Authentication"],
    )
)
class LoginView(generics.GenericAPIView):
    serializer_class = user_serializers.LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'refresh': serializer.validated_data['refresh'],
            'access': serializer.validated_data['access'],
        }, status=status.HTTP_200_OK)

@extend_schema(
    summary="User Logout",
    description="Invalidates the current session/token on the client side. Requires authentication.",
    tags=["Authentication"],
    responses={200: OpenApiTypes.OBJECT},
)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )

@extend_schema_view(
    put=extend_schema(
        summary="Update User Profile",
        description="Allows authenticated users to fully update their own profile information (e.g., username, email, etc.).",
        tags=["Authentication"],
    ),
    patch=extend_schema(
        summary="Partial Update User Profile",
        description="Allows authenticated users to partially update their own profile information.",
        tags=["Authentication"],
    ),
)
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = user_serializers.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema_view(
    post=extend_schema(
        summary="Change Password",
        description="Allows authenticated users to change their password by providing the old password and a new one.",
        tags=["Authentication"],
    )
)
class ChangePasswordView(generics.GenericAPIView):
    serializer_class = user_serializers.ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )