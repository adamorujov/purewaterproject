from django.contrib import admin
from mainpage.models import SettingsModel, ServiceModel, SocialMediaModel, CategoryModel, OurProductModel, TestimonialModel
from django.contrib.auth.models import Group

@admin.register(SettingsModel)
class SettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("SAYTIN ƏSAS PARAMETRLƏRİ", {'fields': ('logo', 'slogan', 'favicon')}),
        ("META PARAMETRLƏR", {'fields': ('keywords', 'description')}),
        ("BANNER", {'fields': ('banner_title', 'banner_text', 'banner_image1', 'banner_image2')}), 
        ("HAQQIMIZDA", {'fields': ('about_text', 'about_image1', 'about_image2')}),  
        ("ƏLAQƏ MƏLUMATLARI", {'fields': ('contact_number', 'email', 'address')}), 
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
admin.site.register(ServiceModel)
admin.site.register(SocialMediaModel)

admin.site.register(CategoryModel)

@admin.register(OurProductModel)
class OurProductAdmin(admin.ModelAdmin):
    list_display = ("__str__", "price", "category")
    search_fields = ("title", "category__name")
    list_filter = ("category",)

admin.site.register(TestimonialModel)

admin.site.unregister(Group)   

admin.site.site_title = "Pure Water Administrasiyası"
admin.site.site_header = "Pure Water Administrasiyası"

def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        for app in app_list:
            if app['app_label'] == 'mainpage':
                ordering = {
                    "Parametrlər": 1,
                    "Sosial medialar": 2,
                    "Xidmətlər": 3,
                    "Kateqoriyalar": 4,
                    "Məhsullar": 5,
                    "Müştəri rəyləri": 6
                }
                app['models'].sort(key=lambda x: ordering[x['name']])
            if app['app_label'] == 'productapp':
                ordering = {
                    "Məhsullar": 1,
                    "Hədiyyələr": 2,
                    "Şəhərlər": 3,
                    "Rayonlar": 4,
                    "Kəndlər": 5
                }
                app['models'].sort(key=lambda x: ordering[x['name']])
            if app['app_label'] == 'registrationapp':
                ordering = {
                    "Müştərilər": 1,
                    "Ödəniş məlumatları": 2,
                    "Satıcılar": 3,
                    "Qeydiyyatlar": 4,
                    "Taksit məlumatları": 5,
                    "Taksitlər": 6,
                    "Əlavə ödənişlər": 7,
                    "Filter dəyişdirənlər": 8,
                    "Filtir dəyişimləri": 9,
                    "Servis edən şəxslər": 10,
                    "Servis xidmətləri": 11,
                    "Kreditorlar": 12
                }
                app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list

admin.AdminSite.get_app_list = get_app_list
