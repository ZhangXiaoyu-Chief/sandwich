from django.contrib import admin
from cmdb import models


# Register your models here.

class ServerInline(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)
    # readonly_fields = ['create_date']


class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']


class NICInline(admin.TabularInline):
    model = models.NIC
    extra = 1
    exclude = ('memo',)
    readonly_fields = ['create_date']


class RAMInline(admin.TabularInline):
    model = models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']


class DiskInline(admin.TabularInline):
    extra = 1
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_type', 'sn', 'name', 'manufactory', 'management_ip', 'cabinet', 'business_unit',
                    'admin', 'trade_date', 'status')
    inlines = [ServerInline, CPUInline, RAMInline, DiskInline, NICInline]
    search_fields = ['sn', ]
    choice_fields = ('asset_type', 'status')
    fk_fields = ('manufactory', 'cabinet', 'business_unit', 'admin')
    list_per_page = 20
    list_filter = ('asset_type', 'status', 'manufactory', 'cabinet', 'business_unit', 'admin', 'create_date')
    dynamic_fk = 'asset_type'
    dynamic_list_display = ('model', 'sub_asset_type', 'os_type', 'os_distribution')
    dynamic_choice_fields = ('sub_asset_type',)
    m2m_fields = ('tags',)

admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.EventLog)
admin.site.register(models.Tags)
admin.site.register(models.BusinessUnit)
