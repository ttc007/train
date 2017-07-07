from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser, FormParser
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import status
from rest_framework.views import exception_handler, APIView
from rest_framework.response import Response
from rest_framework import generics as drf_generics
from core.models import *
from api.serializers import *
import helper
import ast
import constants
import utils
from django.db import connections
from core import constants as core_constants
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework.permissions import AllowAny
from django.utils.translation import ugettext, ugettext_lazy as _


def custom_exception_handler(exc, context):
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        try:
            message = exc.detail.values()[0][0] if exc.detail else ""
            field = exc.detail.keys()[0] if exc.detail else ""
        except Exception, e:
            print "custom_exception_handler ", e
            message = "errors"
            field = ""

        response.data['code'] = response.status_code
        response.data['message'] = response.data[
            'detail'] if 'detail' in response.data else str(message)
        response.data['fields'] = field
        if 'detail' in response.data:
            del response.data['detail']

    return response

"""
    Create User by Email
"""
User = get_user_model()


class RegistrationView(drf_generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    email_subject_template = 'websites/api/registration/new_user_notification_subject.txt'

    def send_activation_email(self, user):
        data_render = {
            'site': get_current_site(self.request),
            'user': user,
        }
        # Send email welcome
        subject = render_to_string(self.email_subject_template)
        subject = ' '.join(subject.splitlines())

        message_plain = "websites/api/registration/new_user_notification.txt"
        message_html = "websites/api/registration/new_user_notification.html"

        utils.send_mail(subject=subject, message_plain=message_plain, message_html=message_html, email_from=None, email_to=[user.email],
                        data=data_render)

    def create_inactive_user(self, serializer):
        user = serializer.save()
        self.send_activation_email(user)
        return user

    def perform_create(self, serializer):
        user = self.create_inactive_user(serializer)


"""
    Verify emaill address and send secure code to email
"""


@api_view(['POST'])
@permission_classes((AllowAny,))
def verify_email(request):
    try:
        email = request.data.get('email', '')
        if not email:
            error = {
                "code": 400, "message": _("The email field is required."), "fields": "email"}
            return Response(error, status=400)
        user = User.objects.get(email=email)
        user.secure_code()

        # Send email security code to email
        subject = constants.SUBJECT_VERIFY_EMAIL
        message_plain = "websites/api/registration/verify_email.txt"
        message_html = "websites/api/registration/verify_email.html"
        data_render = {
            "code": user.code,
            'email': user.email
        }
        utils.send_mail(subject=subject, message_plain=message_plain, message_html=message_html, email_from=None, email_to=[user.email],
                        data=data_render)

        return Response({"message": _("Send security code to email successfully."), "flag": True})

    except User.DoesNotExist, e:
        error = {"code": 500, "message": _(
            "Email matching query does not exist."), "fields": "", "flag": False}
        return Response(error, status=500)


@api_view(['POST'])
@permission_classes((AllowAny,))
def reset_password(request):
    try:
        email = request.data.get('email', '')
        secure_code = request.data.get('secure_code', '')
        password1 = request.data.get('password1', '')
        password2 = request.data.get('password2', '')

        if not email or not secure_code or not password1 or not password2:
            error = {
                "code": 400, "message": _("Please check required fields : [email, secure_code, password1, password2]"), "fields": ""}
            return Response(error, status=400)
        if password1 != password2:
            error = {"code": 400, "message": _("Password does not match."),
                     "fields": "Password"}
            return Response(error, status=400)

        user = User.objects.get(email=email, code=secure_code)
        user.set_password(password1)
        user.code = None
        user.save()

        return Response({"message": _("Reset Password Successfully."), "flag": True})

    except User.DoesNotExist, e:
        error = {"code": 500, "message": _("The email or secure code matching query does not exist."),
                 "fields": "", "flag": False}
        return Response(error, status=500)


class FileUploadView(APIView):
    parser_classes = (FileUploadParser, MultiPartParser, FormParser)

    def put(self, request, filename, format=None):
        try:
            file_obj = request.data['file']
            user = self.request.user
            user.avatar = file_obj
            user.save()
            return Response({"message": _("Update Avatar Successfully."), "flag": True}, status=204)
        except Exception, e:
            error = {
                "code": 500, "message": _("Upload avatar error. Please contact administartor"), "fields": "avatar", "flag": False}
            return Response(error, status=500)
        # path = '/Users/tiendang/Downloads/testimg.png'
        # with open(path, 'w') as open_file:
        #     for c in file_obj.chunks():
        #         open_file.write(c)
        #         open_file.close()

        # # write image (base64 string encode upload)
        # import base64
        # import json
        # # open_file.write(json.loads(file_obj.file.read())['file1'].decode('base64'))
        # open_file.write(file_obj.file.read())
        # open_file.close()


"""
    Update User Infomation
"""


@api_view(['PUT'])
def user_info(request):
    try:
        # TODO : Check user i not anonymous
        if not request.user.anonymously:
            user = request.user
            user.first_name = request.data.get('first_name', '')
            user.last_name = request.data.get('last_name', '')
            user.birth_date = request.data.get('birth_date', '')
            user.phone = request.data.get('phone', '')
            user.personal_id = request.data.get('personal_id', '')
            user.country = request.data.get('country', '')
            user.address = request.data.get('address', '')
            user.city = request.data.get('city', '')
            user.device_uid = request.data.get('device_uid', '')
            user.save()

        return Response({'flag': True, 'message': _('Update infomation user successfully.')})

    except Exception, e:
        print 'Erro Update user_info ',e
        error = {"code": 500, "message": _("Cannot update infomation user. Please contact administrator."),
                 "fields": "", "flag": False}
        return Response(error, status=500)


"""
    Update unique device id for user register is facebook
"""


@api_view(['PUT'])
def update_unique_device_id(request):
    try:
        # TODO : Check user i not anonymous
        if not request.user.anonymously:
            user = request.user
            user.device_unique = request.data.get('device_unique', '')
            user.save()

        return Response({'flag': True, 'message': _('Update device unique successfully.')})

    except Exception, e:
        print 'update_unique_device_id ',e
        error = {"code": 500, "message": _("Cannot update infomation user. Please contact administrator."),
                 "fields": "", "flag": False}
        return Response(error, status=500)


"""
    Get User Infomation
"""


@api_view(['GET'])
def users(request):
    try:
        email = request.GET.get("email")
        error = helper.is_empty(email)
        if error:
            errors = {"code": 400, "message": "%s" %
                      error, "fields": "email"}
            return Response(errors, status=400)

        # TODO : Check user i not anonymous
        if not request.user.anonymously:
            user = User.objects.get(email=email)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        else:
            return Response({'message': _('Anonymous User Cannot Get User Infomation')}, status=400)

    except User.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "email"}
        return Response(error, status=400)
    except Exception, e:
        print "Error Get User ", e
        error = {"code": 500, "message": _("Internal Server Error. Please contact administrator."),
                 "fields": "", "flag": False}
        return Response(error, status=500)


