from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, UserSerializer


class RegistrationAPIView(APIView):
    """API endpoint for user registration."""

    permission_classes: list = []

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeAPIView(APIView):
    """Return details for the authenticated user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
