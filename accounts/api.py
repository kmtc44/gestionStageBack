from django.contrib.auth.models import User
from rest_framework.parsers import FileUploadParser
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from accounts.models import Department
from accounts.serializers import DepartmentSerializer

from .models import Framer, Promotion, Student, Teacher, Classroom, Task, Project
from .serializers import (FramerSerializer, LoginSerializer,
                          PromotionSerializer, RegisterSerializer,
                          StudentSerializer, TeacherSerializer, UserSerializer, ClassroomSerializer, TaskSerializer, ProjectSerializer)


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    parser_class = (FileUploadParser,)
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
        email = request.data["email"]
        try:
            User.objects.get(email=email)
            return Response({
                "error": "email deja utilise"
            })
        except:
            pass
        image = ''
        try:
            image = request.data["image"]
        except:
            pass
        if request.data['status'] == 'student':
            department_name = request.data['department']
            birthday = request.data['birthday']
            department = Department.objects.get(name=department_name)
            classroom = Classroom.objects.get(name=request.data['classe'])
            promo = Promotion.objects.get(
                name=request.data['promotion'])
            user = serializer.save()
            Student.objects.create(user=user, promotion=promo, first_name=first_name,
                                   last_name=last_name, department=department, classroom=classroom, phone=phone, image=image, birthday=birthday)

        elif request.data['status'] == 'teacher':
            department_name = request.data['department']
            department = Department.objects.get(name=department_name)
            user = serializer.save()
            Teacher.objects.create(user=user, first_name=first_name,
                                   last_name=last_name, department=department, phone=phone, image=image)

        elif request.data['status'] == 'framer':
            user = serializer.save()
            Framer.objects.create(user=user, first_name=first_name,
                                  last_name=last_name, phone=phone, image=image)

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


class StudentAPI(viewsets.ModelViewSet):
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


class PromotionAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class ClassroomAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
