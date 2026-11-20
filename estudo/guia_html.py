"""Gera o guia de estudo do aluno: uma página HTML só, que abre no navegador do celular ou do computador, sem internet.

Tudo o que aparece vem do materia.json (já conferido) e do diário. O aluno marca o que quer estudar hoje,
alterna entre ler, ver, vida real, pegadinhas e questões, monta o plano até a prova, imprime a folha de resumo
e exporta os resultados para o kit registrar (python3 -m estudo importar resultados.json).
"""
import json

from .dados import diario, fontes
from .experimento import placar
from .metodos import METODOS
from .plano import situacao
from . import VERSAO


def _metodo_atual(eventos):
    atual = {}
    for ev in eventos:
        if ev.get("tipo") == "metodo":
            atual[ev["objetivo"]] = {"metodo": ev["metodo"], "motivo": ev.get("motivo", "")}
    return atual


def montar(materia: dict, p=None, eventos=None) -> str:
    eventos = diario(p) if eventos is None else eventos
    dados = {
        "versao": VERSAO,
        "materia": materia,
        "metodos": METODOS,
        "atual": _metodo_atual(eventos),
        "situacao": situacao(materia, eventos),
        "placar": placar(materia, eventos=eventos),
        "fontes": sorted(fontes(p)),
    }
    js = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    titulo = materia.get("nome", "Guia de estudo")
    return MODELO.replace("__DADOS__", js).replace("__TITULO__", _esc(titulo))


def _esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


MODELO = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITULO__ · guia de estudo</title>
<style>
:root{--bg:#0c0c10;--bg2:#14141b;--card:#16161e;--line:#272730;--txt:#e9e9ee;--mut:#9a9aa6;--amb:#FACC15;--ok:#4ade80;--bad:#f87171;--ink:#1a1206}
body.light{--bg:#f6f7f9;--bg2:#eceef2;--card:#ffffff;--line:#e1e3ea;--txt:#1a1a22;--mut:#5b5b68;--amb:#a16207;--ok:#15803d;--bad:#b91c1c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--txt);font:16px/1.55 Inter,system-ui,sans-serif}
h1,h2,h3,button,.tab{font-family:Sora,Inter,system-ui,sans-serif}
header{padding:18px 16px 8px;max-width:1000px;margin:0 auto}
h1{font-size:1.45rem;margin:0 0 4px}
.mut{color:var(--mut)}
nav{display:flex;gap:6px;flex-wrap:wrap;padding:8px 16px;max-width:1000px;margin:0 auto;position:sticky;top:0;background:var(--bg);z-index:2;border-bottom:1px solid var(--line)}
.tab{background:transparent;border:1px solid var(--line);color:var(--txt);border-radius:999px;padding:7px 13px;font-size:.9rem;cursor:pointer}
.tab.on{background:var(--amb);color:var(--ink);border-color:var(--amb)}
main{max-width:1000px;margin:0 auto;padding:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:0 0 14px;min-width:0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.chip{display:inline-block;font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--line);border-radius:999px;padding:2px 9px;margin:2px 4px 2px 0}
.chip.ok{border-color:var(--ok);color:var(--ok)} .chip.bad{border-color:var(--bad);color:var(--bad)}
button.b{background:var(--amb);color:var(--ink);border:0;border-radius:10px;padding:9px 14px;font-weight:600;cursor:pointer;margin:4px 6px 4px 0}
button.s{background:transparent;color:var(--txt);border:1px solid var(--line);border-radius:10px;padding:8px 12px;cursor:pointer;margin:4px 6px 4px 0}
label{cursor:pointer}
.opc{display:block;width:100%;text-align:left;margin:6px 0}
.certo{border-color:var(--ok)!important} .errado{border-color:var(--bad)!important}
.fonte{font-size:.9rem;border-left:3px solid var(--amb);padding:6px 10px;margin-top:8px;color:var(--mut)}
.fluxo{display:flex;align-items:stretch;gap:8px;margin:10px 0}
.etapa{flex:1 1 0;min-width:0;border:2px solid var(--amb);border-radius:12px;padding:10px 12px;background:var(--bg2);overflow-wrap:anywhere}
.etapa b{display:block;margin-bottom:4px}
.seta{align-self:center;font-size:1.6rem;color:var(--mut)}
@media (max-width:640px){.fluxo{flex-direction:column}.seta{transform:rotate(90deg);text-align:center}}
textarea,input[type=date]{width:100%;background:var(--bg2);color:var(--txt);border:1px solid var(--line);border-radius:10px;padding:9px;font:inherit}
table{border-collapse:collapse;width:100%} td,th{border-bottom:1px solid var(--line);padding:7px;text-align:left;vertical-align:top}
.oculto{display:none}
.rolar{overflow-x:auto;max-width:100%}
#imprimir{display:none}
@media print{
 body{background:#fff;color:#000} header,nav,main{display:none!important} #imprimir{display:block!important;color:#000}
 #imprimir .card{border:1px solid #000;break-inside:avoid;background:#fff}
 #imprimir .etapa{border-color:#000;background:#fff} #imprimir .seta{color:#000}
}
</style>
</head>
<body>
<header>
 <h1 id="titulo"></h1>
 <div class="mut" id="sub"></div>
</header>
<nav id="abas"></nav>
<main id="tela"></main>
<div id="imprimir"></div>
<script type="application/json" id="dados">__DADOS__</script>
<script>
"use strict";
const D = JSON.parse(document.getElementById("dados").textContent);
const M = D.materia, OBJ = M.objetivos || [];
const REGRA = (M.professor || {}).regra_objetivo_inteiro !== false;
const guarda = {
  ler(k, v){ try{ const x = localStorage.getItem("estudo:" + M.nome + ":" + k); return x ? JSON.parse(x) : v }catch(e){ return v } },
  gravar(k, v){ try{ localStorage.setItem("estudo:" + M.nome + ":" + k, JSON.stringify(v)) }catch(e){} }
};
let escolhidos = guarda.ler("escolhidos", OBJ.map(o => o.id));
let resultados = guarda.ler("resultados", []);
if (guarda.ler("tema", "") === "claro") document.body.classList.add("light");

function el(tag, attrs, ...filhos){
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})){
    if (k === "on") for (const [ev, fn] of Object.entries(v)) e.addEventListener(ev, fn);
    else if (k === "class") e.className = v; else e.setAttribute(k, v);
  }
  for (const f of filhos.flat()) if (f !== null && f !== undefined) e.append(f instanceof Node ? f : document.createTextNode(String(f)));
  return e;
}
const metodoDe = oid => (D.atual[oid] || {}).metodo;
function situacaoLocal(oid){
  const meus = resultados.filter(r => r.objetivo === oid);
  if (meus.length) return dominou(meus[meus.length - 1]) ? "dominado" : "errou";
  return D.situacao[oid] || "nao-testado";
}
const dominou = r => REGRA ? r.acertos === r.total : r.acertos / r.total >= 0.8;
const rotulo = {dominado: ["ok", "dominado"], errou: ["bad", "ainda não"], "nao-testado": ["", "não testado"]};
function chipSit(oid){ const [c, t] = rotulo[situacaoLocal(oid)]; return el("span", {class: "chip " + c}, t) }

