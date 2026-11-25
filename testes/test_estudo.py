"""Testes do kit. Rodar: python3 -m pytest -q testes"""
import asyncio
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from estudo import dados, experimento, formula, plano, verificador  # noqa: E402
from estudo.cli import principal  # noqa: E402


@pytest.fixture
def demo(tmp_path, monkeypatch):
    monkeypatch.setenv("ESTUDO_PASTA", str(tmp_path / "m"))
    assert principal(["demo"]) == 0
    return tmp_path / "m"


def ev_metodo(o, m):
    return {"tipo": "metodo", "objetivo": o, "metodo": m}


def ev_res(o, a, t, origem="pratica"):
    return {"tipo": "resultado", "objetivo": o, "acertos": a, "total": t, "origem": origem}


MAT = {"professor": {"regra_objetivo_inteiro": True}, "aluno": {"jeito": ["visual", "vida-real"]}, "objetivos": []}


# ---------- dados ----------
def test_normalizar_tira_acento_e_pontuacao():
    assert dados.normalizar("  Fotossíntese, ATP!  ") == "fotossintese atp"


def test_diario_so_acrescenta(tmp_path):
    dados.registrar({"tipo": "x", "n": 1}, tmp_path)
    primeira = (tmp_path / "diario.jsonl").read_text().splitlines()[0]
    dados.registrar({"tipo": "x", "n": 2}, tmp_path)
    linhas = (tmp_path / "diario.jsonl").read_text().splitlines()
    assert len(linhas) == 2 and linhas[0] == primeira


def test_sem_materia_da_erro_legivel(tmp_path, capsys):
    assert principal(["passos", "--pasta", str(tmp_path / "nada")]) == 2
    assert "demo" in capsys.readouterr().err


# ---------- demo e guia ----------
def test_demo_cria_tudo_e_confere(demo, capsys):
    for f in ("materia.json", "diario.jsonl", "plano.md", "guia.html", "fontes/fotossintese.txt"):
        assert (demo / f).exists(), f
    assert principal(["conferir"]) == 0
    assert "0 erro(s)" in capsys.readouterr().out


def test_demo_nao_sobrescreve(demo):
    assert principal(["demo"]) == 2


def test_demo_placar_mostra_pouco_dado(demo, capsys):
    principal(["placar"])
    assert "pouco dado" in capsys.readouterr().out


def test_guia_html_tem_dados_e_escapa_script(demo):
    m = dados.carregar()
    m["objetivos"][0]["leitura"] = "texto </script><script>alert(1)</script>"
    dados.salvar(m)
    assert principal(["guia"]) == 0
    html = (demo / "guia.html").read_text()
    bloco = re.search(r'<script type="application/json" id="dados">(.*?)</script>', html, re.S).group(1)
    assert "</script" not in bloco
    assert json.loads(bloco)["materia"]["objetivos"][0]["leitura"].startswith("texto </script>")


def test_guia_recusa_com_questao_sem_prova(demo, capsys):
    m = dados.carregar()
    m["objetivos"][0]["questoes"][0]["trecho"] = "isto nêo está escrito em lugar nenhum da fonte"
    dados.salvar(m)
    assert principal(["guia"]) == 1
    assert "nêo foi gerado" in capsys.readouterr().out


# ---------- verificador ----------
FONTES = {"a.txt": "A glicólise ocorre no citoplasma e nêo precisa de oxigênio."}


def q(**kw):
    base = {"id": "q1", "pergunta": "Onde?", "resposta": "Citoplasma", "fonte": "a.txt", "trecho": "A glicólise ocorre no citoplasma"}
    base.update(kw)
    return base


def test_trecho_que_existe_passa_mesmo_sem_acento():
    erros, avisos = verificador.conferir_questao(q(trecho="a glicolise ocorre no CITOPLASMA"), FONTES)
    assert erros == [] and avisos == []


def test_trecho_inventado_e_recusado():
    erros, _ = verificador.conferir_questao(q(trecho="A glicólise ocorre na mitocôndria"), FONTES)
    assert any("nêo existe" in e for e in erros)


def test_fonte_que_nao_existe_e_recusada():
    erros, _ = verificador.conferir_questao(q(fonte="livro.txt"), FONTES)
    assert any("nêo está em fontes" in e for e in erros)