"""
    Change Password User
"""


@api_view(['PUT'])
def change_password(request):
    try:
        # TODO : Check user i not anonymous
        if not request.user.anonymously:
            old_password = request.data.get('old_password', '')
            new_password = request.data.get('new_password', '')

            if not old_password or not new_password:
                error = {
                    "code": 400, "message": _("Please check required fields : [old_password, new_password]"), "fields": "",
                    "flag": False}
                return Response(error, status=400)

            user = request.user
            # verify old password
            valid_pass = user.check_password(old_password)
            if not valid_pass:
                error = {
                    "code": 400, "message": _("OldPassword does not match."), "fields": "old_password",
                    "flag": False}
                return Response(error, status=400)

            user.set_password(new_password)
            user.save()
        return Response({'flag': True, 'message': _('Update password for user successfully.')})

    except Exception, e:
        print "ERROR change_password ", e
        error = {"code": 500, "message": _("Cannot update password for user. Please contact administrator."),
                 "fields": "", "flag": False}
        return Response(error, status=500)


"""
    Send Feedback
"""


@api_view(['POST'])
@permission_classes((AllowAny,))
def send_feedback(request):
    try:
        serializer = FeedBackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"code": 400, "message": "%s" % serializer.errors,
                         "fields": ""}, status=400)
    except Exception, e:
        error = {"code": 500, "message": _("Cannot send feedback. Please contact administrator."),
                 "fields": ""}
        return Response(error, status=500)

