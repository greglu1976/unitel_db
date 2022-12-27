import ezdxf
import math
import re
from .dxfconfig import RENDER_SIGNAL_NUMBERS, RENDER_SIGNAL_NUMBERS_RIGHT, CHANGES



MARGIN_PUT = 5 # отступ от верхней части блока до линии первого входа и от последнего входа до нижней границы
DISTANCE_BTW_PUTS = 5
MARGIN_SW = 5 # расстояние от последнего входа/выхода до блока переключателей
DISTANCE_BTW_SW =5 # расстояние между переключателями
BLOCK_LENGTH = 80 # длина блока, стандартная
OUTPUT_LINE_LENGTH = 100 # длина линии выхода была 80
#TEXT_OUTPUT_LENGTH = 45 # длина надписи выхода TEXT_OUTPUT_LENGTH = 60 - для АПТ - перенесено в файл настроек 18.10.22
DESC_OUTPUT_LENGTH = 100 # длина надписи пояснения выхода



def draw_func(msp, pointer_output, format_dxf, x=0, y=0, inputs=[], outputs=[], switches=[], func_name=('test block', '', False), fb_name = 'test fb'):
    """ функция для прорисовки одиночного ЛУ, x,y координаты верхней левой точки """
    # выставляем длину надписи выхода для АПТ и прочих защит



    TEXT_OUTPUT_LENGTH = 45 # длина надписи в блоке, нормальный режим
    BLOCK_LENGTH = 80  # длина блока, стандартная
    if format_dxf == 'apt':
        TEXT_OUTPUT_LENGTH = 60 # длина надписи в блоке, режим АПТ, АРН
        BLOCK_LENGTH = 72 # регулировка ширины блока и отступа
        x = x + 8

    # определяем высоту блока
    block_height_inputs = MARGIN_PUT + DISTANCE_BTW_PUTS*len(inputs) # высота блока по входам
    block_height_outputs = MARGIN_PUT + DISTANCE_BTW_PUTS*len(outputs) # высота блока по выходам
    block_height = block_height_outputs
    if block_height_inputs > block_height_outputs:
        block_height = block_height_inputs
    rel_pos_start_swblock = block_height # относительная координата начала блока переключателей
    if len(switches) !=0: # если есть переключатели то
        msp.add_line((x, - y - block_height), (x + BLOCK_LENGTH, - y - block_height), dxfattribs={'layer': 'Тонкая'})
        block_height = math.ceil(len(switches)/2)*DISTANCE_BTW_SW+MARGIN_SW + block_height # прибавляем блок переключателей , по 2 столбца

    # рисуем прямоугольник
    points = [(x, -y), (BLOCK_LENGTH+x, -y), (BLOCK_LENGTH+x, -y-block_height), (x, -y-block_height), (x, -y)]
    msp.add_lwpolyline(points, dxfattribs={'layer': 'Основная'}, close=True)

    # выставляем имя блока

    func_name_text = func_name[1] +' (' + str(func_name[0]) + ')'
    if str(func_name[1]) == str(func_name[0]):
        func_name_text = func_name[1]

    if func_name[2]:
        func_name_text = f"\{{ " + func_name_text + f" \}}" # иначе dxf не воспринимает {} скобки, надо экранировать
    mtext = msp.add_mtext(
        func_name_text,
        dxfattribs={
            "layer": "Основная",
            "style": "Narrow"
        })
    #mtext.set_bg_color(9, scale=1)
    mtext.set_location(insert=(x+BLOCK_LENGTH/2, -y+1, 0), rotation=0, attachment_point=8)
    mtext.dxf.width = BLOCK_LENGTH

    ###################
    # выставляем входы
    for n, input_item in enumerate(inputs):
        msp.add_line((x, -y-n*DISTANCE_BTW_PUTS-MARGIN_PUT), (x-5, -y-n*DISTANCE_BTW_PUTS-MARGIN_PUT), dxfattribs={'layer': 'Линии связи'})

        # если есть номер прибавляем его к надписи
        input_full_name = input_item.name # = input_item[0]
        mtext = msp.add_mtext(
            input_full_name,
            dxfattribs={
                "layer": "Основная",
                "style": "Narrow"
            })
        mtext.set_location(insert=(x-6, -y-n*DISTANCE_BTW_PUTS-MARGIN_PUT, 0), rotation=0, attachment_point=6)
        mtext.dxf.width = 50
        # выставляем переключатель входа
        if input_item.sw_type != '-': #if input_item[1] != 'None':
            msp.add_blockref(input_item.sw_type, (x+1, -y-n*DISTANCE_BTW_PUTS-MARGIN_PUT))
            # подписываем переключатель входа
            mtext = msp.add_mtext(
                input_item.sw_name, #input_item[2],
                dxfattribs={
                    "layer": "Основная",
                    "style": "Narrow"
                })
            mtext.set_location(insert=(x + 7, -y - n * DISTANCE_BTW_PUTS - MARGIN_PUT, 0), rotation=0,
                               attachment_point=4)
            mtext.dxf.width = 30

    # выставляем выходы
    for n, output_item in enumerate(outputs):

        # дополнительные условия
        # например сигнал Индикация режима работы (Состояние) заменить на рисунке на состояние
        signal_out = CHANGES.get(str(output_item.signal), str(output_item.signal))
        #print('signal_out==========', signal_out)
        # очищаем сигнал от содержимого в скобках, чтобы вывести внутри функции
        signal_out_no_braces = re.sub(r'\([^()]*\)', '', signal_out)
        # если сигнал есть управляющий, то не рисуем
        if output_item.cdc in ('ENC_ctl', 'SPC_ctl', 'APC_ctl'):
            continue
        #output_item[8] - находится тип сигнала SPC, ENC и пр
        mtext = msp.add_mtext(
            ' ' + signal_out_no_braces, # пробел в начале, чтобы не сливалось с краем - берем 3 столбец - там сигнал
            dxfattribs={
                "layer": "Основная",
                "style": "Narrow"
            })
        mtext.set_location(insert=(x - TEXT_OUTPUT_LENGTH + BLOCK_LENGTH, -y - n * DISTANCE_BTW_PUTS - MARGIN_PUT, 0), rotation=0, attachment_point=4)
        mtext.set_bg_color(9, scale=1)
        mtext.dxf.width = TEXT_OUTPUT_LENGTH
        mtext.dxf.defined_height = 4

        # если сигнал внутренний, то рисуем линию и проставлям поясняющую надпись
        if 'Внутр' in output_item.signal_type:
            layer = 'Линии связи'
            if 'ВнутрШтрих' in output_item.signal_type: # Если внутренний сигнал то делаем штриховой слой для линии
                layer = 'Основная прерывистая'
            msp.add_line((x + BLOCK_LENGTH, -y - n * DISTANCE_BTW_PUTS - MARGIN_PUT),
                         (x + BLOCK_LENGTH + OUTPUT_LINE_LENGTH, -y - n * DISTANCE_BTW_PUTS - MARGIN_PUT),
                         dxfattribs={'layer': layer})
            #output_text = fb_name +' / '+ func_name[0]+': '+output_item[2] здесь имя блока бралось напрямую
            output_text = func_name[3].split('_')[0] + ' / ' + func_name[0] + ': ' + signal_out #output_item[2] # используем текст с заменой из словаря CHANGES и отбрасываем после _
            if output_item.signal_number != 0 and RENDER_SIGNAL_NUMBERS:
                output_text +=' ['+str("{:04d}".format(output_item.signal_number)) + ']'
            outtext = msp.add_mtext(
                output_text,
                dxfattribs={
                    "layer": 'Сигналы внутр.',
                    "style": "Narrow"
                })
            outtext.set_location(insert=(x + BLOCK_LENGTH+7, -y - n * DISTANCE_BTW_PUTS - MARGIN_PUT+2, 0),
                               rotation=0, attachment_point=4)
            outtext.dxf.width = DESC_OUTPUT_LENGTH
            outtext.dxf.defined_height = 4

            # пробуем вывести номер справа в слое Сигнатура
            if output_item.signal_number != 0 and RENDER_SIGNAL_NUMBERS_RIGHT:
                outtext = msp.add_mtext(
                    str("{:04d}".format(output_item.signal_number)),
                    dxfattribs={
                        "layer": 'Сигнатура',
                        "style": "Narrow"
                    })
                outtext.set_location(insert=(x + BLOCK_LENGTH + OUTPUT_LINE_LENGTH-1, -y - n * DISTANCE_BTW_PUTS - MARGIN_PUT+2, 0),
                                     rotation=0, attachment_point=6)
                outtext.dxf.width = 15
                outtext.dxf.defined_height = 4


