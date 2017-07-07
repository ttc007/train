from push_notifications.models import APNSDevice, GCMDevice

def send_notification_all_user(subject, message, **kwargs):
    try:
        print "CALL Signal "
        data_notify = {"title": subject, "body" : message}
        for name, value in kwargs.items():
            data_notify[name] = value
        
        devices_ios = APNSDevice.objects.filter(user__flag_notification=True)
        devices_ios.send_message(message=data_notify, extra=data_notify)

        fcm_devices = GCMDevice.objects.filter(user__flag_notification=True)
        fcm_devices.send_message(subject, extra=data_notify)
        return True
    except Exception, e:
        print "Error send_notification_all_user : ",e
        return False