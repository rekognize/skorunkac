from django.contrib import admin
from skorunkac.cities.models import City, District


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass
