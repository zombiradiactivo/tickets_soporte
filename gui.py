import json
import threading
import requests
import customtkinter as ctk
from io import StringIO
from contextlib import redirect_stdout

from config.config import MODEL_NAME, OLLAMA_HOST
from src.pipeline import Pipeline
from src.preprocess import Preprocessor
from src.nlp_analyzer import NLPAnalyzer
from src.actions import ActionExecutor
from src.models import TicketAnalizado

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TicketAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tickets Soporte NLP - Análisis de Tickets")
        self.geometry("1200x750")
        self.configure(fg_color="#1a1a1a")

        self.pipeline = Pipeline(
            analyzer=NLPAnalyzer(),
            preprocessor=Preprocessor(),
            action_executor=ActionExecutor()
        )

        self.current_ticket = None
        self.current_pipeline_output = ""
        self.current_acciones_output = ""
        self.current_json_output = ""
        self.active_tab = "pipeline"

        self.header_label = ctk.CTkLabel(
            self,
            text="📁 Sistema de Análisis de Tickets de Soporte con NLP",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.header_label.pack(pady=(20, 10))

        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=40)

        self.ollama_status = ctk.CTkLabel(self.status_frame, text="⏳ Verificando Ollama...", text_color="#FFA500", font=ctk.CTkFont(size=12))
        self.ollama_status.pack(side="left")

        self.model_status = ctk.CTkLabel(self.status_frame, text=f"🤖 Modelo: {MODEL_NAME}", text_color="gray", font=ctk.CTkFont(size=12))
        self.model_status.pack(side="right")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.left_column = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.right_column = ctk.CTkFrame(self.main_container, fg_color="#2b2b2b", corner_radius=10)
        self.right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.setup_left_column()
        self.setup_right_column()
        self.check_ollama_connection()

    def check_ollama_connection(self):
        try:
            r = requests.get(OLLAMA_HOST, timeout=2)
            if r.status_code == 200:
                self.ollama_status.configure(text="✅ Ollama conectado", text_color="#4CAF50")
            else:
                self.ollama_status.configure(text="❌ Ollama no responde", text_color="#E74C3C")
        except:
            self.ollama_status.configure(text="❌ Ollama desconectado (ejecuta 'ollama serve')", text_color="#E74C3C")

    def setup_left_column(self):
        ctk.CTkLabel(self.left_column, text="📝 Ticket a analizar", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 5))
        self.ticket_input = ctk.CTkTextbox(self.left_column, height=150, fg_color="#121212", border_color="#333")
        self.ticket_input.pack(fill="x", pady=(0, 10))
        self.ticket_input.insert("1.0", "Ejemplo: No puedo acceder a mi cuenta, olvidé mi contraseña...")

        self.btn_row1 = ctk.CTkFrame(self.left_column, fg_color="transparent")
        self.btn_row1.pack(fill="x", pady=(0, 10))

        self.btn_analizar = ctk.CTkButton(self.btn_row1, text="🔍 Analizar Ticket", fg_color="#3498db", hover_color="#2980b9", command=self.analizar_ticket)
        self.btn_analizar.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_limpiar = ctk.CTkButton(self.btn_row1, text="🗑️ Limpiar", fg_color="#e74c3c", hover_color="#c0392b", command=self.limpiar)
        self.btn_limpiar.pack(side="right", expand=True, fill="x", padx=(5, 0))

        ctk.CTkLabel(self.left_column, text="📋 Procesamiento por lotes", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(10, 5))

        self.lote_text = ctk.CTkTextbox(self.left_column, height=100, fg_color="#121212", border_color="#333")
        self.lote_text.pack(fill="x", pady=(0, 10))
        self.lote_text.insert("1.0", "Ticket 1\nTicket 2\nTicket 3")

        self.btn_row2 = ctk.CTkFrame(self.left_column, fg_color="transparent")
        self.btn_row2.pack(fill="x", pady=(0, 10))

        self.btn_cargar_json = ctk.CTkButton(self.btn_row2, text="📁 Cargar JSON", fg_color="#4CAF50", hover_color="#388E3C", command=self.cargar_json)
        self.btn_cargar_json.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_procesar_lote = ctk.CTkButton(self.btn_row2, text="⚡ Procesar Lote", fg_color="#f39c12", hover_color="#e67e22", command=self.procesar_lote)
        self.btn_procesar_lote.pack(side="right", expand=True, fill="x", padx=(5, 0))

        self.progress = ctk.CTkProgressBar(self.left_column, progress_color="#3498db")
        self.progress.set(0)
        self.progress.pack(fill="x", pady=(5, 5))

        self.lbl_progress = ctk.CTkLabel(self.left_column, text="Listo", font=ctk.CTkFont(size=11), text_color="gray")
        self.lbl_progress.pack()

    def setup_right_column(self):
        self.tab_frame = ctk.CTkFrame(self.right_column, fg_color="transparent")
        self.tab_frame.pack(fill="x", pady=15, padx=20)

        self.tab_buttons = {}
        tabs = [("🔄 Pipeline", "pipeline"), ("⚡ Acciones", "acciones"), ("📄 JSON", "json"), ("📊 Modelos", "modelos")]
        for text, name in tabs:
            btn = ctk.CTkButton(
                self.tab_frame, text=text, width=80, height=28,
                fg_color="#3498db" if name == "pipeline" else "transparent",
                border_width=1 if name != "pipeline" else 0,
                border_color="gray30",
                command=lambda n=name: self.switch_tab(n)
            )
            btn.pack(side="left", padx=5)
            self.tab_buttons[name] = btn

        self.output_text = ctk.CTkTextbox(self.right_column, fg_color="#121212", text_color="#00FF00", font=ctk.CTkFont(family="Courier", size=12))
        self.output_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.output_text.insert("1.0", "Presiona '🔍 Analizar Ticket' para comenzar...")

    def switch_tab(self, tab_name):
        self.active_tab = tab_name
        for name, btn in self.tab_buttons.items():
            if name == tab_name:
                btn.configure(fg_color="#3498db", border_width=0)
            else:
                btn.configure(fg_color="transparent", border_width=1)

        self.output_text.delete("1.0", "end")
        if tab_name == "pipeline":
            self.output_text.insert("end", self.current_pipeline_output)
        elif tab_name == "acciones":
            self.output_text.insert("end", self.current_acciones_output)
        elif tab_name == "json":
            self.output_text.insert("end", self.current_json_output)
        elif tab_name == "modelos":
            self.output_text.insert("end", "📊 Modelos disponibles:\n\n- qwen3.5:2b (recomendado para español)\n- llama3.1:8b\n- mistral:7b\n- llama3.2:3b\n- phi3:mini")
        self.output_text.see("end")

    def parse_output(self, full_output, ticket):
        pipeline_part = full_output
        acciones_part = ""

        # Split output into pipeline steps and acciones
        if "⚡ ACCIONES A EJECUTAR" in full_output:
            parts = full_output.split("⚡ ACCIONES A EJECUTAR", 1)
            pipeline_part = parts[0]
            acciones_part = "⚡ ACCIONES A EJECUTAR" + parts[1] if len(parts) > 1 else ""

        # Build JSON output from ticket
        if ticket:
            json_data = {
                "categoria": ticket.categoria.value,
                "urgencia": ticket.urgencia.value,
                "intencion": ticket.intencion,
                "accion_sugerida": ticket.accion_sugerida,
                "entidades": ticket.entidades
            }
            json_output = json.dumps(json_data, indent=2, ensure_ascii=False)
        else:
            json_output = "No hay datos disponibles"

        return pipeline_part, acciones_part, json_output

    def limpiar(self):
        self.ticket_input.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.current_pipeline_output = ""
        self.current_acciones_output = ""
        self.current_json_output = ""
        self.current_ticket = None

    def analizar_ticket(self):
        texto = self.ticket_input.get("1.0", "end").strip()
        if not texto or texto == "Ejemplo: No puedo acceder a mi cuenta, olvidé mi contraseña...":
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", "❌ Error: Escribe un ticket válido")
            return
        threading.Thread(target=self._analizar_thread, args=(texto,), daemon=True).start()

    def _analizar_thread(self, texto):
        self.btn_analizar.configure(state="disabled", text="⏳ Procesando...")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("end", "⏳ Procesando...\n")
        self.output_text.see("end")

        try:
            buffer = StringIO()
            with redirect_stdout(buffer):
                ticket = self.pipeline.procesar(texto)
            output = buffer.getvalue()

            pipeline_out, acciones_out, json_out = self.parse_output(output, ticket)

            self.current_pipeline_output = pipeline_out
            self.current_acciones_output = acciones_out
            self.current_json_output = json_out
            self.current_ticket = ticket

            self.switch_tab(self.active_tab)
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", f"❌ Error: {str(e)}")
        finally:
            self.btn_analizar.configure(state="normal", text="🔍 Analizar Ticket")

    def cargar_json(self):
        try:
            with open("data/tickets_ejemplo.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            tickets = [item["texto"] for item in data]
            self.lote_text.delete("1.0", "end")
            self.lote_text.insert("1.0", "\n".join(tickets))
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", f"✅ Cargados {len(tickets)} tickets desde data/tickets_ejemplo.json")
        except FileNotFoundError:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", "❌ No se encontró data/tickets_ejemplo.json")

    def procesar_lote(self):
        texto = self.lote_text.get("1.0", "end").strip()
        if not texto:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", "❌ No hay tickets para procesar")
            return
        tickets = [t.strip() for t in texto.split("\n") if t.strip()]
        threading.Thread(target=self._procesar_lote_thread, args=(tickets,), daemon=True).start()

    def _procesar_lote_thread(self, tickets):
        self.btn_procesar_lote.configure(state="disabled", text="⏳ Procesando...")
        self.output_text.delete("1.0", "end")

        all_pipeline = []
        all_acciones = []
        all_json = []
        resultados = []

        try:
            for i, ticket_text in enumerate(tickets, 1):
                self.lbl_progress.configure(text=f"📋 Procesando ticket {i}/{len(tickets)}...")
                self.progress.set(i / len(tickets))

                buffer = StringIO()
                with redirect_stdout(buffer):
                    ticket = self.pipeline.procesar(ticket_text)
                output = buffer.getvalue()

                pipeline_out, acciones_out, json_out = self.parse_output(output, ticket)

                all_pipeline.append(pipeline_out)
                all_acciones.append(acciones_out)
                all_json.append(json.loads(json_out) if ticket else {})
                if ticket:
                    resultados.append(ticket)

            self.current_pipeline_output = "\n" + "="*70 + "\n".join(all_pipeline)
            self.current_acciones_output = "\n" + "="*70 + "\n".join(all_acciones)
            self.current_json_output = json.dumps(all_json, indent=2, ensure_ascii=False)

            if resultados:
                with open("resultados_lote.json", "w", encoding="utf-8") as f:
                    json.dump([t.to_dict() for t in resultados], f, indent=2, ensure_ascii=False)
                self.output_text.insert("end", f"\n💾 {len(resultados)} tickets exportados a resultados_lote.json\n")

            self.switch_tab(self.active_tab)
        except Exception as e:
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", f"❌ Error: {str(e)}")
        finally:
            self.btn_procesar_lote.configure(state="normal", text="⚡ Procesar Lote")
            self.lbl_progress.configure(text="Listo")
            self.progress.set(1.0)


if __name__ == "__main__":
    app = TicketAnalyzerApp()
    app.mainloop()
