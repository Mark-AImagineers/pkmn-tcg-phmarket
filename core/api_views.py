from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView


User = get_user_model()


class SendTestEmailAPIView(APIView):
    """Send a test email after verifying the superuser password."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user: User = request.user
        password = request.data.get("password")

        if not user.is_superuser:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        if not password or not user.check_password(password):
            return Response(
                {"detail": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )

        send_mail(
            subject="PrivateEmail App Password Test",
            message="This message confirms the app password works.",
            from_email=None,
            recipient_list=["markb@aimagineers.io"],
            fail_silently=False,
        )
        return Response({"detail": "Email sent"})