def test_trecho_curto_demais_e_recusado():
    erros, _ = verificador.conferir_questao(q(trecho="no citoplasma"), FONTES)
    assert any("curto" in e for e in erros)


def test_resposta_fora_das_opcoes_e_recusada():
    erros, _ = verificador.conferir_questao(q(opcoes=["Núcleo", "Estroma"]), FONTES)
    assert any("opções" in e for e in erros)


def test_resposta_que_nao_aparece_no_trecho_vira_aviso():
    erros, avisos = verificador.conferir_questao(q(resposta="Ribossomo"), FONTES)
    assert erros == [] and avisos


def test_adicionar_recusa_arquivo_inteiro_se_uma_questao_falha(demo, tmp_path, capsys):
    antes = (demo / "materia.json").read_text()
    novo = {"objetivos": [{"id": "novo", "titulo": "Novo", "questoes": [
        q(id="n1", fonte="respiracao.txt", trecho="Glicólise: ocorre no citoplasma"),
        q(id="n2", fonte="respiracao.txt", trecho="a glicólise acontece no núcleo da célula")]}]}
    arq = tmp_path / "obj.json"
    arq.write_text(json.dumps(novo))
    assert principal(["adicionar", str(arq)]) == 1
    assert (demo / "materia.json").read_text() == antes
    assert "Nada foi gravado" in capsys.readouterr().out


def test_adicionar_grava_e_substitui_pelo_id(demo, tmp_path):
    novo = {"objetivos": [{"id": "respiracao", "titulo": "Respiraçêo (refeito)", "fontes": ["respiracao.txt"],
                           "questoes": [q(id="r9", fonte="respiracao.txt", trecho="Glicólise: ocorre no citoplasma")]}]}
    arq = tmp_path / "obj.json"
    arq.write_text(json.dumps(novo))
    assert principal(["adicionar", str(arq)]) == 0
    m = dados.carregar()
    assert len(m["objetivos"]) == 3
    assert dados.objetivo(m, "respiracao")["titulo"] == "Respiraçêo (refeito)"


def test_respostas_do_aluno_erradas_sao_apontadas(demo):
    m = dados.carregar()
    alertas = verificador.conferir_respostas(m, {"f1": "Estroma", "f2": "Da água", "g3": "só aparece em dose dupla aa", "zz": "x"})
    ids = {a["questao"] for a in alertas}
    assert ids == {"f1", "zz"}
    f1 = next(a for a in alertas if a["questao"] == "f1")
    assert f1["na_fonte"] == "Tilacoides" and "tilacoides" in f1["trecho"]


# ---------- experimento ----------
def test_regra_do_objetivo_inteiro():
    assert not experimento.dominou(2, 3, True)
    assert experimento.dominou(3, 3, True)
    assert experimento.dominou(4, 5, False)


def test_resultado_conta_para_o_metodo_anotado_antes():
    evs = [ev_res("a", 1, 3, "prova"), ev_metodo("a", "redesenhar"), ev_res("a", 3, 3)]
    pl = experimento.placar(MAT, eventos=evs)
    por = {l["metodo"]: l for l in pl["linhas"]}
    assert por["sem-metodo"]["dominados"] == 0 and por["redesenhar"]["dominados"] == 1


def test_prova_vale_mais_que_pratica_no_mesmo_par():
    evs = [ev_metodo("a", "redesenhar"), ev_res("a", 3, 3, "prova"), ev_res("a", 1, 3, "pratica")]
    linha = experimento.placar(MAT, eventos=evs)["linhas"][0]
    assert linha["dominados"] == 1


def test_menos_de_tres_objetivos_nunca_e_lider():
    evs = []
    for o in ("a", "b"):
        evs += [ev_metodo(o, "redesenhar"), ev_res(o, 3, 3)]
    for o in ("c", "d", "e"):
        evs += [ev_metodo(o, "releitura"), ev_res(o, 0, 3)]
    pl = experimento.placar(MAT, eventos=evs)
    assert pl["lider"] is None
    assert {l["metodo"]: l["pouco_dado"] for l in pl["linhas"]}["redesenhar"] is True


def test_lider_com_dados_e_vantagem():
    evs = []
    for o in ("a", "b", "c"):
        evs += [ev_metodo(o, "redesenhar"), ev_res(o, 3, 3)]
    for o in ("d", "e", "f"):
        evs += [ev_metodo(o, "releitura"), ev_res(o, 1, 3)]
    pl = experimento.placar(MAT, eventos=evs)
    assert pl["lider"] == "redesenhar" and "na frente por enquanto" in pl["veredito"]


