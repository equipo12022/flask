#*=======================°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°=========================================
#*=======================°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°=========================================
#*=======================°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°=========================================
from flask import Flask, render_template,session #*== IMPORT FLASK, RENDER_TEMPLATES
from flask import url_for  #*== IMPORT URL_FOR
from flask import request #*== IMPORT  MODULO REQUEST
from flask import redirect #*== IMPORT REDIRECT
import json  #== IMPORT LIBRERIA JSON
from Modelo.usuario import Usuario #== IMPORT USUARIO
from Modelo.medicos import Medico
from Modelo.enfermeria import Enfermeria
from Modelo.otros import Otros_datos
from Modelo.usuariosistema import UsuarioSistema
from Modelo.sensores import Sensores
from Modelo.login_users import Login_users
#*========================°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°========================================
import pyrebase #*== IMPORT PYREBASE
#°°°°°°° CONFIGURACION DE CONEXION A LA BASE DE DATOS FIREBASE °°°°°°°°°°
config={
    #  =====CONEXION A PRUEVA=====================
    # ======CONEXION A SYSTEM CORE ===============
  "apiKey": "AIzaSyDZcGa1nC02SOTixWScg6kIE2ZGUrfhojE",
  "authDomain": "systemcore-2ad2f.firebaseapp.com",
  "databaseURL": "https://systemcore-2ad2f-default-rtdb.firebaseio.com",
  "projectId": "systemcore-2ad2f",
  "storageBucket": "systemcore-2ad2f.appspot.com",
  "messagingSenderId": "37384614589",
  "appId": "1:37384614589:web:db7aca76e0021a72eb3dd4",
  "measurementId": "G-VG5YMVGZ7R"
}
firebase=pyrebase.initialize_app(config)#= °°°VARIABLE PARA ENLAZAR COMUNICACION CON FIREBASE
db=firebase.database()#== °°°°°°°°°°°°°°°°°VARIABLE PARA EJECUTAR DATOS DE LA BASE DE DATOS
auth = firebase.auth()
#Initialize Firebase
app = Flask(__name__)
app.secret_key='secret'
#*================================================================
# ==== °°°°°°°°°°RUTA PARA DAR ALTA A REGISTRO
@app.route('/alta/<name>')# RUTA
def alta(name):# FUNCION
    db.child('').push({"nombre":name})
    return ' Registro realizado con Exito '#== RETORNO
#*================================================================
# ====RUTA PARA ELIMINAR A REGISTRO
@app.route('/eliminar')# RUTA
def eliminar():# FUNCION
    db.child("").child("-MxY43EFYEFn4zhVOms-").remove()
    return 'Registro eliminado con Exito'#== RETORNO
#*================================================================
# ====RUTA PARA MODIFICAR REGISTRO
@app.route('/actualizar')# RUTA
def actualizar():# FUNCION
    #ACTUALIZAR PASANDO ID
    db.child("").child("kkaksjdhfedsf").update({"fechadeingreso":"05-07-13"})
    return 'Registro actualizado con Exito'#== RETORNO

#*=================================ALTA,BAJA DE PACIENTES===============================
#*================================°° OBTENER DATOS Y LISTA DE INDICES °°°°================================
#== ROUTE  NAME OBTENER DATOS DE LA BASE DE DATOS FIREBASE
@app.route('/registropacientes')# RUTA
def registropacientes():# FUNCION
    #PARA OBTENER DATOS DE FIREBASE
    lista_registros = db.child("registrospacientes").get().val()
    try:# SI AY REGISTRO CON LLAVE MOSTRAR TABLA
        # LISTA DE INDICES DE LOS DATOS REGISTRADOS EN LA TABLA
        lista_indices = lista_registros.keys()
        lista_indice_final = list(lista_indices)
        #* ESTO ES PARA OBTENER DATOS DE FIREBASE AL FORMULARIO                            #* ESTO ES PARA OBTENER INDICE FINAL 
        return render_template('registropacientes.html',elementos_registros=lista_registros.values(), lista_indice_final = lista_indice_final)#== RETORNO
    except:#SI NO MOSTRARLO VACIO
        return render_template('registropacientes.html')
    #return 'Datos obtenidos con exito'#== RETORNO----
