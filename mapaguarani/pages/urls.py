from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register(r'', views.FlatpageViewSet, base_name='flatpage')

urlpatterns = []

urlpatterns.extend(router.urls)
