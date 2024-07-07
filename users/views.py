from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import parsers, renderers, status
from users.models import User, VerificationCode
from users.serializers import UserSerializer, ProfilePictureSerializer, AuthTokenSerializer
from users.custom_renderers import ImageRenderer
import jwt, datetime
import random


class LoginView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            token = jwt.encode({
                'email': serializer.validated_data['email'],
                'iat': datetime.datetime.now(datetime.timezone.utc),
                'nbf': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=-5),
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            }, settings.SECRET_KEY, algorithm='HS256')
            return Response({'token': token})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView): 
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            instance.set_password(request.data['password'])
            instance.save()
            return Response({'email': request.data['email']})
        print(serializer.errors)
        return Response(serializer.errors, status=500)

class ForgetPasswordView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data.get('email')).first()
        if not user:
            return Response({'error': 'There is no user with such email'}, status=400)
        code = ''.join([str(random.choice(range(10))) for i in range(5)])
        verificationCode = VerificationCode(code=code, user=user, password=request.data.get('password'))
        verificationCode.save()
        subject = 'Sara\'s Password Reset'
        message = f'Hi {user.first_name} {user.last_name} , you have requested to reset your password, your verification code is: {code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = (user.email,)
        send_mail( subject, message, email_from, recipient_list )
        return Response({'email': user.email})


class ForgetPassowrdVerificationView(APIView):  
    def post(self, request):
        code = request.data['code'] 
        user = User.objects.filter(email=request.data['email']).first()
        user_code = VerificationCode.objects.filter(user=user.id).first()
        print(user_code.code)
        print(code)
        print(user_code.user.email, user.email)
        if code == user_code.code:
            
            user.set_password(user_code.password)
            user.save()
            user_code.delete()
            return Response({'email': user.email})
        return Response({'error': 'Can\'t verify user'}, status=400)


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user_data = dict(UserSerializer(instance=user).data)
        try:
            user_data.pop('password')
        except: pass
        return Response(data=user_data)
    def put(self, request):
        user = request.user
        data = {}
        for key in request.data:
            if key in ['email', 'gender', 'age']:
                data[key] = request.data[key]
            if key == 'name':
                data['first_name'] = request.data[key].split()[0]
                data['last_name'] = request.data[key].split()[1]
        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=500)


class ProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    renderers_classes = [ImageRenderer]
    def post(self, request):
        user = request.user
        serializer = ProfilePictureSerializer(instance=user, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=500)
    
    def get(self, request):
        data = User.objects.get(id=request.user.id).picture
        return HttpResponse(data, content_type='image/' + data.path.split(".")[-1])
