from django.shortcuts import render
from django.http import HttpResponse

from .models import Cabinets, Terminals, PhDLDconnections, LogicDevices, LogicNodesTypes, DataObjects, LDLNconnections, \
    LogicNodeInstantiated, LNobject, LNtypeObjConnections
from .wordprocessor import word_report
from .dxfprocessor import dxf_report

def index(request):
    return render(request, 'base_types/main.html')

def reports(request):
    cabinets = Cabinets.objects.all()
    cabinets = cabinets.order_by('name')
    cabinets1 = list() # шкафы 1 архитектуры
    cabinets2 = list() # шкафы 2 архитектуры
    for cabinet in cabinets:
        if cabinet.name[-1] =='1':
            cabinets1.append(cabinet)
        else:
            cabinets2.append(cabinet)
    return render(request, 'base_types/reports.html', {'cabinets1': cabinets1, 'cabinets2': cabinets2 })

def get_report(request):
    cab = request.GET.get('name')
    type = request.GET.get('type')
    if type == 'cabinet':
        return word_report(request, cab)
    if type == 'dxf':
        return dxf_report(request, cab)


# показываем шкаф
def cabinet(request):
    cab = request.GET.get('name')
    type = request.GET.get('type')
    cabinet= Cabinets.objects.get(name=cab)
    print('OK', cabinet.terminal1)
    return render(request, 'base_types/cabinet.html', {'cabinet': cabinet})



def show(request):
    name = request.GET.get('name')
    type = request.GET.get('type')

# -------------------------------обработка ied------------------------------
    if type == 'ied':
        ied = Terminals.objects.get(name=name)
        conns = PhDLDconnections.objects.all().filter(ied_id=ied.id)
        conns = conns.order_by('ld')
        lds = list()
        for item in conns.iterator():
            obj = LogicDevices.objects.get(name=item.ld)
            #print(obj)
            lds.append(obj)
        lds.sort(key=lambda x: x.name)
        return render(request, 'base_types/showld.html', {'ied': ied, 'lds': lds})

# -------------------------------обработка ld------------------------------
    if type == 'ld':
        ld = LogicDevices.objects.get(name=name)
        lns_conns = LDLNconnections.objects.all().filter(ld_id=ld.id)
        lns_conns = lns_conns.order_by('ld')

        lns = list()
        for item in lns_conns.iterator():
            print('------------>', item.ln)
            ln = LogicNodeInstantiated.objects.get(short_name=item.ln)
            #print(ln)
            lns.append(ln)
        lns.sort(key=lambda x: x.class_name)
        return render(request, 'base_types/showldobj.html', {'ld':ld, 'lns': lns})

    # -------------------------------обработка ln------------------------------
    if type == 'ln':
        lntype = LogicNodesTypes.objects.get(name=name)
        #print('++++++++++++++', lntype.id)
        #fb = LogicNodeInstantiated.objects.filter(ln_type=lntype.id).first()
        #print(fb.short_name)
        #fb_desc = LogicNodeInstantiated.objects.get(short_name=fb)
        #fb_desc = LogicNodeInstantiated.objects.all().filter(ln_type=lntype)
        objects = LNtypeObjConnections.objects.all().filter(ln_type=lntype.id)

        objs = list()
        for item in objects.iterator():
            print('------------>', item.ln_obj)
            object_id = DataObjects.objects.get(name=item.ln_obj)
            object = LNobject.objects.get(data_object=object_id)
            objs.append(object)
            print('------------>', objs)
        objs.sort(key=lambda x: (str(x.dataset), str(x.func_group))) #str(x.cdc)[2], str(x.cdc)[0]
        return render(request, 'base_types/showlnobj.html', {'objs': objs, 'lntype':lntype})

def lntypes(request):
    lntypes = LogicNodesTypes.objects.all()
    return render(request, 'base_types/lntypes.html', {'lntypes':lntypes})

def connslntype(request):
    name = request.GET.get('name')
    type = request.GET.get('type')
    if type == 'ln_type':
        lntype = LogicNodesTypes.objects.get(name=name)
        ln_inst = LogicNodeInstantiated.objects.all().filter(ln_type=lntype.id)
        for inst in ln_inst:
            print(inst.short_name)
        return render(request, 'base_types/conns.html', {'ln_type': name, 'ln_inst':ln_inst})
    if type == 'inst_ln':
        lntype = request.GET.get('lntype')
        ln_id = LogicNodeInstantiated.objects.get(short_name=name)
        print('>', ln_id.id)
        lds = LDLNconnections.objects.all().filter(ln=ln_id.id)
        objs = list()
        for ld in lds:
            print('>>>>>>', ld.ld)
            #objs.append(ld)
            ldevice = LogicDevices.objects.get(name=ld.ld)
            print('>>>>>+', ldevice.fb_name)
            objs.append(ldevice)
        return render(request, 'base_types/connsfb.html', {'fb': name, 'lntype':lntype, 'objs': objs})
    return HttpResponse('error')