"""
    Get Hots List to show in Homepage
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def hots(request):
    try:
        hot_list = Hot.objects.filter(is_show=True).order_by('-created')[:5]
        serializer = HotsSerializer(hot_list, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Get All Game Type By Category
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def game_types_by_category(request, category_id):
    try:
        error = helper.check_id_valid(category_id)
        if not helper.is_empty(error):
            errors = {"code": 400, "message": "%s" %
                      error, "fields": "type_id"}
            return Response(errors, status=400)

        game_types = Type.objects.filter(category_id=category_id)
        serializer = TypeSerializer(game_types, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get All Game Play by Type ID
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def games(request):
    try:
        game_type_id = request.GET.get("type_id")
        error = helper.check_id_valid(game_type_id)
        if not helper.is_empty(error):
            errors = {"code": 400, "message": "%s" %
                      error, "fields": "type_id"}
            return Response(errors, status=400)

        game_list = Game.objects.filter(
            is_draft=False, game_type_id=game_type_id)
        serializer = GameSerializer(game_list, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get Game Detail by ID
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def game_detail(request, game_id):
    try:
        error = helper.check_id_valid(game_id)
        if error:
            errors = {"code": 400, "message": "%s" %
                      error, "fields": "game_id"}
            return Response(errors, status=400)

        game_detail = Game.objects.get(pk=game_id)
        serializer = GameDetailSerializer(game_detail, many=False)
        return Response(serializer.data)
    except Game.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "game_id"}
        return Response(error, status=400)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get Entertainment Detail By ID (Entertainments containt redemption, coffee, bakery ...etc )
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def entertainment_detail(request, id_or_key_query):
    try:
        if helper.is_int(id_or_key_query):
            entertainment_detail = Entertainment.objects.get(
                pk=id_or_key_query)
        else:
            entertainment_detail = Entertainment.objects.get(
                key_query=id_or_key_query)

        serializer = EntertainmentDetailSerializer(
            entertainment_detail, many=False)
        return Response(serializer.data)
    except Entertainment.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "id"}
        return Response(error, status=400)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Get All Events
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def events(request):
    try:
        event_list = Event.objects.filter(is_draft=False)
        serializer = EventsSerializer(event_list, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get Latest Events
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def events_latest(request):
    try:
        event_list = Event.objects.filter(
            is_draft=False).order_by('-created')[:2]
        serializer = EventsSerializer(event_list, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get All Events
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def event_detail(request, event_id):
    try:
        error = helper.check_id_valid(event_id)
        if error:
            errors = {"code": 400, "message": "%s" %
                      error, "fields": "event_id"}
            return Response(errors, status=400)

        event_list = Event.objects.get(pk=event_id)
        serializer = EventsSerializer(event_list, many=False)
        return Response(serializer.data)
    except Event.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "id"}
        return Response(error, status=400)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get posts by type
"""


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@permission_classes((AllowAny,))
def posts(request):
    # TODO : Posts_image in request /posts is required?
    try:
        type_id = request.GET.get("type_id")

        error = helper.check_id_valid(type_id)
        if error:
            errors = {"code": 400, "message": "%s" %
                      error, "fields": "type_id"}
            return Response(errors, status=400)

        post_list = Post.objects.filter(is_draft=False, post_type_id=type_id)
        print "description type ", post_list[0].post_type.description
        serializer = PostsSerializer(post_list, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get posts details
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def post_detail(request, id_or_key_query):
    try:
        if helper.is_empty(id_or_key_query):
            error = {"code": 400, "message": "This field is required.",
                     "fields": "id_or_key_query"}
            return Response(error, status=400)

        if helper.is_int(id_or_key_query):
            post_item = Post.objects.get(pk=id_or_key_query)
        else:
            post_item = Post.objects.get(key_query=id_or_key_query)

        serializer = PostsSerializer(post_item, many=False)
        return Response(serializer.data)
    except Post.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "id_or_key_query"}
        return Response(error, status=400)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get promotions by type
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def promotions(request):
    try:
        category_id = request.GET.get("category_id")

        lst_item = Promotion.objects.filter(is_draft=False)

        if category_id:
            if helper.is_int(category_id):
                lst_item = lst_item.filter(promotion_category_id=category_id)
            else:
                errors = {"code": 400, "message": _(
                    "This value must be is integer."), "fields": "category_id"}
                return Response(errors, status=400)

        serializer = PromotionsSerializer(lst_item, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get posts details
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def promotion_detail(request, promotion_id):
    try:
        promotion_item = Promotion.objects.get(pk=promotion_id)
        serializer = PromotionsSerializer(promotion_item)
        return Response(serializer.data)

    except Promotion.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "promotion_id"}
        return Response(error, status=400)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get Transaction Type
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def transactions_type(request):
    try:
        lst_item = Transaction_Type.objects.all()
        serializer = TransactionTypeSerializer(lst_item, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get ALL FAQs
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def faqs(request):
    try:
        category_id = request.GET.get("category_id", "")

        if category_id:
            faq_list = FAQ.objects.filter(category_id=category_id)
        else:
            faq_list = FAQ.objects.all()

        serializer = FAQsSerializer(faq_list, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Get Card Information
"""


@api_view(['GET'])
def card_information(request, card_id):
    print "API get card information"
    try:
        if not card_id:
            error = {
                "code": 400, "message": _("Card id field is required."), "fields": "card_id"}
            return Response(error, status=400)

        cursor = connections['sql_db'].cursor()

        query_str = """ WITH UPGRADE_INFO AS (SELECT Customer_Id, Transaction_DateTime FROM (SELECT DISTINCT ROW_NUMBER() OVER(partition by C.Customer_Id Order by Transaction_DateTime DESC) AS RN_C, 
                                     C.Customer_Id, CT.Transaction_DateTime FROM Cards C 
                                     INNER JOIN Card_Transactions CT ON CT.Card_Barcode = C.Card_Barcode 
                                     WHERE Transaction_Type = 506 AND C.Customer_Id IS NOT NULL) AS TEMP WHERE RN_C = 1)

                SELECT C.Card_Added, C.Card_Status, C.Card_State, C.Cash_Balance, C.Bonus_Balance, C.ETickets,
                     Cust.Firstname, Cust.Surname, Cust.DOB, Cust.PostCode, Cust.Address1, Cust.EMail, Cust.Mobile_Phone, 
                     UI.Transaction_DateTime, C.ReIssued_To_Card, Cust.Customer_Id  FROM Cards C
                 LEFT JOIN Customers Cust ON C.Customer_Id = Cust.Customer_Id
                 LEFT JOIN UPGRADE_INFO UI ON Cust.Customer_Id = UI.Customer_Id WHERE C.Card_Barcode = {0}"""

        # print query_str.format(card_id)

        cursor.execute(query_str.format(card_id))
        result = utils.card_information_mapper(cursor.fetchone())

        return Response(result)

    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)

"""
    Play Transaction
"""


@api_view(['GET'])
def play_transactions(request):
    try:
        card_id = request.GET.get("card_id", "")
        if not card_id:
            error = {
                "code": 400, "message": _("Card id field is required."), "fields": "card_id"}
            return Response(error, status=400)

        filter_id = request.GET.get("filter_id", "")
        sub_query = ""
        if filter_id:
            if not helper.is_int(filter_id):
                errors = {"code": 400, "message": _(
                    "This value must be is integer."), "fields": "filter_id"}
                return Response(errors, status=400)
            filter_object = Transaction_Type.objects.get(pk=filter_id)
            sub_query = " WHERE transaction_type like '" + filter_object.name_en + "'"

        cursor = connections['sql_db'].cursor()

        query_str = """ WITH PLAY_TRANSACTION AS (SELECT PT.Transaction_DateTime, PT.Transaction_Amount, GD.Game_Description,
                                 (CASE WHEN GD.Game_Group_Id = 0 THEN 'Refund' ELSE 'Play' END) AS transaction_type
                                 FROM Play_Transactions PT
                                 LEFT JOIN Game_Swipers GS ON PT.Game_Id = GS.Game_Id
                                 LEFT JOIN Game_Details GD ON GS.Game_ML_Id = GD.Game_ML_Id
                                 WHERE PT.Card_Barcode = {0})
                        SELECT TOP 50 * FROM PLAY_TRANSACTION {1} ORDER BY Transaction_DateTime DESC"""

        print query_str.format(card_id, sub_query)

        cursor.execute(query_str.format(card_id, sub_query))
        result = utils.play_transactions_mapper(cursor.fetchall())

        return Response(result)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Card Transaction
"""


@api_view(['GET'])
def card_transactions(request):
    try:
        card_id = request.GET.get("card_id", "")
        if not card_id:
            error = {
                "code": 400, "message": _("Card id field is required."), "fields": "card_id"}
            return Response(error, status=400)

        cursor = connections['sql_db'].cursor()

        query_str = """ SELECT TOP 50 ST.Transaction_DateTime, SCT.Cash_Amount FROM Sale_Card_Transactions SCT 
                                 INNER JOIN Sale_Transactions ST ON ST.Transaction_Id = SCT.Transaction_Id
                                 WHERE SCT.Card_Barcode = {0} ORDER BY ST.Transaction_DateTime DESC"""

        cursor.execute(query_str.format(card_id))

        print query_str.format(card_id)
        result = utils.card_transactions_mapper(cursor.fetchall())

        return Response(result)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Reissue History
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def reissue_history(request):
    try:
        card_id = request.GET.get("card_id", "")
        if not card_id:
            error = {
                "code": 400, "message": _("Card id field is required."), "fields": "card_id"}
            return Response(error, status=400)

        cursor = connections['sql_db'].cursor()

        query_str = """WITH REISSUE_HISTORY AS (SELECT CT.Transaction_DateTime, CT.Card_Barcode, CT.Transfer_Card_Barcode,
                                 (CASE WHEN CT.Transaction_Type = 506 THEN 'Upgraded' ELSE 'Reissue' END) AS Transaction_Type_Txt, 
                                 CT.Transaction_Type FROM Card_Transactions CT
                                 WHERE CT.Transaction_Type IN (500, 501, 506) AND CT.Card_Barcode = {0})

                        SELECT TOP 50 * FROM REISSUE_HISTORY ORDER BY Transaction_DateTime DESC"""

        cursor.execute(query_str.format(card_id))
        result = utils.reissue_history_mapper(cursor.fetchall())
        return Response(result)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Get Open Time
"""


@api_view(['GET'])
@permission_classes((AllowAny,))
def open_time(request):
    try:
        open_date = request.GET.get("open_date", "")
        if not open_date:
            error = {
                "code": 400, "message": _("Date request is required."), "fields": "open_date"}
            return Response(error, status=400)

        opentimes = OpenTime.objects.get(open_date=open_date.strip())
        serializer = OpenTimeSerializer(opentimes, many=False)
        return Response(serializer.data)
    except OpenTime.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "open_date"}
        return Response(error, status=400)
    except ValidationError, e:
        error = {"code": 400, "message": "%s" % e,
                 "fields": ""}
        return Response(error, status=400)
    except Exception, e:
        print "Action open_time : ", e
        error = {"code": 500, "message": _("Internal Server Error. Please contact administrator."),
                 "fields": ""}
        return Response(error, status=500)


"""
    Get all notifications
"""


@api_view(['GET'])
def notifications(request):
    try:
        category_id = request.GET.get("category_id", "")
        user = request.user

        if category_id:
            notification_list = User_Notification.objects.filter(
                notification__category_id=category_id, user=user)
        else:
            notification_list = User_Notification.objects.filter(user=user)

        serializer = UserNotificationSerializer(notification_list, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Get notificatons by category
"""


@api_view(['GET'])
def notification_category(request):
    try:
        categories = Category_Notification.objects.all()
        serializer = CategoryNotificationSerializer(categories, many=True)
        return Response(serializer.data)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Update current user read notification
"""


@api_view(['POST'])
def user_read_notification(request):
    try:
        user = request.user
        notification_id = request.data.get('notification_id', '')
        if not notification_id:
            return Response({'message': _('Notification Id is required.')}, status=400)
        if user.anonymously:
            return Response({'message': _('Anonymous User Cannot Update Notification')}, status=400)

        obj, created = User_Notification.objects.update_or_create(
            notification_id=notification_id, user=user)
        obj.is_read = True
        obj.save()
        return Response({'message': _('Successfull')})

    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Get notificaton detail
"""


@api_view(['GET'])
def notification_detail(request, notification_id):
    try:
        notification_obj = Notification.objects.get(pk=notification_id)
        print 'notification_obj ', notification_obj
        serializer = NotificationSerializer(notification_obj, many=False)
        return Response(serializer.data)

    except User_Notification.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e, "fields": "notification_id"}
        return Response(error, status=400)
    except Exception, e:
        error = {"code": 500, "message": "%s" % e, "fields": ""}
        return Response(error, status=500)


"""
    Turn off Notification
"""


@api_view(['PUT'])
def turn_off_notification(request):
    try:
        if not request.user.anonymously:
            user = request.user
            user.flag_notification = False
            user.save()
            return Response({'message': _('Turn off notification successful.')})
        else:
            return Response({'message': _('Anonymous User Cannot Call This Action.')}, status=400)

    except Exception, e:
        print "Error turn_off_notification ", e
        return Response({'message': _('Internal Server Error. Please Contact Administrator.')}, status=500)


"""
    Turn on Notification
"""


@api_view(['PUT'])
def turn_on_notification(request):
    try:
        if not request.user.anonymously:
            user = request.user
            user.flag_notification = True
            user.save()
            return Response({'message': _('Turn on notification successful.')})
        else:
            return Response({'message': _('Anonymous User Cannot Call This Action.')}, status=400)

    except Exception, e:
        print "Error turn_on_notification ", e
        return Response({'message': _('Internal Server Error. Please Contact Administrator.')}, status=500)


"""
    API add new notification for testing
"""


@api_view(['POST'])
def add_notification(request):
    try:
        # TODO : Check user i not anonymous
        if not request.user.anonymously:
            subject = request.data.get('subject', '')
            message = request.data.get('message', '')
            category_id = request.data.get('category_id', '')
            sub_url = request.data.get('sub_url', '')
            if not subject or not message or not category_id:
                error = {
                    "code": 400, "message": "Please check required fields : [subject, message, category_id]", "fields": "",
                    "flag": False}
                return Response(error, status=400)

            category_obj = Category_Notification.objects.get(pk=category_id)
            notify_obj = Notification(
                subject=subject, message=message, category=category_obj, sub_url=sub_url)
            notify_obj.save()

            serializer = NotificationSerializer(notify_obj, many=False)
            return Response(serializer.data)

    except Category_Notification.DoesNotExist, e:
        error = {"code": 400, "message": "%s" % e,
                 "fields": ""}
        return Response(error, status=400)
    except Exception, e:
        error = {"code": 500, "message": _("Cannot add new notification. Please contact administrator."),
                 "fields": ""}
        return Response(error, status=500)


"""
    API send notifications to devices
"""


@api_view(['POST'])
@permission_classes((AllowAny,))
def send_notification(request):
    try:
        # TODO : Check user i not anonymous
        print 'request.data ', request.data
        notification_id = request.data.get('notification_id', '')
        if not notification_id:
            error = {
                "code": 400, "message": "Please check required fields : [notification_id]", "fields": "",
                "flag": False}
            return Response(error, status=400)

        notify_obj = Notification.objects.get(pk=notification_id)
        user_of_notification = User_Notification.objects.filter(
            notification_id=notification_id).values_list('user_id', flat=True)

        data_notify = {"title": notify_obj.subject, "body": notify_obj.message,
                       "sub_url": notify_obj.sub_url, "image": notify_obj.image.url if notify_obj.image else "",
                       "notification_id": notify_obj.id}

        devices_ios = APNSDevice.objects.filter(
            user__flag_notification=True, user__id__in=user_of_notification)
        if devices_ios:
            devices_ios.send_message(message=data_notify, extra=data_notify)

        fcm_devices = GCMDevice.objects.filter(
            user__flag_notification=True, user__id__in=user_of_notification)
        if fcm_devices:
            fcm_devices.send_message(notify_obj.subject, extra=data_notify)

        return Response({'message': _('Push Notification Successfull')})

    except Notification.DoesNotExist, e:
        print "error PUSH notification ", e
        error = {"code": 400, "message": "%s" % e,
                 "fields": ""}
        return Response(error, status=400)
    except Exception, e:
        print "ERROR send_notification : ", e
        error = {"code": 500, "message": _("Cannot push notification. Please contact administrator."),
                 "fields": ""}
        return Response(error, status=500)


"""
    Connect Device for User
"""


@api_view(['POST'])
def connect_device(request):
    try:
        user = request.user

        if not request.user.anonymously:
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            device_uid = request.data.get("device_uid", "")

            if not device_uid:
                error = {
                    "code": 400, "message": _("The device_uid field is required."), "fields": "device_uid"}
                return Response(error, status=400)

            if user_agent:
                if 'ios' in user_agent.lower():
                    try:
                        device = APNSDevice.objects.get(
                            registration_id=device_uid)
                        device.user = user
                        device.save()

                    except APNSDevice.DoesNotExist, e:
                        device = APNSDevice(
                            user=user, name=user.email, registration_id=device_uid)
                        device.save()
                else:
                    device = GCMDevice(
                        user=user, name=user.email, registration_id=device_uid, cloud_message_type="FCM")
                    device.save()
            return Response({'message': _('Connect device successful.')})
        else:
            return Response({'message': _('Anonymous User Cannot Call This Action.')}, status=400)

    except Exception, e:
        print "Error connect_device : ", e
        return Response({'message': _('Internal Server Error. Please Contact Administrator.')}, status=500)


"""
    Connect Device for User
"""


@api_view(['POST'])
def disconnect_device(request):
    try:
        user = request.user

        if not request.user.anonymously:
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            device_uid = request.data.get("device_uid", "")

            if not device_uid:
                error = {
                    "code": 400, "message": _("The device_uid field is required."), "fields": "device_uid"}
                return Response(error, status=400)

            if user_agent:
                if 'ios' in user_agent.lower():
                    device = APNSDevice.objects.get(registration_id=device_uid)
                    device.user = None
                    device.save()
                else:
                    device = GCMDevice.objects.get(registration_id=device_uid)
                    device.user = None
                    device.save()

            return Response({'message': _('Disconnect device successful.')})
        else:
            return Response({'message': _('Anonymous User Cannot Call This Action.')}, status=400)

    except APNSDevice.DoesNotExist, e:
        return Response({'message': _('Cannot disconnect device. DeviceID not found.')}, status=400)
    except GCMDevice.DoesNotExist, e:
        return Response({'message': _('Cannot disconnect device. DeviceID not found.')}, status=400)
    except Exception, e:
        print "Error connect_device : ", e
        return Response({'message': _('Internal Server Error. Please Contact Administrator.')}, status=500)


"""
    Update user have get a gift
"""


@api_view(['PUT'])
def gift_user(request):
    try:
        if not request.user.anonymously:
            user = request.user
            print "## Current User ", user
            promotion_id = request.data.get('promotion_id', '')

            if not promotion_id:
                error = {
                    "code": 400, "message": _("The promotion_id is required."), "fields": "promotion_id"}
                return Response(error, status=400)

            obj_promotion = Promotion.objects.get(pk=promotion_id)

            # CHECK Promotion Category is new user install app helio
            if obj_promotion.id == core_constants.PROMOTION_ID_SETUP_DEVICE:
                return gift_install_app(user, promotion_id)

            gift = Gift.objects.get(user=user, promotion_id=promotion_id)

            message = _("Error. User or Deivce Have get gift from promotion")
            status_code = 501
            if not gift.is_used:
                message = "Success"
                status_code = 200
                gift.is_used = True
                gift.save()

            return Response({'message': message}, status=status_code)
        else:
            return Response({'message': _('Anonymous User Cannot Call This Action.')}, status=400)

    except Promotion.DoesNotExist, e:
        error = {"code": 400, "message": _("Promotion for user does not matching. Please check again."),
                 "fields": ""}
        return Response(error, status=400)
    except Gift.DoesNotExist, e:
        error = {"code": 400, "message": _("Your account not apply current promotion. Please contact administrator."),
                 "fields": ""}
        return Response(error, status=400)
    except Exception, e:
        print "Error gift_user ", e
        error = {"code": 500, "message": _("Your account not apply current promotion. Please contact administrator."),
                 "fields": ""}
        return Response(error, status=500)


"""
    Gift for user install app
"""


def gift_install_app(user, promotion_id):
    try:
        """ 
            Case 1 : Check user is new registration
            Case 2 : Check Device have using
         """
        if user.is_new_register:
            if not user.device_unique:
                return Response({'message': _("Error. DeivceID of user is empty. Please check again.")}, status=501)

            try:
                gift = Gift.objects.get(
                    device_id=user.device_unique, promotion_id=promotion_id)
            except Gift.DoesNotExist, e:
                # IF query does not exist then is new user and device
                gift = Gift(user=user, device_id=user.device_unique,
                            promotion_id=promotion_id)
                gift.save()
        else:
            return Response({'message': _("Error. User or Deivce Have get gift from promotion")}, status=501)

        message = _("Error. User or Deivce Have get gift from promotion")
        status_code = 501
        if not gift.is_used:
            message = "Success"
            status_code = 200
            gift.is_used = True
            gift.save()
            # Update User have gift
            user.is_new_register = False
            user.save()

        return Response({'message': message}, status=status_code)

    except Exception, e:
        print "Error gift_install_app ", e
        error = {"code": 500, "message": _("Your account not apply current promotion. Please contact administrator."),
                 "fields": ""}
        return Response(error, status=500)
