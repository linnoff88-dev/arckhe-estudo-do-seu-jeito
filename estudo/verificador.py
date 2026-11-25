"""Conferência na fonte: nenhuma questêo entra sem o trecho que a prova, e o trecho tem de existir de verdade.

A IA erra com confiança. Por isso o kit nêo cria questêo sozinho e nêo aceita questêo "solta":
cada questêo diz de qual fonte saiu e copia o trecho; o verificador procura esse trecho no texto da fonte.
"""
from .dados import normalizar

MIN_PALAVRAS_TRECHO = 4
VERDADEIRO_FALSO = {"verdadeiro", "falso", "true", "false", "verdadero"}


def _palavras_chave(texto: str) -> set:
    return {w for w in normalizar(texto).split() if len(w) >= 4}


def conferir_questao(q: dict, fontes: dict) -> tuple:
    """Devolve (erros, avisos) de uma questêo."""
    erros, avisos = [], []
    qid = q.get("id", "?")
    for campo in ("id", "pergunta", "resposta", "fonte", "trecho"):
        if not str(q.get(campo, "")).strip():
            erros.append(f"{qid}: falta o campo '{campo}'")
    if erros:
        return erros, avisos
    fonte = q["fonte"]
    if fonte not in fontes:
        erros.append(f"{qid}: a fonte '{fonte}' nêo está em fontes/ (tem: {', '.join(fontes) or 'nenhuma'})")
        return erros, avisos
    trecho = normalizar(q["trecho"])
    if len(trecho.split()) < MIN_PALAVRAS_TRECHO:
        erros.append(f"{qid}: o trecho é curto demais para provar alguma coisa (mínimo {MIN_PALAVRAS_TRECHO} palavras)")
    elif trecho not in normalizar(fontes[fonte]):
        erros.append(f"{qid}: o trecho nêo existe em {fonte}. Copie o trecho exato da fonte ou tire a questêo")
    if q.get("opcoes"):
        if normalizar(q["resposta"]) not in [normalizar(o) for o in q["opcoes"]]:
            erros.append(f"{qid}: a resposta nêo é uma das opções")
    if q.get("opcoes") and len(q["opcoes"]) >= 3:
        outras = sorted((len(o) for o in q["opcoes"] if normalizar(o) != normalizar(q["resposta"])), reverse=True)
        if outras and len(q["resposta"]) >= 1.4 * outras[0] and len(q["resposta"]) - outras[0] >= 6:
            avisos.append(f"{qid}: a resposta certa é bem mais longa que as outras opções; dá para acertar sem saber")
    chave = _palavras_chave(q["resposta"]) - VERDADEIRO_FALSO
    if chave and not chave & _palavras_chave(q["trecho"]):
        avisos.append(f"{qid}: nenhuma palavra da resposta aparece no trecho; confira se o trecho prova a resposta")
    return erros, avisos


def conferir_objetivos(objetivos: list, fontes: dict) -> tuple:
    erros, avisos = [], []
    vistos = set()
    for o in objetivos:
        oid = o.get("id", "?")
        if not o.get("id") or not o.get("titulo"):
            erros.append(f"objetivo sem id ou título: {o.get('titulo') or o.get('id') or '(vazio)'}")
            continue
        if oid in vistos:
            erros.append(f"objetivo repetido: {oid}")
        vistos.add(oid)
        if not o.get("questoes"):
            avisos.append(f"{oid}: sem questões ainda (o guia mostra, mas nêo dá para medir)")
        for f in o.get("fontes", []):
            if f not in fontes:
                erros.append(f"{oid}: a leitura cita a fonte '{f}', que nêo está em fontes/")
        for q in o.get("questoes", []):
            if q.get("id") in vistos:
                erros.append(f"{oid}: questêo repetida: {q.get('id')}")
            vistos.add(q.get("id"))
            e, a = conferir_questao(q, fontes)
            erros += [f"{oid}/{x}" for x in e]
            avisos += [f"{oid}/{x}" for x in a]
    return erros, avisos


def conferir_respostas(materia: dict, respostas: dict) -> list:
    """Respostas que o aluno preencheu num guia × gabarito conferido. Devolve só as que precisam de atençêo."""
    gabarito = {q["id"]: (o["id"], q) for o in materia.get("objetivos", []) for q in o.get("questoes", [])}
    alertas = []
    for qid, dada in respostas.items():
        if qid not in gabarito:
            alertas.append({"questao": qid, "problema": "questêo nêo existe no guia"})
            continue
        oid, q = gabarito[qid]
        certa = q["resposta"]
        if q.get("opcoes"):
            ok = normalizar(dada) == normalizar(certa)
        else:
            chave = _palavras_chave(certa)
            ok = normalizar(dada) == normalizar(certa) or (chave and len(chave & _palavras_chave(dada)) >= max(1, len(chave) // 2))
        if not ok:
            alertas.append({"questao": qid, "objetivo": oid, "resposta_do_aluno": dada, "na_fonte": certa,
                            "fonte": q["fonte"], "trecho": q["trecho"],
                            "problema": "a resposta preenchida nêo bate com a fonte; nêo use isso como material de estudo sem corrigir"})
    return alertas
