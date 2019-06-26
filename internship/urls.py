from rest_framework import routers
from .api import EnterpriseViewSet

router = routers.DefaultRouter()
router.register('enterprise', EnterpriseViewSet, 'enterprise')

urlpatterns = router.urls