### ЭКСПЕРИМЕНТАЛЬНАЯ ФИЧА
### ВЫВОД выходов с меткой внутр слева в столбец
            output_coord_x = -700
            msp.add_line((output_coord_x, -pointer_output*5),
                         (output_coord_x + OUTPUT_LINE_LENGTH, -pointer_output*5),
                         dxfattribs={'layer': 'Линии связи'})
            outtext2 = msp.add_mtext(
                output_text,
                dxfattribs={
                    "layer": 'Сигналы внутр.',
                    "style": "Narrow"
                })
            outtext2.set_location(insert=(output_coord_x+10, -pointer_output*5+2, 0),
                                 rotation=0, attachment_point=4)
            outtext2.dxf.width = DESC_OUTPUT_LENGTH
            outtext2.dxf.defined_height = 4
            # выводим номер
            outnum = msp.add_mtext(
                str("{:04d}".format(output_item.signal_number)),
                dxfattribs={
                    "layer": 'Сигнатура',
                    "style": "Narrow"
                })
            outnum.set_location(
                insert=(output_coord_x+1, -pointer_output*5+2, 0),
                rotation=0, attachment_point=4)
            outnum.dxf.width = 15
            outnum.dxf.defined_height = 4
            pointer_output = pointer_output + 1
### КОНЕЦ ЭКСПЕРИМЕНТАЛЬНОЙ ФИЧИ


    # выставляем переключатели
    row = -1
    for n, switch_item in enumerate(switches):
        coord_x = x
        if n%2 != 0:
            coord_x = x + BLOCK_LENGTH/2
        else:
            row = row + 1

        sw_type = 'SW.2'
        if len(str(switch_item.sg_modes).split('/'))>2:
            sw_type = 'SW.3'

        msp.add_blockref(sw_type, (coord_x + 1, -y - rel_pos_start_swblock - row * DISTANCE_BTW_PUTS - MARGIN_PUT))
        switch_text = switch_item.sgras_name
        if not switch_item.dataset: # если переключатель опциональный, то заключаем к скобки, не в датасете
            switch_text = f"\{{ " + switch_text + f" \}}"
        swtext = msp.add_mtext(
            switch_text,
            dxfattribs={
                "layer": "Основная",
                "style": "Narrow"
            })
        swtext.set_location(insert=(coord_x + 7, -y - rel_pos_start_swblock - row * DISTANCE_BTW_PUTS - MARGIN_PUT, 0),
                             rotation=0, attachment_point=4)
    return block_height, pointer_output
