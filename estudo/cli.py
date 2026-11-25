"""python3 -m estudo <comando>. Tudo em texto simples; --json para agentes (Claude Code, Codex, Jarvis)."""
import argparse
import json
import shutil
import sys
from datetime import date, datetime, timedelta
from importlib import resources
from pathlib import Path

from . import VERSAO
from .dados import ErroEstudo, carregar, diario, fontes, materia_vazia, objetivo, pasta, registrar, salvar
from .experimento import anotar_metodo, anotar_resultado, placar, proximo
from .formula import estado
from .guia_html import montar
from .metodos import JEITOS, METODOS
from .plano import plano_prova, situacao
from .verificador import conferir_objetivos, conferir_respostas


def _saida(args, dados, texto):
    if getattr(args, "json", False):
        print(json.dumps(dados, ensure_ascii=False, indent=1))
    else:
        print(texto)


def txt_placar(pl):
    linhas = ["Placar dos métodos (só o que já foi registrado)"]
    for l in pl["linhas"]:
        aviso = "  · pouco dado" if l["pouco_dado"] else ""
        linhas.append(f"  {l['nome']:<38} {l['dominados']} de {l['n']} objetivos dominados ({l['taxa']}%){aviso}")
    if len(linhas) == 1:
        linhas.append("  nada registrado ainda")
    linhas.append(pl["veredito"])
    return "\n".join(linhas)


def txt_passos(ps):
    out = ["A fórmula, passo a passo"]
    for i, s in enumerate(ps, 1):
        out.append(f"  {'[x]' if s['feito'] else '[ ]'} {i}. {s['titulo']}")
        if not s["feito"]:
            out.append(f"       como: {s['como']}")
    falta = [s for s in ps if not s["feito"]]
    out.append("Tudo em dia." if not falta else f"Próximo: {falta[0]['titulo']}.")
    return "\n".join(out)


def cmd_nova(a):
    d = pasta(a.pasta)
    if (d / "materia.json").exists() and not a.forcar:
        raise ErroEstudo(f"já existe uma matéria em {d} (use outra --pasta ou --forcar)")
    m = materia_vazia(a.nome)
    salvar(m, a.pasta)
    (d / "fontes").mkdir(exist_ok=True)
    print(f"Matéria criada em {d}. Agora: preencha professor e aluno no materia.json (jeitos: {', '.join(JEITOS)}).")


def _demo_diario(p):
    hoje = datetime.now().astimezone().replace(microsecond=0)
    q = lambda dias: (hoje - timedelta(days=dias)).isoformat()
    eventos = [
        ({"tipo": "resultado", "objetivo": "fotossintese", "acertos": 1, "total": 3, "origem": "prova", "quem": "tutor", "nota": "prova 1, antes do kit"}, 21),
        ({"tipo": "resultado", "objetivo": "respiracao", "acertos": 2, "total": 3, "origem": "prova", "quem": "tutor", "nota": "prova 1, antes do kit"}, 21),
        ({"tipo": "resultado", "objetivo": "genetica", "acertos": 3, "total": 3, "origem": "prova", "quem": "tutor", "nota": "prova 1, antes do kit"}, 21),
        ({"tipo": "tutor", "objetivo": "fotossintese", "minutos": 120}, 20),
        ({"tipo": "tutor", "objetivo": "respiracao", "minutos": 150}, 19),
        ({"tipo": "semana", "fonte": "fotossintese.txt"}, 18),
        ({"tipo": "metodo", "objetivo": "fotossintese", "metodo": "redesenhar", "motivo": "é visual; começa pelo método com menos testes"}, 18),
        ({"tipo": "metodo", "objetivo": "respiracao", "metodo": "vida-real", "motivo": "precisa de exemplo concreto"}, 18),
        ({"tipo": "resultado", "objetivo": "fotossintese", "acertos": 3, "total": 3, "origem": "pratica", "quem": "aluno"}, 15),
        ({"tipo": "resultado", "objetivo": "respiracao", "acertos": 2, "total": 3, "origem": "pratica", "quem": "aluno"}, 15),
        ({"tipo": "resultado", "objetivo": "fotossintese", "acertos": 3, "total": 3, "origem": "prova", "quem": "tutor", "nota": "prova 2"}, 7),
        ({"tipo": "resultado", "objetivo": "respiracao", "acertos": 2, "total": 3, "origem": "prova", "quem": "tutor", "nota": "prova 2"}, 7),
        ({"tipo": "semana", "fonte": "genetica.txt"}, 3),
    ]
    with open(pasta(p) / "diario.jsonl", "w", encoding="utf-8") as f:
        for ev, dias in eventos:
            f.write(json.dumps({"quando": q(dias), **ev, "exemplo": True}, ensure_ascii=False) + "\n")


