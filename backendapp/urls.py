from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    
    path('api/products/',product_handlerapi.as_view()),
     path('api/products/<int:productid>/',product_handlerapi.as_view()),
      path('api/category/', ProductCategoryAPI.as_view()),
      path('api/signup/',signupapi.as_view()),
      path('api/login/',loginapi.as_view()),
      path('api/order/',orderapi.as_view()),
      path('api/order/<int:pk>/', orderapi.as_view()),
    # JWT token URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #   path('api/orderproduct/',orderproductapi.as_view())
]