from __future__ import unicode_literals

from django.apps import AppConfig
# from django.db.models.signals import post_migrate



# custom user related permissions
# def add_user_permissions(sender, **kwargs):
#     from django.contrib.contenttypes.models import ContentType
#     from django.contrib.auth.models import Permission
    
#     ct = ContentType.objects.get(app_label='core', model='user')
#     perm, created = Permission.objects.get_or_create(codename='is_owner_promotion', name='Owner Promotions', content_type=ct)
#     pass

class CoreConfig(AppConfig):
    name = 'core'

    # def ready(self):
        # import signals
    #     post_migrate.connect(add_user_permissions, sender=self)