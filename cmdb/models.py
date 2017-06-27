from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.

class Asset(models.Model):
    """
    资产总表，用来存放不同资产公共部分
    """
    asset_type = models.CharField(verbose_name=u'资产类型', max_length=64, choices=settings.ASSET_TYPE_CHOICES,
                                  default=u'server')
    name = models.CharField(verbose_name=u'资产名', max_length=64, unique=True)
    asset_num = models.CharField(verbose_name=u'资产编号', max_length=64, unique=True, null=True, blank=True)
    sn = models.CharField(verbose_name=u'资产SN号', max_length=128, unique=True)
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True)
    management_ip = models.GenericIPAddressField(verbose_name=u'管理IP', blank=True, null=True)
    contract = models.ForeignKey('Contract', verbose_name=u'合同', null=True, blank=True)
    trade_date = models.DateField(verbose_name=u'购买时间', null=True, blank=True)
    expire_date = models.DateField(verbose_name=u'过保修期', null=True, blank=True)
    price = models.FloatField(verbose_name=u'价格', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线', null=True, blank=True)
    tags = models.ManyToManyField('Tags', blank=True)
    admin = models.ForeignKey(User, verbose_name=u'资产管理员', null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='admin_asset')
    operation = models.ForeignKey(User, verbose_name=u'运维人员', null=True, blank=True, related_name='operated_asset')
    cabinet = models.ForeignKey('Cabinet', verbose_name=u'所属机柜', null=True, blank=True)
    status = models.SmallIntegerField(choices=settings.ASSET_STATUS_CHOICES, verbose_name=u'设备状态', default=0)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)
    memo = models.TextField(u'备注', null=True, blank=True)





    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_base_info(self):
        return {
            "id": self.id,
            "hostname": self.name if self.name else "",
            "management_ip": self.management_ip if self.management_ip else "",
            "operation": self.operation.username if self.operation else "",
            "ram": self.ram.capacity if hasattr(self, 'ram') and self.ram.capacity else "",
            "cpu_model": self.cpu.model if hasattr(self, 'cpu') and self.cpu.model else "",
            "os_distribution": self.server.os_distribution if hasattr(self,
                                                                      'server') and self.server.os_distribution else "",
            "status": self.get_status_display()
        }

    def get_info(self):
        return {
            "base": {
                "asset_type": self.get_asset_type_display(),
                "name": self.name if self.name else "",
                "asset_num": self.asset_num if self.asset_num else "",
                "sn": self.sn if self.sn else "",
                "manufactory": self.manufactory.name if self.manufactory else "",
                "management_ip": self.management_ip if self.management_ip else "",
                "contract": self.contract if self.contract else "",
                "trade_date": self.trade_date.strftime("%Y-%m-%d") if self.trade_date else "",
                "expire_date": self.expire_date.strftime("%Y-%m-%d") if self.expire_date else "",
                "price": self.price if self.price else 0,
                "business_unit": self.business_unit if self.business_unit else "",
                "tags": [tag.name for tag in self.tags.all()] if self.tags.all() else [],
                "admin": self.admin.username if self.admin else "",
                "operation": self.operation.username if self.operation else "",
                "cabinet": self.cabinet if self.cabinet else "",
                "create_date": self.create_date.strftime("%Y-%m-%d %H:%M:%S") if self.create_date else "",
                "update_date": self.update_date.strftime("%Y-%m-%d %H:%M:%S") if self.update_date else "",
                "status": self.get_status_display(),
                "memo": self.memo if self.memo else "",

            },
            self.asset_type: getattr(self, self.asset_type).get_info() if hasattr(self,
                                                                                  "server") and self.server else {},
            "logs": [log.get_info() for log in self.logs.all().order_by('-date')] if hasattr(self, "logs")
                                                                                     and self.logs.all() else []
        }

    class Meta:
        verbose_name = u'资产总表'
        verbose_name_plural = u"资产总表"
        permissions = (
            ("view_asset", "Can View Asset"),
        )


