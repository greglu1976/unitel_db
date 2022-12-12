from docx import Document
from docx.shared import Inches
import io
from django.http import HttpResponse

import pandas as pd

from .tables import add_row_table_reports, add_table_reports, add_spec_row_table_reports
from .models import Cabinets, PhDLDconnections, LogicDevices, DataObjects, LDLNconnections, LogicNodeInstantiated

def word_report(request, cab):

# СОЗДАЕМ ОТЧЕТ


    document = Document('base_types/templates/template.docx')
    document.add_heading(cab, 2)

    #cabinets = Cabinet.objects.all()
    #cabinets = cabinets.order_by('name')
    #for item in cabinets.iterator():
     #   add_row_table_reports(t,(item.name,'','','','','','',''))

    df = pd.DataFrame(columns=['signal', 'iec', 'attr_name', 'attr_status', 'alm', 'cus', 'rdu', 'ras', 'dataset'])
    datasets = set()

    # ищем шкаф в базе
    cabinet = Cabinets.objects.get(name=cab)


    if cabinet.terminal1: # если есть терминал 1 то добавляем таблицу
        document.add_heading('ИЭУ1: '+str(cabinet.terminal1), 4)


        #ищем состав лог. устройств в нем
        connections = PhDLDconnections.objects.all().filter(ied=cabinet.terminal1)
        for item in connections:
            en_ld_name = item.ld
            print('en_ld_name---->', en_ld_name)
            ld = LogicDevices.objects.get(name=item.ld)
            ru_ld_name  = ld.fb_name
            print('ru_ld_name---->', ru_ld_name)
            ldln_conns = LDLNconnections.objects.all().filter(ld=item.ld)
            for ldln_conn in ldln_conns:
                ru_ln_name = ldln_conn.ln
                print('1Столбец ======>', ru_ld_name, '/', ru_ln_name)
                LogicNodeInstantiated



        datasets = list(datasets)
        datasets.sort()

        dataframe_list = list()
        for dataset in datasets: # делим датафрейм на части по датасетам
            dataframe_list.append(df[df['dataset'] == dataset])

        p1 = document.add_paragraph('Основные параметры функций')
        p1.style = 'ДОК Таблица Название'
        t1 = add_table_reports(document)

        for dataframe in dataframe_list:
            add_spec_row_table_reports(t1, ('Имя набора данных:', dataframe.iloc[0]['dataset']))

            dataframe = dataframe.sort_values('alm')
            print('вторая часть марлезонского балета')
            for row in dataframe.itertuples():
                print(row)
                row_no_index = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                dataframe = dataframe.reset_index(drop=True)
                add_row_table_reports(t1, row_no_index)





# СОХРАНЕНИЕ ДОКУМЕНТА
    bio = io.BytesIO()
    document.save(bio) # save to memory stream
    length = bio.tell()
    print(length, '++++++++++++++++++')
    bio.seek(0) # rewind the stream

    response = HttpResponse(
            bio.getvalue(),  # use the stream's contents
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    response["Content-Disposition"] = 'attachment; filename = {0}'.format(cab+".docx")
    response["Content-Encoding"] = "UTF-8"
    response['Content-Length'] = length
    
    return response
    
