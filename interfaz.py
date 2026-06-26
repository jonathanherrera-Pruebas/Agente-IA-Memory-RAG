import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from agente import agent


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class InterfazAgente(ctk.CTk):
	def __init__(self) -> None:
		super().__init__()

		# Ventana principal con diseño oscuro y tamaño tipo chat moderno.
		self.title("AGENTE IA")
		self.geometry("1000x700")
		self.minsize(900, 600)

		self.configure(fg_color="#0f1115")

		self._respuesta_en_curso = False
		self._placeholder_idx = None

		self.grid_rowconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self._crear_encabezado()
		self._crear_area_chat()
		self._crear_panel_inferior()

	def _crear_encabezado(self) -> None:
		encabezado = ctk.CTkFrame(self, fg_color="#151a23", corner_radius=18)
		encabezado.grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 12))
		encabezado.grid_columnconfigure(0, weight=1)

		titulo = ctk.CTkLabel(
			encabezado,
			text="AGENTE IA",
			font=ctk.CTkFont(size=26, weight="bold"),
			text_color="#f5f7fb",
		)
		titulo.grid(row=0, column=0, sticky="w", padx=18, pady=(14, 2))

		subtitulo = ctk.CTkLabel(
			encabezado,
			text="Tools + RAG + Memory",
			font=ctk.CTkFont(size=14),
			text_color="#9aa4b2",
		)
		subtitulo.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 10))

		estado = ctk.CTkLabel(
			encabezado,
			text="🟢 Sistema listo",
			font=ctk.CTkFont(size=13, weight="bold"),
			text_color="#7ee787",
		)
		estado.grid(row=0, column=1, rowspan=2, sticky="e", padx=18)

	def _crear_area_chat(self) -> None:
		contenedor = ctk.CTkFrame(self, fg_color="#10151d", corner_radius=18)
		contenedor.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 12))
		contenedor.grid_rowconfigure(0, weight=1)
		contenedor.grid_columnconfigure(0, weight=1)

		self.chat_historial = ctk.CTkTextbox(
			contenedor,
			wrap="word",
			font=ctk.CTkFont(size=14),
			fg_color="#0f141c",
			text_color="#e8eef7",
			corner_radius=14,
			border_width=1,
			border_color="#243041",
		)
		self.chat_historial.grid(row=0, column=0, sticky="nsew", padx=14, pady=14)
		self.chat_historial.configure(state="disabled")

		self._configurar_tags_historial()

	def _crear_panel_inferior(self) -> None:
		panel = ctk.CTkFrame(self, fg_color="#151a23", corner_radius=18)
		panel.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
		panel.grid_columnconfigure(0, weight=1)
		panel.grid_columnconfigure(1, weight=0)
		panel.grid_rowconfigure(0, weight=1)
		panel.grid_rowconfigure(1, weight=0)

		self.caja_texto = ctk.CTkTextbox(
			panel,
			height=95,
			wrap="word",
			font=ctk.CTkFont(size=14),
			fg_color="#0f141c",
			text_color="#f3f6fb",
			border_width=1,
			border_color="#2a3342",
			corner_radius=12,
		)
		self.caja_texto.grid(row=0, column=0, columnspan=2, sticky="ew", padx=14, pady=(14, 10))
		self.caja_texto.bind("<Return>", self._manejar_enter)

		botones = ctk.CTkFrame(panel, fg_color="transparent")
		botones.grid(row=1, column=0, columnspan=2, sticky="ew", padx=14, pady=(0, 14))
		botones.grid_columnconfigure(0, weight=1)

		grupo_izquierdo = ctk.CTkFrame(botones, fg_color="transparent")
		grupo_izquierdo.grid(row=0, column=0, sticky="w")

		btn_limpiar = ctk.CTkButton(
			grupo_izquierdo,
			text="Limpiar conversación",
			command=self.limpiar_conversacion,
			fg_color="#334155",
			hover_color="#475569",
			text_color="#ffffff",
			corner_radius=12,
			height=40,
		)
		btn_limpiar.grid(row=0, column=0, padx=(0, 10))

		btn_salir = ctk.CTkButton(
			grupo_izquierdo,
			text="Salir",
			command=self.destroy,
			fg_color="#7f1d1d",
			hover_color="#991b1b",
			text_color="#ffffff",
			corner_radius=12,
			height=40,
		)
		btn_salir.grid(row=0, column=1)

		btn_enviar = ctk.CTkButton(
			botones,
			text="Enviar",
			command=self.enviar_mensaje,
			fg_color="#2563eb",
			hover_color="#1d4ed8",
			text_color="#ffffff",
			corner_radius=12,
			height=44,
			width=160,
		)
		btn_enviar.grid(row=0, column=1, sticky="e")

	def _configurar_tags_historial(self) -> None:
		widget_texto = getattr(self.chat_historial, "_textbox", None)
		if widget_texto is None:
			return

		widget_texto.tag_configure("usuario", foreground="#93c5fd")
		widget_texto.tag_configure("ia", foreground="#f9fafb")
		widget_texto.tag_configure("etiqueta_usuario", foreground="#60a5fa", font=("Segoe UI", 11, "bold"))
		widget_texto.tag_configure("etiqueta_ia", foreground="#34d399", font=("Segoe UI", 11, "bold"))
		widget_texto.tag_configure("placeholder", foreground="#94a3b8", font=("Segoe UI", 11, "italic"))

	def _insertar_texto(self, texto, tag=None) -> None:
		self.chat_historial.configure(state="normal")
		if tag is None:
			self.chat_historial.insert("end", texto)
		else:
			widget_texto = getattr(self.chat_historial, "_textbox", None)
			if widget_texto is not None:
				widget_texto.insert("end", texto, tag)
			else:
				self.chat_historial.insert("end", texto)
		self.chat_historial.see("end")
		self.chat_historial.configure(state="disabled")

	def _agregar_mensaje_usuario(self, mensaje) -> None:
		self._insertar_texto("👤 Usuario\n", "etiqueta_usuario")
		self._insertar_texto(f"{mensaje}\n\n", "usuario")

	def _agregar_mensaje_ia(self, mensaje) -> None:
		self._insertar_texto("🤖 IA\n", "etiqueta_ia")
		self._insertar_texto(f"{mensaje}\n\n", "ia")

	def _agregar_placeholder(self) -> None:
		self._placeholder_idx = self.chat_historial.index("end-1c")
		self._insertar_texto("🤖 Pensando...\n\n", "placeholder")

	def _reemplazar_placeholder(self, mensaje) -> None:
		self.chat_historial.configure(state="normal")
		if self._placeholder_idx is not None:
			self.chat_historial.delete(self._placeholder_idx, "end")
		self.chat_historial.configure(state="disabled")
		self._placeholder_idx = None
		self._agregar_mensaje_ia(mensaje)

	def _manejar_enter(self, event):
		if event.state & 0x0001:
			return None
		self.enviar_mensaje()
		return "break"

	def _obtener_texto_caja(self):
		texto = self.caja_texto.get("1.0", "end").strip()
		return texto

	def enviar_mensaje(self) -> None:
		if self._respuesta_en_curso:
			return

		pregunta = self._obtener_texto_caja()
		if not pregunta:
			return

		self.caja_texto.delete("1.0", "end")
		self._agregar_mensaje_usuario(pregunta)
		self._agregar_placeholder()

		# La consulta se procesa fuera del hilo principal para no congelar la UI.
		self._respuesta_en_curso = True
		hilo = threading.Thread(target=self._procesar_mensaje, args=(pregunta,), daemon=True)
		hilo.start()

	def _procesar_mensaje(self, pregunta) -> None:
		try:
			respuesta = agent.invoke(
				{
					"messages": [
						{
							"role": "user",
							"content": pregunta,
						}
					]
				},
				config={
					"configurable": {
						"thread_id": "jonathan"
					}
				}
			)

			mensaje_final = self._extraer_texto_respuesta(respuesta)
			self.after(0, lambda: self._mostrar_respuesta(mensaje_final))

		except Exception as error:
			mensaje_error = str(error)
			self.after(0, lambda e=mensaje_error: self._mostrar_error(e))

	def _mostrar_respuesta(self, mensaje) -> None:
		self._reemplazar_placeholder(mensaje)
		self._respuesta_en_curso = False

	def _mostrar_error(self, error) -> None:
		self.chat_historial.configure(state="normal")
		if self._placeholder_idx is not None:
			self.chat_historial.delete(self._placeholder_idx, "end")
			self._placeholder_idx = None
		self.chat_historial.configure(state="disabled")
		self._respuesta_en_curso = False

		mensaje_error = str(error)
		if "429" in mensaje_error or "RESOURCE_EXHAUSTED" in mensaje_error:
			mensaje_error = "La cuota gratuita de Gemini se agotó. Intenta nuevamente más tarde."

		messagebox.showerror("Error", mensaje_error)

	def _extraer_texto_respuesta(self, respuesta) -> str:
		# El agente puede devolver mensajes anidados; aquí se normaliza a texto plano.
		if isinstance(respuesta, dict):
			mensajes = respuesta.get("messages", [])
			if mensajes:
				ultimo = mensajes[-1]
				contenido = getattr(ultimo, "content", None)
				if contenido is None and isinstance(ultimo, dict):
					contenido = ultimo.get("content")
				return self._normalizar_contenido(contenido)

		return self._normalizar_contenido(respuesta)

	def _normalizar_contenido(self, contenido) -> str:
		if isinstance(contenido, str):
			return contenido.strip()

		if isinstance(contenido, dict):
			texto = contenido.get("text")
			if isinstance(texto, str):
				return texto.strip()
			return str(contenido)

		if isinstance(contenido, (list, tuple)):
			partes = []
			for elemento in contenido:
				if isinstance(elemento, str):
					partes.append(elemento)
				elif isinstance(elemento, dict):
					texto = elemento.get("text")
					if isinstance(texto, str):
						partes.append(texto)
					else:
						texto = elemento.get("content")
						if isinstance(texto, str):
							partes.append(texto)
				else:
					texto = getattr(elemento, "text", None)
					if isinstance(texto, str):
						partes.append(texto)

			return "".join(partes).strip()

		if hasattr(contenido, "text"):
			texto = getattr(contenido, "text")
			if isinstance(texto, str):
				return texto.strip()

		return str(contenido).strip()

	def limpiar_conversacion(self) -> None:
		self.chat_historial.configure(state="normal")
		self.chat_historial.delete("1.0", "end")
		self.chat_historial.configure(state="disabled")
		self.caja_texto.delete("1.0", "end")
		self._placeholder_idx = None


def main() -> None:
	app = InterfazAgente()
	app.mainloop()


if __name__ == "__main__":
	main()
