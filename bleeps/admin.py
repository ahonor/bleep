from bleeps.models import Bleep, Comment, UserProfile, UserAuthToken
from django.contrib import admin

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

class BleepAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['bleep_message',
                                         'bleep_client',
                                         'bleep_service',
                                         'bleep_status']}),
        ('Date information', {'fields': ['bleep_pub_date']}),
        ('Request data', {'fields':['bleep_get_data',
                                    'bleep_post_data',
                                    'bleep_content_type']}),
    ]
    inlines = [CommentInline]
    list_display = ('bleep_client', 'bleep_service', 'bleep_pub_date', 
                    'was_published_today','bleep_status')
    list_filter = ['bleep_pub_date']
    search_fields = ['bleep_client']
    date_hierarchy = 'bleep_pub_date'

admin.site.register(Bleep, BleepAdmin)


class UserAuthTokenInline(admin.TabularInline):
    model = UserAuthToken
    extra = 1

class UserProfileAdmin(admin.ModelAdmin):
    fields = ('user','organization','url','daily_digest_subscription',)
    inlines = [UserAuthTokenInline]
    
admin.site.register(UserProfile, UserProfileAdmin)

