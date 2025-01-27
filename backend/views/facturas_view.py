from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker
from rest_framework.response import Response
from backend.serializers import FacturaSerializer
from ..models import Factura, ComunidadRegantes, Perfil, Consumos, LineaFactura
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_payment_report(request):
    user = request.user
    facturas = Factura.objects.filter(parcela__plot__usuarios=user)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payment_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, fontSize=14)
    elements.append(Paragraph("Listado del Libro Diario", title_style))
    elements.append(Spacer(1, 12))

    data = [['Asiento', 'Fecha', 'Subcuenta', 'Concepto', 'Debe', 'Haber', 'Título de la Subcuenta']]

    for factura in facturas:
        data.append([
            factura.numero_factura,
            factura.fecha_emision.strftime("%d/%m/%Y"),
            "4300001",  # Subcuenta - Esto puede variar dependiendo de tus datos
            f"Factura {factura.numero_factura}/{factura.fecha_emision.year}",
            str(factura.total_facturado) if factura.estado == 'Pendiente' else "",
            str(factura.total_facturado) if factura.estado == 'Pagado' else "",
            factura.parcela.plot.usuarios.first().first_name  # Título de la Subcuenta
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_facturas(request):
    user = request.user
    facturas = Factura.objects.filter(parcela__plot__usuarios=user)
    serializer = FacturaSerializer(facturas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_invoice(request, factura_id):
    try:
        factura = Factura.objects.get(id=factura_id)
    except Factura.DoesNotExist:
        return HttpResponse(status=404, content="Factura no encontrada")

    parcela = factura.parcela
    plot = parcela.plot
    cliente = plot.usuarios.first()  # Asumiendo que 'usuarios' field en Plot apunta al cliente User

    # Verificar que el usuario autenticado es el propietario de la parcela
    if request.user != cliente:
        return HttpResponse(status=403, content="No autorizado para ver esta factura")

    perfil_cliente = cliente.perfil
    comunidad = perfil_cliente.comunidades_regantes.first()  # Obteniendo la primera comunidad regante del perfil del cliente
    if not comunidad:
        return HttpResponse(status=400, content="Comunidad de regantes no encontrada para el cliente")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura_id}.pdf"'
    
    # Definir márgenes personalizados
    left_margin = 50
    right_margin = 50
    top_margin = 50
    bottom_margin = 50
    doc = SimpleDocTemplate(response, pagesize=letter,
                            leftMargin=left_margin, rightMargin=right_margin,
                            topMargin=top_margin, bottomMargin=bottom_margin)
    
    elements = []

    # Estilos
    styles = getSampleStyleSheet()

    # Crear un estilo personalizado para colorear el texto
        # Crear un estilo personalizado para texto en negrita y negro oscuro
    bold_black_style = ParagraphStyle(
        'BoldBlackStyle',
        parent=styles['Normal'],
        textColor=colors.HexColor('#000000'),  # Negro muy oscuro
        fontName='Helvetica-Bold'  # Texto en negrita
    )

    # Información de la factura
    elements.append(Paragraph(f"Factura No: {factura.numero_factura}", styles['Title']))
    elements.append(Paragraph(f"<b>Fecha de Emisión:</b> {factura.fecha_emision}", styles['Normal']))
    elements.append(Paragraph(f"<b>Fecha de Vencimiento:</b> {factura.fecha_vencimiento}", styles['Normal']))
    elements.append(Paragraph(f"<b>Estado:</b> {factura.estado}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # Información de la comunidad (a la izquierda)
    data_left = [
        [Paragraph("Comunidad:", bold_black_style), Paragraph(comunidad.nombre, styles['Normal'])],
        [Paragraph("Dirección:", bold_black_style), Paragraph(comunidad.direccion, styles['Normal'])],
        [Paragraph("Localidad:", bold_black_style), Paragraph(comunidad.localidad, styles['Normal'])],
        [Paragraph("Código Postal:", bold_black_style), Paragraph(comunidad.codigo_postal, styles['Normal'])],
        [Paragraph("Teléfonos:", bold_black_style), Paragraph(f"{comunidad.telefono_fijo}, {comunidad.telefono_movil}", styles['Normal'])],
    ]
    table_left = Table(data_left, colWidths=[100, 200])
    table_left.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))

    # Información del cliente (a la derecha)
    data_right = [
        [Paragraph("Nombre:", bold_black_style), Paragraph(f"{cliente.first_name} {cliente.last_name}", styles['Normal'])],
        [Paragraph("DNI/CIF:", bold_black_style), Paragraph(cliente.perfil.cif, styles['Normal'])],
        [Paragraph("Domicilio:", bold_black_style), Paragraph(cliente.perfil.direccion, styles['Normal'])],
        [Paragraph("Población:", bold_black_style), Paragraph(cliente.perfil.localidad, styles['Normal'])],
        [Paragraph("Código Postal:", bold_black_style), Paragraph(cliente.perfil.codigo_postal, styles['Normal'])],
        [Paragraph("Parcela:", bold_black_style), Paragraph(parcela.identificacion, styles['Normal'])],
    ]

    table_right = Table(data_right, colWidths=[100, 200])
    table_right.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))

    # Crear una tabla contenedora para colocar las tablas de la izquierda y la derecha en la misma fila
    data_combined = [[table_left, Spacer(1,1), table_right]]
    table_combined = Table(data_combined, colWidths=[270, 20, 230])
    table_combined.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))

    # Agregar la tabla combinada a los elementos del documento
    elements.append(table_combined)
    elements.append(Spacer(1, 24))  # Espacio antes de los detalles de la factura

    # Título de la tabla de conceptos imputados
    elements.append(Paragraph("Conceptos Imputados", styles['Title']))
    elements.append(Spacer(1, 12))

    # Tabla de conceptos imputados
    data_conceptos = [['Concepto', 'Unidades', 'Precio', 'Importe']]
    for linea in factura.lineas.all():
        data_conceptos.append([
            linea.concepto,
            f"{linea.unidades}",
            f"{linea.precio_unitario} €/unidad",
            f"{linea.total} €"
        ])
    
    # Añadir el total a pagar
    data_conceptos.append(['', 'TOTAL A PAGAR: ', f"{factura.total_facturado} €", ''])

    table_conceptos = Table(data_conceptos, colWidths=[150, 100, 100, 100])
    table_conceptos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('SPAN', (2, -1), (3, -1)),
        ('ALIGN', (2, -1), (3, -1), 'RIGHT'),
        ('TEXTCOLOR', (2, -1), (3, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (2, -1), (3, -1), 'Helvetica-Bold'),
    ]))
    elements.append(table_conceptos)
    elements.append(Spacer(1, 24))

    # Datos de consumo (Lecturas)
    try:
        consumo = Consumos.objects.filter(parcela=parcela).latest('periodo_facturacion')
        data_consumo = [
            ['Lectura Actual', 'Fecha'],
            [f"{consumo.volumen_medido} l", consumo.periodo_facturacion],
        ]
    except Consumos.DoesNotExist:
        data_consumo = [
            ['Lectura Actual', 'Fecha'],
            ['19.500 test', '31/05/2012'],
        ]
    table_consumo = Table(data_consumo)
    table_consumo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(table_consumo)
    elements.append(Spacer(1, 24))

    # Gráfico de consumo
    consumos = Consumos.objects.filter(parcela=parcela).order_by('periodo_facturacion')
    data = []
    for idx, consumo in enumerate(consumos):
        # Convierte periodo_facturacion en un número de secuencia para el gráfico
        periodo = idx + 1
        data.append((periodo, float(consumo.volumen_medido)))

    if data:
        drawing = Drawing(400, 200)
        lp = LinePlot()
        lp.x = 50
        lp.y = 50
        lp.height = 125
        lp.width = 300
        lp.data = [data]
        lp.joinedLines = 1
        lp.lineLabelFormat = '%2.0f'
        lp.strokeColor = colors.black
        lp.lines[0].symbol = makeMarker('FilledCircle')
        drawing.add(lp)
        elements.append(drawing)
    else:
        elements.append(Paragraph("No hay datos de consumo disponibles.", styles['Normal']))

    # Construir el PDF
    doc.build(elements)
    return response
