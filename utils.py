from datetime import datetime
from typing import Optional


def validar_valor(valor: str) -> Optional[float]:
    try:
        v = float(valor.replace(".", "").replace(",", "."))
        return v if v >= 0 else None
    except (ValueError, AttributeError):
        return None


def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def data_hora_atual() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
