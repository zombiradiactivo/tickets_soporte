"""
SISTEMA DE ANÁLISIS DE TICKETS DE SOPORTE CON NLP (Ollama)
=======================================================
Versión refactorizada con arquitectura modular.
"""

import json
import logging
from typing import List, Optional

from src.pipeline import Pipeline
from src.preprocess import Preprocessor
from src.nlp_analyzer import NLPAnalyzer
from src.actions import ActionExecutor
from src.models import TicketAnalizado

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def exportar_resultados(tickets: List[TicketAnalizado], archivo: str = "resultados.json") -> None:
    datos = [ticket.to_dict() for ticket in tickets]
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Resultados exportados a {archivo}")


def ejecutar_ejemplos(pipeline: Pipeline) -> List[TicketAnalizado]:
    print("\n" + "🔹" * 35)
    print("EJECUTANDO EJEMPLOS")
    print("🔹" * 35)

    tickets_texto = [
        "¡URGENTE! Llevo 3 días sin poder acceder a mi cuenta. "
        "Ya restablecí la contraseña dos veces y sigue sin funcionar. "
        "Mi email es usuario@ejemplo.com. Necesito solución YA.",
        "La aplicación se cierra sola cuando intento subir una imagen. "
        "Uso la versión 2.3.1 en Windows 11. El error dice 'MemoryError'.",
        "Me cobraron dos veces la suscripción de este mes. "
        "El pedido es #12345 y el cargo apareció el 15 de marzo. "
        "Necesito que me devuelvan el dinero."
    ]

    resultados = []
    for texto in tickets_texto:
        ticket = pipeline.procesar(texto)
        if ticket:
            resultados.append(ticket)

    return resultados


def main():
    print("🎯 SISTEMA DE ANÁLISIS DE TICKETS DE SOPORTE (Ollama)")
    print("=" * 60)

    pipeline = Pipeline(
        analyzer=NLPAnalyzer(),
        preprocessor=Preprocessor(),
        action_executor=ActionExecutor()
    )

    while True:
        print("\n📋 MENÚ PRINCIPAL")
        print("1. Ejecutar ejemplos")
        print("2. Procesar ticket personalizado")
        print("3. Procesar múltiples tickets")
        print("4. Cargar tickets desde JSON")
        print("5. Salir")

        opcion = input("\n👉 Elige una opción (1-5): ").strip()

        if opcion == "1":
            tickets = ejecutar_ejemplos(pipeline)
            if tickets:
                exportar_resultados(tickets)

        elif opcion == "2":
            print("\n📝 Escribe tu ticket (o 'salir' para volver):")
            texto = input("> ").strip()
            if texto.lower() != 'salir' and texto:
                ticket = pipeline.procesar(texto)
                if ticket:
                    exportar_resultados([ticket], "ticket_personalizado.json")

        elif opcion == "3":
            tickets_texto = []
            print("\n📝 Escribe varios tickets (línea vacía para terminar):")
            while True:
                linea = input(f"Ticket {len(tickets_texto)+1}: ").strip()
                if not linea:
                    break
                tickets_texto.append(linea)

            if tickets_texto:
                resultados = pipeline.procesar_lote(tickets_texto)
                if resultados:
                    exportar_resultados(resultados, "tickets_lote.json")

        elif opcion == "4":
            try:
                with open("data/tickets_ejemplo.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                tickets_texto = [item["texto"] for item in data]
                print(f"\n📂 Cargados {len(tickets_texto)} tickets desde el archivo")
                resultados = pipeline.procesar_lote(tickets_texto)
                if resultados:
                    exportar_resultados(resultados, "tickets_desde_json.json")
            except FileNotFoundError:
                print("❌ No se encontró el archivo data/tickets_ejemplo.json")

        elif opcion == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")


if __name__ == "__main__":
    main()