#*=============================°°° ALTA DE REGISTROS DE PACIENTES°°°===================================
#°°°°°°-ROUTE  CAPTURAR DATOS DEL FORMULARIO Y GUARDARLO A FIREBASE
@app.route('/save_data', methods=['POST'])# RUTA
def save_data(): # FUNCION
    nombre=request.form.get('nombre') #*****************DATO DEL FORMULARIO 
    apellidopaterno=request.form.get('apellidopaterno')#*****DATO DEL FORMULARIO 
    apellidomaterno=request.form.get('apellidomaterno')#****DATO DEL FORMULARIO 
    edad=request.form.get('edad')#**********************DATO DEL FORMULARIO 
    fechadeingreso=request.form.get('fechadeingreso')#*****DATO DEL FORMULARIO 
    horadeingreso=request.form.get('horadeingreso')#*******DATO DEL FORMULARIO 
    numerocama=request.form.get('numerocama')#*********DATO DEL FORMULARIO 
    trauma =request.form.get('trauma')#*********DATO DEL FORMULARIO 
    # lista_registros=db.child("registros").get().val() 
    #=== OBJETO DE LA CLASE USUARIO
    nueva_persona=Usuario(nombre, apellidopaterno, apellidomaterno, edad, fechadeingreso, horadeingreso, numerocama,trauma)
    objeto_enviar= json.dumps(nueva_persona.__dict__)
    formato= json.loads(objeto_enviar)
    db.child("registrospacientes").push(formato)
    #return render_template('tablaregistropaciente.html',elementos_registros=lista_registros.values())
    lista_registros=db.child("registrospacientes").get().val()
    #* PARA RETORNAR LA TABLA CON LOS NUEVOS REGISTROS DE ALTA FORMA LARGA
    #return  render_template('tablaregistropaciente.html',elementos_registros=lista_registros.values() )#== RETORNO
    #* PARA RETORNAR LA TABLA CON LOS NUEVOS REGISTROS DE ALTA FORMA CORTA
    return redirect(url_for('registropacientes'))#== RETORNO
#*=============================°°° ELIMINAR REGISTROS DE PACIENTES°°°===================================
@app.route('/eliminar_paciente/', methods=["GET"])
def eliminar_paciente():
    id = request.args.get("id")#AGREGAR SOLO ESTO
    db.child("registrospacientes").child(str(id)).remove()
    return redirect(url_for('registropacientes'))
#*================================================================
#*================================================================ 

'''#== ROUTE NUMEBER 1 NAME ESTRUCTURA
@app.route('/estructura')# RUTA
def estructura(): # FUNCION
    return render_template('estructura.html')#== RETORNO'''
#*=================================================================
#== ROUTE NUMEBER 2 NAME INICO
@app.route('/inicio')# RUTA
def inicio():# FUNCION
    return render_template('inicio.html')#== RETORNO
#*================================================================
#== ROUTE NUMEBER 3 NAME CURSOS
@app.route('/cursos')# RUTA
def cursos():# FUNCION
    return render_template('cursos.html')#== RETORNO
#*================================================================
#== ROUTE NUMEBER 4 NAME PROCEDIMIENTOS
@app.route('/procedimientos')# RUTA
def procedimientos():# FUNCION
    return render_template('procedimientos.html')#== RETORNO
#*================================================================
#== ROUTE NUMEBER 5 NAME SIGNOS VITALES
@app.route('/signosvitales')# RUTA
def signosvitales():# FUNCION
    return render_template('signosvitales.html')#== RETORNO
#*================================================================
#== ROUTE NUMEBER 6 NAME FARMACOS
@app.route('/farmacos')# RUTA
def farmacos():# FUNCION
    return render_template('farmacos.html')#== RETORNO
#*================================================================
#== ROUTE NUMEBER 7 NAME LOGIN
@app.route('/login')# RUTA
def login():# FUNCION
    db.child("login_user").get().val()
    if('user' in session):
        return 'Hi, {}'.format(session['user'])
    if request.method=='POST':
        user = request.form.get('User')
        contrasena = request.form.get('contrasena')
        try:
            user = auth.sign_in_with_user_and_contrasena(user,contrasena)
            session['user'] = user
            session['contrasena'] = contrasena
        except:
            return render_template('login.html')
    return render_template('login.html')

    return render_template('login.html')#== RETORNO
# NOW WE CREATE THE NAME PATH ENTER
@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    # WE VALIDATE THE TYPE OF CALL GET, POST
    if request.method=="GET":
       # CONSULTATION
        return render_template ('login.html')
    elif request.method=="POST":
       # REGISTER THE DATA FROM THE DATABASE
       nombre = request.form.get('nombre')
       apellidopaterno = request.form.get('apellidopaterno')
       apellidomaterno = request.form.get('apellidomaterno')
       usuario = request.form.get('usuario')
       contrasena = request.form.get('contrasena')
       tipo = request.form.get('tipo')
       nueva_persona_usuario = Login_users(nombre, apellidopaterno, apellidomaterno, usuario, contrasena, tipo)
       objeto_enviar_usuario = json.dumps(nueva_persona_usuario.__dict__)
       formato_usuario = json.loads(objeto_enviar_usuario)
       db.child("login_user").push(formato_usuario)
        #SESSION VARIABLE TO BE ABLE TO IDENTIFY IF THE USER REGISTERED CORRECTLY
       # session['nombreUsuario']=nombre

        #return redirect(url_for('entrar'))
    else:
        return redirect(url_for('inicio'))