class Server(models.Model):
    """
    服务器表
    """
    asset = models.OneToOneField('Asset', related_name='server')
    created_by = models.CharField(verbose_name=u'创建类型', choices=settings.CREATED_BY_CHOICES, max_length=32,
                                  default='auto')
    hosted_on = models.ForeignKey('self', verbose_name=u'宿主机', related_name='hosted_on_server', blank=True, null=True)
    model = models.CharField(verbose_name=u'型号', max_length=128, null=True, blank=True)
    kernel_release = models.CharField(verbose_name=u'内核', max_length=128, null=True, blank=True)
    raid_type = models.CharField(u'raid级别', max_length=512, blank=True, null=True)
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发行版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)

    def __str__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)

    def __unicode__(self):
        return '%s sn:%s' % (self.asset.name, self.asset.sn)

    def get_info(self):
        return {
            "cpu": self.asset.cpu.get_info() if hasattr(self.asset, "cpu") and self.asset.cpu else {},
            "created_by": self.get_created_by_display() if self.created_by else "",
            "hosted_on": self.hosted_on.asset.name if self.hosted_on else "",
            "model": self.model if self.model else "",
            "kernel_release": self.kernel_release if self.kernel_release else "",
            "raid_type": self.raid_type if self.raid_type else "",
            "os_type": self.os_type if self.os_type else "",
            "os_distribution": self.os_distribution if self.os_distribution else "",
            "os_release": self.os_release if self.os_release else "",
            "ram": self.asset.ram.get_info() if hasattr(self.asset, "ram") and self.asset.ram else {},
            "disks": [disk.get_info() for disk in self.asset.disks.all()] if hasattr(self.asset,
                                                                                     "disks") and self.asset.disks else [],
            "nics": [nic.get_info() for nic in self.asset.nics.all()] if hasattr(self.asset,
                                                                                 "nics") and self.asset.nics else [],
        }

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"


class CPU(models.Model):
    """
    CPU表
    """
    asset = models.OneToOneField('Asset', related_name='cpu')
    model = models.CharField(u'CPU型号', max_length=128, blank=True)
    count = models.SmallIntegerField(u'物理cpu个数')
    core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.model

    def __unicode__(self):
        return self.model

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"

    def get_info(self):
        return {
            "count": self.count if self.count else 0,
            "core_count": self.core_count if self.core_count else 0,
            "model": self.model if self.model else "",
            "memo": self.memo if self.memo else "",
            "create_date": self.create_date.strftime("%Y-%m-%d %H:%M:%S") if self.create_date else "",
            "update_date": self.update_date.strftime("%Y-%m-%d %H:%M:%S") if self.update_date else "",
        }


class RAM(models.Model):
    """
    内存表
    """
    asset = models.OneToOneField('Asset', related_name='ram', )
    capacity = models.IntegerField(verbose_name=u'内存大小(MB)')
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return '%s:%s' % (self.asset_id, self.capacity)

    def __unicode__(self):
        return '%s:%s' % (self.asset_id, self.capacity)

    def get_info(self):
        return {
            "capacity": self.capacity if self.capacity else 0,
            "create_date": self.create_date.strftime("%Y-%m-%d %H:%M:%S") if self.create_date else "",
            "update_date": self.update_date.strftime("%Y-%m-%d %H:%M:%S") if self.update_date else "",
            "memo": self.memo if self.memo else "",
        }

    class Meta:
        verbose_name = u'内存'
        verbose_name_plural = u"内存"


class Disk(models.Model):
    """
    本地磁盘表
    """

    asset = models.ForeignKey('Asset', related_name='disks')
    name = models.CharField(verbose_name=u'磁盘名', max_length=64)
    capacity = models.FloatField(verbose_name=u'磁盘容量GB')
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return '%s:name:%s capacity:%s' % (self.asset_id, self.name, self.capacity)

    def __unicode__(self):
        return '%s:name:%s capacity:%s' % (self.asset_id, self.name, self.capacity)

    def get_info(self):
        return {
            "name": self.name if self.name else "",
            "capacity": self.capacity if self.capacity else "",
            "create_date": self.create_date.strftime("%Y-%m-%d %H:%M:%S") if self.create_date else "",
            "update_date": self.update_date.strftime("%Y-%m-%d %H:%M:%S") if self.update_date else "",
            "memo": self.memo if self.memo else "",
        }

    class Meta:
        unique_together = ("asset", "name")
        verbose_name = u'磁盘'
        verbose_name_plural = u"磁盘"


class NIC(models.Model):
    """
    网卡表
    """
    asset = models.ForeignKey('Asset', related_name='nics')
    name = models.CharField(verbose_name=u'网卡名', max_length=64, blank=True, null=True)
    sn = models.CharField(verbose_name=u'SN号', max_length=128, blank=True, null=True)
    mac_address = models.CharField(verbose_name=u'MAC', max_length=64, blank=True, null=True)
    ip_address = models.GenericIPAddressField(verbose_name=u'IP', blank=True, null=True)
    netmask = models.CharField(verbose_name=u'子网掩码', max_length=64, blank=True, null=True)
    memo = models.CharField(verbose_name=u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间', blank=True, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间', blank=True, null=True)

    def __str__(self):
        return '%s:%s' % (self.asset_id, self.mac_address)

    def __unicode__(self):
        return '%s:%s' % (self.asset_id, self.mac_address)

    def get_info(self):
        return {
            "name": self.name if self.name else "",
            "sn": self.sn if self.sn else "",
            "mac_address": self.mac_address if self.mac_address else "",
            "ip_address": self.ip_address if self.ip_address else "",
            "netmask": self.netmask if self.netmask else "",
            "create_date": self.create_date.strftime("%Y-%m-%d %H:%M:%S") if self.create_date else "",
            "update_date": self.update_date.strftime("%Y-%m-%d %H:%M:%S") if self.update_date else "",
            "memo": self.memo if self.memo else "",
        }

    class Meta:
        unique_together = ("asset", "name", "mac_address")
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"


