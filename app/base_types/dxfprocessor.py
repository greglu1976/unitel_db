import ezdxf
import io
from django.http import HttpResponse

def dxf_report(request, cab):

    document = ezdxf.readfile('base_types/templates/template.dxf')
    msp = document.modelspace()
    # пробуем нарисовать полилинию
    points = [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)]
    msp.add_polyline2d(points, dxfattribs={'layer': 'Основная'})

    # Save the DXF document.
    #doc.saveas("test.dxf")

    # СОХРАНЕНИЕ ДОКУМЕНТА

    bio = io.BytesIO()
    document.write(bio)  # save to memory stream
    length = bio.tell()
    print(length, '++++++++++++++++++')
    bio.seek(0)  # rewind the stream

    response = HttpResponse(
        bio.getvalue(),  # use the stream's contents
        content_type="image/x-dxf",
    )

    response["Content-Disposition"] = 'attachment; filename = {0}'.format(cab.split(' ')[1] + ".dxf")
    response["Content-Encoding"] = "UTF-8"
    response['Content-Length'] = length

    return response