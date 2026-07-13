import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historico.db")


def _conectar() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def inicializar():
    with _conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                resultado TEXT NOT NULL,
                pontuacao INTEGER NOT NULL,
                motivos TEXT NOT NULL,
                dados_json TEXT NOT NULL,
                usuario TEXT DEFAULT 'Colaborador'
            )
        """)


def salvar_analise(
    dados: Dict,
    resultado: str,
    motivos: List[str],
    pontuacao: int,
    usuario: str = "Colaborador",
) -> int:
    with _conectar() as conn:
        cur = conn.execute(
            """
            INSERT INTO analises (data_hora, resultado, pontuacao, motivos, dados_json, usuario)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                resultado,
                pontuacao,
                json.dumps(motivos, ensure_ascii=False),
                json.dumps(dados, ensure_ascii=False),
                usuario,
            ),
        )
        return cur.lastrowid


def listar_analises(limite: int = 50) -> List[Dict]:
    with _conectar() as conn:
        rows = conn.execute(
            """
            SELECT id, data_hora, resultado, pontuacao, motivos, usuario
            FROM analises
            ORDER BY id DESC
            LIMIT ?
            """,
            (limite,),
        ).fetchall()
        return [dict(r) for r in rows]


def buscar_analises(termo: str, limite: int = 50) -> List[Dict]:
    with _conectar() as conn:
        rows = conn.execute(
            """
            SELECT id, data_hora, resultado, pontuacao, motivos, usuario
            FROM analises
            WHERE resultado LIKE ? OR motivos LIKE ? OR usuario LIKE ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (f"%{termo}%", f"%{termo}%", f"%{termo}%", limite),
        ).fetchall()
        return [dict(r) for r in rows]


def carregar_analise(analise_id: int) -> Optional[Dict]:
    with _conectar() as conn:
        row = conn.execute(
            "SELECT * FROM analises WHERE id = ?", (analise_id,)
        ).fetchone()
        if row is None:
            return None
        result = dict(row)
        result["motivos"] = json.loads(result["motivos"])
        result["dados_json"] = json.loads(result["dados_json"])
        return result
