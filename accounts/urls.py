from django.urls import include, path
from knox import views as knox_views
from rest_framework import routers


from .api import (ClassroomAPI, FramerAPI, LoginAPI, ProjectViewSet,
                  PromotionAPI, RegisterAPI, SkillViewSet, StudentAPI,
                  TaskViewSet, TeacherAPI, UserAPI, UsersAPI, CommentViewSet, DepartmentAPI)

router = routers.DefaultRouter()
router.register('students', StudentAPI, 'student')
router.register('teachers', TeacherAPI, 'teacher')
router.register('framers', FramerAPI, 'framer')

router.register('skills',SkillViewSet , 'skills')

router.register('classroom', ClassroomAPI, 'classroom')
router.register('task', TaskViewSet, 'task')
router.register('project', ProjectViewSet, 'project')
router.register('comments', CommentViewSet, 'comments')



urlpatterns = [
    path('auth', include('knox.urls')),
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/users', UsersAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
    # path('teachers', TeacherAPI.as_view()),
    # path('framers', FramerAPI.as_view()),
    path('promos', PromotionAPI.as_view()),
    path('department', DepartmentAPI.as_view()),
    # path('classroom', ClassroomAPI.as_view()),
] + router.urls
