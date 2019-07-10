from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


# from internship.serializers import EnterpriseSerializers

from .models import Framer, Promotion, Student, Teacher, Department, Classroom, Skill

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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill 
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    # enterprise = EnterpriseSerializers(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Student
        fields = '__all__'



class TeacherSerializer(serializers.ModelSerializer):
    # user = UserSerializer(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'


class FramerSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    # enterprise = EnterpriseSerializers(many=False, read_only=True)

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


