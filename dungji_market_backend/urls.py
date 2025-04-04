"""
URL configuration for dungji_market_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    CategoryViewSet, ProductViewSet, GroupBuyViewSet,
    ParticipationViewSet, register_user, create_sns_user,
    UserProfileView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('groupbuys', GroupBuyViewSet)
router.register('participations', ParticipationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include([
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('register/', register_user, name='register'),
        path('sns-login/', create_sns_user, name='sns_login'),
        path('profile/', UserProfileView.as_view(), name='profile'),
    ])),
    path('api/', include(router.urls)),
]