# RUTA PARA BORRAR USUARIO
@app.route('/delete_user', methods=['GET'])
def delete_user():
    session.pop('user')
    return render_template('registrarme.html')


#=================================================================
# RUTA PARA REGISTRAR USUARIO
@app.route('/registrarme', methods=['GET'])
def registrarme():
    return render_template('registrarme.html')

#*================================================================
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°RUTA PARA LOS CURSOS
#== ROUTE NUMEBER 8 CURSOANATOMIA
@app.route('/cursoanatomia')# RUTA
def cursoanatomia():# FUNCION
    return render_template('cursoanatomia.html')#== RETORNO
# ruta fisiologia
@app.route('/cursofisiologia')
def cursofisiologia():
    return render_template('cursofisiologia.html')
# ruta cursoneonatologia
@app.route('/cursoneonatologia')
def cursoneonatologia():
    return render_template('cursoneonatologia.html')
# cursogeriatria
@app.route('/cursosgeriatria')
def cursosgeriatria():
    return render_template('cursosgeriatria.html')
#cursourgencias
@app.route('/cursourgencias')
def cursourgencias():
    return render_template('cursourgencias.html')
#cursoembriologia
@app.route('/cursoembriologia')
def cursoembriologia():
    return render_template('cursoembriologia.html')
#*================================================================
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°RUTA PARA LOS PROCEDIMIENTOS
# PARTE I
#procedimientolavadodemano
@app.route('/procedimientolavadodemano')
def procedimientolavadodemano():
    return render_template('procedimientolavadodemano.html')
#procedimientohiportermia
@app.route('/procedimientohiportermia')
def procedimientohiportermia():
    return render_template('procedimientohiportermia.html')
#procedimientolipotimia
@app.route('/procedimientolipotimia')
def procedimientolipotimia():
    return render_template('procedimientolipotimia.html')
#procedimientoemergencia
@app.route('/procedimientoemergencia')
def procedimientoemergencia():
    return render_template('procedimientoemergencia.html')
#procedimientoembarazo
@app.route('/procedimientoembarazo')
def procedimientoembarazo():
    return render_template('procedimientoembarazo.html')
#procedimientodiabetes
@app.route('/procedimientodiabetes')
def procedimientodiabetes():
    return render_template('procedimientodiabetes.html')

# PARTE II
#procedimientomanejodebata
@app.route('/procedimientomanejodebata')
def procedimientomanejodebata():
    return render_template('procedimientomanejodebata.html')
#procedimientousodecubreboca
@app.route('/procedimientousodecubreboca')
def procedimientousodecubreboca():
    return render_template('procedimientousodecubreboca.html')
#procedimientousodeturbante
@app.route('/procedimientousodeturbante')
def procedimientousodeturbante():
    return render_template('procedimientousodeturbante.html')
#procedimientousodeguantes
@app.route('/procedimientousodeguantes')
def procedimientousodeguantes():
    return render_template('procedimientousodeguantes.html')
#procedimientomanejodeequipo
@app.route('/procedimientomanejodeequipo')
def procedimientomanejodeequipo():
    return render_template('procedimientomanejodeequipo.html')
#procedimientomanejoderopa
@app.route('/procedimientomanejoderopa')
def procedimientomanejoderopa():
    return render_template('procedimientomanejoderopa.html')

# PARTE III
#procedimientoenemaevacuante
@app.route('/procedimientoenemaevacuante')
def procedimientoenemaevacuante():
    return render_template('procedimientoenemaevacuante.html')
#procedimientocolostomia
@app.route('/procedimientocolostomia')
def procedimientocolostomia():
    return render_template('procedimientocolostomia.html')
#procedimientocontrolheces
@app.route('/procedimientocontrolheces')
def procedimientocontrolheces():
    return render_template('procedimientocontrolheces.html')
#procedimientosondajes
@app.route('/procedimientosondajes')
def procedimientosondajes():
    return render_template('procedimientosondajes.html')
#procedimientoaplicaciondefrio
@app.route('/procedimientoaplicaciondefrio')
def procedimientoaplicaciondefrio():
    return render_template('procedimientoaplicaciondefrio.html')
#procedimientovendajes
@app.route('/procedimientovendajes')
def procedimientovendajes():
    return render_template('procedimientovendajes.html')

# PARTE IV
#procedimientoaplicaciondecalor
@app.route('/procedimientoaplicaciondecalor')
def procedimientoaplicaciondecalor():
    return render_template('procedimientoaplicaciondecalor.html')
