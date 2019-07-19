from django.contrib.auth.models import User
from rest_framework.parsers import FileUploadParser
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response

from accounts.models import Department
from accounts.serializers import DepartmentSerializer
from internship.models import Enterprise

from .models import Framer, Promotion, Student, Teacher, Classroom, Task, Project, Skill
from .serializers import (FramerSerializer, LoginSerializer,
                          PromotionSerializer, RegisterSerializer,
                          StudentSerializer, TeacherSerializer, UserSerializer, ClassroomSerializer, TaskSerializer, SkillSerializer, ProjectSerializer)


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
            enterprise = Enterprise.objects.get(id=request.data['enterprise'])
            Framer.objects.create(user=user, first_name=first_name,
                                  last_name=last_name, phone=phone, image=image, enterprise=enterprise)

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
    parser_class = (FileUploadParser,)

    def update(self, request, pk):
        student = Student.objects.get(id=pk)
        if 'skills' in request.data:
            skills_id = request.data['skills']
            skills = []
            for id in skills_id:
                skills.append(Skill.objects.get(id=id))

            student.skills.add(*skills)

        if 'skill' in request.data:

            skill_id = request.data['skill']
            skill = Skill.objects.get(id=skill_id)
            student.skills.remove(skill)

        if 'first_name' in request.data:
            student.first_name = request.data["first_name"]
        if 'last_name' in request.data:
            student.last_name = request.data["last_name"]
        if 'image' in request.data:
            if request.data['image'] != 'undefined':
                student.image = request.data['image']
        if 'phone' in request.data:
            student.phone = request.data["phone"]
        if 'gender' in request.data:
            student.gender = request.data["gender"]
        if 'socialStatus' in request.data:
            student.socialStatus = request.data["socialStatus"]
        if 'address' in request.data:
            student.address = request.data["address"]
        student.save()

        return Response(StudentSerializer(student).data)


class TeacherAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class FramerAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Framer.objects.all()
    serializer_class = FramerSerializer


class PromotionAPI(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Promotion.objects.all().order_by('-id')
    serializer_class = PromotionSerializer


class ClassroomAPI(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('-id')
    serializer_class = SkillSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    
    def create(self, request):
        title = request.data['title']
        description = request.data['description']
        framer = Framer.objects.get(id=request.data['framer'])
        task = Task.objects.create(
            title=title, description=description, framer=framer)
        
        if 'project' in request.data:
            project = Project.objects.get(id=request.data['project']) 
            task.project = project
        if 'starting_time' in request.data:
            task.starting_time = request.data['starting_time']
        if 'finish_time' in request.data :
            task.finish_time = request.data['finish_time']
            
        task.save()

        for id in request.data['students']:
            task.students.add(Student.objects.get(id=id))

        return Response(TaskSerializer(task).data)

    def update(self, request, pk):
        task = Task.objects.get(id=pk)
        state = request.data['state']
        task.state = state 
        task.save()
        
        return Response(TaskSerializer(task).data)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-id')
    serializer_class = ProjectSerializer

    def create(self, request):
        name = request.data['name']
        description = request.data['description']
        aim = request.data['aim']        
        enterprise = Enterprise.objects.get(id=request.data['enterprise']) 
        framer = Framer.objects.get(id=request.data['framer'])
        pro = Project.objects.create(
            name=name, description=description, aim=aim, framer=framer, enterprise=enterprise)
        
        
                 
        if 'starting_time' in request.data:
            pro.starting_time = request.data['starting_time']
        if 'finish_time' in request.data :
            pro.finish_time = request.data['finish_time']

        pro.save()

        for id in request.data['students']:
            pro.students.add(Student.objects.get(id=id))

        return Response(ProjectSerializer(pro).data)