def test_empate_quando_diferenca_pequena():
    evs = []
    for i, o in enumerate("abc"):
        evs += [ev_metodo(o, "redesenhar"), ev_res(o, 3 if i < 2 else 1, 3)]
    for i, o in enumerate("def"):
        evs += [ev_metodo(o, "releitura"), ev_res(o, 3 if i < 2 else 1, 3)]
    pl = experimento.placar(MAT, eventos=evs)
    assert pl["lider"] is None and "Empate" in pl["veredito"]


def test_proximo_escolhe_o_menos_testado_e_evita_o_que_falhou():
    evs = [ev_metodo("a", "redesenhar"), ev_res("a", 1, 3), ev_metodo("b", "vida-real"), ev_res("b", 3, 3)]
    r = experimento.proximo(MAT, "a", eventos=evs)
    assert r["metodo"] == "pratica-sem-consulta"
    assert "Ver e redesenhar" in r["motivo"]


def test_proximo_usa_o_lider_quando_todos_tem_dados():
    mat = {**MAT, "aluno": {"jeito": ["visual"]}}  # candidatos: redesenhar, pratica-sem-consulta, releitura
    evs = []
    for o, met, ac in [("a", "redesenhar", 3), ("b", "redesenhar", 3), ("c", "redesenhar", 3),
                       ("d", "pratica-sem-consulta", 1), ("e", "pratica-sem-consulta", 1), ("f", "pratica-sem-consulta", 1),
                       ("g", "releitura", 1), ("h", "releitura", 1), ("i", "releitura", 1)]:
        evs += [ev_metodo(o, met), ev_res(o, ac, 3)]
    assert experimento.proximo(mat, "novo", eventos=evs)["metodo"] == "redesenhar"


def test_resultado_impossivel_e_recusado(tmp_path):
    for a, t in ((4, 3), (-1, 3), (0, 0)):
        with pytest.raises(dados.ErroEstudo):
            experimento.anotar_resultado("a", a, t, p=tmp_path)


# ---------- plano ----------
def test_plano_comeca_pelo_que_errou_e_termina_em_revisao(demo):
    m = dados.carregar()
    hoje = date.today()
    pl = plano.plano_prova(m, dados.diario(), hoje + timedelta(days=4), hoje)
    assert pl[0]["objetivos"][0] == "respiracao"
    assert pl[-1]["tarefa"].startswith("revisêo geral")


def test_plano_nao_deixa_objetivo_de_fora():
    m = {"objetivos": [{"id": f"o{i}"} for i in range(9)]}
    hoje = date.today()
    pl = plano.plano_prova(m, [], hoje + timedelta(days=3), hoje)
    estudados = {o for d in pl[:-1] for o in d["objetivos"]}
    assert estudados == {f"o{i}" for i in range(9)}


def test_plano_com_data_passada_fica_vazio():
    assert plano.plano_prova({"objetivos": [{"id": "a"}]}, [], date.today(), date.today()) == []


# ---------- fórmula ----------
def test_formula_materia_vazia_nada_feito(tmp_path):
    m = dados.materia_vazia("x")
    dados.salvar(m, tmp_path)
    assert not any(s["feito"] for s in formula.estado(m, tmp_path))


def test_formula_bastao_depois_de_tres_resultados_do_aluno(demo, tmp_path):
    m = dados.carregar()
    assert {s["id"]: s["feito"] for s in formula.estado(m)}["bastao"] is False
    arq = tmp_path / "resultados.json"
    arq.write_text(json.dumps({"resultados": [{"objetivo": "respiracao", "acertos": 3, "total": 3, "metodo": "explicar-falando"}]}))
    principal(["importar", str(arq)])
    assert {s["id"]: s["feito"] for s in formula.estado(m)}["bastao"] is True


# ---------- importar e semana ----------
def test_importar_anota_metodo_do_app_e_pula_objetivo_desconhecido(demo, tmp_path, capsys):
    arq = tmp_path / "r.json"
    arq.write_text(json.dumps({"resultados": [
        {"objetivo": "respiracao", "acertos": 3, "total": 3, "metodo": "explicar-falando", "quem": "aluno"},
        {"objetivo": "quimica", "acertos": 1, "total": 1}]}))
    principal(["importar", str(arq)])
    out = capsys.readouterr().out
    assert "1 resultado(s) importado(s)" in out and "pulado quimica" in out
    evs = dados.diario()
    assert evs[-2]["tipo"] == "metodo" and evs[-2]["metodo"] == "explicar-falando"