#procedimientolavadovesical
@app.route('/procedimientolavadovesical')
def procedimientolavadovesical():
    return render_template('procedimientolavadovesical.html')
#procedimientosondajerectal
@app.route('/procedimientosondajerectal')
def procedimientosondajerectal():
    return render_template('procedimientosondajerectal.html')
#procedimientoenemas
@app.route('/procedimientoenemas')
def procedimientoenemas():
    return render_template('procedimientoenemas.html')
#procedimientoestomaurinario
@app.route('/procedimientoestomaurinario')
def procedimientoestomaurinario():
    return render_template('procedimientoestomaurinario.html')
#*================================================================
#°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°RUTA PARA LOS FARMACOS
#PARTE I
#farmacosanalgesico
@app.route('/farmacosanalgesico')
def farmacosanalgesico():
    return render_template('farmacosanalgesico.html')
#farmacosantipiretico
@app.route('/farmacosantipiretico')
def farmacosantipiretico():
    return render_template('farmacosantipiretico.html')
#farmacosantidiuretico
@app.route('/farmacosantidiuretico')
def farmacosantidiuretico():
    return render_template('farmacosantidiuretico.html')
#farmacosantiarritmias
@app.route('/farmacosantiarritmias')
def farmacosantiarritmias():
    return render_template('farmacosantiarritmias.html')
#farmacosantiinflamatorios
@app.route('/farmacosantiinflamatorios')
def farmacosantiinflamatorios():
    return render_template('farmacosantiinflamatorios.html')
#farmacosantiespasmodico
@app.route('/farmacosantiespasmodico')
def farmacosantiespasmodico():
    return render_template('farmacosantiespasmodico.html')
#PARTE II
#farmacosantialergicos
@app.route('/farmacosantialergicos')
def farmacosantialergicos():
    return render_template('farmacosantialergicos.html')
#farmacosantiinfecciosos
@app.route('/farmacosantiinfecciosos')
def farmacosantiinfecciosos():
    return render_template('farmacosantiinfecciosos.html')
#farmacosantitusivos
@app.route('/farmacosantitusivos')
def farmacosantitusivos():
    return render_template('farmacosantitusivos.html')
#farmacosantiulceroso
@app.route('/farmacosantiulceroso')
def farmacosantiulceroso():
    return render_template('farmacosantiulceroso.html')
#farmacosantiacido
@app.route('/farmacosantiacido')
def farmacosantiacido():
    return render_template('farmacosantiacido.html')
#farmacosmucoliticos
@app.route('/farmacosmucoliticos')
def farmacosmucoliticos():
    return render_template('farmacosmucoliticos.html')

#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#*°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°° RUTA PARA REGISTROS °°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#*================================================================
#== ROUTE NUMEBER 9 NAME  REGISTER 
#@app.route('/registropacientes')# RUTA
#def registropacientes():# FUNCION
#    return render_template('registropacientes.html')#== RETORNO
#*=========°°°°°°  REGISTRO DE PERSONAL °°°°°°°°°======================
#== ROUTE NUMEBER 10 NAME TABLA DE REGISTRO DE PERSONAL
@app.route('/tablaregistropersonal')# RUTA
def tablaregistropersonal():# FUNCION
    return render_template('tablaregistropersonal.html')#== RETORNO
#*===============================°°°°°°°°°°°°°°°°°°°°°°°°°°ALTA DE DATOS DE MEDICOS °°°°°=================================
#== ROUTE NUMEBER 11  REGISTRO MEDICO
@app.route('/registromedicos')# RUTA
def registromedicos():# FUNCION
    #db.child("registros_medicos").push({}) 
    lista_registros_medicos = db.child("registros_medicos").get().val()
    try:
        # OBTENER INDICE DE CADA REGISTROS
        lista_indice_medicos = lista_registros_medicos.keys()
        lista_indice_final_medicos = list(lista_indice_medicos)
        return render_template('registromedicos.html',  elementos_registros_medicos=lista_registros_medicos.values(), lista_indice_final_medicos=lista_indice_final_medicos)#== RETORNO
    except:
        return render_template('registromedicos.html')
    #return 'Dato guardado con exito'
#*==============================°°°°°°-ROUTE  CAPTURAR DATOS DEL FORMULARIO Y GUARDARLO A FIREBASE
@app.route('/save_data_medic', methods=['POST'])
def save_data_medic():
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    fechadeingreso = request.form.get('fechadeingreso')
    area = request.form.get('area')
    especialidad = request.form.get('especialidad')
    cedulaprofesional = request.form.get('cedulaprofesional')
    #=== OBJETO DE LA CLASE MEDIC
    nueva_persona_medicos = Medico(nombre, apellidopaterno, apellidomaterno, fechadeingreso, area, especialidad, cedulaprofesional)
    objeto_enviar_medicos = json.dumps(nueva_persona_medicos.__dict__)
    formato_medico= json.loads(objeto_enviar_medicos)
    db.child("registros_medicos").push(formato_medico)
    return redirect(url_for('registromedicos'))

