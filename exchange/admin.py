from django.contrib import admin
from exchange.models import Phone, Product, Category, Feedback, Deal, DealOffer, Notification, Chat


class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'detail', 'quantity', 'created_date', 'category', 'want_product', 'owner')

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = ('__all__',)

admin.site.register(Category, CategoryAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    fields = ('__all__',)
    list_filter = ['created_date']
    search_fields = ['title']
admin.site.register(Feedback, FeedbackAdmin)

class DealAdmin(admin.ModelAdmin):
    fields = ('__all__',)
    list_filter = ['created_date', 'owner_accept', 'offerer_accept', 'expired_datetime', 'is_cancel']
    search_fields = ['product']
admin.site.register(Deal, DealAdmin)

class DealOffererAdmin(admin.ModelAdmin):
    fields = ('__all__',)
    search_fields = ['deal']
admin.site.register(DealOffer, DealOffererAdmin)

class NotificationAdmin(admin.ModelAdmin):
    fields = ('__all__',)
    list_filter = ['created_date', 'is_readed']
    search_fields = ['user']
admin.site.register(Notification, NotificationAdmin)

class ChatAdmin(admin.ModelAdmin):
    fields = ('__all__',)
    search_fields = ['deal']
    list_filter = ['created_date']
admin.site.register(Chat, ChatAdmin)

class PhoneAdmin(admin.ModelAdmin):
    fields = ('__all__',)
    search_fields = ['phone_number']
    list_filter = ['is_verification']
admin.site.register(Phone, PhoneAdmin)