function diagrama(etapas, esconder){
  const f = el("div", {class: "fluxo", role: "img", "aria-label": etapas.map(e => e.nome).join(" → ")});
  etapas.forEach((e, i) => {
    const vazio = "______";
    f.append(el("div", {class: "etapa"}, el("b", {}, e.nome),
      el("div", {}, "onde: ", esconder ? vazio : e.onde),
      el("div", {}, "entra: ", esconder ? vazio : e.entra),
      el("div", {}, "sai: ", esconder ? vazio : e.sai)));
    if (i < etapas.length - 1) f.append(el("div", {class: "seta", "aria-hidden": "true"}, "→"));
  });
  return f;
}

function caixaMetodo(oid){
  const m = metodoDe(oid);
  if (!m) return el("div", {class: "fonte"}, "Método desta semana: ainda não escolhido. Quem ensina escolhe com: python3 -m estudo proximo --objetivo " + oid);
  const info = D.metodos[m];
  return el("div", {class: "fonte"}, el("b", {}, "Método desta semana: " + info.nome + ". "), info.faz, " ", el("span", {class: "mut"}, "Por quê: " + (D.atual[oid].motivo || info.porque)));
}

// ---------- telas ----------
const TELAS = {
  hoje(){
    const lista = el("div", {class: "grid"}, OBJ.map(o => el("label", {class: "card"},
      el("input", {type: "checkbox", ...(escolhidos.includes(o.id) ? {checked: ""} : {}), on: {change: ev => {
        escolhidos = ev.target.checked ? [...new Set([...escolhidos, o.id])] : escolhidos.filter(x => x !== o.id);
        guarda.gravar("escolhidos", escolhidos); }}}),
      " ", el("b", {}, o.titulo), el("div", {}, chipSit(o.id)),
      el("div", {class: "mut"}, (o.topicos || []).join(" · ")))));
    return [el("div", {class: "card"}, el("h2", {}, "O que você quer estudar hoje?"),
      el("p", {class: "mut"}, "Marque só o que precisa. As outras abas mostram apenas o que estiver marcado. Você pode mudar quando quiser.")), lista];
  },
  estudar(){
    const sel = OBJ.filter(o => escolhidos.includes(o.id));
    if (!sel.length) return [el("div", {class: "card"}, "Nada marcado. Volte em Hoje e escolha um objetivo.")];
    return sel.map(o => {
      const corpo = el("div", {});
      const modos = {
        "Ler": () => [el("p", {}, o.leitura || ""), el("div", {class: "mut"}, "Fonte: " + (o.fontes || []).join(", "))],
        "Ver": () => { let esc = false; const box = el("div", {}, diagrama(o.etapas || [], false));
          return [box, el("button", {class: "s", on: {click: ev => { esc = !esc; box.replaceChildren(diagrama(o.etapas || [], esc)); ev.target.textContent = esc ? "Mostrar de novo e comparar" : "Esconder e redesenhar de memória" }}}, "Esconder e redesenhar de memória"),
            el("p", {class: "mut"}, "Redesenhe no papel, com setas, antes de comparar.")] },
        "Vida real": () => [el("p", {}, o.vida_real || "")],
        "Pegadinhas": () => [el("ul", {}, (o.pegadinhas || []).map(p => el("li", {}, p)))],
        "Questões": () => questoes(o)
      };
      const barra = el("div", {});
      const abrir = nome => { corpo.replaceChildren(...modos[nome]()); [...barra.children].forEach(b => b.classList.toggle("on", b.textContent === nome)) };
      Object.keys(modos).forEach(n => barra.append(el("button", {class: "tab", on: {click: () => abrir(n)}}, n)));
      const card = el("div", {class: "card"}, el("h2", {}, o.titulo, " "), chipSit(o.id), caixaMetodo(o.id), barra, corpo);
      const sub = decodeURIComponent(location.hash.split(":")[1] || "");
      abrir(sub in modos ? sub : "Ler");
      return card;
    });
  },
  plano(){
    const saida = el("div", {});
    const data = el("input", {type: "date", on: {change: () => {
      const prova = new Date(data.value + "T12:00:00"), hoje = new Date(); hoje.setHours(12, 0, 0, 0);
      const dias = Math.round((prova - hoje) / 864e5);
      if (!(dias >= 1)) { saida.replaceChildren(el("p", {}, "Escolha uma data depois de hoje.")); return }
      const peso = {errou: 0, "nao-testado": 1, dominado: 2};
      const fila = [...OBJ].sort((a, b) => peso[situacaoLocal(a.id)] - peso[situacaoLocal(b.id)] || a.id.localeCompare(b.id));
      const pend = fila.filter(o => situacaoLocal(o.id) !== "dominado"), rev = fila.filter(o => situacaoLocal(o.id) === "dominado");
      const porDia = dias > 1 ? Math.max(2, Math.ceil(pend.length / (dias - 1))) : 2;
      const linhas = [];
      for (let i = 0; i < dias; i++){
        const d = new Date(hoje.getTime() + i * 864e5).toLocaleDateString("pt-BR", {weekday: "short", day: "2-digit", month: "2-digit"});
        if (i === dias - 1) { linhas.push([d, "revisão geral: só as questões, sem consultar", fila]); continue }
        let bloco = pend.slice(i * porDia, (i + 1) * porDia), tarefa = "estudar com o método da semana e fazer as questões";
        if (!bloco.length && rev.length) { bloco = [rev[i % rev.length]]; tarefa = "revisar um objetivo já dominado (para não esquecer)" }
        if (bloco.length) linhas.push([d, tarefa, bloco]);
      }
      saida.replaceChildren(el("div", {class: "rolar"}, el("table", {}, el("tr", {}, el("th", {}, "Dia"), el("th", {}, "O quê"), el("th", {}, "Objetivos")),
        linhas.map(([d, t, b]) => el("tr", {}, el("td", {}, d), el("td", {}, t), el("td", {}, b.map(o => o.titulo).join("; ")))))));
    }}});
    return [el("div", {class: "card"}, el("h2", {}, "Plano até a prova"),
      el("p", {class: "mut"}, "Primeiro o que você errou, depois o que ainda não testou; no último dia, só questões sem consultar."),
      el("p", {}, "Data da prova: ", data), saida)];
  },
  resumo(){
    let modo = "tudo";
    const marcar = el("div", {}, ["tudo", "só diagramas", "só questões"].map(m => el("label", {}, el("input", {type: "radio", name: "modo", value: m, ...(m === "tudo" ? {checked: ""} : {}), on: {change: () => { modo = m }}}), " " + m + "  ")));
    return [el("div", {class: "card"}, el("h2", {}, "Folha de resumo para imprimir"),
      el("p", {class: "mut"}, "Preto e branco, só com os objetivos marcados em Hoje. Leve no bolso."), marcar,
      el("button", {class: "b", on: {click: () => { montarImpressao(modo); window.print() }}}, "Imprimir"))];
  },
  placar(){
    const P = D.placar;
    return [el("div", {class: "card"}, el("h2", {}, "Qual método está funcionando para você"),
      el("p", {}, P.veredito),
      el("div", {class: "rolar"}, el("table", {}, el("tr", {}, el("th", {}, "Método"), el("th", {}, "Testados"), el("th", {}, "Dominados")),
        P.linhas.map(l => el("tr", {}, el("td", {}, l.nome, l.pouco_dado ? el("div", {}, el("span", {class: "chip"}, "pouco dado")) : ""), el("td", {}, l.n), el("td", {}, l.dominados + " (" + l.taxa + "%)"))))),
      el("h3", {}, "As regras do teste"),
      el("ol", {}, [
        "Antes de estudar um objetivo, o método é escolhido e anotado, com o motivo.",
        "O resultado conta para o método anotado por último naquele objetivo.",
        REGRA ? "Dominado = acertar todas as questões do objetivo (a regra do professor)." : "Dominado = acertar 80% ou mais.",
        "Com menos de " + P.min_n + " objetivos, o método fica como \"pouco dado\" e não é chamado de melhor.",
        "Este placar mostra o que já foi importado no kit. Resultados de hoje ainda não importados: " + resultados.length + "."
      ].map(t => el("li", {}, t))))];
  },
  dicas(){
    const d = [
      ["Tente lembrar antes de reler", "Fazer as questões sem consultar fixa mais do que ler de novo."],
      ["Espalhe o estudo", "Um pouco por dia, vários dias, rende mais que uma noite inteira antes da prova."],
      ["Misture os objetivos", "Alternar assuntos na mesma sessão ajuda a saber qual regra usar em cada questão."],
      ["Explique com as suas palavras", "Se travou ao explicar, achou o ponto que falta."],
      ["Desenhe o processo", "Esquema com setas, de memória, e depois compare."],
      ["Corrija na fonte", "Errou? Leia o trecho da fonte que vem com a resposta, não só o gabarito."]
    ];
    return [el("div", {class: "grid"}, d.map(([t, x]) => el("div", {class: "card"}, el("h3", {}, t), el("p", {class: "mut"}, x))))];
  },
  exportar(){
    const txt = JSON.stringify({materia: M.nome, resultados}, null, 1);
    return [el("div", {class: "card"}, el("h2", {}, "Mandar os resultados para o kit"),
      el("p", {class: "mut"}, "Baixe o arquivo e quem cuida do kit roda: python3 -m estudo importar resultados.json. Depois disso o placar e o plano levam em conta o que você fez."),
      el("p", {}, "Resultados guardados neste aparelho: " + resultados.length),
      el("button", {class: "b", on: {click: () => { const a = el("a", {href: URL.createObjectURL(new Blob([txt], {type: "application/json"})), download: "resultados.json"}); document.body.append(a); a.click(); a.remove() }}}, "Baixar resultados.json"),
      el("button", {class: "s", on: {click: () => { resultados = []; guarda.gravar("resultados", resultados); trocar("exportar") }}}, "Limpar depois de importar"),
      el("textarea", {rows: 6, readonly: ""}, txt))];
  }
};

