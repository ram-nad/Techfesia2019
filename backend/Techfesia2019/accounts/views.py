from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.utils import account_activation_token, send_account_activation_email
from registration.permissions import SelfOrStaff
from registration.models import User


class EmailConfirmed(APIView):
    """
        Deals with email confirmation of a user
    """

    permission_classes = (IsAuthenticated, SelfOrStaff)

    def get(self, request, username):
        """
            return True if email
        """

        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)

        return Response(status=status.HTTP_200_OK, data={"email_confirmed": user.email_confirmed})


    def post(self, request, username):
        """
            Send account activation email to user
        """

        permission_classes = (IsAuthenticated, SelfOrStaff)

        user = get_object_or_404(User, username=username)
        self.check_object_permissions(request, user)

        if user.email_confirmed:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={"message":"Your account email is already confirmed"})

        send_account_activation_email(request, user)
        return Response(status=status.HTTP_200_OK, data={"message":"Account Confirmation email will be sent shortly "})



def activate(request, username, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        return HttpResponse("Your email was successfully confirmed. You may go ahead and login now")
    else:
        return HttpResponse("Invalid token!")
