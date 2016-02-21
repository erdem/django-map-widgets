from django.contrib.gis import admin
from cities.models import City, District


class DistrictAdminInline(admin.TabularInline):
    model = District
    extra = 3


class CityAdmin(admin.ModelAdmin):
    inlines = (DistrictAdminInline,)


class DistrictAdmin(admin.ModelAdmin):
    pass


admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