#*=============================°°° ELIMINAR REGISTROS DE MEDICOS°°°===================================
@app.route('/eliminar_medicos/', methods=['GET'])
def eliminar_medicos():
    id = request.args.get("id")
    db.child('registros_medicos').child(str(id)).remove()
    return redirect(url_for('registromedicos'))


#*================================== °°°°°°°°°°°°°°°°°°°°°°°°°ALTA DE DATOS DE ENFERMERIA °°°°°==============================
#== ROUTE NUMEBER 12  PARA REGISTRO DE ENFERMERIA
@app.route('/registroenfermeria')# RUTA
def registroenfermeria():# FUNCION
    #db.child("registros_enfermeria").push({})
    lista_registros_enfermeria = db.child("registros_enfermeria").get().val()
    try:
        # OBTENER INDICE DE CADA REGISTROS PARA ELIMINAR POR ID
        lista_indice_enfermeria = lista_registros_enfermeria.keys()
        lista_indice_final_enfermeria = list(lista_indice_enfermeria)
        return render_template('registroenfermeria.html', elementos_registros_enfermeria=lista_registros_enfermeria.values(), lista_indice_final_enfermeria=lista_indice_final_enfermeria)#== RETORNO
    except:
        return render_template('registroenfermeria.html')

#===============================°°°°°°-ROUTE  CAPTURAR DATOS DEL FORMULARIO Y GUARDARLO A FIREBASE
@app.route('/save_data_enfermeria', methods=["POST"])
def save_data_enfermeria():
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    especialidad = request.form.get('especialidad')
    area = request.form.get('area')
    cedulaprofesional = request.form.get('cedulaprofesional')
    ingresodetrabajo = request.form.get('ingresodetrabajo')
    #=== OBJETO DE LA CLASE ENFERMERIA
    nueva_persona_enfermeria = Enfermeria(nombre, apellidopaterno, apellidomaterno, especialidad, area, cedulaprofesional, ingresodetrabajo)
    objeto_enviar_enfermeria = json.dumps(nueva_persona_enfermeria.__dict__)
    formato_enfermeria = json.loads(objeto_enviar_enfermeria)
    db.child('registros_enfermeria').push(formato_enfermeria)
    return redirect(url_for('registroenfermeria'))

#*=============================°°° ELIMINAR REGISTROS DE MEDICOS°°°===================================
@app.route('/eliminar_enfermeria/', methods=["GET"])
def eliminar_enfermeria():
    id = request.args.get("id")
    db.child("registros_enfermeria").child(str(id)).remove()
    return redirect(url_for('registroenfermeria'))

#*============================= °°°°°°°°°°°°°°°°°°°°°°°°°ALTA DE DATOS DE OTROS REGISTROS °°°°°======================
#== ROUTE NUMEBER 13 OTROS 
@app.route('/registrootros')# RUTA
def registrootros():# FUNCION
    #db.child("registros_otros").push({})
    lista_registros_otros = db.child("registros_otros").get().val()
    try:
        # OBTENER INDICE DE CADA REGISTROS PARA ELIMINAR POR ID
        lista_indice_otros = lista_registros_otros.keys()
        lista_indice_final_otros = list(lista_indice_otros)
        return render_template('registrootros.html',elementos_registros_otros=lista_registros_otros.values(),lista_indice_final_otros=lista_indice_final_otros)#== RETORNO
    except:
        return render_template('registrootros.html')

#===============================°°°°°°-ROUTE  CAPTURAR DATOS DEL FORMULARIO Y GUARDARLO A FIREBASE
@app.route('/save_data_otros',methods=["POST"])
def save_data_otros():
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    fechadeingreso = request.form.get('fechadeingreso')
    area = request.form.get('area')
    telefono = request.form.get('telefono')
    #=== OBJETO DE LA CLASE OTROSDATOS
    nueva_persona_otros = Otros_datos(nombre, apellidopaterno, apellidomaterno, fechadeingreso, area, telefono)
    objeto_enviar_otros = json.dumps(nueva_persona_otros.__dict__)
    formato_otros = json.loads(objeto_enviar_otros)
    db.child("registros_otros").push(formato_otros)
    return redirect(url_for('registrootros'))

#*=============================°°° ELIMINAR REGISTROS DE OTROS°°°===================================
@app.route('/eliminar_otros/', methods=["GET"])
def eliminar_otros():
    id = request.args.get("id")
    db.child("registros_otros").child(str(id)).remove()
    return redirect(url_for('registrootros'))
