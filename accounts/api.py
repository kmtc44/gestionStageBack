from django.contrib.auth.models import User
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from accounts.models import Department
from accounts.serializers import DepartmentSerializer

from .models import Framer, Promotion, Student, Teacher
from .serializers import (FramerSerializer, LoginSerializer,
                          PromotionSerializer, RegisterSerializer,
                          StudentSerializer, TeacherSerializer, UserSerializer)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        first_name = request.data['firstname']
        last_name = request.data['lastname']
        phone = request.data["phone"]
        if request.data['status'] == 'student':
            department_name = request.data['department']
            department = Department.objects.get(name=department_name)
            classe = request.data['classe']
            promo = Promotion.objects.create(
                name=request.data['promotion']+"eme promo")
            user = serializer.save()
            Student.objects.create(user=user, promotion=promo, first_name=first_name,
                                   last_name=last_name, department=department, classe=classe, phone=phone)

        elif request.data['status'] == 'teacher':
            department_name = request.data['department']
            department = Department.objects.get(name=department_name)
            user = serializer.save()
            Teacher.objects.create(user=user, first_name=first_name,
                                   last_name=last_name, department=department, phone=phone)

        elif request.data['status'] == 'framer':
            user = serializer.save()
            Framer.objects.create(user=user, first_name=first_name,
                                  last_name=last_name, phone=phone)

        user.save()
        print("Authtoken values : ", AuthToken.objects.create(user))
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]

    def post(self, request, *args, **kwargs):
        print((request.data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UsersAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = User.objects.all()


class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user


class DepartmentAPI(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]


class StudentAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class FramerAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Framer.objects.all()
    serializer_class = FramerSerializer


class PromotionAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
