from django.utils import translation
from django.conf import settings
from core.models import Advertisement, Post
import core.constants as const

# class SetLocaleMiddleware:
#     def set_language(request):
#         response = http.HttpResponseRedirect(next)
#         if request.method == 'GET':
#             lang_code = request.GET.get('language', None)
#             if lang_code and check_for_language(lang_code):
#                 if hasattr(request, 'session'):
#                     request.session['django_language'] = lang_code
#                 else:
#                     response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
#                 translation.activate(lang_code)
#         return response



def set_language_code(request):
    LANGUAGE_CODE = ''
    try:
        LANGUAGE_CODE = request.session["_language"]
    except:
        pass
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'LANGUAGE_CODE': LANGUAGE_CODE}


def get_app_fb_id(request):
    FB_APP_ID = ''
    try:
        FB_APP_ID = settings.FB_APP_ID
    except:
        pass
    return {'FB_APP_ID': FB_APP_ID}

def get_advertisement(request):
    advertisements = {}
    try:
        advertisements = Advertisement.objects.filter(is_show=True)
    except:
        pass
    return {'advertisements': advertisements}

def get_time_active(request):
    time_active = {}
    try:
        time_active = Post.objects.get(key_query=const.TIME_ACTIVE_KEY_QUERY)
        print time_active
    except Exception, e:
        print e
    return {'time_active': time_active}
