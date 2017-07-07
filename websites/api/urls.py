from django.conf.urls import url, include
from api import views

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    url(r'^hots/$', views.hots, name="get-hosts"),
    url(r'^games/$', views.games, name="get-games"),
    url(r'^games/(?P<game_id>[0-9]+)/detail/$', views.game_detail, name="get-game-detail"),
    url(r'^games/types/categories/(?P<category_id>[0-9]+)/$', views.game_types_by_category, name="get-game-types"),
    url(r'^entertainments/(?P<id_or_key_query>[\w\+%_&]+)/detail/$', views.entertainment_detail, name="get-entertaiments-detail"),
    url(r'^events/$', views.events, name="get-events"),
    url(r'^events/latest/$', views.events_latest, name="get-events-latest"),
    url(r'^events/(?P<event_id>[0-9]+)/detail/$', views.event_detail, name="get-events-detail"),
    url(r'^posts/$', views.posts, name="get-posts"),
    url(r'^posts/(?P<id_or_key_query>[\w\+%_&]+)/detail/$', views.post_detail, name="get-posts-detail"),
    url(r'^promotions/$', views.promotions, name="get-promotions"),
    url(r'^promotions/(?P<promotion_id>[0-9]+)/detail/$', views.promotion_detail, name="get-promotions-detail"),
    url(r'^transaction/filter/$', views.transactions_type, name="get-transactions-filter"),
    url(r'^faqs/$', views.faqs),

    url(r'^accounts/verify/email/$', views.verify_email, name="verify-email"),
    url(r'^accounts/registrations/$',
        views.RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/reset/password/$', views.reset_password, name="reset-password"),
    url(r'^accounts/$', views.user_info, name="update-account"),
    url(r'^accounts/password/$', views.change_password, name="update-account-password"),
    url(r'^accounts/feedback/$', views.send_feedback, name="accounts-feedback"),
    url(r'^accounts/users/$', views.users, name="accounts-users-info"),
    url(r'^device/connect/$', views.connect_device, name="connect-device-user"),
    url(r'^device/disconnect/$', views.disconnect_device, name="disconnect-device-user"),
    
    url(r'^accounts/login/$', obtain_jwt_token, name="accounts-login"),
    # Social Login : alias name url is : login_social_jwt_user and url is : api/login/social/jwt_user/
    url(r'^login/', include('rest_social_auth.urls_jwt')),
    url(r'^accounts/facebook/deviceuid/$', views.update_unique_device_id, name="update-unique-device-id"),
    # url(r'^api-token-verify/', verify_jwt_token),
    url(r'^accounts/upload/avatar/(?P<filename>[^/]+)$', views.FileUploadView.as_view(), name="upload-avatar"),

    url(r'^card/(?P<card_id>[0-9]+)/information/$', views.card_information, name="card-information"),
    url(r'^transactions/play/$', views.play_transactions, name="play-transactions"),
    url(r'^transactions/card/$', views.card_transactions, name="card-transactions"),
    url(r'^reissue/history/$', views.reissue_history, name="reissue-history"),
    url(r'^open/time/$', views.open_time, name="open-time"),
    url(r'^promotion/gift/$', views.gift_user, name="gift-user"),
    # url(r'^promotion/gift/install/app/$', views.gift_install_app, name="gift-install-app"),
    
    url(r'^notifications/$', views.notifications, name="notification-category"),
    url(r'^notification/new/$', views.add_notification, name="add-notification"),
    url(r'^notification/category/$', views.notification_category, name="notifications"),
    url(r'^notification/read/$', views.user_read_notification, name="notification-read"),
    url(r'^notification/off/$', views.turn_off_notification, name="turn-off-notification"),
    url(r'^notification/on/$', views.turn_on_notification, name="turn-on-notification"),
    url(r'^notification/(?P<notification_id>[0-9]+)/detail/$', views.notification_detail, name="get-notification-detail"),
    url(r'^notification/push/$', views.send_notification, name="push-notification"),
    

]
