# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *
from modeltranslation.admin import TranslationAdmin
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
import custom_models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from multiupload.admin import MultiUploadAdmin
# from django.contrib.admin import SimpleListFilter


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = custom_models.User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = custom_models.User
        fields = ('email', 'password', 'birth_date', 'phone', 'personal_id', 'first_name', 'last_name',
                  'country', 'address', 'city', 'is_active', 'is_staff', 'is_superuser', 'groups', 'code', 
                  'avatar', 'anonymously', 'flag_notification', 'device_unique', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ('code', 'anonymously', 'flag_notification', 'device_unique' )

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'country', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birth_date', 'phone',
                                      'personal_id', 'country', 'address', 'city', 'avatar', )}),
        ('Permissions', {'fields': ('is_staff',
                                    'is_superuser', 'is_active', 'anonymously', 'groups', )}),
        ('Security', {'fields': ('code', 'device_unique', )}),
        ('Notification', {'fields': ('flag_notification', )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...

admin.site.register(custom_models.User, UserAdmin)


class CategoryAdmin(TranslationAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


class TypeAdmin(TranslationAdmin):
    pass
admin.site.register(Type, TypeAdmin)

# Register Posts Type Model to Admin Site

class PostTypeAdmin(TranslationAdmin):
    pass
admin.site.register(Post_Type, PostTypeAdmin)


class PostImageInline(admin.TabularInline):
    model = Post_Image
    extra = 3

class PostMultiuploadMixing(object):

    def process_uploaded_file(self, uploaded, post, request):
        if post:
            image_obj = post.posts_image.create(image=uploaded)
        else:
            image_obj = Post_Image.objects.create(image=uploaded, post=None)
        return {
            'url': image_obj.image.url,
            'thumbnail_url': image_obj.image.url,
            'id': image_obj.id,
            'name': image_obj.filename
        }

# Add Filter Post Type


# class PostTypeFilter(SimpleListFilter):
#     title = 'Type'  # or use _('country') for translated title
#     parameter_name = 'post_type'

#     def lookups(self, request, model_admin):
#         # You can also use hardcoded model name like "Post_Type" instead of
#         # "model_admin.model" if this is not direct foreign key filter

#         post_types = set(
#             [c.post_type for c in model_admin.model.objects.all()])
#         result = [(pt.id, pt.name) for pt in post_types if pt != None]

#         return result

#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(post_type__id__exact=self.value())
#         else:
#             return queryset


# Register Posts Model to Admin Site


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):

        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class PostAdmin(PostMultiuploadMixing, MultiUploadAdmin, TranslationAdmin):
    list_filter = (('post_type__name', custom_titled_filter('Post Type')), )
    # list_filter = (PostTypeFilter, )
    inlines = [PostImageInline, ]
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }
    multiupload_form = True
    multiupload_list = False

    def delete_file(self, pk, request):
        '''
        Delete an image.
        '''
        obj = get_object_or_404(Image, pk=pk)
        return obj.delete()

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('key_query',)
        return self.readonly_fields

    pass
admin.site.register(Post, PostAdmin)

# Events


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'

    def clean(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            msg = u"Ngày kết thúc phải lớn hơn ngày bắt đầu."
            self._errors["end_date"] = self.error_class([msg])

        return self.cleaned_data


class EventAdmin(TranslationAdmin):
    form = EventForm
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }
    pass
admin.site.register(Event, EventAdmin)

# Games


class GameAdmin(TranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }
    pass
admin.site.register(Game, GameAdmin)


# FAQs


class FAQsAdmin(TranslationAdmin):
    pass
admin.site.register(FAQ, FAQsAdmin)


class ContactAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contact, ContactAdmin)


class BannerAdmin(TranslationAdmin):
    pass
admin.site.register(Banner, BannerAdmin)


class PromotionAdmin(TranslationAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget()},
    }
    pass
admin.site.register(Promotion, PromotionAdmin)

# Hots


class HotForm(forms.ModelForm):

    class Meta:
        model = Hot
        fields = '__all__'

    def clean_is_show(self):
        is_show = self.cleaned_data.get('is_show')
        total_show = Hot.objects.filter(is_show=True).count()
        print 'total_show ',total_show
        print 'is_show ',is_show
        # case update db is 4:

        if total_show < 4 or not is_show:
            pass
        elif self.instance.pk and self.instance.is_show == is_show and total_show == 4:
            pass
        else:
            raise forms.ValidationError('Hot giới hạn tối đa 4 bài được hiển thị. Vui lòng chọn bỏ bớt trường is_show và chọn lại.',
                                            code='invalid_is_show',
                                            params={'is_show': is_show},
                                            )

        return self.cleaned_data['is_show']


class HotsAdmin(TranslationAdmin):
    form = HotForm
    list_display = ('name', 'is_show', )
    pass
admin.site.register(Hot, HotsAdmin)


class FeedBackAdmin(admin.ModelAdmin):
    pass
admin.site.register(FeedBack, FeedBackAdmin)


class AdvertisementAdmin(TranslationAdmin):
    pass
admin.site.register(Advertisement, AdvertisementAdmin)


class PromotionLabelAdmin(TranslationAdmin):
    pass
admin.site.register(Promotion_Label, PromotionLabelAdmin)


class TransactionTypeAdmin(TranslationAdmin):
     pass
admin.site.register(Transaction_Type, TransactionTypeAdmin)


class OpenTimeAdmin(admin.ModelAdmin):
     pass
admin.site.register(OpenTime, OpenTimeAdmin)


class NotificationAdmin(TranslationAdmin):
     pass
admin.site.register(Notification, NotificationAdmin)


class CategoryNotificationAdmin(TranslationAdmin):
     pass
admin.site.register(Category_Notification, CategoryNotificationAdmin)
