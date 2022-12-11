from django.shortcuts import render
from django.http import HttpResponse

from .models import Cabinets, Terminals, PhDLDconnections, LogicDevices, LogicNodesTypes, DataObjects, LDLNconnections, \
    LogicNodeInstantiated, LNobjConnections, LNobject
from .wordprocessor import word_report

def index(request):
    return render(request, 'base_types/main.html')

def reports(request):
    cabinets = Cabinets.objects.all()
    cabinets = cabinets.order_by('name')

    return render(request, 'base_types/reports.html', {'cabinets': cabinets})

def get_report(request):
    cab = request.GET.get('name')
    type = request.GET.get('type')
    if type == 'cabinet':
        return word_report(request, cab)
    else:
        return HttpResponse('')

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

        return render(request, 'base_types/showldobj.html', {'ld':ld, 'lns': lns})

    # -------------------------------обработка ln------------------------------
    if type == 'ln':
        lntype = LogicNodesTypes.objects.get(name=name)
        print('++++++++++++++', lntype.id)
        fb = LogicNodeInstantiated.objects.get(ln_type=lntype.id)
        print(fb.short_name)
        fb_desc = LogicNodeInstantiated.objects.get(short_name=fb)
        objects = LNobjConnections.objects.all().filter(ln_inst=fb.id)

        objs = list()
        for item in objects.iterator():
            print('------------>', item.ln_obj)
            object_id = DataObjects.objects.get(name=item.ln_obj)
            object = LNobject.objects.get(data_object=object_id)
            objs.append(object)
            print('------------>', objs)
        return render(request, 'base_types/showlnobj.html', {'fb': fb_desc, 'objs': objs})


