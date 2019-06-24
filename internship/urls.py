# from django.urls import path

# from .views import EnterpriseListView, EnterpriseDetailView, EnterpriseListCreateView

# urlpatterns = [
#     path('enterprise/', EnterpriseListCreateView.as_view()),
#     path('enterprise/', EnterpriseListView.as_view()),
#     path('enterprise/<pk>/', EnterpriseDetailView.as_view())
# ]

from rest_framework import routers
from .api import EnterpriseViewSet

router = routers.DefaultRouter()
router.register('enterprise', EnterpriseViewSet, 'enterprise')

urlpatterns = router.urls
