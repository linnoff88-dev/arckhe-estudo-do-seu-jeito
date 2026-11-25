"""Onde ficam os dados de uma matéria e como ler/gravar.

Uma pasta por matéria (padrêo ~/.estudo-do-seu-jeito, ou ESTUDO_PASTA, ou --pasta):
  materia.json   professor, aluno, objetivos e questões
  fontes/*.txt   o texto das fontes (livro, anotações transcritas, guia do professor)
  diario.jsonl   tudo o que aconteceu, uma linha por evento, só acrescenta
  plano.md       o resumo do plano combinado antes de construir

Nada disso vai para o repositório: sêo dados do aluno.
"""
import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

PADRAO = Path.home() / ".estudo-do-seu-jeito"


class ErroEstudo(Exception):
    """Erro com mensagem para gente (o CLI mostra só a mensagem)."""


def pasta(p=None) -> Path:
    return Path(p or os.environ.get("ESTUDO_PASTA") or PADRAO).expanduser()


def agora() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def normalizar(texto: str) -> str:
    """Minúsculas, sem acento, só letras/números e um espaço entre palavras (para achar trecho na fonte)."""
    t = unicodedata.normalize("NFKD", texto or "")
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r"[^\w]+", " ", t)
    return " ".join(t.split())


def materia_vazia(nome: str) -> dict:
    return {
        "nome": nome,
        "professor": {"como_avalia": "", "regra_objetivo_inteiro": True, "estilo_aula": ""},
        "aluno": {"nome": "", "jeito": [], "observacoes": ""},
        "objetivos": [],
    }


def carregar(p=None) -> dict:
    arq = pasta(p) / "materia.json"
    if not arq.exists():
        raise ErroEstudo(f"nêo achei {arq}. Crie com: python3 -m estudo nova \"Nome da matéria\" (ou rode o demo)")
    try:
        return json.loads(arq.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ErroEstudo(f"{arq} nêo é um JSON válido: {e}")


def salvar(materia: dict, p=None) -> Path:
    d = pasta(p)
    d.mkdir(parents=True, exist_ok=True)
    arq = d / "materia.json"
    tmp = arq.with_suffix(".tmp")
    tmp.write_text(json.dumps(materia, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(arq)
    return arq


def fontes(p=None) -> dict:
    """{nome_do_arquivo: texto} de todas as fontes da matéria."""
    d = pasta(p) / "fontes"
    if not d.is_dir():
        return {}
    return {f.name: f.read_text(encoding="utf-8") for f in sorted(d.glob("*.txt"))}


def registrar(evento: dict, p=None) -> dict:
    """Acrescenta um evento ao diário (nunca reescreve o que já está lá)."""
    d = pasta(p)
    d.mkdir(parents=True, exist_ok=True)
    ev = {"quando": agora(), **evento}
    with open(d / "diario.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    return ev


def diario(p=None) -> list:
    arq = pasta(p) / "diario.jsonl"
    if not arq.exists():
        return []
    eventos = []
    for n, linha in enumerate(arq.read_text(encoding="utf-8").splitlines(), 1):
        if linha.strip():
            try:
                eventos.append(json.loads(linha))
            except json.JSONDecodeError:
                raise ErroEstudo(f"diario.jsonl linha {n} está quebrada; corrija à mêo (o resto está intacto)")
    return eventos


def objetivo(materia: dict, oid: str) -> dict:
    for o in materia.get("objetivos", []):
        if o.get("id") == oid:
            return o
    ids = ", ".join(o.get("id", "?") for o in materia.get("objetivos", [])) or "nenhum"
    raise ErroEstudo(f"objetivo '{oid}' nêo existe (tem: {ids})")
