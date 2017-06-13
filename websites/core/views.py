from django.shortcuts import render
from models import *
from custom_models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import ast
import constants as const
import time
from datetime import *
from forms import *
import api.utils as utils
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from django.utils.translation import LANGUAGE_SESSION_KEY



def home(request):
    try:
        request.session[LANGUAGE_SESSION_KEY] = 'vi'
        result = {}
        # banners on home page
        banners = Banner.objects.filter(is_show=True).order_by('position')
        banners_map = {}
        if banners:
            for item in banners:
                banners_map[item.position] = item
        result["banners"] = banners_map

        # hots
        hots = Hot.objects.filter(is_show=True).order_by('-modified')[:4]
        result["hots"] = hots

        # game section
        result["night_life_types"] = Type.objects.filter(category_id=const.NIGHT_LIFE_CATEGORY)
        result["play_types"] = Type.objects.filter(category_id=const.HELIO_PLAY_CATEGORY)
        result["kids_types"] = Type.objects.filter(category_id=const.HELIO_KIDS_CATEGORY)
        result["coffee_types"] = Type.objects.filter(category_id=const.COFFEE_CATEGORY)
        
        # game categorys
        events = Event.objects.all().order_by('-start_date')[:2]
        result["events"] = events
        return render(request, 'websites/home.html', {"result":result})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def power_card(request):
    print "***START Power Card Introduction PAGE***"
    try:
        result = {}
        # Powercard info
        powercard_type = Post_Type.objects.get(pk=const.POWERCARD_POST_TYPE_ID)
        result["powercard_type"] = powercard_type

        # Powercard list
        powercards = Post.objects.filter(post_type = powercard_type)
        result["powercards"] = powercards

        faqs = FAQ.objects.filter(category_id=const.POWERCARD_CATEGORY).order_by('-created')
        result["faqs"] = faqs
        return render(request, 'websites/power_card.html', {"result":result})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def faqs(request):
    print "***START FAQs PAGE***"
    try:
        faqs_categorys = Category.objects.filter(pk__in=(const.HELIO_PLAY_CATEGORY, const.HELIO_KIDS_CATEGORY, const.POWERCARD_CATEGORY, const.REDEMPTION_STORE_CATEGORY, const.OTHER_PRODUCT_CATEGORY))

        datas = {}
        if faqs_categorys:
            for faqs_category in faqs_categorys:
                datas[faqs_category] = faqs_category.faq_category_rel.all().order_by('-created')
 
        return render(request, 'websites/faqs.html', {"datas":datas})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

        
def contact(request):
    print "***START CONTACT CONTENT PAGE***"
    try:
        message_success = {}
        contact_form = ContactForm(request=request)
        if request.method == 'POST':
            contact_form = ContactForm(request.POST, request=request)
            if contact_form.is_valid():
                contact_form.save() 
                message_success = 'Successfully!'
                return HttpResponse(json.dumps(message_success),content_type="application/json")
            else:
                errors = {}
                errors[k] = [v[0] for k, v in contact_form.errors.items()]
                return HttpResponse(json.dumps(errors), content_type="application/json", status=400)

        return render(request, 'websites/contact.html', {"form":contact_form})

    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def helio_kids(request):
    print "***START HELIO KIDS PAGE***"
    try:
        games = {}
        #Get page info
        page_info = Category.objects.get(pk=const.HELIO_KIDS_CATEGORY)
        #Get kids pricing
        kids_pricing = Post.objects.get(key_query=const.KIDS_PRICING_KEY_QUERY)

        # Game type
        if page_info:
            kids_types = page_info.game_category_rel.all()
            promotions = {}
            if kids_types:
                for item in kids_types:
                    games[item] = item.game_type_rel.filter(is_draft=False).order_by('-created')

        promotions = Promotion.objects.filter(is_draft=False, promotion_category_id=const.HELIO_KIDS_CATEGORY).order_by('-created')

        return render(request, 'websites/helio_kids.html', {"page_info": page_info, "kids_pricing": kids_pricing, "map_games": games, "promotions": promotions})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")
    

