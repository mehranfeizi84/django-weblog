from django.contrib import admin
from .models import Article, Category, IPAddress

# admin header title
admin.site.site_header = "مدیریت جنگو"


# action for make some object to publish status
def make_published(modeladmin, request, queryset):
    row_updated = queryset.update(status='p')
    if row_updated == 1:
        message_bit = "منتشر شد"
    else:
        message_bit = "منتشر شدند"
    modeladmin.message_user(request, f"{row_updated} مقاله {message_bit} ")


make_published.short_description = "انتشار مقالات انتخاب شده"


# action for make some object to draft status
def make_draft(modeladmin, request, queryset):
    row_updated = queryset.update(status='d')
    if row_updated == 1:
        message_bit = "پیش نویس شد"
    else:
        message_bit = "پیش نویس شدند"
    modeladmin.message_user(request, f"{row_updated} مقاله {message_bit} ")


make_draft.short_description = "پیش نویس کردن مقالات انتخاب شده"


# action for make some object to true status
def make_true(modeladmin, request, queryset):
    row_updated = queryset.update(status=True)
    if row_updated == 1:
        message_bit = " فعال شد"
    else:
        message_bit = "فعال شدند"
    modeladmin.message_user(request, f"{row_updated} دسته بندی {message_bit}")


make_true.short_description = "فعال کردن دسته بندی های انتخاب شده"


# action for make some object to false status
def make_false(modeladmin, request, queryset):
    row_updated = queryset.update(status=False)
    if row_updated == 1:
        message_bit = " غیر فعال شد"
    else:
        message_bit = "غیر فعال شدند"
    modeladmin.message_user(request, f"{row_updated} دسته بندی {message_bit} ")


make_false.short_description = "غیر فعال کردن دسته بندی های انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'parent', 'status']
    list_filter = (['status'])
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_true, make_false]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumbnail_tag', 'author',
                    'jpublish', 'status', 'is_special', 'category_to_str']
    list_filter = ['category', 'status']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(IPAddress)
# admin.site.disable_action('delete_selected')