function questoes(o){
  const qs = o.questoes || [];
  let respondidas = 0, acertos = 0;
  const fim = el("div", {});
  const fechar = () => {
    if (respondidas < qs.length) return;
    const r = {objetivo: o.id, acertos, total: qs.length, origem: "pratica", quem: "aluno", metodo: metodoDe(o.id) || null, quando: new Date().toISOString()};
    resultados.push(r); guarda.gravar("resultados", resultados);
    fim.replaceChildren(el("p", {}, el("b", {}, acertos + " de " + qs.length + ". "), dominou(r) ? "Objetivo dominado." : (REGRA ? "Pela regra do professor, errar uma questão perde o objetivo inteiro: estude o trecho da fonte e tente de novo amanhã." : "Ainda não chegou a 80%.")), el("p", {class: "mut"}, "Resultado guardado. Mande para o kit na aba Exportar."));
  };
  return [el("p", {class: "mut"}, "Responda sem consultar. As opções mudam de ordem cada vez que você abre. Depois de cada resposta aparece o trecho da fonte que prova a certa."),
    ...qs.map(q => {
      const caixa = el("div", {class: "card"}, el("b", {}, q.pergunta));
      const prova = () => el("div", {class: "fonte"}, (q.explicacao ? q.explicacao + " " : ""), el("i", {}, "“" + q.trecho + "”"), " — " + q.fonte);
      const marcar = ok => { respondidas++; if (ok) acertos++; fechar() };
      if (q.opcoes && q.opcoes.length){
        const ordem = [...q.opcoes]; for (let i = ordem.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [ordem[i], ordem[j]] = [ordem[j], ordem[i]] }
        const bts = ordem.map(op => el("button", {class: "s opc", on: {click: () => {
          if (caixa.dataset.feito) return; caixa.dataset.feito = 1;
          const ok = op === q.resposta;
          bts.forEach(b => { if (b.textContent === q.resposta) b.classList.add("certo"); else if (b.textContent === op) b.classList.add("errado") });
          caixa.append(el("p", {}, ok ? "Certo." : "Não. A certa é: " + q.resposta), prova()); marcar(ok);
        }}}, op));
        caixa.append(...bts);
      } else {
        const t = el("textarea", {rows: 2, placeholder: "Sua resposta, com as suas palavras"});
        const ver = el("button", {class: "s", on: {click: () => {
          if (caixa.dataset.feito) return; caixa.dataset.feito = 1; ver.remove();
          caixa.append(el("p", {}, "Resposta da fonte: " + q.resposta), prova(),
            el("button", {class: "b", on: {click: ev => { if (ev.target.dataset.f) return; ev.target.dataset.f = 1; marcar(true) }}}, "Acertei"),
            el("button", {class: "s", on: {click: ev => { if (ev.target.dataset.f) return; ev.target.dataset.f = 1; marcar(false) }}}, "Errei"));
        }}}, "Ver resposta");
        caixa.append(t, ver);
      }
      return caixa;
    }), fim];
}