def night_life(request):
    print "***START NIGHT LIFE CONTENT PAGE***"
    try:
        night_life = Post.objects.get(key_query=const.NIGHT_LIFE_KEY_QUERY)
        return render(request, 'websites/night_life.html', {"night_life": night_life})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def helio_play(request):
    print "***START HELIO PLAY PAGE***"
    try:
        games = {}
        #Get page info
        page_info = Category.objects.get(pk=const.HELIO_PLAY_CATEGORY)

        # Game type
        if page_info:
            play_types = page_info.game_category_rel.all()
            if play_types:
                for item in play_types:
                    games[item] = item.game_type_rel.filter(is_draft=False).order_by('-created')

        promotions = Promotion.objects.filter(is_draft=False, promotion_category_id=const.HELIO_PLAY_CATEGORY).order_by('-created')

        return render(request, 'websites/helio_play.html', {"page_info": page_info, "map_games": games, "promotions": promotions})

    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def helio_introduction(request):
    print "***START HELIO ABOUT PAGE***"
    try:
        # Helio About info
        about_type = Post_Type.objects.get(pk=const.HELIO_ABOUT_POST_TYPE_ID)

        # Helio About list
        abouts = Post.objects.filter(is_draft=False, post_type = about_type)
        
        return render(request, 'websites/helio_introduction.html', {"about_type": about_type, "abouts": abouts})

    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def term_condition(request):
    print "***START TERM & CONDITION PAGE***"
    try:
        # Experience info
        term = Post.objects.get(key_query=const.TERM_AND_CONDITION_KEY_QUERY)
        
        return render(request, 'websites/term_condition.html', {"term": term})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def events(request):
    print "***START EVENTS PAGE***"
    try:
        current_time =  datetime.now()

        result = {}
        events = Event.objects.filter(is_draft=False).order_by('-start_date')
        events_map = {}

        event_list = []
        if events:
            for event in events:
                event.start_datetime = datetime.combine(event.start_date, event.start_time)
                event.end_datetime = datetime.combine(event.end_date, event.end_time)

                # if current event then show on top
                if event.start_datetime < current_time and current_time < event.end_datetime:
                    event_list.insert(0, event)
                else:
                    event_list.append(event)

                key = event.start_date.strftime('%Y_%m')
                if key not in events_map.keys():
                    events_map[key] = []
                events_map[key].append(event)

        result["events"] = event_list
        result["events_map"] = sorted(events_map.items())
        result["event_hots"] = event_list[:3]

        return render(request, 'websites/events.html', {"result": result})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def event_detail(request, event_id):
    try:
        print "***START EVENT DETAIl PAGE***"
        event = Event.objects.get(pk=event_id)
        if event:
            event.start_datetime = datetime.combine(event.start_date, event.start_time)
            event.end_datetime = datetime.combine(event.end_date, event.end_time)

        other_events = Event.objects.all().order_by('-created')[:3]

        return render(request, 'websites/event_detail.html', {"event": event, "other_events": other_events})

    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def experience(request):
    print "***START EXPERIENCE CONTENT PAGE***"
    try:
        result = {}
        # Experience info
        experience_type = Post_Type.objects.get(pk=const.EXPERIENCE_POST_TYPE_ID)
        result["experience_type"] = experience_type

        # Experience list
        experiences = Post.objects.filter(is_draft=False, post_type = experience_type).order_by('-created')
        result["experiences"] = experiences

        result["experiences_hots"] = experiences[:5]
        print experiences
        
        return render(request, 'websites/experience.html', {"result": result})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def experience_detail(request, experience_id):
    try:
        print "***START EVENT CONTENT PAGE***"
        experience = Post.objects.get(pk=experience_id)

        other_experiences = Post.objects.filter(post_type_id=const.EXPERIENCE_POST_TYPE_ID).order_by('-created')[:3]

        return render(request, 'websites/experience_detail.html', {"experience": experience, "other_experiences": other_experiences})

    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def news(request):
    print "***START News PAGE***"
    try:
        result = {}
        # News info
        news_type = Post_Type.objects.get(pk=const.NEWS_POST_TYPE_ID)
        
        # News list
        news = Post.objects.filter(is_draft=False, post_type = news_type).order_by('-created')

        return render(request, 'websites/news.html', {"news_type": news_type, "news": news, "news_hots": news[:5]})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def new_detail(request, new_id):
    print "***START NEW CONTENT PAGE***"
    try:
        new = Post.objects.get(pk=new_id)

        other_news = Post.objects.filter(post_type_id=const.NEWS_POST_TYPE_ID).order_by('-created')[:3]

        return render(request, 'websites/new_detail.html', {"new": new, "other_news": other_news})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def coffee_bakery(request):
    print "***START HELIO COFFEE CONTENT PAGE***"
    try:
        coffee_page = Post.objects.get(key_query=const.COFFEE_KEY_QUERY)
        
        list_images = {}
        if coffee_page:
            list_images = coffee_page.posts_image.all()[:6]

        return render(request, 'websites/coffee_bakery.html', {"page_info":coffee_page, "list_images": list_images})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def redemption_store(request):
    print "***START HELIO COFFEE CONTENT PAGE***"
    try:
        result = {}
        redemption_page = Post.objects.get(key_query=const.REDEMPTION_STORE_KEY_QUERY)
        result["page_info"] = redemption_page

        list_images = {}
        if redemption_page:
            list_images = redemption_page.posts_image.all()[:6]

        result["list_images"] = list_images

        # FAQs list
        faqs = FAQ.objects.filter(category_id=const.REDEMPTION_STORE_CATEGORY).order_by('-created')
        result["faqs"] = faqs
        
        return render(request, 'websites/redemption_store.html', {"result":result})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def promotions(request):
    print "***START EVENT CONTENT PAGE***"
    try:
        result = {}
        promotions = Promotion.objects.filter(is_draft=False).order_by('-created')
        datas = {}
        if promotions:
            for promotion in promotions:
                if promotion.promotion_category:
                    key = promotion.promotion_category
                    if key not in datas.keys():
                        datas[key] = []
                    datas[key].append(promotion)


            category_all = Category();
            category_all.id = 0
            datas[category_all] = promotions

        # Promotion hots to show coursel
        promotions_hots = promotions[:3]

        return render(request, 'websites/promotions.html', {"promotions_hots": promotions_hots, "datas": datas})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def promotion_detail(request, promotion_id):
    print "***START PROMOTION DETAIl PAGE***"
    try:
        promotion = Promotion.objects.get(pk=promotion_id)

        other_promotions = Promotion.objects.all().order_by('-created')[:3]

        return render(request, 'websites/promotion_detail.html', {"promotion": promotion, "other_promotions": other_promotions})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def careers(request):
    print "***START CARRER CONTENT PAGE***"
    try:
        result = {}
        # Careers info
        careers_type = Post_Type.objects.get(pk=const.CAREERS_POST_TYPE_ID)
        result["careers_type"] = careers_type

        # Careers pin to top
        careers_pin_top = Post.objects.filter(is_draft=False, pin_to_top=True).first()
        result["careers_pin_top"] = careers_pin_top

        # Careers list
        careers = Post.objects.filter(is_draft=False, post_type = careers_type).order_by('-created')
        result["careers"] = careers

        return render(request, 'websites/careers.html', {"result": result})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def career_detail(request, career_id):
    try:
        print "***START CARRER DETAIl PAGE***"
        career = Post.objects.get(pk=career_id)

        other_careers = Post.objects.filter(is_draft=False, post_type_id=const.CAREERS_POST_TYPE_ID).order_by('-created')[:3]

        return render(request, 'websites/carrer_detail.html', {"career": career, "other_careers": other_careers})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def other_product(request):
    print "***START other product PAGE***"
    try:
        result = Post.objects.filter(post_type_id=const.ORTHER_PROD_POST_TYPE_ID).order_by('-created')
        
        # print "products ", products
        products = []
        for product in result:
            if product:
                #get list post images
                product.post_images = product.posts_image.all()[:6]
                products.append(product)

        return render(request, 'websites/other_product.html', {"products":products})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def policy(request):
    print "***START POLICY PAGE***"
    try:
        # Policy
        policy = Post.objects.get(key_query=const.POLICY_KEY_QUERY)

        return render(request, 'websites/policy.html', {"policy":policy})
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