def test_semana_copia_fonte_e_nao_sobrescreve(demo, tmp_path):
    f = tmp_path / "aula-7.txt"
    f.write_text("conteúdo novo da aula sete")
    assert principal(["semana", str(f)]) == 0
    assert (demo / "fontes" / "aula-7.txt").exists()
    assert principal(["semana", str(f)]) == 2


# ---------- prompts ----------
@pytest.mark.parametrize("idioma", ["pt", "en", "es"])
def test_prompts_nos_tres_idiomas(idioma, capsys):
    assert principal(["prompts", "--idioma", idioma]) == 0
    assert len(capsys.readouterr().out.splitlines()) >= 8


# ---------- plugin do INTELECTO ----------
INTELECTO = Path.home() / "projetos" / "intelecto-v2"


@pytest.fixture
def intelecto():
    if not (INTELECTO / "intelecto").is_dir():
        pytest.skip("intelecto-v2 nêo está nesta máquina")
    sys.path.insert(0, str(INTELECTO))
    from intelecto.ferramentas import plugins
    from intelecto.config import Config
    from intelecto.ferramentas.base import Registro
    return plugins, Config, Registro


def test_plugin_carrega_sem_aviso_e_nao_troca_ferramenta(intelecto, demo):
    plugins, Config, Registro = intelecto
    from estudo.intelecto_plugin import ferramentas

    class EP:
        name = "estudo"
        def load(self):
            return ferramentas

    reg = Registro([])
    avisos = plugins.carregar(Config(plugins=["estudo"]), None, reg, [EP()])
    nomes = [f.nome for f in reg.todas()]
    assert avisos == [] and len(nomes) == len(set(nomes)) == 6
    assert all(n.startswith("estudo_") for n in nomes)


def test_plugin_executa_e_erro_vira_resultado(intelecto, demo):
    from estudo.intelecto_plugin import ferramentas
    fs = {f.nome: f for f in ferramentas()}
    r = asyncio.run(fs["estudo_placar"].executar())
    assert r.ok and "pouco dado" in r.saida
    r = asyncio.run(fs["estudo_registrar_resultado"].executar(objetivo="nao-existe", acertos=1, total=1))
    assert not r.ok and "nêo existe" in r.saida
    r = asyncio.run(fs["estudo_proximo_metodo"].executar(objetivo="respiracao", anotar=True))
    assert r.ok and dados.diario()[-1]["tipo"] == "metodo"


# ---------- portêo: o repositório nêo cita a fonte de inspiraçêo ----------
def test_repositorio_sem_fonte_de_inspiracao():
    proibido = re.compile("|".join(["hum" + "anly", "\\bam" + "y\\b", "\\bem" + "ma\\b", "simp" + "son", "o0o3" + "D"]), re.I)
    achados = []
    for f in RAIZ.rglob("*"):
        if f.is_file() and ".git" not in f.parts and "__pycache__" not in f.parts and f.suffix in {".py", ".md", ".html", ".json", ".txt", ".toml"}:
            if proibido.search(f.read_text(encoding="utf-8", errors="ignore")):
                achados.append(str(f.relative_to(RAIZ)))
    assert achados == []


def test_resposta_bem_mais_longa_vira_aviso():
    fontes = {"a.txt": "a proporçêo de fenótipos é 3 dominantes para 1 recessivo"}
    qq = {"id": "q", "pergunta": "?", "opcoes": ["1 : 1", "3 dominantes para 1 recessivo", "1 : 2 : 1"],
          "resposta": "3 dominantes para 1 recessivo", "fonte": "a.txt", "trecho": "proporçêo de fenótipos é 3 dominantes"}
    _, avisos = verificador.conferir_questao(qq, fontes)
    assert any("mais longa" in a for a in avisos)


def test_app_embaralha_as_opcoes(demo):
    principal(["guia"])
    assert "Math.random()" in (demo / "guia.html").read_text()


def test_exemplo_sem_resposta_adivinhavel(demo, capsys):
    principal(["conferir"])
    assert "mais longa" not in capsys.readouterr().out
