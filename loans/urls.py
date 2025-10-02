from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'loans', views.LoanViewSet, basename='loan')

# Web URL patterns
web_urlpatterns = [
    path('apply/', views.loan_apply_view, name='loan_apply'),
    path('list/', views.loan_list_view, name='loan_list'),
    path('<int:pk>/', views.loan_detail_view, name='loan_detail'),
]

# API URL patterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('', include(web_urlpatterns)),
]
