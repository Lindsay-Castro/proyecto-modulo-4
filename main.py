import tkinter as tk
from tkinter import messagebox, ttk
from database import BaseDatosGIC
from api_services import ServicioAPI, logging

class ValidacionError(Exception):
    """Excepción para capturar errores de validación de negocio."""
    pass

class Cliente:
    """Clase base con encapsulamiento explícito."""
    def __init__(self, id_cliente, nombre, email, telefono):
        self._id_cliente = id_cliente.strip()
        self._nombre = nombre.strip()
        self._email = email.strip()
        self._telefono = telefono.strip()
        self.validar_datos()

    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    @property
    def telefono(self):
        return self._telefono

    def validar_datos(self):
        """Valida que los campos cumplan con el formato mínimo."""
        if not self._id_cliente or not self._nombre:
            raise ValidacionError("El ID y el Nombre son obligatorios.")
        if "@" not in self._email or "." not in self._email:
            raise ValidacionError("El correo electrónico no tiene un formato válido.")
        if not self._telefono.isdigit() or len(self._telefono) < 7:
            raise ValidacionError("El teléfono debe contener solo números (mínimo 7 dígitos).")

    def obtener_descuento(self):
        """Método polimórfico base."""
        return 0.0

    def __str__(self):
        return f"[{self._id_cliente}] {self._nombre} | Email: {self._email} | Tel: {self._telefono}"

    def __eq__(self, otro):
        """Método especial para comparar dos clientes por su ID."""
        if isinstance(otro, Cliente):
            return self._id_cliente == otro._id_cliente
        return False


class ClienteRegular(Cliente):
    """Subclase Cliente Regular."""
    def obtener_descuento(self):
        return 5.0

    def __str__(self):
        return f"[REGULAR] {super().__str__()} | Descuento: {self.obtener_descuento()}%"


class ClientePremium(Cliente):
    """Subclase Cliente Premium."""
    def __init__(self, id_cliente, nombre, email, telefono, nivel_membresia="Gold"):
        super().__init__(id_cliente, nombre, email, telefono)
        if not nivel_membresia.strip():
            raise ValidacionError("Debe especificar el nivel de membresía.")
        self._nivel_membresia = nivel_membresia.strip()

    @property
    def nivel_membresia(self):
        return self._nivel_membresia

    def obtener_descuento(self):
        return 15.0

    def __str__(self):
        return f"[PREMIUM - {self._nivel_membresia}] {super().__str__()} | Descuento: {self.obtener_descuento()}%"


class ClienteCorporativo(Cliente):
    """Subclase Cliente Corporativo."""
    def __init__(self, id_cliente, nombre, email, telefono, empresa):
        if not empresa.strip():
            raise ValidacionError("Debe especificar el nombre de la empresa.")
        super().__init__(id_cliente, nombre, email, telefono)
        self._empresa = empresa.strip()

    @property
    def empresa(self):
        return self._empresa

    def obtener_descuento(self):
        return 25.0

    def __str__(self):
        return f"[CORPORATIVO - {self._empresa}] {super().__str__()} | Descuento: {self.obtener_descuento()}%"

