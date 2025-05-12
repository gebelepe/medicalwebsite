import inspect, os, os.path, csv
from flask import Blueprint, render_template, render_template_string, flash, redirect, url_for, send_file, request
from .logic import doc_gen_func, getPath
from pathlib import Path

path = getPath(inspect.getframeinfo(inspect.currentframe()).filename)
base_datos_quejas = path+'/database/quejas.csv'
complaintlist=[]
with open(base_datos_quejas,'r',encoding='utf-8-sig') as csvfile:
    quejas = list(csv.reader(csvfile))
    for i in quejas:
        complaintlist.append(i[0])
    






formlogic = Blueprint('formlogic',__name__)

@formlogic.route('/submit', methods=['GET','POST'])
def formsubmit():
    if request.method == 'POST':
        data = request.form
        nombre = data.get('nombre')
        email = data.get('email')
        carrera = data.get('carrera')
        carrera_inst = data.get('carrera_inst')
        carrera_ced = data.get('carrera_ced')
        esp = data.get('esp')
        esp_inst = data.get('esp_inst')
        esp_ced = data.get('esp_ced')
        rep_nombre = data.get('rep_nombre')
        rep_numero = data.get('rep_numero')

        items=[nombre,carrera,carrera_inst,carrera_ced,esp,esp_inst,esp_ced,rep_nombre,rep_numero]

        file = Path(path+"/database/"+"constancia_"+carrera_ced+"_"+esp_ced+".pdf")
        if esp == 'unsp' or esp_inst == 'unsp':
            file = Path(path+"/database/"+"constancia_"+carrera_ced+".pdf")
            items=[nombre,carrera,carrera_inst,carrera_ced,rep_nombre,rep_numero]
        if file.is_file():
            return render_template("existingform.html")
        else:
            flag = True
            for i in items:
                if i == '':
                    flag = False
            if flag:
                flag2 = True
                for i in complaintlist:
                    if i.lower() == nombre.lower():
                        flag2 = False
                if flag2:
                    doc_gen_func(nombre,carrera,carrera_inst,carrera_ced,esp,esp_inst,esp_ced,rep_nombre,rep_numero)
                    return render_template("submitted.html")
                else: return render_template("complaintfound.html")
            else:
                return redirect(url_for('formlogic.formsubmit'))

    
    return render_template("submit.html")

@formlogic.route('/request', methods=['GET','POST'])
def formrequest():
    if request.method == 'POST':
        data = request.form
        request1 = data.get('carrera_ced')
        request2 = data.get('esp_ced')

        file = Path(path+"/database/"+"constancia_"+request1+"_"+request2+".pdf")
        if request2 == '':
            file = Path(path+"/database/"+"constancia_"+request1+".pdf")
        if file.is_file():
            return send_file(file, as_attachment=True)
        else:
            return render_template("filenotfound.html")
    return render_template("request.html")
