from tkinter import *
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import hashlib
import os
from datetime import datetime


class GenerarHash(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Generador de Hash by JoseLu Web Soluciones")
        self.geometry("500x400+200+100")
        self.resizable(False, False)

        # Cargar el archivo de imagen desde el disco como ícono
        try:
            icono = tk.PhotoImage(file="assets/logo.png")
            self.iconphoto(True, icono)
        except Exception as e:
            print(f"No se pudo cargar el ícono: {e}")

        # Crear contenedor principal
        self.container = Frame(self)
        self.container.pack(side=TOP, fill=BOTH, expand=True)
        self.container.configure(bg="#1974b0")

        # Label para mostrar instrucciones
        self.label_instrucciones = tk.Label(
            self.container,
            text="Elija el archivo para generar su hash SHA256:",
            font="Arial 12 bold",
            bg="#1974b0",
            fg="#ffffff",
        )
        self.label_instrucciones.pack(pady=10)

        # Botón para buscar archivo
        self.boton_buscar = tk.Button(
            self.container,
            text="Buscar Archivo",
            font="Arial 12 bold",
            command=self.buscar_archivo,
            bg="#00B4D8",
            fg="#ffffff",
        )
        self.boton_buscar.pack(pady=10)

        # Label para mostrar la ruta del archivo seleccionado
        self.label_ruta = tk.Label(
            self.container, text="", font="Arial 10 bold", bg="#1974b0", fg="white"
        )
        self.label_ruta.pack(pady=5)

        # Frame para el widget Text y su scrollbar
        self.text_frame = Frame(self.container)
        self.text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Barra de desplazamiento vertical
        self.scrollbar = Scrollbar(self.text_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Widget Text para mostrar el contenido del archivo hash.txt
        self.text_contenido = Text(
            self.text_frame,
            font="Courier 10",
            bg="#1974b0",
            fg="white",
            wrap=WORD,
            yscrollcommand=self.scrollbar.set,
            state="disabled",  # Desactivado para solo mostrar texto
        )
        self.text_contenido.pack(fill=BOTH, expand=True)
        self.scrollbar.config(command=self.text_contenido.yview)

    def buscar_archivo(self):
        """
        Abre el explorador de archivos para seleccionar un archivo y genera su hash.
        """
        ruta = filedialog.askopenfilename(title="Seleccionar archivo")
        if ruta:
            self.label_ruta.config(text=f"Archivo seleccionado:\n{ruta}")
            self.generar_y_guardar_hash(ruta)
            self.label_ruta.config(text=f"Archivo seleccionado:\n{ruta}\n\nRuta del archivo que contiene el HASH:\n{self.ruta_salida}")

    def generar_y_guardar_hash(self, ruta_archivo):
        """
        Genera el hash SHA256 del archivo seleccionado y lo guarda en un archivo de texto.
        """
        hash_resultado = self.generar_hash_sha256(ruta_archivo)

        if "Error" not in hash_resultado:
            # Preguntar por el nombre del archivo de salida
            nombre_txt = simpledialog.askstring(
                "Guardar Hash",
                "Ingrese el nombre del archivo para guardar el hash (sin extensión):",
            )
            if nombre_txt:
                self.ruta_salida = os.path.join(os.path.dirname(ruta_archivo), f"{nombre_txt}.txt")
                self.exportar_hash(hash_resultado, ruta_archivo, self.ruta_salida)

                # Mostrar mensaje de éxito
                messagebox.showinfo("HASH generado con éxito", f"Hash guardado correctamente en: {self.ruta_salida}")

                # Mostrar el contenido del archivo hash.txt
                self.mostrar_contenido_hash(self.ruta_salida)
        else:
            messagebox.showerror("Error", hash_resultado)

    def generar_hash_sha256(self, ruta_archivo):
        """
        Genera el hash SHA256 de un archivo.
        
        :param ruta_archivo: Ruta del archivo a procesar.
        :return: Hash SHA256 en formato hexadecimal.
        """
        sha256 = hashlib.sha256()
        try:
            with open(ruta_archivo, "rb") as archivo:
                while chunk := archivo.read(8192):  # Leer en bloques de 8 KB
                    sha256.update(chunk)
            return sha256.hexdigest()
        except FileNotFoundError:
            return "Error: Archivo no encontrado."
        except Exception as e:
            return f"Error: {e}"

    def exportar_hash(self, hash_resultado, ruta_archivo, ruta_salida):
        """
        Exporta el hash, junto con detalles adicionales, a un archivo de texto.
        
        :param hash_resultado: Hash generado.
        :param ruta_archivo: Ruta del archivo procesado.
        :param ruta_salida: Ruta del archivo donde se guarda el hash.
        """
        try:
            nombre_archivo = os.path.basename(ruta_archivo)  # Obtiene el nombre del archivo
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha y hora actual

            with open(ruta_salida, "w") as archivo_salida:
                archivo_salida.write(f"Nombre del archivo: {nombre_archivo}\n")
                archivo_salida.write(f"Ruta del archivo: {ruta_archivo}\n")
                archivo_salida.write(f"Fecha de generación: {fecha_actual}\n")
                archivo_salida.write(f"Hash SHA256: {hash_resultado}\n")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el hash: {e}")

    def mostrar_contenido_hash(self, ruta_salida):
        """
        Muestra el contenido del archivo hash.txt en la ventana principal.
        """
        try:
            with open(ruta_salida, "r") as archivo:
                contenido = archivo.read()

            # Habilitar el widget Text, insertar el contenido y volver a deshabilitarlo
            self.text_contenido.config(state="normal")
            self.text_contenido.delete("1.0", END)  # Limpiar contenido previo
            self.text_contenido.insert("1.0", contenido)  # Insertar el contenido del archivo
            self.text_contenido.config(state="disabled")  # Volver a deshabilitar el widget
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")


if __name__ == "__main__":
    app = GenerarHash()
    app.mainloop()