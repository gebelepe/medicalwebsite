# importing modules 
import inspect, os.path, os, errno
from reportlab.pdfgen import canvas 
from reportlab.pdfbase import pdfmetrics 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.lib import colors 
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab_qrcode import QRCodeImage


def getPath(executer):
    return os.path.dirname(os.path.abspath(executer)).replace("\\","/")
 
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

path = getPath(inspect.getframeinfo(inspect.currentframe()).filename)

Width, Height = A4
# initializing variables with values 
#Se encuentra el origen de este archivo para ordenar todos los caminos aqui


#Se definen imagenes para suarse durante la creacion del archivo
camejalLogo = ImageReader('https://portalesmuli.s3.amazonaws.com/camejal/original_images/logos_camejal_1.jpg')
signature = ImageReader(path+"/static/signature.jpg")

#Funcion de generacion de archivo, devuelve el path del archivo
def doc_gen_func(nombre,carrera,carrera_inst,carrera_ced,esp,esp_inst,esp_ced,rep_nombre,rep_numero):
    #Se define el nombre de archivo


    fileName = "constancia_"+carrera_ced+"_"+esp_ced+".pdf"
    filepath = path+"/database/"+fileName
    make_sure_path_exists(path+'/database')

    #Texto Titulo
    title = 'CONSTANCIA DE NO QUÉJA MÉDICA'

    #texto de aprobacion
    aprob = 'Constancia aprobada de forma automatizada.    Contacto: (33) 2568-1007'

    #texto de advertencia, cuerpo del archivo
    disc = [
    'Se le informa a traves de la presente que la persona solicitante es apta para cumplir sus',
    'funciones medicas especificadas anteriormente en este documento aprobado por la',
    'Comisión de Arbitraje Médico del Estado de Jalisco "CAMEJAL".',
    '',
    'Tambien se le  informa que este documento es trunco y toda informacion aqui mostrada',
    'es Fabricada y no cuenta con ningun tipo de aplicacion legal, medica o de cualquier',
    'indole de caracter serio. El unico Proposito de este documento es una demostración del',
    'funcionamiento de una pieza de software.']

    #Aqui se guardan en una lista los datos mandados a traves de la funcion, que serian los datos que el usuario provee
    values = [carrera,"     "+carrera_inst,"      #"+carrera_ced,esp,"     "+esp_inst,"      #"+esp_ced,"Representante: "+rep_nombre,"      Contactar al "+rep_numero]

    for i in values:
        if i == "unsp":
            values = [carrera,"     "+carrera_inst,"    #"+carrera_ced,"Representado/a por "+rep_nombre,"      Contactar al "+rep_numero]
            fileName = "constancia_"+carrera_ced+".pdf"
            filepath = path+"/database/"+fileName

    # Se crea el archivo
    pdf = canvas.Canvas(filepath) 

    # se le da el titulo al archivo
    pdf.setTitle("Constancia") 


    # Se definen las fuentes a usarse
    pdfmetrics.registerFont(TTFont('TNR', 'TIMES.ttf'))
    pdfmetrics.registerFont(TTFont('consolas', 'CONSOLA.ttf')) 
    pdfmetrics.registerFont(TTFont('arial', 'ARIAL.ttf')) 
    pdfmetrics.registerFont(TTFont('arialround', 'ARLRDBD.ttf')) 


    #Escribimos el nombre del aplicante
    pdf.setFont('TNR', 30) 
    pdf.drawCentredString(295, Height-70, title)
    pdf.setFont('arialround', 25) 
    pdf.drawString(60, 720, nombre)

    #aqui se usa la lista antes creada y se itera a traves de ella para dar la informacion necesaria
    pdf.setFont('arial', 20) 
    j = 690
    for i in values:
        pdf.drawString(80, j, i)
        j-=28


    #aqui se definen las lineas de firma
    pdf.setFont('arial', 16) 
    pdf.drawCentredString(Width-160, 320, 'Firma del Arbitro')
    #y se aplica la firma del arbitro digitalmente
    pdf.drawCentredString(160, 320, 'Firma del Solicitante')
    pdf.drawImage(signature,Width-200, 340, width=100,height=100,mask='auto')

    #Se usa la imagen antes definida y se pone al fondo del documento
    pdf.drawImage(camejalLogo, Width-450, 40, width=446,height=100,mask='auto')

    #Aqui se define el texto de cuerpo en el que se explica el funcionamiento del documento, esta informacion puede ser editada en la linea 36
    disclaimer = pdf.beginText()
    disclaimer.setTextOrigin(60, 280)
    disclaimer.setFont('arial', 12)
    disclaimer.setFillColor(colors.gray)
    for i in disc:
        disclaimer.textLine(text=i)
    pdf.drawText(disclaimer)

    #Se crea el QR a partir del numero de cedula provisto la informacion se escribe directamente en la url y al abrir el link la pagina muestra si esa solicitud ha sido procesada
    qr = QRCodeImage('127.0.0.1:5000/certificate/'+filepath, size=45 * mm,fill_color='black')
    qr.drawOn(pdf, 25, 25)

    #Se escribe el texto de aprobacion
    pdf.setFont('consolas', 12) 
    pdf.setFillColor('red')
    pdf.drawString(40, 15, aprob)

    # Se guarda el archivo
    pdf.save()

    #Se devuelve el path del archivo para darselo al usuario
    return None