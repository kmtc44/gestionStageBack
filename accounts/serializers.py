from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


# from internship.serializers import EnterpriseSerializers
from internship.models import Enterprise

<<<<<<< HEAD
from .models import Framer, Promotion, Student, Teacher, Department, Classroom, Task, Project, Skill, Attachments
=======
from .models import (
    Framer, 
    Promotion, 
    Student, 
    Teacher, 
    Department, 
    Classroom, 
    Task, 
    Project, 
    Skill,
    Comment
)

>>>>>>> 83f89c3a182e50afc7d97ac8675ef354911f97b4

# serializer that are not use directy but allow inly for nested data

# serializer for the  student in nested skills  or other
class SSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

# the serializer for nested project in the real student serializer


class ProjSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'aim')


class SkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ('id', 'name', 'students')

# serializer for the enterprise


class EnterpriseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'
# classroom for student


class CRSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = ('id', 'name')

class PromoSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Promotion
        fields = ('id', 'name')
# real serializer  that are used buy the api view to serve or receive data


# User serializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'student')

# Register Serializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user

# login


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")


# the department serializer for the different department or ginus in the school
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# serialzer for the skills of students and students that have a skill
class SkillSerializer(serializers.ModelSerializer):
    students = SSerializer(many=True, read_only=True)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'students')


class AttachmentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attachments
        fields = '__all__' 

class StudentSerializer(serializers.ModelSerializer):
    skills = SkSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    enterprise = EnterpriseSerializers(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)
    projects = ProjSerializer(many=True, read_only=True)
    classroom = CRSerializer(many=False, read_only=True)
<<<<<<< HEAD
    attachments = AttachmentsSerializer(many=False, read_only=True)
=======
    promotion = PromoSerializer(many=False, read_only=True)
>>>>>>> 83f89c3a182e50afc7d97ac8675ef354911f97b4

    class Meta:
        model = Student
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'


class FramerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    enterprise = EnterpriseSerializers(many=False, read_only=True)

    class Meta:
        model = Framer
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Promotion
        fields = ('id', 'name', 'students')


class UserSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)
    teacher = TeacherSerializer(many=False, read_only=True)
    framer = FramerSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'student', 'teacher', 'framer')


class ClassroomSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ('id', 'name', 'students')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Comment 
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    students = SSerializer(many=True, read_only=True)
    framer = FramerSerializer(many=False, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

<<<<<<< HEAD
=======

>>>>>>> 83f89c3a182e50afc7d97ac8675ef354911f97b4
