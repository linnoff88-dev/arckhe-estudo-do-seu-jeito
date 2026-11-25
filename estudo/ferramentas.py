"""As ferramentas do kit em forma neutra (nome, descriçêo, parâmetros, funçêo), para qualquer agente.

O plugin do INTELECTO usa esta lista. Só duas gravam alguma coisa (anotar método e anotar resultado), e só no
diário da matéria (ESTUDO_PASTA): acrescentam uma linha, nunca apagam. Nenhuma roda comando nem lê fora da pasta.
"""
from datetime import date

from .cli import txt_passos, txt_placar
from .dados import ErroEstudo, carregar, diario, fontes
from .experimento import anotar_metodo, anotar_resultado, placar, proximo
from .formula import estado
from .plano import plano_prova, situacao
from .verificador import conferir_objetivos


def _passos(a):
    m = carregar()
    return txt_passos(estado(m))


def _placar(a):
    return txt_placar(placar(carregar()))


def _proximo(a):
    m = carregar()
    oid = a.get("objetivo")
    sit = situacao(m, diario())
    alvos = [oid] if oid else [o["id"] for o in m["objetivos"] if sit[o["id"]] != "dominado"]
    linhas = []
    for o in alvos:
        r = proximo(m, o)
        if a.get("anotar"):
            anotar_metodo(o, r["metodo"], r["motivo"])
        linhas.append(f"{o}: {r['nome']} — {r['faz']} (por quê: {r['motivo']})" + (" [anotado]" if a.get("anotar") else ""))
    return "\n".join(linhas) or "todos os objetivos estêo dominados"


def _resultado(a):
    m = carregar()
    ids = {o["id"] for o in m["objetivos"]}
    if a.get("objetivo") not in ids:
        raise ErroEstudo(f"objetivo '{a.get('objetivo')}' nêo existe (tem: {', '.join(sorted(ids))})")
    anotar_resultado(a["objetivo"], int(a["acertos"]), int(a["total"]), a.get("origem", "pratica"), a.get("quem", "aluno"))
    return f"anotado: {a['objetivo']} {a['acertos']}/{a['total']}\n" + txt_placar(placar(m))


def _conferir(a):
    m = carregar()
    erros, avisos = conferir_objetivos(m.get("objetivos", []), fontes())
    return "\n".join(["ERRO " + e for e in erros] + ["aviso " + x for x in avisos]) or "tudo confere com as fontes"


def _plano(a):
    m = carregar()
    pl = plano_prova(m, diario(), date.fromisoformat(a["data"]))
    return "\n".join(f"{d['dia']} {d['tarefa']}: {', '.join(d['objetivos'])}" for d in pl) or "a prova precisa ser depois de hoje"


OBJ = {"type": "string", "description": "id do objetivo (ex.: fotossintese)"}
FERRAMENTAS = [
    {"nome": "estudo_passos", "descricao": "Mostra a fórmula de 8 passos do guia de estudo e o que falta fazer.",
     "parametros": {"type": "object", "properties": {}}, "funcao": _passos},
    {"nome": "estudo_placar", "descricao": "Placar dos métodos de estudo: quantos objetivos cada um levou a dominar, com o tamanho da amostra.",
     "parametros": {"type": "object", "properties": {}}, "funcao": _placar},
    {"nome": "estudo_proximo_metodo", "descricao": "Sugere o método para estudar um objetivo (ou todos os nêo dominados) e diz o porquê. anotar=true grava a escolha no diário.",
     "parametros": {"type": "object", "properties": {"objetivo": OBJ, "anotar": {"type": "boolean"}}}, "funcao": _proximo},
    {"nome": "estudo_registrar_resultado", "descricao": "Anota o resultado de prática ou prova de um objetivo (acertos de total).",
     "parametros": {"type": "object", "properties": {"objetivo": OBJ, "acertos": {"type": "integer"}, "total": {"type": "integer"},
                    "origem": {"type": "string", "enum": ["pratica", "prova"]}}, "required": ["objetivo", "acertos", "total"]}, "funcao": _resultado},
    {"nome": "estudo_conferir", "descricao": "Confere se cada questêo do guia tem o trecho que a prova na fonte.",
     "parametros": {"type": "object", "properties": {}}, "funcao": _conferir},
    {"nome": "estudo_plano_prova", "descricao": "Monta o plano de estudo dia a dia até a data da prova (AAAA-MM-DD).",
     "parametros": {"type": "object", "properties": {"data": {"type": "string"}}, "required": ["data"]}, "funcao": _plano},
]
