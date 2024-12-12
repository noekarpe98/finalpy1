from tkinter import *
import sqlite3
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import filedialog
from tkcalendar import DateEntry, Calendar
from tkinter.ttk import Combobox
import random
import string
import re

################################## CONEXION A LA BASE DE DATOS#####################################################

conexion = sqlite3.connect('integrador_base_datos.db')
cursor = conexion.cursor()

###################################### FUNCIONES #####################################################################

def ingresar():
    conexion = sqlite3.connect('integrador_base_datos.db')
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND contrasena=?", (usuario.get(), contrasena.get()))
    lista=cursor.fetchall()
    if lista==[]:
        print('Usuario o contraseña incorrectos')
        messagebox.showinfo('Error', 'Usuario o contraseña incorrectos')
    for fila in lista:
        if (fila[1])==usuario.get() and (fila[2])==contrasena.get():
            print('Usuario y contraseña correctos')
            if fila[3] == "alumno":
                mesaexaminadora()
            elif fila[3] == "administrador":
                abrir_panel_administrador()
    
    conexion.close()
    
def requisitos_contrasena():
        return (
        "La contraseña debe tener al menos 10 caracteres\n",
        "La primer letra debe ser una letra mayúscula\n",
        "Debe contener al menos un número\n",
        "Debe contener al menos una letra\n",
        "Debe contener al menos un caracter especial\n"
    )

'''def agregar():
    conexion = sqlite3.connect('integrador_base_datos.db')
    cursor = conexion.cursor()
    valido = contrasena.get()
    b = 0
    cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario.get(),))
    var = cursor.fetchone()

    if var is not None:
        print('Usuario ya existe')
        messagebox.showinfo('Error', 'Usuario ya existe')
    else:
        if valido[0].isalpha(): 
            if len(valido) >= 10:
                for i in valido:
                    if i.isdigit():
                        b = 1
                    elif i.isalpha():
                        b = 1
                if b == 1:
                    cursor.execute("INSERT INTO usuarios (usuario, contrasena, nivel) VALUES (?,?,?)", (usuario.get(), contrasena.get(), "alumno"))
                    print('Usuario agregado')
                    messagebox.showinfo('Agregado', 'Usuario agregado correctamente')
                else:
                    print('Contraseña no válida')
                    messagebox.showinfo('Contraseña no válida', requisitos_contrasena())
            else:
                print('Contraseña no válida')
                messagebox.showinfo('Contraseña no válida', requisitos_contrasena())
        else:
            print('Contraseña no válida')
            messagebox.showinfo('Contraseña no válida', requisitos_contrasena())

    conexion.commit()
    conexion.close()'''



def modificar():
    conexion = sqlite3.connect('integrador_base_datos.db')
    cursor = conexion.cursor()
    valido=contrasena.get()
    b=0
    cursor.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario.get(),))
    var = cursor.fetchone()
    
    if var is None:
        print('Usuario no existe')
        messagebox.showinfo('Error', 'Usuario no existe')
    else:

        if valido[0].isalpha():
            if len(valido)>=10:
                for i in valido:
                    if i.isdigit():
                        b=1
                    elif i.isalpha():
                        b=1
                
                if b==1:
                    cursor.execute("UPDATE usuarios set contrasena=? WHERE usuario LIKE ?", (valido,usuario.get()))
                    print('Contraseña modificada')
                    messagebox.showinfo('Modificación exitosa', '¡Contraseña modificada!')
                if b==0:
                    print('No es valida')
                    messagebox.showinfo('¡Contraseña incorrecta! ', requisitos_contrasena() )      


            else:
                print('No es valida')
                messagebox.showinfo('¡Contraseña incorrecta!', requisitos_contrasena())     
        else:
            print('no es valida')
            messagebox.showinfo('¡Contraseña incorrecta!', requisitos_contrasena())
    
    conexion.commit()
    conexion.close()