class AppGIC:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor Inteligente de Clientes (GIC)")
        self.root.geometry("800x650")
        
        self.db = BaseDatosGIC()
        self._crear_interfaz()
        self.cargar_datos_tabla()

    def _crear_interfaz(self):
        # Frame Formulario
        frame_form = ttk.LabelFrame(self.root, text=" Formulario de Cliente ", padding=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="ID Cliente:").grid(row=0, column=0, sticky="w", pady=2)
        self.txt_id = ttk.Entry(frame_form)
        self.txt_id.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="w", pady=2)
        self.txt_nombre = ttk.Entry(frame_form)
        self.txt_nombre.grid(row=0, column=3, sticky="ew", pady=2)

        ttk.Label(frame_form, text="Email:").grid(row=1, column=0, sticky="w", pady=2)
        self.txt_email = ttk.Entry(frame_form)
        self.txt_email.grid(row=1, column=1, sticky="ew", pady=2)

        ttk.Label(frame_form, text="Teléfono:").grid(row=1, column=2, sticky="w", pady=2)
        self.txt_telefono = ttk.Entry(frame_form)
        self.txt_telefono.grid(row=1, column=3, sticky="ew", pady=2)

        ttk.Label(frame_form, text="Tipo Cliente:").grid(row=2, column=0, sticky="w", pady=2)
        self.combo_tipo = ttk.Combobox(frame_form, values=["Regular", "Premium", "Corporativo"], state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=2, column=1, sticky="ew", pady=2)
        self.combo_tipo.bind("<<ComboboxSelected>>", self._on_tipo_change)

        self.lbl_extra = ttk.Label(frame_form, text="Dato Extra:")
        self.txt_extra = ttk.Entry(frame_form)

        for col in range(4):
            frame_form.columnconfigure(col, weight=1)

        self._on_tipo_change()

        frame_acciones = ttk.Frame(self.root, padding=5)
        frame_acciones.pack(fill="x", padx=10)

        ttk.Button(frame_acciones, text="Guardar / Actualizar", command=self.guardar_cliente).pack(side="left", padx=5)
        ttk.Button(frame_acciones, text="Eliminar Seleccionado", command=self.eliminar_cliente).pack(side="left", padx=5)
        ttk.Button(frame_acciones, text="Limpiar Formulario", command=self._limpiar_formulario).pack(side="left", padx=5)
        
        ttk.Button(frame_acciones, text="Exportar a JSON", command=self.exportar_json).pack(side="right", padx=5)
        ttk.Button(frame_acciones, text="Exportar a CSV", command=self.exportar_csv).pack(side="right", padx=5)

        frame_tabla = ttk.LabelFrame(self.root, text=" Clientes Registrados ", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("ID", "Nombre", "Email", "Teléfono", "Tipo", "Extra")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tabla.bind("<Double-1>", self.cargar_registro_seleccionado)

    def _on_tipo_change(self, event=None):
        tipo = self.combo_tipo.get()
        if tipo == "Regular":
            self.lbl_extra.grid_forget()
            self.txt_extra.grid_forget()
        elif tipo == "Premium":
            self.lbl_extra.config(text="Nivel Membresía:")
            self.lbl_extra.grid(row=2, column=2, sticky="w", pady=2)
            self.txt_extra.grid(row=2, column=3, sticky="ew", pady=2)
        elif tipo == "Corporativo":
            self.lbl_extra.config(text="Empresa:")
            self.lbl_extra.grid(row=2, column=2, sticky="w", pady=2)
            self.txt_extra.grid(row=2, column=3, sticky="ew", pady=2)

    def guardar_cliente(self):
        id_c = self.txt_id.get()
        nombre = self.txt_nombre.get()
        email = self.txt_email.get()
        telefono = self.txt_telefono.get()
        tipo = self.combo_tipo.get()
        extra = self.txt_extra.get()

        try:
            if tipo == "Regular":
                cliente = ClienteRegular(id_c, nombre, email, telefono)
            elif tipo == "Premium":
                cliente = ClientePremium(id_c, nombre, email, telefono, extra)
            elif tipo == "Corporativo":
                cliente = ClienteCorporativo(id_c, nombre, email, telefono, extra)

            # Integración con Servicio de API Externa
            ServicioAPI.validar_email_api(cliente.email)

            # Guardado en SQLite
            self.db.guardar_cliente(cliente, tipo, extra)

            # Notificación API
            ServicioAPI.enviar_notificacion_bienvenida(cliente.nombre, cliente.email)

            self.cargar_datos_tabla()
            self._limpiar_formulario()
            messagebox.showinfo("Éxito", f"Cliente {tipo} guardado correctamente.")

        except ValidacionError as ve:
            messagebox.showwarning("Error de Validación", str(ve))
        except Exception as e:
            logging.error(f"Error inesperado al guardar cliente: {e}")
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {str(e)}")

    def eliminar_cliente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccione un cliente de la tabla para eliminar.")
            return

        item = self.tabla.item(seleccion[0])
        id_cliente = item["values"][0]

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al cliente con ID {id_cliente}?"):
            self.db.eliminar_cliente(id_cliente)
            self.cargar_datos_tabla()
            self._limpiar_formulario()
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")

    def cargar_datos_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        registros = self.db.obtener_todos()
        for r in registros:
            self.tabla.insert("", "end", values=r)

    def cargar_registro_seleccionado(self, event):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item["values"]
            self._limpiar_formulario()
            
            self.txt_id.insert(0, valores[0])
            self.txt_nombre.insert(0, valores[1])
            self.txt_email.insert(0, valores[2])
            self.txt_telefono.insert(0, valores[3])
            
            tipo = valores[4]
            self.combo_tipo.set(tipo)
            self._on_tipo_change()
            
            if tipo in ["Premium", "Corporativo"]:
                self.txt_extra.insert(0, valores[5])

    def _limpiar_formulario(self):
        self.txt_id.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_telefono.delete(0, tk.END)
        self.txt_extra.delete(0, tk.END)

    def exportar_json(self):
        self.db.exportar_json()
        messagebox.showinfo("Exportación", "Datos exportados exitosamente a 'clientes.json'.")

    def exportar_csv(self):
        self.db.exportar_csv()
        messagebox.showinfo("Exportación", "Datos exportados exitosamente a 'clientes.csv'.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppGIC(root)
    root.mainloop()