function montarImpressao(modo){
  const alvo = document.getElementById("imprimir");
  alvo.replaceChildren(el("h2", {}, M.nome + " — folha de resumo"));
  OBJ.filter(o => escolhidos.includes(o.id)).forEach(o => {
    const c = el("div", {class: "card"}, el("h3", {}, o.titulo));
    if (modo !== "só questões") { c.append(diagrama(o.etapas || [], false)); c.append(el("ul", {}, (o.pegadinhas || []).map(p => el("li", {}, p)))) }
    if (modo !== "só diagramas") c.append(el("ol", {}, (o.questoes || []).map(q => el("li", {}, q.pergunta + "  ________________"))));
    alvo.append(c);
  });
}

const NOMES = {hoje: "Hoje", estudar: "Estudar", plano: "Plano da prova", resumo: "Folha de resumo", placar: "Placar dos métodos", dicas: "Dicas", exportar: "Exportar"};
function trocar(t){
  document.getElementById("tela").replaceChildren(...TELAS[t]());
  [...document.querySelectorAll("#abas .tab")].forEach(b => b.classList.toggle("on", b.dataset.t === t));
  guarda.gravar("aba", t);
}
document.getElementById("titulo").textContent = M.nome;
const aluno = (M.aluno || {}).nome;
document.getElementById("sub").textContent = (aluno ? "Guia de " + aluno + " · " : "") + (M.exemplo ? "exemplo com dados inventados · " : "") + "versão " + D.versao;
const abas = document.getElementById("abas");
Object.entries(NOMES).forEach(([k, v]) => abas.append(el("button", {class: "tab", "data-t": k, on: {click: () => trocar(k)}}, v)));
abas.append(el("button", {class: "tab", on: {click: () => { document.body.classList.toggle("light"); guarda.gravar("tema", document.body.classList.contains("light") ? "claro" : "escuro") }}}, "Claro/escuro"));
const hashAba = location.hash.slice(1).split(":")[0];
const pedida = hashAba in TELAS ? hashAba : guarda.ler("aba", "hoje");
trocar(pedida in TELAS ? pedida : "hoje");
</script>
</body>
</html>
"""
