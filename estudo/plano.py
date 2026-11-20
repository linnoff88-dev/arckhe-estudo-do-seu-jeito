"""Plano antes da prova: espalha os objetivos ainda não dominados pelos dias que faltam, os mais fracos primeiro."""
from datetime import date, timedelta

from .experimento import _pares


def situacao(materia: dict, eventos: list) -> dict:
    """{objetivo: 'dominado' | 'errou' | 'nao-testado'} pelo último resultado de cada objetivo."""
    regra = bool(materia.get("professor", {}).get("regra_objetivo_inteiro", True))
    ultimo = {}
    for (oid, _m), r in _pares(eventos, regra).items():
        ultimo[oid] = r["dominou"]
    out = {}
    for o in materia.get("objetivos", []):
        v = ultimo.get(o["id"])
        out[o["id"]] = "nao-testado" if v is None else ("dominado" if v else "errou")
    return out


def plano_prova(materia: dict, eventos: list, prova: date, hoje: date = None, por_dia: int = 2) -> list:
    hoje = hoje or date.today()
    dias = (prova - hoje).days
    if dias < 1:
        return []
    sit = situacao(materia, eventos)
    peso = {"errou": 0, "nao-testado": 1, "dominado": 2}
    fila = sorted(materia.get("objetivos", []), key=lambda o: (peso[sit[o["id"]]], o["id"]))
    pendentes = [o for o in fila if sit[o["id"]] != "dominado"]
    revisao = [o for o in fila if sit[o["id"]] == "dominado"]
    if dias > 1:  # nenhum pendente fica de fora: aperta o dia se for preciso
        por_dia = max(por_dia, -(-len(pendentes) // (dias - 1)))
    plano = []
    for i in range(dias):
        dia = hoje + timedelta(days=i)
        if i == dias - 1:
            plano.append({"dia": dia.isoformat(), "tarefa": "revisão geral: só as questões, sem consultar", "objetivos": [o["id"] for o in fila]})
            continue
        bloco = pendentes[i * por_dia:(i + 1) * por_dia]
        if not bloco and revisao:
            bloco = [revisao[i % len(revisao)]]
            tarefa = "revisar um objetivo já dominado (para não esquecer)"
        else:
            tarefa = "estudar com o método sugerido e fazer as questões"
        if bloco:
            plano.append({"dia": dia.isoformat(), "tarefa": tarefa, "objetivos": [o["id"] for o in bloco]})
    return plano