#*---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#*°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°RURA PARA FORMULARIOS°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°
#== ROUTE NUMEBER 14 FORMULARIO REGISTRO MEDICO
@app.route('/formulariomedicos') # RUTA
def formulariomedicos():# FUNCION
    return render_template('formulariomedicos.html')#== RETORNO

#*================================================================
#== ROUTE NUMEBER 15 FORMULARIO REGISTRO ENFERMERIA
@app.route('/formularioenfermeria')# RUTA
def formularioenfermeria():# FUNCION
    return render_template('formularioenfermeria.html')#== RETORNO

#*================================================================
#== ROUTE NUMEBER 16 FORMULARIO  PARA OTROS REGISTRO 
@app.route('/formulariootros')# RUTA
def formulariootros():# FUNCION
    return render_template('formulariootros.html')#== RETORNO

#*================================================================
#== ROUTE NUMEBER 16 FORMULARIO  PARA OTROS REGISTRO 
@app.route('/formulariopacientes')# RUTA
def formulariopacientes():# FUNCION
    return render_template('formulariopacientes.html')#== RETORNO
#*================================================================
#*================================================================
#===================RUTAS PARA  ACTUALIZAR LOS REGISTROS
#== RUTA  ACTUALIZAR PACIENTES
@app.route('/actualizar_pacientes/<id>')
def actualizar_pacientes(id):
    lista_pacientes = db.child("registrospacientes").child(str(id)).get().val()
    #print("lista_pacientes:",lista_pacientes)
    return render_template("actualizarpacientes.html",lista_pacientes=lista_pacientes,id_pacientes=id)

#=====  Ruta para modificar los valores con base al ID---------------------
@app.route('/update_pacientes',methods=["POST"])
def update_pacientes():
    idpacientes=request.form.get('id')
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    edad = request.form.get('edad')
    fechadeingreso = request.form.get('fechadeingreso')
    horadeingreso = request.form.get('horadeingreso')
    numerocama = request.form.get('numerocama')
    trauma = request.form.get('trauma')
    modificar_dato_pacientes = Usuario(nombre, apellidopaterno, apellidomaterno, edad, fechadeingreso , horadeingreso,numerocama,trauma)
    #print("idpacientes",idpacientes)
    objeto_enviar_pacientes = json.dumps(modificar_dato_pacientes.__dict__)
    datos_pacientes = json.loads(objeto_enviar_pacientes)
    db.child("registrospacientes").child(str(idpacientes)).update(datos_pacientes)
    return redirect(url_for('registropacientes'))

#=================================================================
#=================================================================
#== RUTA ACTUALIZAR  MEDICOS
@app.route('/actualizar_medicos/<id>')
def actualizar_medicos(id):
    lista_medicos = db.child("registros_medicos").child(str(id)).get().val()
    #print("lista:",lista)
    return render_template("actualizarmedicos.html",lista_medicos=lista_medicos,id_medicos=id)

#=====  Ruta para modificar los valores con base al ID---------------------
@app.route('/update_medicos',methods=["POST"])
def update_medicos():
    idmedicos=request.form.get('id')
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    fechadeingreso = request.form.get('fechadeingreso')
    area = request.form.get('area')
    especialidad = request.form.get('especialidad')
    cedulaprofesional = request.form.get('cedulaprofesional')

    modificar_dato_medicos = Medico(nombre,apellidopaterno,apellidomaterno, fechadeingreso,area,especialidad,cedulaprofesional)
    #print("idpersona",idpersona)
    objeto_enviar_de_medicos = json.dumps(modificar_dato_medicos.__dict__)
    datos_medicos = json.loads(objeto_enviar_de_medicos)
    db.child("registros_medicos").child(str(idmedicos)).update(datos_medicos)
    return redirect(url_for('registromedicos'))

#=================================================================
#=================================================================
#== RUTA ACTUALIZAR ENFERMERIA
@app.route('/actualizar_enfermeria/<id>')
def actualizar_enfermeria(id):
    lista_enfermeria = db.child("registros_enfermeria").child(str(id)).get().val()
    #print("lista:",lista)
    return render_template("actualizarenfermeria.html",lista_enfermeria=lista_enfermeria,id_enfermeria=id)

#=====  Ruta para modificar los valores con base al ID---------------------
@app.route('/update_enfermeria',methods=["POST"])
def update_enfermeria():
    idenfermeria = request.form.get('id')
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    especialidad = request.form.get('especialidad')
    area = request.form.get('area')
    cedulaprofesional = request.form.get('cedulaprofesional')
    ingresodetrabajo = request.form.get('ingresodetrabajo')
    modificar_dato_enfermeria = Enfermeria(nombre, apellidopaterno, apellidomaterno, especialidad, area, cedulaprofesional, ingresodetrabajo)
    #print("idpersona",idpersona)
    objeto_enviar_de_enfermeria = json.dumps(modificar_dato_enfermeria .__dict__)
    datos_enfermeria = json.loads(objeto_enviar_de_enfermeria)
    db.child("registros_enfermeria").child(str(idenfermeria)).update(datos_enfermeria)
    return redirect(url_for('registroenfermeria'))

