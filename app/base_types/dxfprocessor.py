import ezdxf
import io
from django.http import HttpResponse
from .models import Cabinets, PhDLDconnections, LogicDevices, Input, LDLNconnections, LogicNodeInstantiated, \
    LNtypeObjConnections, LNobject
from .dxfdraw import draw_func

MARGIN_LEFT = 25 # отступ от края ФБ для функции
MARGIN_TOP = 10 # отступ от края ФБ для функции
DISTANCE_BTW_FUNCS = 10
# выбираем логические блоки, которые нужно нарисовать
def render_dxf(doc, msp, ied, cab):
    format_dxf = 'apt' # как пример
    DISTANCE_BTW_FB = 320
    x = 0
    y = 0
    pointers = [0, 0, 0, 0] # координаты по х (жестко задаются): аналог, ммс асу, гус , ммс фк. Координаты по У - они меняются
    pointer_output = 0
    # ищем лог. устройства в терминале
    #func_name = 'БУ_ДТЗ'
    #inputs = Input.objects.all().filter(ln_inst=func_name)
    #for input in inputs:
        #print(input.name)

    coord_x = x + MARGIN_LEFT
    coord_y = y + MARGIN_TOP



    connections = PhDLDconnections.objects.all().filter(ied=ied)
    for item in connections:
        ld = LogicDevices.objects.get(name=item.ld)
        print('*******', ld.fb_name)
        ldln_conns = LDLNconnections.objects.all().filter(ld=item.ld)
        for ldln_conn in ldln_conns:

            _ru_ln_name = str(ldln_conn.ln).split('_')[0]  # отрезаем часть после подчеркивания
            #print('===========>>>', _ru_ln_name)
            got_ln = LogicNodeInstantiated.objects.get(short_name=ldln_conn.ln)  # ищем тип ЛУ, чтобы вывести его объекты

            inputs = Input.objects.all().filter(ln_inst=ldln_conn.ln).order_by('name')

            lnobj_conns = LNtypeObjConnections.objects.all().filter(ln_type=got_ln.ln_type)
            #print(got_ln.ln_type, '(((((((((((((((((((',lnobj_conns)

            testoutputs = (
            ('АРН АТ', 'БУ', 'Индикация состояния', 'ATATCC', '', 'LLN0', 'Beh', '{Beh}', 'ENS', 22, '*', '', '',
             '', '', 0, 'dsrpt_DT'),)
            testswitches = (('SW.3', 'Направленность', ' '),)

            objs = []
            for obj in lnobj_conns:
                obj_obj = LNobject.objects.get(pk=obj.ln_obj_id)
                #print('-----------',obj_obj)
                objs.append(obj_obj)
            print(objs)

            l, pointer_output = draw_func(msp, pointer_output, format_dxf, coord_x, coord_y, func_name=(_ru_ln_name, got_ln.full_name, False),
                      inputs=inputs,
                      outputs=testoutputs, switches=testswitches)
            #print('pointer_output', l)
            coord_y = l + DISTANCE_BTW_FUNCS + coord_y

        x += DISTANCE_BTW_FB






def dxf_report(request, cab):
    doc = ezdxf.readfile('base_types/templates/template.dxf')
    msp = doc.modelspace()

    # ищем шкаф в базе
    cabinet = Cabinets.objects.get(name=cab)
    # анализируем состав шкафа
    ied1 = cabinet.terminal1
    ied2 = cabinet.terminal2
    ied3 = cabinet.terminal3

    if ied1:
        render_dxf(doc, msp, ied1, cab)
    # Save the DXF document.
    doc.saveas("test.dxf")
    # СОХРАНЕНИЕ ДОКУМЕНТА

    bio = io.StringIO()
    doc.write(bio)  # save to memory stream
    length = bio.tell()
    #print(length, '++++++++++++++++++')
    bio.seek(0)  # rewind the stream

    response = HttpResponse(
        bio.getvalue(),  # use the stream's contents
        content_type="image/x-dxf",
    )

    response["Content-Disposition"] = 'attachment; filename = {0}'.format(cab.split(' ')[1] + ".dxf")
    response["Content-Encoding"] = "UTF-8"
    response['Content-Length'] = length

    return response