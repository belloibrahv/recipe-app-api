"""
Mapping url for the user API.
"""

from django.urls import path

from user.views import (CreateUserView, AuthTokenView, ManageUserView)

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', AuthTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