def helio_photos(request):
    print "***START HELIO PHOTOS PAGE***"
    try:
        photos_type = Post_Type.objects.get(pk=const.HELIO_PHOTOS_POST_TYPE_ID)

        # Helio photos
        photos = Post.objects.filter(post_type=photos_type)

        for photo in photos:
            # get len of post images
            photo.images_len =  len(photo.posts_image.all())

        return render(request, 'websites/helio_photos.html', {"photos_type": photos_type, "photos": photos});
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")


def list_photos_by_album(request):
    list_images = {}
    try:
        if request.method == 'POST':
            album_id = request.POST["album_id"]
            print "album_id", album_id
            if album_id:
                album = Post.objects.get(pk=album_id)
                if album:
                    list_images = list(album.posts_image.all().values('image'))
    except Exception, e:
        print "Error: ", e
        raise Exception("ERROR : Internal Server Error .Please contact administrator.")

    return HttpResponse(
        json.dumps(list_images),
        content_type="application/json"
    )

@login_required(login_url='/admin/login/')
def admin_promotions(request):
    promotions = Promotion.objects.filter(is_draft=False).order_by('-created')

    return render(request, 'websites/admin_promotions.html', {"promotions":promotions})

@login_required(login_url='/admin/login/')
def admin_promotion_detail(request, promotion_id):
    promotion = Promotion.objects.get(pk=promotion_id)
    users = User.objects.all()

    list_gift = Gift.objects.filter(promotion_id=promotion_id)

    promotion_user_ids = list_gift.values_list('user_id', flat=True)

    for user in users:
        if user.id in promotion_user_ids:
            user.is_selected = True

    return render(request, 'websites/admin_promotion_detail.html', {"promotion":promotion, "users": users})

@login_required(login_url='/admin/login/')
def update_promotions_user(request):
    if request.method == 'POST':

        promotion_id = request.POST.get("promotion_id")
        list_user = map(long,request.POST.getlist('list_user[]'))

        list_delete = []
        if promotion_id:
            # Gift.objects.filter(promotion_id=promotion_id).delete()
            promotion_user_db =  Gift.objects.filter(promotion_id=promotion_id).values_list('user_id', flat=True)
            list_update_user = set(list_user)^set(promotion_user_db)
            if list_update_user:
                for user_id in list_update_user:
                    if user_id not in promotion_user_db:
                        gift_item = Gift()
                        gift_item.promotion_id = promotion_id
                        gift_item.user_id = user_id
                        gift_item.save()
                    else:
                        list_delete.append(user_id)

                if list_delete:
                    Gift.objects.filter(user_id__in=list_delete).delete()

        return HttpResponse(
            json.dumps({}),
            content_type="application/json"
        )
    return render(request, 'websites/admin_promotion_detail.html', {"promotion":promotion, "users": users})