#=================================================================
#=================================================================
#== RUTA ACTUALIZAR OTROS
@app.route('/actualizar_otros/<id>')
def actualizar_otros(id):
    lista_otros = db.child("registros_otros").child(str(id)).get().val()
    #print("lista:",lista)ccccccccccccccccccc
    return render_template("actualizarotros.html",lista_otros=lista_otros,id_otros=id)

#=====  Ruta para modificar los valores con base al ID---------------------
@app.route('/update_otros',methods=["POST"])
def update_otros():
    idotros=request.form.get('id')
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    fechadeingreso = request.form.get('fechadeingreso')
    area = request.form.get('area')
    telefono = request.form.get('telefono')
    modificar_dato_otros = Otros_datos(nombre, apellidopaterno, apellidomaterno, fechadeingreso, area, telefono)
    #print("idpersona",idpersona)
    objeto_enviar_de_otros = json.dumps(modificar_dato_otros.__dict__)
    datos_otros = json.loads(objeto_enviar_de_otros )
    db.child("registros_otros").child(str(idotros)).update(datos_otros)
    return redirect(url_for('registrootros'))


#------------------formulario de registro de usuarios del sistema--------------------------
#RUTA PARA FORMULARIO USUARIO SISTEMA
@app.route('/formularioaltausuariosistema')
def formularioaltausuariosistema():
    return render_template("formularioaltausuariosistema.html")
#RUTA REGISTROS USUARIOS DEL SISTEMA
#*===== °°°°°°°°°°°°°°°°°°°°°°°°°ALTA DE DATOS DE  REGISTROS  DE USUARIO DEL SISTEMA°°°°°======================
#== ROUTE NUMEBER 13 OTROS 
@app.route('/registroaltausuariosistema')# RUTA
def registroaltausuariosistema():# FUNCION
    #db.child("registros_otros").push({})
    lista_registroaltausuariosistema = db.child("registros_usuario_sistema").get().val()
    try:
        # OBTENER INDICE DE CADA REGISTROS PARA ELIMINAR POR ID
        lista_indice_registroaltausuariosistema = lista_registroaltausuariosistema.keys()
        lista_indice_final_registroaltausuariosistema = list(lista_indice_registroaltausuariosistema)
        return render_template('registroaltausuariosistema.html',elementos_registros_registroaltausuariosistema=lista_registroaltausuariosistema.values(),lista_indice_final_registroaltausuariosistema=lista_indice_final_registroaltausuariosistema)#== RETORNO
    except:
        return render_template('registroaltausuariosistema.html')

#===============================°°°°°°-ROUTE  CAPTURAR DATOS DEL FORMULARIO Y GUARDARLO A FIREBASE
#---------------- ruta para obtener los datos del formulario y crear el usuario.--------------
@app.route('/se',methods=['POST'])
def se():
    if request.method=='POST':
        nombre = request.form.get('nombre')
        apellidopaterno = request.form.get('apellidopaterno')
        apellidomaterno =request.form.get('apellidomaterno')
        email = request.form.get('email')
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')
        telefono = request.form.get('telefono')
        tipo = request.form.get('tipo')
        try:
            usuario_sistema_nuevo = UsuarioSistema(nombre, apellidopaterno, apellidomaterno, email, usuario, contrasena, telefono, tipo)
            objeto_enviar = json.dumps(usuario_sistema_nuevo.__dict__)
            y=json.loads(objeto_enviar)
            db.child("registros_usuario_sistema").push(y)

        except:
            print("error")

    return render_template("registroaltausuariosistema.html")