def mesaexaminadora():
    global carrera, nombre, tree, id
    login.destroy()
    mesaexam = Tk()
    conexion = sqlite3.connect('integrador_base_datos.db')
    cursor = conexion.cursor()
    nombre = StringVar()
    id = IntVar()
    carrera = StringVar()

    mesaexam.title('Mesa Examinadora')
    mesaexam.geometry('600x600')
    lblnombre1 = Label(mesaexam, text='ID de Alumno: ',font=("Helvetica", 8, "bold"),  bg="lightblue", fg="black")
    lblnombre1.place(x=50, y=120)
    entrada1 = Entry(mesaexam, textvariable=id,state='readonly')
    entrada1.place(x=150, y=120)
    lblnombre2 = Label(mesaexam, text='Alumno: ',font=("Helvetica", 8, "bold"),  bg="lightblue", fg="black")
    lblnombre2.place(x=290, y=120)
    entrada2 = Entry(mesaexam, textvariable=nombre,state='readonly')
    entrada2.place(x=350, y=120)
    lblnombre3 = Label(mesaexam, text='Carrera: ',font=("Helvetica", 8, "bold"),  bg="lightblue", fg="black")
    lblnombre3.place(x=50, y=160)
    entrada3 = Entry(mesaexam, textvariable=carrera,state='readonly')
    entrada3.place(x=110, y=160)
    lbltitulo = Label(mesaexam, text="Inscripción a Mesas de Exámenes", font=("Helvetica", 16, "bold"), bg="lightblue", fg="black", width=48, height=2)
    lbltitulo.place(x=0, y=30)
    btninscripcion = Button(mesaexam, text='INSCRIBIRME', command=inscripcion, bg="lightblue",fg='black',font=("Helvetica",8, "bold"),relief="raised",bd=3, width=10,height=2, activebackground="lightblue",activeforeground='white')
    btninscripcion.place(x=180, y=500)
    btnverinsc = Button(mesaexam, text='VER INSCRIPCIONES', command=verinscripciones, bg="lightblue",fg='black',font=("Helvetica",8, "bold"),relief="raised",bd=3, width=15,height=2, activebackground="lightblue",activeforeground='white')
    btnverinsc.place(x=300, y=500)
    #CONSULTA
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND nivel='alumno'", (usuario.get(),))
    var = cursor.fetchall()
    for fila in var:
        alum_id = fila[4]
    #CONSULTA
    cursor.execute("SELECT * FROM alumno WHERE id=?", (alum_id,))
    var = cursor.fetchall()
    for fila in var:
        print('Alumno: ' + fila[1])
        print('ID de Alumno: ' + str(fila[0]))
        id.set(fila[0])
        nombre.set(fila[1])
    #CONSULTA
    cursor.execute("SELECT carrera.nombre FROM alumno, carrera WHERE alumno.id_carrera=carrera.id AND alumno.id=?", (alum_id,))
    var = cursor.fetchall()
    for fila in var:
        print('Carrera: ' + fila[0])
        carrera.set(fila[0])
    #TREEVIEW
    columnas = ('Mesa', 'Materia', 'Fecha')
    tree = ttk.Treeview(mesaexam, columns=columnas, show='headings')
    tree.heading('Mesa', text='Mesa')
    tree.column('Mesa', anchor='center', width=100)
    tree.heading('Materia', text='Materia')
    tree.column('Materia', anchor='center', width=200)
    tree.heading('Fecha', text='Fecha')
    tree.column('Fecha', anchor='center', width=300)

    #DISEÑO 

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", 
                    background="lightblue",  # Color de fondo
                    foreground="black",      # Color de texto
                    font=("Helvetica", 10, "bold"))  # Fuente y tamaño del texto

    #CONSULTA
    #Trae solo las mesas de las materias regulares
    cursor.execute("""
        SELECT mesas.id, materias.nombre, mesas.fecha
        FROM mesas
        JOIN materias ON mesas.id_materia = materias.id
        JOIN materias_regularizadas mr ON materias.id = mr.id_materia
        WHERE mr.id_alumno = ?
    """, (alum_id,))
    
    mesas_regularizadas = cursor.fetchall()
    for mesa in mesas_regularizadas:
        tree.insert('', tk.END, values=mesa)

    def item_selected(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']

    tree.bind('<<TreeviewSelect>>', item_selected)
    tree.place(x=0, y=250)

    scrollbar = ttk.Scrollbar(mesaexam, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=580, y=250, height=200)

    mesaexam.mainloop()
    conexion.commit()
    conexion.close()

def inscripcion():
    conexion = sqlite3.connect('integrador_base_datos.db')
    cursor = conexion.cursor()
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showinfo("Error", "Por favor, selecciona una mesa de examen.")
        return
    
    item = tree.item(selected_items[0])
    mesa_id, materia, fecha = item['values']
    alumno_id = id.get()
    #CONSULTA
    # Verifica si ya existe la inscripción
    cursor.execute("SELECT * FROM mesa_examinadora WHERE id_alumno = ? AND id_mesa = ?", (alumno_id, mesa_id))
    existe_inscripcion = cursor.fetchone()
    
    if existe_inscripcion:
        messagebox.showinfo("Inscripción Duplicada", f"Ya estás inscrito en {materia} el {fecha}.")
    else:
        confirmacion = messagebox.askyesno("Confirmación de Inscripción", f"¿Estás seguro de inscribirte en {materia} el {fecha}?")
        if confirmacion:
            try:
                cursor.execute("INSERT INTO mesa_examinadora (id_alumno, id_mesa) VALUES (?, ?)", (alumno_id, mesa_id))
                conexion.commit()
                messagebox.showinfo("Inscripción Exitosa", f"Inscripción realizada para {materia} el {fecha}.")
                
                # Genera el comprobante PDF
                generar_comprobante_pdf(materia, fecha)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Hubo un problema con la inscripción: {e}")
    
    conexion.close()

def generar_comprobante_pdf(materia, fecha):
    #pide ubicación para guardar el archivo
    nombre_archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf", 
        filetypes=[("PDF files", "*.pdf")], 
        title="Guardar Comprobante",
        initialfile=f"comprobante_inscripcion_{usuario.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    
    if nombre_archivo:
        c = canvas.Canvas(nombre_archivo, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 750, "Comprobante de Inscripción a Mesa de Examen")
        c.setFont("Helvetica", 12)
        c.drawString(100, 700, f"Alumno: {nombre.get()}")
        c.drawString(100, 680, f"ID de Alumno: {id.get()}")
        c.drawString(100, 660, f"Carrera: {carrera.get()}")
        c.drawString(100, 620, f"Materia: {materia}")
        c.drawString(100, 600, f"Fecha de Examen: {fecha}")
        c.drawString(100, 560, f"Fecha de Inscripción: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Cierra y guarda el PDF
        c.save()
        messagebox.showinfo("PDF Generado", f"Comprobante guardado como: {nombre_archivo}")
    else:
        messagebox.showinfo("Operación cancelada", "No se guardó el archivo.")


def verinscripciones():
    global alumno_id
    conexion = sqlite3.connect('integrador_base_datos.db')
    cursor = conexion.cursor()
    alumno_id = id.get()
    #CONSULTA
    # obtiene las inscripciones del alumno desde la tabla mesa_examinadora
    cursor.execute("""
        SELECT materias.nombre, mesas.fecha, mesas.id
        FROM mesa_examinadora
        JOIN mesas ON mesa_examinadora.id_mesa = mesas.id
        JOIN materias ON mesas.id_materia = materias.id
        WHERE mesa_examinadora.id_alumno = ?
    """, (alumno_id,))

    inscripciones = cursor.fetchall()

    if not inscripciones:
        messagebox.showinfo("Sin Inscripciones", "No tienes inscripciones a ninguna mesa de examen.")
    else:
        mis_inscripciones = Toplevel()
        mis_inscripciones.title("Mis Inscripciones")
        mis_inscripciones.geometry("500x400")
        columnas = ('Materia', 'Fecha', 'Mesa')
        tree_inscripciones = ttk.Treeview(mis_inscripciones, columns=columnas, show='headings')
        tree_inscripciones.heading('Materia', text='Materia')
        tree_inscripciones.column('Materia', anchor='center', width=200)
        tree_inscripciones.heading('Fecha', text='Fecha')
        tree_inscripciones.column('Fecha', anchor='center', width=200)
        tree_inscripciones.heading('Mesa', text='Mesa')
        tree_inscripciones.column('Mesa', anchor='center', width=100)
        
        #DISEÑO
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", background="lightblue", foreground="black", font=("Helvetica", 10, "bold"))

        def cerrar():
            mis_inscripciones.destroy()

        for inscripcion in inscripciones:
            tree_inscripciones.insert('', tk.END, values=inscripcion)

        def eliminar_inscripcion():
            selected_items = tree_inscripciones.selection()
            if not selected_items:
                messagebox.showinfo("Error", "Por favor, selecciona una inscripción para eliminar.")
            else:
                item = tree_inscripciones.item(selected_items[0])
                mesa_id = item['values'][2]
                cursor.execute("DELETE FROM mesa_examinadora WHERE id_alumno = ? AND id_mesa = ?", (alumno_id, mesa_id))
                conexion.commit()

                tree_inscripciones.delete(selected_items)
                messagebox.showinfo("Eliminación exitosa", "Inscripción eliminada correctamente.")

        btn_eliminar = Button(mis_inscripciones, text="Eliminar Inscripción", command=eliminar_inscripcion, bg="lightblue", fg="black", font=("Helvetica", 10, "bold"), relief="raised", bd=4)
        btn_eliminar.place(x=170, y=250)
        tree_inscripciones.place(x=0, y=0)
        btncerrar = Button(mis_inscripciones, text="CERRAR", command=cerrar, bg="red", fg="white", font=("Helvetica", 9, "bold"), relief="raised", bd=3)
        btncerrar.place(x=210, y=300)
        scrollbar = ttk.Scrollbar(mis_inscripciones, orient=tk.VERTICAL, command=tree_inscripciones.yview)
        tree_inscripciones.configure(yscroll=scrollbar.set)
        scrollbar.place(x=580, y=0, height=300)

        mis_inscripciones.mainloop()
        conexion.close()

##########################################################################################################################################################
############################################################ NIVEL ADMINISTRADOR #########################################################################
###########################################################################################################################################################
def abrir_panel_administrador():
    login.destroy()
    panel_admin = Tk()
    conexion = sqlite3.connect('integrador_base_datos.db')
    cursor = conexion.cursor()
    nombreadmin = StringVar()
    idadmin = IntVar()

    panel_admin.title('Panel de Administrador')
    panel_admin.geometry('800x800')
    panel_admin.config(bg="lightblue")

    label1 =Label(panel_admin, text='ADMINISTRADOR: ',font=("Helvetica", 9, "bold"),bg="lightblue", fg="black")
    label1.place(x=10, y=680)
    label2 = Label(panel_admin, text='ID: ',font=("Helvetica", 9, "bold"),bg="lightblue", fg="black")
    label2.place(x=10, y=710)
    entrada11 = Entry(panel_admin, textvariable=nombreadmin,state='readonly')
    entrada11.place(x=115, y=680)
    entrada22 = Entry(panel_admin, textvariable=idadmin,state='readonly')
    entrada22.place(x=115, y=710)
    #CONSULTA
    cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND nivel='administrador'", (usuario.get(),))
    var = cursor.fetchall()
    for fila in var:
        admin_id = fila[5]
        print(admin_id)
    #CONSULTA
    cursor.execute("SELECT * FROM administradores WHERE id=?", (admin_id,))
    var = cursor.fetchall()
    for fila in var:
        print('Administrador: ' + fila[1])
        print('ID de Administrador: ' + str(fila[0]))
        idadmin.set(fila[0])
        nombreadmin.set(fila[1])

    #DISEÑO CONTENEDOR
    frame_central = Frame(panel_admin, bg="white")
    frame_central.place(x=250, y=80, width=530, height=650)

    def limpiar_frame():
        for widget in frame_central.winfo_children():
            widget.destroy()

##################################################### GESTION DE MESAS ######################################################################

    def gestionar_mesas_examen():
        limpiar_frame()
        Label(frame_central, text="Gestionar Mesas de Examen", font=("Helvetica", 14, "bold"), bg="lightblue").pack(pady=20)
        Label(frame_central, text="Seleccione una opción:", font=("Helvetica", 12), bg="white").pack(pady=10)
        Button(frame_central, text="Crear Nueva Mesa", font=("Helvetica", 12), command=agregar_mesa, bg="lightblue").pack(pady=10)
        Button(frame_central, text="Ver Mesas Existentes", font=("Helvetica", 12), command=ver_inscripciones, bg="lightblue").pack(pady=10)
        


#######################################FORMULARIO PARA AGREGAR UNA MESA DE EXAMEN ##################################################

    def agregar_mesa():
        limpiar_frame()
        Label(frame_central, text="Agregar Nueva Mesa de Examen", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)
        Label(frame_central, text="Seleccione la Materia:", font=("Helvetica", 12), bg="white").pack(pady=10)
        
        cursor.execute("SELECT nombre FROM materias")
        materias = [row[0] for row in cursor.fetchall()]
        materia_seleccionada = StringVar()
        combo_materias = ttk.Combobox(frame_central, textvariable=materia_seleccionada, values=materias, state="readonly")
        combo_materias.pack(pady=10)
        combo_materias.set("Seleccione una materia")
        
        Label(frame_central, text="Seleccione la Fecha:", font=("Helvetica", 12), bg="white").pack(pady=10)
        from tkcalendar import DateEntry
        calendario = DateEntry(frame_central, date_pattern="dd-mm-yyyy", width=12, background="darkblue", foreground="white", borderwidth=2)
        calendario.pack(pady=10)

        def guardar_mesa():
            materia = materia_seleccionada.get()
            fecha = calendario.get()

            if not materia or materia == "Seleccione una materia":
                messagebox.showwarning("Advertencia", "Debe seleccionar una materia.")
                return
            
            if not fecha:
                messagebox.showwarning("Advertencia", "Debe seleccionar una fecha.")
                return

            #Validación de fecha
            fecha_seleccionada = datetime.strptime(fecha, "%d-%m-%Y")
            fecha_actual = datetime.now()

            if fecha_seleccionada < fecha_actual:
                messagebox.showwarning("Advertencia", "La fecha seleccionada no puede ser una fecha pasada. Seleccione una fecha a partir de hoy.")
                return
            #Comprueba si ya existe una mesa para esa materia y fecha
            try:
                cursor.execute("""
                    SELECT 1 FROM mesas
                    JOIN materias ON mesas.id_materia = materias.id
                    WHERE materias.nombre = ? AND mesas.fecha = ?
                """, (materia, fecha))
                if cursor.fetchone():
                    messagebox.showwarning("Advertencia", "Ya existe una mesa de examen para esta materia en esa fecha.")
                    return
                #INSERTA LA NUEVA MESA EN LA BASE DE DATOS
                cursor.execute("INSERT INTO mesas (id_materia, fecha) VALUES ((SELECT id FROM materias WHERE nombre = ?), ?)", (materia, fecha))
                conexion.commit()
                messagebox.showinfo("Éxito", "Mesa de examen creada correctamente.")
                limpiar_frame()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Hubo un error al guardar la mesa: {e}")

        Button(frame_central, text="CREAR MESA DE EXAMEN", font=("Helvetica", 11), command=guardar_mesa, bg="lightblue").pack(pady=20)


########################################### FORMULARIO PARA VER LAS INSCRIPCIONES POR FECHA Y MATERIA#####################################

    def ver_inscripciones():
        limpiar_frame()
        Label(frame_central, text="Buscar por:", font=("Helvetica", 12), bg="lightblue").pack(pady=10)
        filtro_seleccionado = StringVar()

        #OPCIONES DE LA LISTA PARA FILTRAR
        filtros = ["Fecha", "Materia"]
        combo_filtros = ttk.Combobox(frame_central, textvariable=filtro_seleccionado, values=filtros, state="readonly")
        combo_filtros.pack(pady=10)
        combo_filtros.set("Seleccione")

        frame_filtro = Frame(frame_central, bg="white")
        frame_filtro.pack(pady=20, fill="both", expand=True)

        def actualizar_filtro(*args):
            for widget in frame_filtro.winfo_children():
                widget.destroy()
            #POR FECHA
            if filtro_seleccionado.get() == "Fecha":
                Label(frame_filtro, text="Seleccione una fecha:", font=("Helvetica", 12), bg="lightblue").pack(pady=10)
                from tkcalendar import DateEntry
                calendario = DateEntry(frame_filtro, date_pattern="dd-mm-yyyy", width=12, background="darkblue", foreground="white", borderwidth=2)
                calendario.pack(pady=10)

                def buscar_por_fecha():
                    fecha = calendario.get()
                    conexion = sqlite3.connect('integrador_base_datos.db')
                    cursor = conexion.cursor()

                    query = """
                        SELECT 
                            mesas.id AS numero_mesa, 
                            materias.nombre AS materia, 
                            mesas.fecha, 
                            COUNT(mesa_examinadora.id_alumno) AS cantidad_inscriptos
                        FROM 
                            mesas
                        JOIN 
                            materias ON mesas.id_materia = materias.id
                        LEFT JOIN 
                            mesa_examinadora ON mesas.id = mesa_examinadora.id_mesa
                        WHERE 
                            mesas.fecha = ?
                        GROUP BY 
                            mesas.id, materias.nombre, mesas.fecha;
                        """
                    cursor.execute(query, (fecha,))
                    resultados = cursor.fetchall()
                    listbox.delete(0, END)

                    #DISEÑO ENCABEZADO DE LA LISTBOX
                    encabezado = f"{'Mesa':<10}{'Materia':<20}{'Fecha':<15}{'Inscriptos':<10}"
                    listbox.insert(tk.END, encabezado)
                    listbox.insert(tk.END, "-" * 55)

                    if resultados:
                        for mesa_id, materia_nombre, fecha, inscritos in resultados:
                            item = f"{mesa_id:<10}{materia_nombre:<20}{fecha:<15}{inscritos:<10}"
                            listbox.insert(tk.END, item)
                            
                    else:
                        listbox.insert(END, "No hay mesas disponibles para la materia seleccionada.")

                Button(frame_filtro, text="Buscar", command=buscar_por_fecha,font=("Helvetica", 9), bg="lightblue").pack(pady=10)

            #POR MATERIA 
            elif filtro_seleccionado.get() == "Materia":
                Label(frame_filtro, text="Seleccione una materia:", font=("Helvetica", 12), bg="lightblue").pack(pady=10)
                cursor.execute("SELECT nombre FROM materias")
                materias = [row[0] for row in cursor.fetchall()]
                
                materia_seleccionada = StringVar()
                combo_materias = ttk.Combobox(frame_filtro, textvariable=materia_seleccionada, values=materias, state="readonly")
                combo_materias.pack(pady=10)
                combo_materias.set("Seleccione una materia")

                def buscar_por_materia():
                    materia = materia_seleccionada.get()
                    if not materia or materia == "Seleccione una materia":
                        messagebox.showwarning("Advertencia", "Debe seleccionar una materia.")
                        return
        
                    try:

                        conexion = sqlite3.connect('integrador_base_datos.db')
                        cursor = conexion.cursor()
            
                        cursor.execute("""
                            SELECT 
                                mesas.id AS NumeroMesa, 
                                materias.nombre AS Materia, 
                                mesas.fecha AS Fecha, 
                                COUNT(mesa_examinadora.id_alumno) AS AlumnosInscriptos
                            FROM 
                                mesas
                            JOIN 
                                materias ON mesas.id_materia = materias.id
                            LEFT JOIN 
                                mesa_examinadora ON mesas.id = mesa_examinadora.id_mesa
                            WHERE 
                                materias.nombre = ?
                            GROUP BY 
                                mesas.id, materias.nombre, mesas.fecha;
                        """, (materia,))
                        
                        resultados = cursor.fetchall()
                        listbox.delete(0, END)
                        #DISEÑO ENCABEZADO DE LA LISTBOX
                        encabezado = f"{'Mesa':<10}{'Materia':<20}{'Fecha':<15}{'Inscriptos':<10}"
                        listbox.insert(tk.END, encabezado)
                        listbox.insert(tk.END, "-" * 55)

                        if resultados:
                            for mesa_id, materia_nombre, fecha, inscritos in resultados:
                                item = f"{mesa_id:<10}{materia_nombre:<20}{fecha:<15}{inscritos:<10}"
                                listbox.insert(tk.END, item)
            
                        else:
                            listbox.insert(END, "No hay mesas disponibles para la materia seleccionada.")
        
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Ocurrió un error al consultar la base de datos: {e}")
        
                    finally:
                        conexion.close()
                
                Button(frame_filtro, text="Buscar", command=buscar_por_materia,font=("Helvetica", 9), bg="lightblue").pack(pady=10)
        filtro_seleccionado.trace("w", actualizar_filtro)
            
        #CREACION DE LA LISTBOX 
        listbox = Listbox(frame_central, width=100, height=40, font=("Courier", 11), bg="white")
        listbox.pack(pady=10)

############################################## GESTION DE USUSARIOS #########################################################################################
######################################### FORMULARIO PARA DAR DE ALTA UN USUARIO NUEVO ##############################################################

    def generar_contrasena(longitud=8):
        #Genera una contraseña aleatoria
        caracteres = string.ascii_letters + string.digits
        return ''.join(random.choice(caracteres) for _ in range(longitud))

    def agregar():
        limpiar_frame()

        Label(frame_central, text="Agregar Nuevo Usuario", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)

        #Selecciona del tipo de usuario
        Label(frame_central, text="Tipo de Usuario:", font=("Helvetica", 12), bg="white").pack(pady=5)
        tipo_usuario = StringVar()
        combo_tipo_usuario = ttk.Combobox(frame_central, textvariable=tipo_usuario, font=("Helvetica", 12), state='readonly', width=30)
        combo_tipo_usuario["values"] = ["alumno", "administrador"]
        combo_tipo_usuario.pack(pady=5)
        combo_tipo_usuario.set("Seleccione un tipo")

        def actualizar_formulario(*args):
            for widget in frame_central.winfo_children():
                if widget != combo_tipo_usuario and widget != Label(frame_central, text="Agregar Nuevo Usuario", font=("Helvetica", 14, "bold"), bg="white"):
                    widget.destroy()

            if tipo_usuario.get() == "alumno":
                formulario_alumno()
            elif tipo_usuario.get() == "administrador":
                formulario_administrador()

        def formulario_alumno():
            Label(frame_central, text="Seleccionar Carrera:", font=("Helvetica", 12), bg="white").pack(pady=5)
            carrera_usuario = StringVar()

            #Extrae los nombres de carreras de la base de datos
            cursor.execute("SELECT nombre FROM carrera")
            carreras = [row[0] for row in cursor.fetchall()]

            combo_carrera = ttk.Combobox(frame_central, textvariable=carrera_usuario, font=("Helvetica", 12), state='readonly', width=30)
            combo_carrera["values"] = carreras
            combo_carrera.pack(pady=5)
            combo_carrera.set("Seleccione una carrera")

            Label(frame_central, text="Nombre Completo:", font=("Helvetica", 12), bg="white").pack(pady=5)
            nombre_usuario = Entry(frame_central, font=("Helvetica", 12), width=30)
            nombre_usuario.pack(pady=5)

            usuario_usuario, contrasena_usuario = crear_campos_usuario(nombre_usuario)

            def guardar_alumno():
                nombre = nombre_usuario.get().strip()
                carrera = carrera_usuario.get().strip()
                usuario = usuario_usuario.get().strip()
                contrasena = contrasena_usuario.get().strip()

                if not nombre or not carrera or not usuario or not contrasena:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                try:
                    # Obtiene ID de carrera
                    cursor.execute("SELECT id FROM carrera WHERE nombre = ?", (carrera,))
                    carrera_data = cursor.fetchone()

                    if not carrera_data:
                        messagebox.showwarning("Advertencia", "La carrera seleccionada no existe.")
                        return

                    id_carrera = carrera_data[0]
                    cursor.execute("INSERT INTO alumno (nombre, id_carrera) VALUES (?, ?)", (nombre, id_carrera))
                    conexion.commit()

                    #Inserta usuario en tabla de usuarios
                    cursor.execute("SELECT id FROM alumno WHERE nombre = ?", (nombre,))
                    id_alumno = cursor.fetchone()[0]
                    cursor.execute("INSERT INTO usuarios (usuario, contrasena, id_alumno, nivel) VALUES (?, ?, ?, ?)",
                                (usuario, contrasena, id_alumno, "alumno"))
                    conexion.commit()

                    messagebox.showinfo("Éxito", "Alumno registrado correctamente.")
                    limpiar_frame()

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Hubo un error al guardar el alumno: {e}")

            Button(frame_central, text="Guardar Alumno", font=("Helvetica", 12), bg="lightblue", command=guardar_alumno).pack(pady=20)

        def formulario_administrador():
            Label(frame_central, text="Nombre Completo:", font=("Helvetica", 12), bg="white").pack(pady=5)
            nombre_usuario = Entry(frame_central, font=("Helvetica", 12), width=30)
            nombre_usuario.pack(pady=5)

            usuario_usuario, contrasena_usuario = crear_campos_usuario(nombre_usuario)

            def guardar_administrador():
                nombre = nombre_usuario.get().strip()
                usuario = usuario_usuario.get().strip()
                contrasena = contrasena_usuario.get().strip()

                if not nombre or not usuario or not contrasena:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                try:
                    cursor.execute("INSERT INTO administradores (nombre) VALUES (?)", (nombre,))
                    conexion.commit()

                    cursor.execute("SELECT last_insert_rowid()")
                    id_admin = cursor.fetchone()[0]

                    cursor.execute("INSERT INTO usuarios (usuario, contrasena, nivel, id_admin) VALUES (?, ?, ?, ?)",
                                (usuario, contrasena, "administrador", id_admin))
                    conexion.commit()

                    messagebox.showinfo("Éxito", "Administrador registrado correctamente.")
                    limpiar_frame()

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Hubo un error al guardar el administrador: {e}")

            Button(frame_central, text="Guardar Administrador", font=("Helvetica", 12), bg="lightblue", command=guardar_administrador).pack(pady=20)

        def crear_campos_usuario(nombre_usuario_entry):
            Label(frame_central, text="Usuario:", font=("Helvetica", 12), bg="white").pack(pady=5)
            usuario_usuario = Entry(frame_central, font=("Helvetica", 12), width=30)
            usuario_usuario.pack(pady=5)

            Label(frame_central, text="Contraseña:", font=("Helvetica", 12), bg="white").pack(pady=5)
            contrasena_usuario = Entry(frame_central, font=("Helvetica", 12), width=30)
            contrasena_usuario.pack(pady=5)

            def sugerir_usuario_contrasena(event=None):
                nombre = nombre_usuario_entry.get().strip()
                if nombre:
                    if not usuario_usuario.get():
                        usuario_usuario.insert(0, nombre.split()[0].lower())
                    if not contrasena_usuario.get():
                        contrasena_usuario.insert(0, generar_contrasena())

            nombre_usuario_entry.bind("<FocusOut>", sugerir_usuario_contrasena)

            return usuario_usuario, contrasena_usuario

        tipo_usuario.trace("w", actualizar_formulario)

############################################## FORMULARIO PRINCIPAL USUARIOS #########################################################################################
    def crud_usuarios():
        limpiar_frame()
        Label(frame_central, text="Gestión de Usuarios", font=("Helvetica", 14, "bold"), bg="lightblue").pack(pady=20)


        # Filtro de Nivel de Usuario
        Label(frame_central, text="Nivel de Usuario:", font=("Helvetica", 12), bg="white").pack(pady=5)
        nivel_filtro = StringVar()
        combo_nivel_filtro = ttk.Combobox(frame_central, textvariable=nivel_filtro, font=("Helvetica", 12), state='readonly', width=30)
        combo_nivel_filtro["values"] = ["Todos", "Alumno", "Administrador"]
        combo_nivel_filtro.pack(pady=5)
        combo_nivel_filtro.set("Todos")

        #Tabla de usuarios
        tabla_usuarios = ttk.Treeview(frame_central, columns=("Usuario", "Nivel"), show="headings", height=10)
        tabla_usuarios.heading("Usuario", text="Usuario")
        tabla_usuarios.heading("Nivel", text="Nivel")
        tabla_usuarios.column("Usuario", width=200, anchor="center")
        tabla_usuarios.column("Nivel", width=100, anchor="center")
        tabla_usuarios.pack(pady=10)

        def cargar_usuarios():
            for row in tabla_usuarios.get_children():
                tabla_usuarios.delete(row)

            nivel = nivel_filtro.get()
            query = "SELECT usuario, nivel FROM usuarios"
            params = ()
            if nivel != "Todos":
                query += " WHERE nivel = ?"
                params = (nivel.lower(),)

            try:
                cursor.execute(query, params)
                usuarios = cursor.fetchall()
                for usuario, nivel in usuarios:
                    tabla_usuarios.insert("", "end", values=(usuario, nivel.capitalize()))
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al cargar usuarios: {e}")
        #ALTA
        def alta_usuario():
            agregar()

        #MODIFICACION
        def modificar_usuario():
            seleccion = tabla_usuarios.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un usuario para modificar.")
                return

            usuario_seleccionado = tabla_usuarios.item(seleccion, "values")[0]
            modificar_contrasena(usuario_seleccionado)

        #BAJA
        def eliminar_usuario():
            seleccion = tabla_usuarios.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar.")
                return

            usuario_seleccionado = tabla_usuarios.item(seleccion, "values")[0]
            confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el usuario '{usuario_seleccionado}'?")
            if confirmacion:
                try:
                    cursor.execute("DELETE FROM usuarios WHERE usuario = ?", (usuario_seleccionado,))
                    conexion.commit()
                    messagebox.showinfo("Éxito", f"Usuario '{usuario_seleccionado}' eliminado correctamente.")
                    cargar_usuarios()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al eliminar usuario: {e}")

        #BOTONES DEL MENU DEL CRUD USUARIOS
        Button(frame_central, text="Alta de Usuario", font=("Helvetica", 12), bg="lightblue", command=alta_usuario).pack(side="left", padx=10)
        Button(frame_central, text="Modificar Contraseña", font=("Helvetica", 12), bg="lightblue", command=modificar_usuario).pack(side="left", padx=10)
        Button(frame_central, text="Eliminar Usuario", font=("Helvetica", 12), bg="lightblue", command=eliminar_usuario).pack(side="left", padx=10)

        # Filtro de usuarios
        nivel_filtro.trace("w", lambda *args: cargar_usuarios())
        #Carga los usuarios al abrir el CRUD
        cargar_usuarios()

        def modificar_contrasena(usuario):
            limpiar_frame()

            Label(frame_central, text=f"Modificar Contraseña: {usuario}", font=("Helvetica", 14, "bold"), bg="white").pack(pady=20)

            Label(frame_central, text="Nueva Contraseña:", font=("Helvetica", 12), bg="white").pack(pady=5)
            nueva_contrasena_entry = Entry(frame_central, font=("Helvetica", 12), width=30, show="*")
            nueva_contrasena_entry.pack(pady=5)

            Label(frame_central, text="Confirmar Contraseña:", font=("Helvetica", 12), bg="white").pack(pady=5)
            confirmar_contrasena_entry = Entry(frame_central, font=("Helvetica", 12), width=30, show="*")
            confirmar_contrasena_entry.pack(pady=5)

            # Validación contraseña
            def verificar_contrasena(contrasena):
                if len(contrasena) < 8:
                    return "La contraseña debe tener al menos 8 caracteres."
                if not any(char.isdigit() for char in contrasena):
                    return "La contraseña debe incluir al menos un número."
                if not any(char.isupper() for char in contrasena):
                    return "La contraseña debe incluir al menos una letra mayúscula."
                if not any(char.islower() for char in contrasena):
                    return "La contraseña debe incluir al menos una letra minúscula."
                return ""

            def guardar_contrasena():
                nueva_contrasena = nueva_contrasena_entry.get().strip()
                confirmar_contrasena = confirmar_contrasena_entry.get().strip()

                if not nueva_contrasena or not confirmar_contrasena:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                if nueva_contrasena != confirmar_contrasena:
                    messagebox.showwarning("Advertencia", "Las contraseñas no coinciden.")
                    return

                error = verificar_contrasena(nueva_contrasena)
                if error:
                    messagebox.showwarning("Advertencia", error)
                    return

                try:
                    cursor.execute("UPDATE usuarios SET contrasena = ? WHERE usuario = ?", (nueva_contrasena, usuario))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
                    crud_usuarios()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error al actualizar contraseña: {e}")

            Button(frame_central, text="Guardar Cambios", font=("Helvetica", 12), bg="lightblue", command=guardar_contrasena).pack(pady=20)


############################################## GESTION DE MATERIAS #########################################################################################

    def form_materias():
        limpiar_frame()
        Label(frame_central, text="Gestión de Materias y Materias Regularizadas", font=("Helvetica", 14, "bold"), bg="lightblue").pack(pady=20)

        Button(frame_central, text="Materias", font=("Helvetica", 14), bg="lightblue", command=crud_materias).pack(pady=20)
        Button(frame_central, text="Materias Regularizadas", font=("Helvetica", 13), bg="lightblue", command=materias_regularizadas).pack(pady=20)
    
    def materias_regularizadas():
            limpiar_frame()
            Label(frame_central, text="Registrar Materias Regularizadas", font=("Helvetica", 14, "bold"), bg="lightblue").pack(pady=20)

            #Carrera
            Label(frame_central, text="Seleccionar Carrera:", font=("Helvetica", 12), bg="white").place(x=20, y=60)
            carrera_seleccionada = tk.StringVar()
            combo_carreras = ttk.Combobox(frame_central, textvariable=carrera_seleccionada, state="readonly", width=30)
            combo_carreras.place(x=20, y=90)

            try:
                cursor.execute("SELECT id, nombre FROM carrera")
                carreras = cursor.fetchall()
                lista_carreras = [carrera[1] for carrera in carreras]
                combo_carreras["values"] = lista_carreras
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Hubo un error al cargar las carreras: {e}")

            #Materia
            Label(frame_central, text="Seleccionar Materia:", font=("Helvetica", 12), bg="white").place(x=20, y=130)
            materia_seleccionada = tk.StringVar()
            combo_materias = ttk.Combobox(frame_central, textvariable=materia_seleccionada, state="readonly", width=30)
            combo_materias.place(x=20, y=160)

            def cargar_materias(event):
                carrera = carrera_seleccionada.get()
                if not carrera:
                    return
                try:
                    cursor.execute("""
                        SELECT materias.nombre 
                        FROM materias
                        INNER JOIN carrera ON materias.id_carrera = carrera.id
                        WHERE carrera.nombre = ?
                    """, (carrera,))
                    materias = cursor.fetchall()
                    lista_materias = [materia[0] for materia in materias]
                    combo_materias["values"] = lista_materias
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Hubo un error al cargar las materias: {e}")

            combo_carreras.bind("<<ComboboxSelected>>", cargar_materias)

            #Alumno
            Label(frame_central, text="Seleccionar Alumno:", font=("Helvetica", 12), bg="white").place(x=20, y=200)
            alumno_seleccionado = tk.StringVar()
            combo_alumnos = ttk.Combobox(frame_central, textvariable=alumno_seleccionado, state="readonly", width=30)
            combo_alumnos.place(x=20, y=230)

            def cargar_alumnos(event):
                carrera = carrera_seleccionada.get()
                materia = materia_seleccionada.get()
                if not carrera or not materia:
                    return
                try:
                    cursor.execute("""
                        SELECT alumno.nombre
                        FROM alumno
                        INNER JOIN carrera ON alumno.id_carrera = carrera.id
                        WHERE carrera.nombre = ?
                    """, (carrera,))
                    alumnos = cursor.fetchall()
                    lista_alumnos = [alumno[0] for alumno in alumnos]
                    combo_alumnos["values"] = lista_alumnos
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Hubo un error al cargar los alumnos: {e}")

            combo_materias.bind("<<ComboboxSelected>>", cargar_alumnos)

            #Calificación
            Label(frame_central, text="Calificación (6-10):", font=("Helvetica", 12), bg="white").place(x=20, y=270)
            nota_regularidad = tk.Entry(frame_central, font=("Helvetica", 12), width=5)
            nota_regularidad.place(x=220, y=270)

            # Fecha
            Label(frame_central, text="Fecha de Regularización:", font=("Helvetica", 12), bg="white").place(x=20, y=310)
            calendario = Calendar(frame_central, selectmode="day", year=2024, month=1, day=1)
            calendario.place(x=20, y=340)
            

            def registrar_regularidad():
                carrera = carrera_seleccionada.get()
                materia = materia_seleccionada.get()
                alumno = alumno_seleccionado.get()
                nota = nota_regularidad.get().strip()
                fecha = calendario.get_date()
                fecha_objeto = datetime.strptime(fecha, "%d/%m/%y")
                fecha_formateada = fecha_objeto.strftime("%d-%m-%Y")


                if not carrera or not materia or not alumno or not nota:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                    return

                try:
                    nota = int(nota)
                    if nota < 6 or nota > 10:
                        raise ValueError("Nota fuera de rango.")
                except ValueError:
                    messagebox.showwarning("Advertencia", "La nota debe ser un número entre 6 y 10.")
                    return
                confirmacion = messagebox.askyesno("Confirmar Registro", f"¿Deseas registrar la regularización de '{materia}' para el alumno '{alumno}' con nota {nota} en la fecha {fecha}?")
                if not confirmacion:
                    return 

                #Verifica si ya existe una regularidad
                try:
                    cursor.execute("""
                        SELECT 1 FROM materias_regularizadas
                        INNER JOIN alumno ON alumno.id = materias_regularizadas.id_alumno
                        INNER JOIN materias ON materias.id = materias_regularizadas.id_materia
                        INNER JOIN carrera ON carrera.id = alumno.id_carrera
                        WHERE alumno.nombre = ? AND materias.nombre = ? AND carrera.nombre = ?
                    """, (alumno, materia, carrera))
                    resultado = cursor.fetchone()

                    if resultado:
                        messagebox.showwarning("Advertencia", f"El alumno '{alumno}' ya tiene registrada la regularización de la materia '{materia}' para la carrera '{carrera}'.")
                        return

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Hubo un error al verificar la regularidad existente: {e}")
                    return
                
                #Regularización
                try:
                    cursor.execute("""
                        INSERT INTO materias_regularizadas (id_alumno, id_materia, calificacion, fecha)
                        SELECT alumno.id, materias.id, ?, ?
                        FROM alumno
                        INNER JOIN materias ON materias.nombre = ? 
                        WHERE alumno.nombre = ? AND materias.nombre = ?
                    """, (nota, fecha_formateada, materia, alumno, materia))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Materia regularizada registrada correctamente.")
                    materias_regularizadas()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Hubo un error al registrar la regularización: {e}")

            Button(frame_central, text="Registrar Regularidad", font=("Helvetica", 12), bg="lightblue", command=registrar_regularidad).pack(side="bottom", pady=30)

############################################################GESTION DE MATERIAS############################################################################

    def crud_materias():
        limpiar_frame()
        Label(frame_central, text="Gestión de Materias", font=("Helvetica", 14, "bold"), bg="lightblue").pack(pady=20)
        Button(frame_central, text="Agregar Nueva Materia", font=("Helvetica", 10), bg="lightblue", command=agregar_materia).place(x=20, y=70)

        ver_materias()
    
    def ver_materias():
        # DISEÑO
        frame_materias = Frame(frame_central, bg="white")
        frame_materias.place(x=40, y=100, width=460, height=400)

        Label(frame_materias, text="Lista de Materias", font=("Helvetica", 12, "bold"), bg="white").place(x=150, y=50)

        # treeview
        treeview = ttk.Treeview(frame_materias, columns=("Materia", "Carrera"), show="headings", height=15)
        treeview.place(x=20, y=90)
        treeview.heading("Materia", text="Materia", anchor="center")
        treeview.heading("Carrera", text="Carrera", anchor="center")
        treeview.column("Materia", width=200, anchor="center")
        treeview.column("Carrera", width=200, anchor="center")

        try:
            # Obtiene las materias y carreras desde la base de datos
            cursor.execute("""
                SELECT materias.id, materias.nombre, carrera.nombre
                FROM materias
                INNER JOIN carrera ON materias.id_carrera = carrera.id
            """)
            materias = cursor.fetchall()

            if materias:
                for id_materia, materia, carrera in materias:
                    treeview.insert("", tk.END, values=(materia, carrera), iid=id_materia)  # Usamos iid para almacenar el id_materia
            else:
                messagebox.showinfo("Información", "No hay materias registradas.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Hubo un error al obtener las materias: {e}")

        def editar_materia():
            selected_items = treeview.selection()
            if not selected_items:
                messagebox.showwarning("Advertencia", "Seleccione una materia para editar.")
                return

            # Obtiene los valores de la fila seleccionada
            selected_item = selected_items[0]
            item = treeview.item(selected_item)
            materia = item["values"][0]
            carrera = item["values"][1]
            id_materia = selected_item

            # Llama a la función para editar
            editar_formulario(materia, carrera, id_materia)


        def eliminar_materia():
            selected_items = treeview.selection()
            if not selected_items:
                messagebox.showwarning("Advertencia", "Seleccione una materia para eliminar.")
                return

            # Obtiene los valores de la fila seleccionada
            selected_item = selected_items[0]
            item = treeview.item(selected_item)
            materia = item["values"][0] 
            id_materia = selected_item

            confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar la materia '{materia}'?")
            if confirmacion:
                try:
                    cursor.execute("DELETE FROM materias WHERE id = ?", (id_materia,))
                    conexion.commit()
                    messagebox.showinfo("Éxito", "Materia eliminada correctamente.")
                    ver_materias()

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Hubo un error al eliminar la materia: {e}")

        Button(frame_central, text="Editar", font=("Helvetica", 12), bg="lightblue", command=editar_materia).place(x=150, y=540)
        Button(frame_central, text="Eliminar Materia", font=("Helvetica", 12), bg="lightblue", command=eliminar_materia).place(x=250, y=540)


    def editar_formulario(materia, carrera, id_materia):
        limpiar_frame()
        Label(frame_central, text="Editar Materia", font=("Helvetica", 14, "bold"), bg="white").place(x=20, y=20)

        Label(frame_central, text="Nombre de la Materia:", font=("Helvetica", 12), bg="white").place(x=20, y=60)
        nombre_materia = Entry(frame_central, font=("Helvetica", 12), width=30)
        nombre_materia.place(x=20, y=90)
        nombre_materia.insert(0, materia)

        Label(frame_central, text="Seleccionar Carrera:", font=("Helvetica", 12), bg="white").place(x=20, y=120)

        try:
            cursor.execute("SELECT id, nombre FROM carrera")
            carreras = cursor.fetchall()
            lista_carreras = [carrera[1] for carrera in carreras]
            lista_ids_carreras = [carrera[0] for carrera in carreras]

            carrera_seleccionada = StringVar()
            combo_carreras = ttk.Combobox(frame_central, textvariable=carrera_seleccionada, values=lista_carreras, state="readonly", width=28)
            combo_carreras.place(x=20, y=150)
            combo_carreras.set(carrera)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Hubo un error al obtener las carreras: {e}")

        def guardar_edicion():
            nuevo_nombre = nombre_materia.get().strip()
            nueva_carrera = carrera_seleccionada.get().strip()

            if not nuevo_nombre:
                messagebox.showwarning("Advertencia", "El nombre de la materia es obligatorio.")
                return

            if not nueva_carrera or nueva_carrera == "Seleccione una carrera":
                messagebox.showwarning("Advertencia", "Debe seleccionar una carrera.")
                return

            try:
                cursor.execute("SELECT id FROM carrera WHERE nombre = ?", (nueva_carrera,))
                id_nueva_carrera = cursor.fetchone()[0]

                # Actualiza la materia en la base de datos
                cursor.execute("UPDATE materias SET nombre = ?, id_carrera = ? WHERE id = ?", (nuevo_nombre, id_nueva_carrera, id_materia))
                conexion.commit()

                messagebox.showinfo("Éxito", "Materia actualizada correctamente.")
                crud_materias()

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Hubo un error al actualizar la materia: {e}")
                
        Button(frame_central, text="Guardar Cambios", font=("Helvetica", 12), bg="lightblue", command=guardar_edicion).place(x=20, y=190)


    def agregar_materia():
        limpiar_frame()
        Label(frame_central, text="Agregar Nueva Materia", font=("Helvetica", 14, "bold"), bg="lightblue").pack(pady=20)
        Label(frame_central, text="Seleccionar Carrera:", font=("Helvetica", 12), bg="white").pack(pady=10)

        # Obtiene las carreras de la base de datos
        try:
            cursor.execute("SELECT id, nombre FROM carrera")
            carreras = cursor.fetchall()
            lista_carreras = [carrera[1] for carrera in carreras]

            carrera_seleccionada = StringVar()
            combo_carreras = ttk.Combobox(frame_central, textvariable=carrera_seleccionada, values=lista_carreras, state="readonly", width=28)
            combo_carreras.pack(pady=10)
            combo_carreras.set("Seleccione una carrera")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Hubo un error al obtener las carreras: {e}")

        Label(frame_central, text="Nombre de la Materia:", font=("Helvetica", 12), bg="white").pack(pady=10)
        nombre_materia = Entry(frame_central, font=("Helvetica", 12), width=30)
        nombre_materia.pack(pady=10)

        def guardar_materia():
            nombre = nombre_materia.get().strip()
            carrera = carrera_seleccionada.get().strip()

            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre de la materia es obligatorio.")
                return
            
            if not carrera or carrera == "Seleccione una carrera":
                messagebox.showwarning("Advertencia", "Debe seleccionar una carrera.")
                return
            
            try:
                cursor.execute("SELECT id FROM carrera WHERE nombre = ?", (carrera,))
                id_carrera = cursor.fetchone()[0]

                # Verifica si la materia ya existe
                cursor.execute("SELECT 1 FROM materias WHERE nombre = ?", (nombre,))
                if cursor.fetchone():
                    messagebox.showwarning("Advertencia", "La materia ya existe.")
                    return

                # Inserta la nueva materia
                cursor.execute("INSERT INTO materias (nombre, id_carrera) VALUES (?, ?)", (nombre, id_carrera))
                conexion.commit()
                messagebox.showinfo("Éxito", "Materia agregada correctamente.")
                crud_materias()

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Hubo un error al agregar la materia: {e}")

        Button(frame_central, text="Agregar Materia", font=("Helvetica", 12), bg="lightblue", command=guardar_materia).pack(pady=20)



############################################## BOTONES DEL MENU PRINCIPAL #########################################################################################
    Label(panel_admin, text="Gestión Administrativa", font=("Helvetica", 24,"bold"),bg="lightblue").place(x=260, y=20)
    Label(panel_admin, text="MENÚ", font=("Helvetica", 11),bg="lightblue").place(x=30, y=80)
    Button(panel_admin, text="MESAS", font=("Helvetica", 11,"bold" ),bg="lightblue", command=gestionar_mesas_examen).place(x=30, y=130, width=200, height=40)
    Button(panel_admin, text="USUARIOS", font=("Helvetica", 11,"bold"),bg="lightblue", command=crud_usuarios).place(x=30, y=180, width=200, height=40)
    Button(panel_admin, text="MATERIAS", font=("Helvetica", 11,"bold"),bg="lightblue", command=form_materias).place(x=30, y=230, width=200, height=40)


    panel_admin.mainloop()
    conexion.commit()
    conexion.close()

########################################################################## DISEÑO DEL LOGIN ###############################################################


login=Tk()
usuario=StringVar()
contrasena=StringVar()

login.title('login')
login.geometry('300x300')
lblnombre1=Label(login, text='Usuario: ', font=("Helvetica",10, "bold"))
lblnombre1.place(x=110, y=30)
lblnombre2=Label(login, text='Contraseña: ',font=("Helvetica",10, "bold"))
lblnombre2.place(x=100, y=90)
entrada1=Entry(login, textvariable=usuario,font=("Arial", 10),relief="solid", bd=1)
entrada1.place(x=70, y=60)
entrada2=Entry(login, textvariable=contrasena,font=("Arial", 10), relief="solid", bd=1, show="*")
entrada2.place(x=70, y=120)
btningresar=Button(login, text='INGRESAR', command=ingresar, bg="lightblue",fg='black',font=("Helvetica",10, "bold"),relief="raised",bd=4, width=10,height=1, activebackground="lightblue",activeforeground='white')
btningresar.place(x=100, y=190)
btnmodificar=Button(login, text='Cambiar Contraseña', command=modificar, bg="lightblue",fg='black',font=("Helvetica",8),relief="raised",bd=2, width=18,height=1, activebackground="lightblue",activeforeground='white')
btnmodificar.place(x=90, y=250)
login.mainloop()
conexion.commit()
conexion.close()

