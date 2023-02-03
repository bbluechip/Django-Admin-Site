from django.contrib import admin
from .models import Product, Review, Category
from django.utils import timezone
from django.utils.safestring import mark_safe
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, DropdownFilter
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from .resources import ReviewResource
from import_export.admin import ImportExportModelAdmin


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 2
    classes = ('collapse',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "create_date", "is_in_stock", "update_date",
                    "added_days_ago", "how_many_reviews", "bring_img_to_list")
    list_editable = ("is_in_stock",)
    # list_display_links = ("create_date",)
    list_filter = ("is_in_stock", ("create_date", DateTimeRangeFilter))
    # ordering = ("-update_date",)
    search_fields = ("name",)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25
    date_hierarchy = "update_date"
    # fields = (('name', 'slug'), 'description', "is_in_stock")
    inlines = (ReviewInline,)

    readonly_fields = ("bring_image",)
    fieldsets = (
        (None, {
            "fields": (
                # to display multiple fields on the same line, wrap those fields in their own tuple
                ('name', "slug"), "is_in_stock"
            ),
            # 'classes': ('wide', 'extrapretty'), wide or collapse
        }),
        ('My section', {
            "classes": ("collapse", ),
            "fields": ("description", "categories", "product_img", "bring_image"),
            'description': "You can use this section for optionals settings"
        })
    )

    filter_vertical = ("categories", )
    actions = ("is_in_stock", )

    def is_in_stock(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f"{count} çeşit ürün stoğa eklendi")

    is_in_stock.short_description = 'İşaretlenen ürünleri stoğa ekle'

    def added_days_ago(self, product):
        fark = timezone.now() - product.create_date
        return fark.days

    def how_many_reviews(self, obj):
        count = obj.reviews.count()
        return count

    def bring_image(self, obj):
        if obj.product_img:
            return mark_safe(f"<img src={obj.product_img.url} width=400 height=400></img>")
        return mark_safe(f"<h3>{obj.name} has not image </h3>")

    def bring_img_to_list(self, obj):
        if obj.product_img:
            return mark_safe(f"<img src={obj.product_img.url} width=50 height=50></img>")
        return mark_safe("******")

    bring_img_to_list.short_description = "product_image"


class ReviewAdmin(ImportExportModelAdmin):
    list_display = ('__str__', 'created_date', 'is_released')
    list_per_page = 50
    raw_id_fields = ('product',)
    # list_filter = ("product",)
    list_filter = (
        ('product', RelatedDropdownFilter),
    )
    resource_class = ReviewResource


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)

admin.site.site_title = "bbluechip Title"
admin.site.site_header = "bbluechip Admin Portal"
admin.site.index_title = "Welcome to bbluechip Admin Portal"
