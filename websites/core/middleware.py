# # -*- coding: utf-8 -*-
# from social_django.middleware import SocialAuthExceptionMiddleware
# from social_django.exceptions import AuthFailed
# from django.contrib import messages

# class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):

#     def get_message(self, request, exception):
#         msg = None
#         if (isinstance(exception, AuthFailed):
#             msg =   u"Not in whitelist" 
#         else:
#             msg =   u"Some other problem"    
#         messages.add_message(request, messages.ERROR, msg) 