class Manufactory(models.Model):
    """
    厂商表
    """
    name = models.CharField(verbose_name=u'厂商名称', max_length=64, unique=True)
    contact = models.CharField(verbose_name=u'联系电话', max_length=30, blank=True, null=True)
    memo = models.CharField(verbose_name=u'备注', max_length=128, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'设备厂商'
        verbose_name_plural = u"设备厂商"


class Cabinet(models.Model):
    """
    机柜表
    """
    id = models.BigIntegerField(primary_key=True)
    room = models.ForeignKey('MachineRoom', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u"所属机房")
    number = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"机柜编号")
    slotcount = models.IntegerField(null=True, blank=True, verbose_name=u"槽位数(U)")
    memo = models.CharField(verbose_name=u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.number

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name = u'机柜'
        verbose_name_plural = u'机柜'


class MachineRoom(models.Model):
    """
    机房表
    """
    id = models.BigIntegerField(primary_key=True)
    center = models.ForeignKey('DataCenter', related_name="related_rooms",
                               on_delete=models.SET_NULL, null=True, blank=True, verbose_name=u"所属中心")
    name = models.CharField(max_length=100, verbose_name=u"机房名称")
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"机房地址")
    admin = models.ForeignKey(User, verbose_name=u'负责人', null=True, blank=True, on_delete=models.SET_NULL)
    contact = models.CharField(verbose_name=u'联系电话', max_length=30, blank=True, null=True)
    memo = models.CharField(verbose_name=u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return "{0}:{1}".format(self.center, self.name)

    class Meta:
        verbose_name_plural = u"机房"
        verbose_name = u"机房"


class DataCenter(models.Model):
    """
    数据中心
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"数据中心")
    admin = models.ForeignKey(User, verbose_name=u'负责人', null=True, blank=True, on_delete=models.SET_NULL)
    contact = models.CharField(verbose_name=u'联系电话', max_length=30, null=True, blank=True)
    memo = models.CharField(verbose_name=u'备注', max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"数据中心"
        verbose_name = u"数据中心"


class BusinessUnit(models.Model):
    """
    业务线表
    """
    parent_unit = models.ForeignKey('self', verbose_name=u'父业务线', related_name='parent_level', blank=True, null=True)
    name = models.CharField(verbose_name=u'业务线', max_length=64, unique=True)
    memo = models.CharField(verbose_name=u'备注', max_length=64, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"

    def get_info(self):
        return {
            "id": self.id,
            "parent": self.parent_unit.name if self.parent_unit else "",
            "name": self.name,
            "memo": self.memo
        }


class Contract(models.Model):
    """
    合同表
    """
    sn = models.CharField(verbose_name=u'合同号', max_length=128, unique=True)
    name = models.CharField(verbose_name=u'合同名称', max_length=64)
    price = models.IntegerField(verbose_name=u'合同金额')
    detail = models.TextField(verbose_name=u'合同详细', blank=True, null=True)
    start_date = models.DateField(verbose_name=u'合同开始时间', blank=True, null=True)
    end_date = models.DateField(verbose_name=u'合同结束时间', blank=True, null=True)
    file = models.FileField(upload_to='uploads/contract', verbose_name=u'合同文件', null=True, blank=True)
    create_date = models.DateField(verbose_name=u'创建时间', auto_now_add=True, null=True, blank=True)
    update_date = models.DateField(verbose_name=u'更新时间', auto_now=True, null=True, blank=True)
    memo = models.TextField(verbose_name=u'备注', blank=True, null=True)

    def __str__(self):
        return self.sn

    def __unicode__(self):
        return self.sn

    class Meta:
        verbose_name = u'合同'
        verbose_name_plural = u"合同"


class Tags(models.Model):
    """
    标签表
    """
    name = models.CharField(verbose_name=u'标签名', max_length=32, unique=True)
    create_date = models.DateField(verbose_name=u'创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u"标签"


class EventLog(models.Model):
    asset = models.ForeignKey('Asset', related_name="logs")
    event_type = models.SmallIntegerField(u'事件类型', choices=settings.EVENT_TYPE_CHOICES)
    operater = models.CharField(u"操作人", max_length=100, null=True, blank=True)
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    memo = models.TextField(u'备注', blank=True, null=True)

    def __str__(self):
        return self.detail

    def get_info(self):
        return {
            "event_type": self.get_event_type_display(),
            "operater": self.operater if self.operater else "",
            "component": self.component if self.component else "",
            "detail": self.detail if self.detail else "",
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S") if self.date else ""
        }

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"
