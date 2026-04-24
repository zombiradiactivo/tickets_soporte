from src.models import TicketAnalizado, CategoriaTicket, UrgenciaTicket


class ActionExecutor:
    def ejecutar(self, ticket: TicketAnalizado) -> None:
        print("\n" + "=" * 60)
        print("⚡ ACCIONES A EJECUTAR")
        print("=" * 60)

        if ticket.categoria == CategoriaTicket.CUENTA:
            print("📌 CATEGORÍA: CUENTA")
            if ticket.urgencia == UrgenciaTicket.ALTA:
                print("   🔴 URGENCIA ALTA → Escalar a soporte inmediatamente")
                print("   📧 Enviar alerta al equipo de soporte")
                print("   💬 Mostrar al usuario: 'Un agente te contactará en menos de 5 minutos'")
            else:
                print("   🟡 URGENCIA MEDIA/BAJA → Enviar email con instrucciones automáticas")
                print("   📧 Enviar guía de recuperación de cuenta")

        elif ticket.categoria == CategoriaTicket.TECNICO:
            print("📌 CATEGORÍA: TÉCNICO")
            if ticket.urgencia == UrgenciaTicket.ALTA:
                print("   🔴 URGENCIA ALTA → Escalar a equipo técnico con prioridad máxima")
                print("   📊 Registrar incidencia en sistema de bugs")
            else:
                print("   🟡 URGENCIA MEDIA/BAJA → Sugerir artículos de la base de conocimiento")

        elif ticket.categoria == CategoriaTicket.FACTURACION:
            print("📌 CATEGORÍA: FACTURACIÓN")
            print("   💰 Derivar a departamento de facturación")
            print("   📧 Enviar email con instrucciones de pago/reembolso")

        elif ticket.categoria == CategoriaTicket.PRODUCTO:
            print("📌 CATEGORÍA: PRODUCTO")
            print("   📦 Registrar feedback de producto")
            print("   💬 Agradecer al usuario por su comentario")

        else:
            print("📌 CATEGORÍA: OTRO")
            print("   👤 Escalar a equipo general para revisión manual")

        print(f"\n🎯 INTENCIÓN DETECTADA: {ticket.intencion}")
        print(f"🔧 ACCIÓN SUGERIDA POR IA: {ticket.accion_sugerida}")

        if ticket.entidades:
            print(f"\n📋 ENTIDADES EXTRAÍDAS:")
            for key, value in ticket.entidades.items():
                print(f"   {key}: {value}")