def cmd_demo(a):
    d = pasta(a.pasta)
    if (d / "materia.json").exists() and not a.forcar:
        raise ErroEstudo(f"já existe uma matéria em {d}; o demo nêo sobrescreve (use --pasta /tmp/demo-estudo ou --forcar)")
    ex = resources.files("estudo") / "exemplo"
    d.mkdir(parents=True, exist_ok=True)
    (d / "fontes").mkdir(exist_ok=True)
    (d / "materia.json").write_text((ex / "materia.json").read_text(encoding="utf-8"), encoding="utf-8")
    for f in (ex / "fontes").iterdir():
        if f.name.endswith(".txt"):
            (d / "fontes" / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    (d / "plano.md").write_text("# Plano (exemplo inventado)\n\nGuia por objetivo, visual, com vida real e questões só das fontes.\n"
                                "Testar: redesenhar, vida real, explicar falando, questões sem consultar e releitura.\n", encoding="utf-8")
    _demo_diario(a.pasta)
    m = carregar(a.pasta)
    saida = d / "guia.html"
    saida.write_text(montar(m, a.pasta), encoding="utf-8")
    print(f"Demo criado em {d} (dados inventados: Clara, biologia, 3 objetivos).\n")
    print(txt_passos(estado(m, a.pasta)))
    print()
    print(txt_placar(placar(m, a.pasta)))
    print(f"\nGuia do aluno: {saida}  (abra no navegador)")


def cmd_passos(a):
    m = carregar(a.pasta)
    ps = estado(m, a.pasta)
    _saida(a, ps, txt_passos(ps))


def cmd_conferir(a):
    m = carregar(a.pasta)
    erros, avisos = conferir_objetivos(m.get("objetivos", []), fontes(a.pasta))
    if getattr(a, "json", False):
        print(json.dumps({"erros": erros, "avisos": avisos}, ensure_ascii=False, indent=1))
    else:
        for e in erros:
            print("ERRO  " + e)
        for x in avisos:
            print("aviso " + x)
        n = sum(len(o.get("questoes", [])) for o in m.get("objetivos", []))
        print(f"{n} questões, {len(erros)} erro(s), {len(avisos)} aviso(s)." + (" Tudo confere com as fontes." if not erros else ""))
    return 1 if erros else 0


def cmd_adicionar(a):
    m = carregar(a.pasta)
    try:
        novo = json.loads(Path(a.arquivo).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ErroEstudo(f"nêo consegui ler {a.arquivo}: {e}")
    novos = novo.get("objetivos", novo if isinstance(novo, list) else [])
    erros, avisos = conferir_objetivos(novos, fontes(a.pasta))
    if erros:
        for e in erros:
            print("ERRO  " + e)
        print(f"Nada foi gravado: {len(erros)} erro(s). Corrija o arquivo e rode de novo.")
        return 1
    por_id = {o["id"]: o for o in m.get("objetivos", [])}
    for o in novos:
        por_id[o["id"]] = o
    m["objetivos"] = list(por_id.values())
    salvar(m, a.pasta)
    for x in avisos:
        print("aviso " + x)
    print(f"{len(novos)} objetivo(s) gravado(s). A matéria tem {len(m['objetivos'])}.")
    return 0


def cmd_semana(a):
    origem = Path(a.arquivo)
    if not origem.exists() or origem.suffix != ".txt":
        raise ErroEstudo("passe um arquivo .txt com a fonte transcrita (veja prompts/5-semana.md)")
    d = pasta(a.pasta) / "fontes"
    d.mkdir(parents=True, exist_ok=True)
    destino = d / origem.name
    if origem.resolve() != destino.resolve():
        if destino.exists() and not a.forcar:
            raise ErroEstudo(f"já existe fontes/{origem.name}; renomeie (ex.: aula-7.txt) ou use --forcar")
        shutil.copyfile(origem, destino)
    registrar({"tipo": "semana", "fonte": origem.name}, a.pasta)
    print(f"Fonte da semana registrada: fontes/{origem.name}. Agora: objetivos.json (prompts/5-semana.md) e adicionar.")


def cmd_tutor(a):
    m = carregar(a.pasta)
    objetivo(m, a.objetivo)
    registrar({"tipo": "tutor", "objetivo": a.objetivo, "minutos": a.minutos}, a.pasta)
    print(f"Anotado: você estudou {a.objetivo} por {a.minutos} min antes de ensinar.")


def cmd_proximo(a):
    m = carregar(a.pasta)
    sit = situacao(m, diario(a.pasta))
    alvos = [a.objetivo] if a.objetivo else [o["id"] for o in m.get("objetivos", []) if sit[o["id"]] != "dominado"]
    if a.objetivo:
        objetivo(m, a.objetivo)
    res = []
    for oid in alvos:
        r = proximo(m, oid, a.pasta)
        if a.anotar:
            anotar_metodo(oid, r["metodo"], r["motivo"], a.pasta)
            r["anotado"] = True
        res.append(r)
    texto = "\n".join(f"{r['objetivo']}: {r['nome']} — {r['faz']}\n   por quê: {r['motivo']}" + ("\n   (anotado no diário)" if r.get("anotado") else "") for r in res)
    _saida(a, res, texto or "Todos os objetivos estêo dominados. Use o plano da prova para revisar.")


def cmd_metodo(a):
    m = carregar(a.pasta)
    objetivo(m, a.objetivo)
    anotar_metodo(a.objetivo, a.metodo, a.motivo or "escolha de quem ensina", a.pasta)
    print(f"Anotado: {a.objetivo} vai ser estudado com {METODOS[a.metodo]['nome']}.")


def cmd_resultado(a):
    m = carregar(a.pasta)
    objetivo(m, a.objetivo)
    anotar_resultado(a.objetivo, a.acertos, a.total, a.origem, a.quem, a.pasta, a.nota or "")
    regra = m.get("professor", {}).get("regra_objetivo_inteiro", True)
    from .experimento import dominou
    print(f"Anotado: {a.objetivo} {a.acertos}/{a.total} ({a.origem}) → {'dominado' if dominou(a.acertos, a.total, regra) else 'ainda nêo'}.")


def cmd_importar(a):
    m = carregar(a.pasta)
    try:
        dados = json.loads(Path(a.arquivo).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ErroEstudo(f"nêo consegui ler {a.arquivo}: {e}")
    ids = {o["id"] for o in m.get("objetivos", [])}
    atual = {}
    for ev in diario(a.pasta):
        if ev.get("tipo") == "metodo":
            atual[ev["objetivo"]] = ev["metodo"]
    feitos, pulados = 0, []
    for r in dados.get("resultados", []):
        oid = r.get("objetivo")
        if oid not in ids:
            pulados.append(f"{oid}: objetivo nêo existe")
            continue
        met = r.get("metodo")
        if met and met in METODOS and atual.get(oid) != met:
            anotar_metodo(oid, met, "veio do guia do aluno", a.pasta)
            atual[oid] = met
        try:
            anotar_resultado(oid, int(r["acertos"]), int(r["total"]), r.get("origem", "pratica"), r.get("quem", "aluno"), a.pasta)
            feitos += 1
        except (ErroEstudo, KeyError, ValueError) as e:
            pulados.append(f"{oid}: {e}")
    for p in pulados:
        print("pulado " + p)
    print(f"{feitos} resultado(s) importado(s).")
    print(txt_placar(placar(m, a.pasta)))


def cmd_placar(a):
    m = carregar(a.pasta)
    pl = placar(m, a.pasta)
    _saida(a, pl, txt_placar(pl))


def cmd_respostas(a):
    m = carregar(a.pasta)
    try:
        resp = json.loads(Path(a.arquivo).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ErroEstudo(f"nêo consegui ler {a.arquivo}: {e}")
    alertas = conferir_respostas(m, resp)
    texto = "\n".join(f"{x['questao']}: respondeu \"{x.get('resposta_do_aluno', '')}\"; a fonte diz \"{x.get('na_fonte', '')}\""
                      f"\n   trecho ({x.get('fonte', '')}): {x.get('trecho', '')}\n   {x['problema']}" for x in alertas)
    _saida(a, alertas, texto or f"As {len(resp)} respostas batem com as fontes.")
    return 1 if alertas else 0


def cmd_plano_prova(a):
    m = carregar(a.pasta)
    try:
        prova = date.fromisoformat(a.data)
    except ValueError:
        raise ErroEstudo("data no formato AAAA-MM-DD")
    pl = plano_prova(m, diario(a.pasta), prova)
    titulos = {o["id"]: o["titulo"] for o in m.get("objetivos", [])}
    texto = "\n".join(f"{d['dia']}  {d['tarefa']}: " + "; ".join(titulos[i] for i in d["objetivos"]) for d in pl)
    _saida(a, pl, texto or "A prova precisa ser depois de hoje.")


def cmd_guia(a):
    m = carregar(a.pasta)
    erros, _ = conferir_objetivos(m.get("objetivos", []), fontes(a.pasta))
    if erros and not a.mesmo_com_erro:
        for e in erros:
            print("ERRO  " + e)
        print("O guia nêo foi gerado: há questêo sem prova na fonte. Corrija (python3 -m estudo conferir).")
        return 1
    saida = Path(a.saida) if a.saida else pasta(a.pasta) / "guia.html"
    saida.write_text(montar(m, a.pasta), encoding="utf-8")
    print(f"Guia do aluno: {saida}")
    return 0


def cmd_prompts(a):
    base = resources.files("estudo") / "prompts" / a.idioma
    arquivos = sorted(f for f in base.iterdir() if f.name.endswith(".md"))
    if a.numero:
        alvo = [f for f in arquivos if f.name.startswith(f"{a.numero}-")]
        if not alvo:
            raise ErroEstudo(f"nêo há prompt {a.numero} (tem 1 a {len(arquivos)})")
        print(alvo[0].read_text(encoding="utf-8"))
    else:
        for f in arquivos:
            print(f"{f.name[:-3]:<24} " + f.read_text(encoding="utf-8").splitlines()[0].lstrip("# "))
        print("\nVer um: python3 -m estudo prompts 1")


def cmd_diario(a):
    evs = diario(a.pasta)[-a.ultimos:]
    _saida(a, evs, "\n".join(json.dumps(e, ensure_ascii=False) for e in evs) or "diário vazio")


def principal(argv=None):
    ap = argparse.ArgumentParser(prog="estudo", description="Ajudante de quem ensina: guia no jeito do aluno, conferido na fonte, com teste dos métodos às claras.")
    ap.add_argument("--versao", action="version", version=VERSAO)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def c(nome, fn, ajuda):
        s = sub.add_parser(nome, help=ajuda)
        s.add_argument("--pasta", help="pasta da matéria (padrêo: ESTUDO_PASTA ou ~/.estudo-do-seu-jeito)")
        s.add_argument("--json", action="store_true", help="saída em JSON (para agentes)")
        s.set_defaults(fn=fn)
        return s

    s = c("nova", cmd_nova, "cria uma matéria vazia"); s.add_argument("nome"); s.add_argument("--forcar", action="store_true")
    s = c("demo", cmd_demo, "cria a matéria de exemplo (dados inventados) e o guia"); s.add_argument("--forcar", action="store_true")
    c("passos", cmd_passos, "a fórmula em 8 passos e o que falta")
    c("conferir", cmd_conferir, "confere cada questêo na fonte")
    s = c("adicionar", cmd_adicionar, "grava objetivos de um JSON (recusa questêo sem prova na fonte)"); s.add_argument("arquivo")
    s = c("semana", cmd_semana, "registra a fonte nova da semana"); s.add_argument("arquivo"); s.add_argument("--forcar", action="store_true")
    s = c("tutor", cmd_tutor, "anota que quem ensina estudou o objetivo"); s.add_argument("--objetivo", required=True); s.add_argument("--minutos", type=int, default=60)
    s = c("proximo", cmd_proximo, "sugere o método de estudo e diz o porquê"); s.add_argument("--objetivo"); s.add_argument("--anotar", action="store_true", help="grava a escolha no diário")
    s = c("metodo", cmd_metodo, "anota um método escolhido por você"); s.add_argument("--objetivo", required=True); s.add_argument("--metodo", required=True, choices=list(METODOS)); s.add_argument("--motivo")
    s = c("resultado", cmd_resultado, "anota um resultado"); s.add_argument("--objetivo", required=True); s.add_argument("--acertos", type=int, required=True)
    s.add_argument("--total", type=int, required=True); s.add_argument("--origem", default="pratica", choices=["pratica", "prova"]); s.add_argument("--quem", default="tutor", choices=["tutor", "aluno"]); s.add_argument("--nota")
    s = c("importar", cmd_importar, "importa o resultados.json do guia do aluno"); s.add_argument("arquivo")
    c("placar", cmd_placar, "qual método está funcionando (com o tamanho da amostra)")
    s = c("respostas", cmd_respostas, "confere respostas que o aluno preencheu"); s.add_argument("arquivo")
    s = c("plano-prova", cmd_plano_prova, "plano de estudo até a prova"); s.add_argument("--data", required=True)
    s = c("guia", cmd_guia, "gera o guia do aluno (HTML)"); s.add_argument("--saida"); s.add_argument("--mesmo-com-erro", action="store_true")
    s = c("prompts", cmd_prompts, "lista ou mostra os prompts para o chat"); s.add_argument("numero", nargs="?"); s.add_argument("--idioma", default="pt", choices=["pt", "en", "es"])
    s = c("diario", cmd_diario, "mostra o diário (tudo o que foi registrado)"); s.add_argument("--ultimos", type=int, default=20)

    a = ap.parse_args(argv)
    try:
        return a.fn(a) or 0
    except ErroEstudo as e:
        print(f"erro: {e}", file=sys.stderr)
        return 2
