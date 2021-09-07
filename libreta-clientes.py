from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hola mundo: treeview")

#<--- CREACION DE LA BASE DE DATOS CON SQLITE3 --->#
conn = sqlite3.connect("libreta.db")
c = conn.cursor()

c.execute(
    """CREATE TABLE if not EXISTS 
    cliente(id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    empresa TEXT NOT NULL);"""
)
#<--- FIN CREACION DE LA BASE DE DATOS CON SQLITE3 --->#


#<--- FUNCIONES NECESARIAS --->#

def render_clientes():
    rows = c.execute("SELECT * FROM cliente").fetchall()

    tree.delete(*tree.get_children()) #Elimina todas las filas
    for row in rows:
        tree.insert("", END, row[0], values=(row[1], row[2], row[3]))


def nuevo_cliente():
    def insertar(cliente):
        c.execute(
            "INSERT INTO cliente (nombre, telefono, empresa) VALUES (?, ?, ?)", 
            (cliente["nombre"], cliente["telefono"], cliente["empresa"])
        )
        conn.commit()
        render_clientes()

    def guardar():
        if not eNombre.get():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        if not eTelefono.get():
            messagebox.showerror("Error", "El telefono es obligatorio")
            return
        if not eEmpresa.get():
            messagebox.showerror("Error", "El empresa es obligatorio")
            return
        cliente = {
            "nombre": eNombre.get(),
            "telefono": eTelefono.get(),
            "empresa": eEmpresa.get(),
        }
        insertar(cliente)
        top.destroy()

    top = Toplevel()
    top.title("Nuevo Cliente")
    
    lNombre = Label(top, text="Nombre")
    lNombre.grid(row=0, column=0)
    eNombre = Entry(top, width=40)
    eNombre.grid(row=0, column=1)

    lTelefono = Label(top, text="Telefono")
    lTelefono.grid(row=1, column=0)
    eTelefono = Entry(top, width=40)
    eTelefono.grid(row=1, column=1)

    lEmpresa = Label(top, text="Empresa")
    lEmpresa.grid(row=2, column=0)
    eEmpresa = Entry(top, width=40)
    eEmpresa.grid(row=2, column=1)

    btnGuardar = Button(top, text="Guardar Cliente", command=guardar)
    btnGuardar.grid(row=3, column=1)
    eNombre.focus()
    top.mainloop()

def eliminar_cliente():
    i = tree.selection()[0]
    cliente = c.execute("SELECT * FROM cliente WHERE id = ?;", (i, )).fetchone()
    resp = messagebox.askokcancel("¿Seguro?", "¿Estás seguro de querer eliminar el registro '" + cliente[1] + "' ?")
    if resp:
        c.execute("DELETE FROM cliente WHERE id = ?;", (i, ))
        conn.commit()
        render_clientes()
#<--- FIN DE LAS FUNCIONES --->#

#<---  --->#
btn = Button(root, text="Nuevo cliente", command=nuevo_cliente)
btn.grid(column=0, row=0)

btn = Button(root, text="Eliminar cliente", command=eliminar_cliente)
btn.grid(column=1, row=0)

#<--- FIN --->#

tree = ttk.Treeview(root)
tree["columns"] = ("Nombre", "Telefono", "Empresa")

tree.column("#0", width=0, stretch=NO)
tree.column("Nombre")
tree.column("Telefono")
tree.column("Empresa")

tree.heading("Nombre", text="Nombre")
tree.heading("Telefono", text="Teléfono")
tree.heading("Empresa", text="Empresa")

tree.grid(row=2, column=0, columnspan=2, sticky="nsew")

render_clientes()
root.mainloop()