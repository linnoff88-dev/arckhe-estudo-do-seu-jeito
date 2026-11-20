"""O teste dos métodos, às claras.

Regra do jogo (é isso que o aluno e quem ensina veem no placar):
1. Antes de estudar um objetivo, o método é escolhido e ANOTADO no diário (com o motivo).
2. Depois vem o resultado (prática ou prova). Ele vale para o método anotado por último naquele objetivo.
3. "Dominado" segue a regra do professor: se perder uma questão perde o objetivo inteiro, só conta acertar todas.
4. Cada par (objetivo, método) conta uma vez: vale o resultado de prova, se houver; senão o último da prática.
5. Com menos de MIN_N objetivos, o método aparece como "pouco dado" e nunca como o melhor.
"""
from .dados import diario, registrar
from .metodos import METODOS, candidatos

MIN_N = 3
VANTAGEM = 20  # pontos percentuais para dizer que um método está na frente


def dominou(acertos: int, total: int, regra_inteiro: bool = True) -> bool:
    if total <= 0:
        return False
    return acertos == total if regra_inteiro else acertos / total >= 0.8


def _pares(eventos: list, regra_inteiro: bool) -> dict:
    """{(objetivo, metodo): {"dominou": bool, "origem": str}} seguindo as regras 2 e 4."""
    metodo_atual = {}
    pares = {}
    for ev in eventos:
        if ev.get("tipo") == "metodo":
            metodo_atual[ev["objetivo"]] = ev["metodo"]
        elif ev.get("tipo") == "resultado":
            oid = ev["objetivo"]
            chave = (oid, metodo_atual.get(oid))
            atual = pares.get(chave)
            novo = {"dominou": dominou(int(ev["acertos"]), int(ev["total"]), regra_inteiro), "origem": ev.get("origem", "pratica")}
            if atual is None or novo["origem"] == "prova" or atual["origem"] != "prova":
                pares[chave] = novo
    return pares


def placar(materia: dict, p=None, eventos=None) -> dict:
    eventos = diario(p) if eventos is None else eventos
    regra = bool(materia.get("professor", {}).get("regra_objetivo_inteiro", True))
    pares = _pares(eventos, regra)
    linhas = {}
    for (oid, metodo), r in pares.items():
        chave = metodo or "sem-metodo"
        l = linhas.setdefault(chave, {"metodo": chave, "n": 0, "dominados": 0, "objetivos": []})
        l["n"] += 1
        l["dominados"] += 1 if r["dominou"] else 0
        l["objetivos"].append(oid)
    for l in linhas.values():
        l["taxa"] = round(100 * l["dominados"] / l["n"]) if l["n"] else 0
        l["pouco_dado"] = l["n"] < MIN_N
        l["nome"] = METODOS.get(l["metodo"], {}).get("nome", "Antes do kit (sem método anotado)")
    testados = [l for l in linhas.values() if l["metodo"] != "sem-metodo"]
    firmes = sorted([l for l in testados if not l["pouco_dado"]], key=lambda l: -l["taxa"])
    lider = None
    if len(firmes) >= 2 and firmes[0]["taxa"] - firmes[1]["taxa"] >= VANTAGEM:
        lider = firmes[0]["metodo"]
    if lider:
        veredito = (f"{firmes[0]['nome']} está na frente por enquanto ({firmes[0]['dominados']} de {firmes[0]['n']} "
                    f"objetivos dominados). Continua valendo testar: matérias diferentes têm dificuldades diferentes.")
    elif len(firmes) >= 2:
        veredito = "Empate técnico entre os métodos com dados suficientes: a diferença ainda é pequena para escolher."
    else:
        veredito = f"Ainda é cedo: cada método precisa de pelo menos {MIN_N} objetivos testados antes de comparar."
    ordem = sorted(linhas.values(), key=lambda l: (l["metodo"] == "sem-metodo", -l["n"], l["metodo"]))
    return {"linhas": ordem, "lider": lider, "veredito": veredito, "min_n": MIN_N}


def proximo(materia: dict, oid: str, p=None, eventos=None) -> dict:
    """Escolhe o método para o próximo estudo deste objetivo e diz o porquê (não grava)."""
    eventos = diario(p) if eventos is None else eventos
    jeito = materia.get("aluno", {}).get("jeito", [])
    opcoes = candidatos(jeito)
    pl = placar(materia, eventos=eventos)
    por_metodo = {l["metodo"]: l for l in pl["linhas"]}
    regra = bool(materia.get("professor", {}).get("regra_objetivo_inteiro", True))
    ja_falhou = {m for (o, m), r in _pares(eventos, regra).items() if o == oid and not r["dominou"] and m}
    livres = [m for m in opcoes if m not in ja_falhou] or opcoes
    if pl["lider"] in livres and all(not por_metodo.get(m, {"pouco_dado": True})["pouco_dado"] for m in opcoes):
        escolhido = pl["lider"]
        motivo = f"todos os métodos já têm dados e {METODOS[escolhido]['nome']} está na frente"
    else:
        escolhido = min(livres, key=lambda m: (por_metodo.get(m, {"n": 0})["n"], opcoes.index(m)))
        n = por_metodo.get(escolhido, {"n": 0})["n"]
        motivo = f"é o método com menos objetivos testados até agora ({n}); assim o teste fica justo"
    if ja_falhou:
        nomes = ", ".join(METODOS[m]["nome"] for m in sorted(ja_falhou))
        motivo += f"; neste objetivo já não deu certo com: {nomes}"
    return {"objetivo": oid, "metodo": escolhido, "nome": METODOS[escolhido]["nome"],
            "faz": METODOS[escolhido]["faz"], "motivo": motivo, "opcoes": opcoes}


def anotar_metodo(oid: str, metodo: str, motivo: str, p=None) -> dict:
    if metodo not in METODOS:
        from .dados import ErroEstudo
        raise ErroEstudo(f"método '{metodo}' não existe (tem: {', '.join(METODOS)})")
    return registrar({"tipo": "metodo", "objetivo": oid, "metodo": metodo, "motivo": motivo}, p)


def anotar_resultado(oid: str, acertos: int, total: int, origem="pratica", quem="aluno", p=None, nota="") -> dict:
    from .dados import ErroEstudo
    if total <= 0 or acertos < 0 or acertos > total:
        raise ErroEstudo(f"resultado impossível: {acertos} de {total}")
    if origem not in ("pratica", "prova"):
        raise ErroEstudo("origem tem de ser 'pratica' ou 'prova'")
    ev = {"tipo": "resultado", "objetivo": oid, "acertos": int(acertos), "total": int(total), "origem": origem, "quem": quem}
    if nota:
        ev["nota"] = nota
    return registrar(ev, p)
