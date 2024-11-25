
# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model

# class CustomAuthenticationBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = get_user_model().objects.get(username=username)
#             if user.check_password(password):
#                 return user
#         except get_user_model().DoesNotExist:
#             return None
