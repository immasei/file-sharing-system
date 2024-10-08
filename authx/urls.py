from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('', Home.as_view()),

    # rest apis
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'), 

    # path('login/', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register')

    # html apis
]

# default TokenObtainPairView -> auth user (username, password)
# custom views.MyTokenObtainPairView -> edit-add fields (ie email, password)
# both class & func based api
# https://dev.to/ki3ani/implementing-jwt-authentication-and-user-profile-with-django-rest-api-part-3-3dh9

# default jwt
# restricted view, cannot access view without being authenticated
# https://plainenglish.io/blog/how-to-implement-user-login-with-jwt-authentication-in-django-rest-framework