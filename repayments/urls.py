from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepaymentViewSet

router = DefaultRouter()
router.register(r'', RepaymentViewSet, basename='repayment')

urlpatterns = [
    path('', include(router.urls)),
]
