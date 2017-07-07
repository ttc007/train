from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from core.models import *
from django.contrib.auth import get_user_model
from message_custom import SetCustomErrorMessagesMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


User = get_user_model()


class UserSerializer(SetCustomErrorMessagesMixin, serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(
        max_length=255, required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(
        max_length=255, required=False, allow_null=True, allow_blank=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    phone = serializers.CharField(
        max_length=50, required=False, allow_null=True, allow_blank=True)
    personal_id = serializers.CharField(
        max_length=50, required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)
    device_unique = serializers.CharField(max_length=255)
    # device_type = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    avatar = serializers.ImageField(
        max_length=1000, allow_null=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'birth_date', 'phone',
                  'personal_id', 'country', 'address', 'city', 'avatar', 'is_staff', 'device_unique')
        custom_error_messages_for_validators = {
            'email': {
                UniqueValidator: _('This email is already taken. Please, try again')
            }
        }
        extra_kwargs = {"username": {"error_messages": {
                                        "required": _("This field may not be blank.")
                                        }
                                    }
                }

    def create(self, validated_data):
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=username, email=email, password=password, **validated_data)
        return user


class HotsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    sub_url = serializers.CharField(max_length=1000)
    image = serializers.ImageField(max_length=1000)
    is_show = serializers.BooleanField()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()


class TypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    category = CategorySerializer(many=False)


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    short_description = serializers.CharField()
    image = serializers.ImageField(max_length=1000)
    game_type = TypeSerializer(many=False)


class GameDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    short_description = serializers.CharField()
    content = serializers.CharField()
    image = serializers.ImageField(max_length=1000)


class FAQsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question = serializers.CharField(max_length=255)
    answer = serializers.CharField()
    category = CategorySerializer(many=False)


class EntertainmentDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=2000)
    short_description = serializers.CharField()
    content = serializers.CharField()
    image1 = serializers.ImageField(max_length=1000)
    image2 = serializers.ImageField(max_length=1000)
    image3 = serializers.ImageField(max_length=1000)
    image4 = serializers.ImageField(max_length=1000)
    image5 = serializers.ImageField(max_length=1000)
    image6 = serializers.ImageField(max_length=1000)
    category = CategorySerializer(many=False)


class EventsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    image = serializers.ImageField(max_length=1000)
    short_description = serializers.CharField(max_length=350)
    content = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    url_share = serializers.SerializerMethodField()

    def get_url_share(self, obj):
        url = reverse("get-events-detail", args=[obj.id])
        url = url.replace("api/", "")
        return url


class PostTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()


class PostImageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField(max_length=1000)


class PostsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    key_query = serializers.CharField(max_length=255)
    image = serializers.ImageField(max_length=1000)
    short_description = serializers.CharField(max_length=350)
    content = serializers.CharField()
    posts_image = PostImageSerializer(many=True)
    post_type = PostTypeSerializer(many=False)


class PromotionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    short_description = serializers.CharField(max_length=350)
    content = serializers.CharField()
    image = serializers.ImageField(max_length=1000)
    promotion_category = CategorySerializer(many=False)
    url_share = serializers.SerializerMethodField()

    def get_url_share(self, obj):
        url = reverse("get-promotions-detail", args=[obj.id])
        url = url.replace("api/", "")
        return url


class TransactionTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)


class FeedBackSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=500)
    email = serializers.EmailField(max_length=500)
    phone = serializers.CharField(
        max_length=500, required=False, allow_null=True, allow_blank=True)
    subject = serializers.CharField(max_length=500)
    message = serializers.CharField()
    rate = serializers.CharField(
        max_length=500, required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        fb = FeedBack.objects.create(**validated_data)
        return fb


class OpenTimeSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    open_date = serializers.DateField(allow_null=True)
    start_time = serializers.TimeField(allow_null=True)
    end_time = serializers.TimeField(allow_null=True)


class CategoryNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category_Notification
        fields = ('id', 'name')


class NotificationSerializer(serializers.ModelSerializer):
    category = CategoryNotificationSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'subject', 'message', 'sub_url', 'category', 'image')


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = User_Notification
        fields = ('user', 'notification', 'is_read',)