#°°°°°°-ROUTE  CAPTURAR DATOS DEL FORMULARIO Y GUARDARLO A FIREBASE
@app.route('/save_data_usersistema', methods=["POST"])
def save_data_usersistema():
    nombre = request.form.get('nombre')
    apellidopaterno = request.form.get('apellidopaterno')
    apellidomaterno = request.form.get('apellidomaterno')
    email = request.form.get('email')
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    telefono = request.form.get('telefono')
    tipo = request.form.get('tipo')
    #=== OBJETO DE LA CLASE ENFERMERIA
    nueva_persona_usersistema = UsuarioSistema(nombre, apellidopaterno, apellidomaterno, email, usuario, contrasena, telefono, tipo)
    objeto_enviar_usersistema = json.dumps(nueva_persona_usersistema.__dict__)
    formato_usersistema = json.loads(objeto_enviar_usersistema)
    db.child('registros_usuario_sistema').push(formato_usersistema)
    return redirect(url_for('registroaltausuariosistema'))

    if request.method=='POST':
        nombre = request.form.get('nombre')
        apellidopaterno = request.form.get('apellidopaterno')
        apellidomaterno =request.form.get('apellidomaterno')
        email = request.form.get('email')
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contrasena')
        telefono = request.form.get('telefono')
        tipo = request.form.get('tipo')
        try:
            usuario_sistema_nuevo = UsuarioSistema(nombre, apellidopaterno, apellidomaterno, email, usuario, contrasena, telefono, tipo)
            objeto_enviar = json.dumps(usuario_sistema_nuevo.__dict__)
            y=json.loads(objeto_enviar)
            db.child("registros_usuario_sistema").push(y)
        except:
            print("error")

#===============ELIMINAR USUARIO SISTEMA======================================
@app.route('/delete_usersistem', methods=['GET'])
def delete_usersistema():
    id = request.args.get("id")
    db.child("registros_usuario_sistema").child(str(id)).remove()
    return redirect(url_for('registroaltausuariosistema'))
#*************************************************************************************************
#*************************************************ENTRADAS************************************************
#===========================RUTA PARA  CREAR DATOS DE LOS SENSORES ENTRADAS
#RUTA formularioregistroentrada
@app.route('/formularioregistroentrada')
def  formularioregistroentrada():
    return render_template('formularioregistroentrada.html')

@app.route('/registro_entrada', methods=['GET'])#---ROUTE
def registro_entrada():#---FUNTION
    #db.child("system_Core").child("19-04-22").push({"Sala A Cama 1":"Ocupado"})#--CHILD()
    #return {"Messje":"Conectado"}#-MESSAJE
    lista_registro_sensores = db.child("system_Core").child("22-04-22").get().val()
    try:
        lista_indice_sensores = lista_registro_sensores.keys()
        lista_indice_final_sensores = list(lista_indice_sensores)
        return render_template('registroentrada.html',  elementos_registro_sensores=lista_registro_sensores.values(), lista_indice_final_sensores=lista_indice_final_sensores)
    except:
        return render_template('registroentrada.html')

#===============ELIMINAR REGISTRO SENSORES======================================
@app.route('/delete_registro_sensores', methods=['GET'])
def delete_registro_sensores():
    id = request.args.get("id")
    db.child("system_Core").child("22-04-22").child(str(id)).remove()
    return redirect(url_for('registro_entrada'))

#RUTA formularioregistroentrada
@app.route('/save_data_registroentrada',methods=['POST'])
def  save_data_registroentrada():
    puerta =  request.form.get('puerta')
    Sala_A_Cama_1 = request.form.get('Sala A Cama 1 ')
    distanciacm = request.form.get('distanciacm')
    fechaHora = request.form.get('fechaHora')
    # CREAMOS UN OBJETO DE LA CLASE SENSORES
    nuevo_registros_sensores = Sensores(puerta, Sala_A_Cama_1, distanciacm, fechaHora)
    # ENVIAAMOS NUESTRO OBJETO
    objeto_enviar_registro_sensores = json.dumps(nuevo_registros_sensores.__dict__)
    #CREAMOS EL FORMATO DE LA CLASE
    formato_registro_sensores = json.loads(objeto_enviar_registro_sensores)
    db.child("system_Core").child("22-04-22").push(formato_registro_sensores)
    #return render_template('registroentrada.html')
    return redirect(url_for('registro_entrada'))

#*************************************************SALIDAS************************************************
@app.route('/registro_salida', methods=['GET'])#---ROUTE
def registro_salida():#---FUNTION
        db.child("system_core").child("22-04-22").push({"Registro":"salida 1"})
        return render_template('registrosalida.html')
#================================SIGNOS VITALES=================================
# RUTA PARA graficatencionarterial
@app.route('/tencionarterial')
def tencionarterial():
    return render_template('tencionarterial.html')

#=================================================================
# RUTA PARA tablarespiracion
@app.route('/tablarespiracion')
def tablarespiracion():
    return render_template('tablarespiracion.html')

#=================================================================
# RUTA PARA frecuenciacardiaca
@app.route('/frecuenciacardiaca')
def frecuenciacardiaca():
    return render_template('frecuenciacardiaca.html')

#=================================================================
# RUTA PARA pulso
@app.route('/pulso')
def pulso():
    return render_template('pulso.html')
#=================================================================
# RUTA PARA tablarespiracion
@app.route('/n')
def b():
    return render_template('b.html')

#=================================================================
# RUTA PARA tablarespiracion
@app.route('/temperatura')
def temperatura():
    return render_template('temperatura.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 