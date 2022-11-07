from django.urls import include,path
from rest_framework import routers
from .views import SignupViewSet, LoginView,MessageView



router = routers.DefaultRouter()
router.register('signup', SignupViewSet),

urlpatterns = [
    path('', include(router.urls)),
    path('login/',LoginView.as_view(),name='login'),
    path('message/', MessageView.as_view())

]
