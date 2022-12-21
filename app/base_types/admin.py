from django.contrib import admin

from .models import Cabinets, PhDLDconnections, Terminals, LogicDevices, LogicNodeInstantiated, LogicNodesTypes, \
    LNobject, CDCs, DataObjects, Statuses, Datasets, Signals, ClueAttrs, LDLNconnections, \
    SwitchesAndLNs, Input, Switch, LNtypeObjConnections, SG_modes

class SG_modesAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name',)
    list_filter = ('name',)
admin.site.register(SG_modes,SG_modesAdmin)


class LNtypeObjConnectionsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('ln_type', 'ln_obj')
    list_filter = ('ln_type',)
admin.site.register(LNtypeObjConnections,LNtypeObjConnectionsAdmin)
'''
class InputsAndLNsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('input', 'ln')
    list_filter = ('input',)
admin.site.register(InputsAndLNs,InputsAndLNsAdmin)
'''
class SwitchesAndLNsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('switch', 'ln')
    list_filter = ('switch',)
admin.site.register(SwitchesAndLNs,SwitchesAndLNsAdmin)

class InputAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('ln_inst', 'name', 'number', 'sw_type', 'sw_name', 'description')
    list_filter = ('ln_inst',)
admin.site.register(Input,InputAdmin)

class SwitchAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('sw_type', 'short_name', 'description')
    list_filter = ('sw_type',)
admin.site.register(Switch,SwitchAdmin)

class CabinetsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'terminal1', 'terminal2', 'terminal3', 'description')
    list_filter = ('name',)
admin.site.register(Cabinets,CabinetsAdmin)

class PhDLDconnectionsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('ied', 'ld')
    list_filter = ('ied',)
admin.site.register(PhDLDconnections, PhDLDconnectionsAdmin)

class LDLNconnectionsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('ld', 'ln')
    list_filter = ('ld', 'ln')
admin.site.register(LDLNconnections, LDLNconnectionsAdmin)
'''
class LNobjConnectionsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('ln_inst', 'ln_obj')
    list_filter = ('ln_inst', 'ln_obj')
admin.site.register(LNobjConnections, LNobjConnectionsAdmin)

'''
class TerminalsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'description')
    list_filter = ('name',)
admin.site.register(Terminals, TerminalsAdmin)

class LogicDevicesAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'fb_name', 'description')
    list_filter = ('name',)
admin.site.register(LogicDevices, LogicDevicesAdmin)

class LogicNodeInstantiatedAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('short_name', 'full_name', 'ln_prefix', 'class_name', 'instance', 'ln_type')
    list_filter = ('short_name',)
admin.site.register(LogicNodeInstantiated, LogicNodeInstantiatedAdmin)

class LogicNodesTypesAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', 'description','explanation')
    list_filter = ('name',)
admin.site.register(LogicNodesTypes, LogicNodesTypesAdmin)

class LNobjectAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('data_object','cdc', 'signal', 'status', 'clue_attr', 'cus', 'rdu', 'ras', 'dataset', 'sgras_name','sg_modes', 'signal_type', 'signal_number')
    list_filter = ('data_object',)
admin.site.register(LNobject, LNobjectAdmin)


class CDCsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name',)
    list_filter = ('name',)
admin.site.register(CDCs,CDCsAdmin)


class ClueAttrsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', )
    list_filter = ('name',)
admin.site.register(ClueAttrs,ClueAttrsAdmin)


class DataObjectsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name',)
    list_filter = ('name',)
admin.site.register(DataObjects,DataObjectsAdmin)


class StatusesAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name',)
    list_filter = ('name',)
admin.site.register(Statuses, StatusesAdmin)


class DatasetsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name',)
    list_filter = ('name',)
admin.site.register(Datasets, DatasetsAdmin)


class SignalsAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ('name', )
    list_filter = ('name',)
admin.site.register(Signals, SignalsAdmin)

