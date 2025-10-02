from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.RepaymentViewSet, basename='repayment')

# Web URL patterns
web_urlpatterns = [
    path('make/<int:loan_id>/', views.repayment_make_view, name='repayment_make'),
    path('history/', views.repayment_history_view, name='repayment_history'),
    path('success/<int:payment_id>/', views.repayment_success_view, name='repayment_success'),
]

# API URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('', include(web_urlpatterns)),
]
