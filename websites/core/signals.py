from django.db.models.signals import post_save
from models import Notification, User_Notification
from custom_models import User
import push_notification


def bulk_user_notifications(sender, instance, created, **kwargs):
    try:
        if created:
            users = User.objects.filter(is_active=True)
            objs = [User_Notification(notification=instance, user=u) for u in users]
            User_Notification.objects.bulk_create(objs)
            push_notification.send_notification_all_user(subject=instance.subject, message=instance.message, sub_url=instance.sub_url, image=instance.image.url)
    except Exception, e:
        print "Error bulk_user_notifications : ",e
        raise Exception("Error. Cannot insert bulk user notifications.")

post_save.connect(bulk_user_notifications, sender=Notification)


# def insert_user_pns(sender, instance, created, **kwargs):
#     try:
#         if created and instance.device_uid:
#             if instance.device_type == 'ios':
#                 try:
#                     device = APNSDevice.objects.get(registration_id=instance.device_uid)
#                     device.user = instance
#                     device.save()

#                 except APNSDevice.DoesNotExist, e:
#                     device = APNSDevice(user=instance, name=instance.email, registration_id=instance.device_uid)
#                     device.save()
#             else:
#                 device = GCMDevice(user=instance, name=instance.email, registration_id=instance.device_uid, cloud_message_type="FCM")
#                 device.save()

#     except Exception, e:
#         print "Error insert_user_pns : ",e
#         raise Exception("Error. Cannot insert insert user push notification.")

# post_save.connect(insert_user_pns, sender=User)