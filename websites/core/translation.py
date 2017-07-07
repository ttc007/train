from modeltranslation.translator import translator, TranslationOptions
from models import *


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )

translator.register(Category, CategoryTranslationOptions)


class TypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'description_detail')

translator.register(Type, TypeTranslationOptions)

# Posts


class PostTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)

translator.register(Post_Type, PostTypeTranslationOptions)


class PostsTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'content', )

translator.register(Post, PostsTranslationOptions)

# Events


class EventsTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'content', )

translator.register(Event, EventsTranslationOptions)

# Games


class GameTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'content', )

translator.register(Game, GameTranslationOptions)


# FAQs


class FAQsTranslationOptions(TranslationOptions):
    fields = ('question', 'answer', )

translator.register(FAQ, FAQsTranslationOptions)

# Hots


class HotTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Hot, HotTranslationOptions)


class BannerTranslationOptions(TranslationOptions):
    fields = ()

translator.register(Banner, BannerTranslationOptions)


class PromotionTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description', 'content')

translator.register(Promotion, PromotionTranslationOptions)


class TransactionTypeTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Transaction_Type, TransactionTypeTranslationOptions)


class PromotionLabelTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Promotion_Label, PromotionLabelTranslationOptions)


class AdvertisementTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Advertisement, AdvertisementTranslationOptions)


class NotificationTranslationOptions(TranslationOptions):
    fields = ('subject', 'message', )

translator.register(Notification, NotificationTranslationOptions)

class CategoryNotificationTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(Category_Notification, CategoryNotificationTranslationOptions)
