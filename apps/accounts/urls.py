from django.urls import path
from .views import edit_profile_settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('edit-profile-settings', edit_profile_settings, name='edit_profile_settings'),

]
