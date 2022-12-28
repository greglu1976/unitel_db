import ezdxf
import re
from django.http import HttpResponse
from django.http import FileResponse
from .models import Cabinets, PhDLDconnections, LogicDevices, Input, LDLNconnections, LogicNodeInstantiated, \
    LNtypeObjConnections, LNobject
from .dxfdraw import draw_func

MARGIN_LEFT = 25 # отступ от края ФБ для функции
MARGIN_TOP = 10 # отступ от края ФБ для функции
DISTANCE_BTW_FUNCS = 10
FBLOCK_LENGTH = 110 # длина блока, стандартная
MARGIN_BOTTOM = 5
START_FB_INPUTS = 10 # начало входов ФБ
INPUT_LINE_LENGTH = 95
DISTANCE_BTW_FB_INPUTS = 5
INPUT_TEXT_LENGTH = 92

SETTINGS = ('ASG', 'ING', 'SPG', 'ENG')
from .dxfconfig import RENDER_SIGNAL_NUMBERS, RENDER_SIGNAL_NUMBERS_RIGHT

# выбираем логические блоки, которые нужно нарисовать
def render_dxf(doc, msp, ied, cab):
    format_dxf = 'apt' # как пример
    DISTANCE_BTW_FB = 320
    x = 0
    y = 0
    pointers = [0, 0, 0, 0] # координаты по х (жестко задаются): аналог, ммс асу, гус , ммс фк. Координаты по У - они меняются
    pointer_output = 0



    connections = PhDLDconnections.objects.all().filter(ied=ied)
    for item in connections:
        coord_x = x + MARGIN_LEFT
        coord_y = y + MARGIN_TOP

        ld = LogicDevices.objects.get(name=item.ld)
        _ld_fb_name = ld.fb_name
        print('*******', ld.fb_name)

        all_inputs = [] # попробуем сюда собрать все входы
        ldln_conns = LDLNconnections.objects.all().filter(ld=item.ld).order_by('ln') # хрен знает, работает этот фильтр или нет....
        for ldln_conn in ldln_conns:
            _ru_ln_name = str(ldln_conn.ln).split('_')[0]  # отрезаем часть после подчеркивания
            #print('===========>>>', _ru_ln_name)
            got_ln = LogicNodeInstantiated.objects.get(short_name=ldln_conn.ln)  # ищем тип ЛУ, чтобы вывести его объекты
            inputs = Input.objects.all().filter(ln_inst=ldln_conn.ln).order_by('name')
            all_inputs.extend(inputs)
            lnobj_conns = LNtypeObjConnections.objects.all().filter(ln_type=got_ln.ln_type).order_by('ln_obj') # хрен знает, работает этот фильтр или нет....
            objs = []
            switches = []
            for obj in lnobj_conns:
                obj_obj = LNobject.objects.get(pk=obj.ln_obj_id)
                #print('obj_obj.cdc', obj_obj.cdc)
                if not str(obj_obj.cdc) in SETTINGS:
                    objs.append(obj_obj)
                if str(obj_obj.cdc) in ('SPG', 'ENG'):
                    switches.append(obj_obj)
            l, pointer_output = draw_func(msp, pointer_output, format_dxf, coord_x, coord_y, func_name=(_ru_ln_name, got_ln.full_name, False, _ld_fb_name),
                      inputs=inputs,
                      outputs=objs, switches=switches)
            coord_y = l + DISTANCE_BTW_FUNCS + coord_y

        # ПРОСТАВЛЯЕМ ВХОДЫ У ФУНКЦ БЛОКА

        # отладочная часть, вроде работает - оставлена пока как есть----------------------
        #print('all_inputs', all_inputs)
        no_dubs_inputs_name = []
        no_dubs_inputs = []
        for input in all_inputs:
            print('input name: ', input.name)
            if not input.name in no_dubs_inputs_name:
                no_dubs_inputs.append(input)
                no_dubs_inputs_name.append(input.name)
        all_inputs = no_dubs_inputs
        all_inputs.sort(key=lambda x: x.name)
        # отладочная часть-----------------------------------------------------------------

        coord_input = y
        for input in all_inputs:
            msp.add_line((x, - coord_input - START_FB_INPUTS), (x - INPUT_LINE_LENGTH, - coord_input - START_FB_INPUTS),
                         dxfattribs={'layer': 'Линии связи'})
            # обозначение входа внутри ФБ
            mtext = msp.add_mtext(
                input.name,
                dxfattribs={
                    "layer": "Основная",
                    "style": "Narrow"
                })
            mtext.set_location(insert=(x + 1, - coord_input - START_FB_INPUTS, 0), rotation=0,
                               attachment_point=4)
            mtext.dxf.width = 50

            # обозначения входа снаружи ФБ

            # проставляем номер входа в слое Сигнатура слева
            delta = 0
            if input.number != 0 and RENDER_SIGNAL_NUMBERS_RIGHT:
                delta = 9  # расстояние от начала линии до надписи внешнего входа
                mtext = msp.add_mtext(
                    str("{:04d}".format(input.number)),
                    dxfattribs={
                        "layer": 'Сигнатура',
                        "style": "Narrow"
                    })
                mtext.set_location(insert=(x - INPUT_TEXT_LENGTH - 2, - coord_input - START_FB_INPUTS + 2, 0),
                                   rotation=0,
                                   attachment_point=4)
                mtext.dxf.width = 10
                mtext.dxf.defined_height = 4

            full_input_name = input.description

            if input.number != 0 and RENDER_SIGNAL_NUMBERS:
                full_input_name = '[' + str(input.number) + '] ' + full_input_name

            layer = 'GOOSE'
            if 'A' in input.name:
                layer = 'Вход-Аналоги'
            if 'C' in input.name:
                layer = 'MMS'
            if 'D' in input.name and '/' in input.description:
                layer = 'Сигналы внутр.'
            if input.number <= 99 and input.number >= 1:
                layer = 'Вход-Дискреты'

            mtext = msp.add_mtext(
                full_input_name,
                dxfattribs={
                    "layer": layer,
                    "style": "Narrow"
                })
            mtext.set_location(insert=(x - INPUT_TEXT_LENGTH + delta - 2, - coord_input - START_FB_INPUTS + 2, 0),
                               rotation=0,
                               attachment_point=4)
            mtext.dxf.width = INPUT_TEXT_LENGTH
            mtext.dxf.defined_height = 4

            coord_input = coord_input + DISTANCE_BTW_FB_INPUTS

            # ЭКСПЕРИМЕНТАЛЬНАЯ ФИЧА - вынес всех входов ФБ за пределы
            # необходимо вынести три столба входов: аналоги, ммс, гуси - соответственно координаты pointer_anal, pointer_mms, pointer_goose
            # это координаты по Y, координаты по Х жесткие
            x_analogue = -500
            x_mms_asu = -400
            x_mms_fk = -300
            x_goose = -200

            # ищем аналоги
            if 'A' in input.name:
                msp.add_line((x_analogue, - pointers[0] * 5), (x_analogue + INPUT_LINE_LENGTH, - pointers[0] * 5),
                             dxfattribs={'layer': 'Линии связи'})

                mtext = msp.add_mtext(
                    full_input_name,
                    dxfattribs={
                        "layer": 'Вход-Аналоги',
                        "style": "Narrow"
                    })
                mtext.set_location(insert=(x_analogue + 1, - pointers[0] * 5 + 2, 0),
                                   rotation=0,
                                   attachment_point=4)
                mtext.dxf.width = INPUT_TEXT_LENGTH
                mtext.dxf.defined_height = 4

                # проставляем номер

                mtext = msp.add_mtext(
                    str("{:04d}".format(input.number)),
                    dxfattribs={
                        "layer": 'Сигнатура',
                        "style": "Narrow"
                    })
                mtext.set_location(insert=(x_analogue + INPUT_LINE_LENGTH - 1, - pointers[0] * 5 + 2, 0), rotation=0,
                                   attachment_point=6)
                mtext.dxf.width = 10
                mtext.dxf.defined_height = 4

                pointers[0] = pointers[0] + 1
            # ищем MMS
            if 'C' in input.name:
                if '92' in str(input.number):
                    msp.add_line((x_mms_asu, - pointers[1] * 5), (x_mms_asu + INPUT_LINE_LENGTH, - pointers[1] * 5),
                                 dxfattribs={'layer': 'Линии связи'})

                    mtext = msp.add_mtext(
                        full_input_name,
                        dxfattribs={
                            "layer": 'MMS',
                            "style": "Narrow"
                        })
                    mtext.set_location(insert=(x_mms_asu + 1, - pointers[1] * 5 + 2, 0),
                                       rotation=0,
                                       attachment_point=4)
                    mtext.dxf.width = INPUT_TEXT_LENGTH
                    mtext.dxf.defined_height = 4

                    # проставляем номер

                    mtext = msp.add_mtext(
                        str("{:04d}".format(input.number)),
                        dxfattribs={
                            "layer": 'Сигнатура',
                            "style": "Narrow"
                        })
                    mtext.set_location(insert=(x_mms_asu + INPUT_LINE_LENGTH - 1, - pointers[1] * 5 + 2, 0), rotation=0,
                                       attachment_point=6)
                    mtext.dxf.width = 10
                    mtext.dxf.defined_height = 4

                    pointers[1] = pointers[1] + 1
                else:
                    msp.add_line((x_mms_fk, - pointers[3] * 10), (x_mms_fk + INPUT_LINE_LENGTH, - pointers[3] * 10),
                                 dxfattribs={'layer': 'Линии связи'})

                    mtext = msp.add_mtext(
                        full_input_name,
                        dxfattribs={
                            "layer": 'MMS',
                            "style": "Narrow"
                        })
                    mtext.set_location(insert=(x_mms_fk + 1, - pointers[3] * 10 + 2, 0),
                                       rotation=0,
                                       attachment_point=4)
                    mtext.dxf.width = INPUT_TEXT_LENGTH
                    mtext.dxf.defined_height = 4

                    # проставляем номер

                    mtext = msp.add_mtext(
                        str("{:04d}".format(input.number)),
                        dxfattribs={
                            "layer": 'Сигнатура',
                            "style": "Narrow"
                        })
                    mtext.set_location(insert=(x_mms_fk + INPUT_LINE_LENGTH - 1, - pointers[3] * 10 + 2, 0), rotation=0,
                                       attachment_point=6)
                    mtext.dxf.width = 10
                    mtext.dxf.defined_height = 4

                    pointers[3] = pointers[3] + 1

            # ищем GOOSE
            if 'D' in input.name and not '/' in input.description:
                msp.add_line((x_goose, - pointers[2] * 5), (x_goose + INPUT_LINE_LENGTH, - pointers[2] * 5),
                             dxfattribs={'layer': 'Линии связи'})

                mtext = msp.add_mtext(
                    full_input_name,
                    dxfattribs={
                        "layer": 'GOOSE',
                        "style": "Narrow"
                    })
                mtext.set_location(insert=(x_goose + 1, - pointers[2] * 5 + 2, 0),
                                   rotation=0,
                                   attachment_point=4)
                mtext.dxf.width = INPUT_TEXT_LENGTH
                mtext.dxf.defined_height = 4

                # проставляем номер

                mtext = msp.add_mtext(
                    str("{:04d}".format(input.number)),
                    dxfattribs={
                        "layer": 'Сигнатура',
                        "style": "Narrow"
                    })
                mtext.set_location(insert=(x_goose + INPUT_LINE_LENGTH - 1, - pointers[2] * 5 + 2, 0), rotation=0,
                                   attachment_point=6)
                mtext.dxf.width = 10
                mtext.dxf.defined_height = 4

                pointers[2] = pointers[2] + 1
        # КОНЕЦ ЭКСПЕРИМЕНТАЛЬНОЙ ФИЧИ


        # рисуем прямоугольник функционального блока
        points = [(x, -y), (FBLOCK_LENGTH + x, -y), (FBLOCK_LENGTH + x, - coord_y + DISTANCE_BTW_FUNCS - MARGIN_BOTTOM),
                  (x, - coord_y + DISTANCE_BTW_FUNCS - MARGIN_BOTTOM), (x, -y)]
        msp.add_lwpolyline(points, dxfattribs={'layer': 'Основная'}, close=True)
        # выставляем имя функционального блока и его описание

        short_fb_name = str(ld.fb_name).split('_')[0] # убираем из короткого имени после подчеркивания все
        desc_fb_name = re.sub(r'\([^()]*\)', '', ld.description) # убираем из описания информацию в скобках

        fb_text_name = short_fb_name + ' (' + desc_fb_name + ')'

        mtext = msp.add_mtext(
            fb_text_name,
            dxfattribs={
                "layer": "Основная",
                "style": "Narrow"
            })
        # mtext.set_bg_color(9, scale=1)
        mtext.set_location(insert=(x + FBLOCK_LENGTH / 2, -y + 1, 0), rotation=0, attachment_point=8)
        mtext.dxf.width = FBLOCK_LENGTH
        x += DISTANCE_BTW_FB






def dxf_report(request, cab):
    doc = ezdxf.readfile('base_types/templates/template.dxf')
    #msp = doc.modelspace()


    # ищем шкаф в базе
    cabinet = Cabinets.objects.get(name=cab)
    # анализируем состав шкафа
    ied1 = cabinet.terminal1
    ied2 = cabinet.terminal2
    ied3 = cabinet.terminal3

    if not ied2 or ied2==ied1:
        msp = doc.modelspace()
        render_dxf(doc, msp, ied1, cab)

    elif ied2 and ied2!=ied1:
        msp = doc.layout('IED1')
        render_dxf(doc, msp, ied1, cab)
        msp = doc.layout('IED2')
        render_dxf(doc, msp, ied2, cab)

    if ied3:
        msp = doc.layout('IED3')
        render_dxf(doc, msp, ied3, cab)

    # Save the DXF document.
    doc.saveas("reports/dxf/test.dxf")

    return FileResponse(open("reports/dxf/test.dxf", 'rb')) # возвращаем сгенерированный файл dxf