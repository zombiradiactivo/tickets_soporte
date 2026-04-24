import pytest
from io import StringIO
from src.models import TicketAnalizado, CategoriaTicket, UrgenciaTicket
from src.actions import ActionExecutor


def test_ejecutar_cuenta_alta(capsys):
    ticket = TicketAnalizado(
        texto_original="test",
        categoria=CategoriaTicket.CUENTA,
        urgencia=UrgenciaTicket.ALTA,
        intencion="recuperar acceso",
        accion_sugerida="resetear contraseña"
    )
    executor = ActionExecutor()
    executor.ejecutar(ticket)
    captured = capsys.readouterr()
    assert "CUENTA" in captured.out
    assert "URGENCIA ALTA" in captured.out


def test_ejecutar_tecnico(capsys):
    ticket = TicketAnalizado(
        texto_original="test",
        categoria=CategoriaTicket.TECNICO,
        urgencia=UrgenciaTicket.MEDIA,
        intencion="bug en app",
        accion_sugerida="escalar a tecnico"
    )
    executor = ActionExecutor()
    executor.ejecutar(ticket)
    captured = capsys.readouterr()
    assert "TÉCNICO" in captured.out


def test_ejecutar_entidades(capsys):
    ticket = TicketAnalizado(
        texto_original="test",
        categoria=CategoriaTicket.OTRO,
        urgencia=UrgenciaTicket.BAJA,
        intencion="consulta",
        accion_sugerida="revisar",
        entidades={"email": "test@test.com"}
    )
    executor = ActionExecutor()
    executor.ejecutar(ticket)
    captured = capsys.readouterr()
    assert "test@test.com" in captured.out
