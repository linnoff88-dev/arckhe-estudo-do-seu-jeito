"""A fórmula em 8 passos, com o estado de cada um calculado dos seus dados (não é checklist de enfeite)."""
from datetime import datetime, timedelta

from .dados import diario, fontes, pasta
from .verificador import conferir_objetivos

PASSOS = [
    ("aprender", "Quem ensina aprende primeiro",
     "Antes de ensinar, estude você o ponto em que o aluno errou, com a IA explicando a partir da fonte.",
     "python3 -m estudo tutor --objetivo <id> --minutos 60"),
    ("professor", "Entender como o professor avalia",
     "Como a matéria é dividida e o que faz perder ponto (ex.: errou uma questão, perdeu o objetivo inteiro).",
     "edite professor.como_avalia no materia.json (ou peça no chat: prompts/1-planejar.md)"),
    ("jeito", "Entender como o aluno aprende",
     "Visual, falado, exemplo da vida real, escrita. Pode ser mais de um.",
     "edite aluno.jeito no materia.json: visual, falado, vida-real, escrita"),
    ("erros", "Partir do que ele já errou",
     "O resultado da última prova diz por onde começar.",
     "python3 -m estudo resultado --objetivo <id> --acertos 0 --total 3 --origem prova"),
    ("plano", "Planejar antes de construir",
     "No chat: conte tudo, peça para a IA perguntar o que não sabe e dar opções; feche com um resumo.",
     "salve o resumo em plano.md (prompts/1-planejar.md e 2-resumo.md)"),
    ("guia", "Guia por objetivo, só com o que está na fonte",
     "Cada objetivo com leitura, visual, vida real, pegadinhas e questões que citam o trecho da fonte.",
     "python3 -m estudo adicionar objetivos.json && python3 -m estudo guia"),
    ("semana", "Toda semana: material novo e conferência",
     "Fotos das anotações e o guia do professor entram como fonte; o guia é refeito e conferido.",
     "python3 -m estudo semana anotacoes.txt"),
    ("bastao", "Passar o bastão",
     "O aluno passa a usar sozinho: escolhe o objetivo, estuda, registra o resultado.",
     "o aluno usa o guia.html e importa os resultados (python3 -m estudo importar resultados.json)"),
]


def estado(materia: dict, p=None, hoje=None) -> list:
    eventos = diario(p)
    fts = fontes(p)
    hoje = hoje or datetime.now().astimezone()
    erros, _ = conferir_objetivos(materia.get("objetivos", []), fts)

    def semana_recente():
        for ev in eventos:
            if ev.get("tipo") == "semana":
                try:
                    if hoje - datetime.fromisoformat(ev["quando"]) <= timedelta(days=8):
                        return True
                except (KeyError, ValueError):
                    continue
        return False

    feito = {
        "aprender": any(e.get("tipo") == "tutor" for e in eventos),
        "professor": bool(materia.get("professor", {}).get("como_avalia", "").strip()),
        "jeito": bool(materia.get("aluno", {}).get("jeito")),
        "erros": any(e.get("tipo") == "resultado" and e.get("origem") == "prova" for e in eventos),
        "plano": (pasta(p) / "plano.md").exists(),
        "guia": bool(materia.get("objetivos")) and bool(fts) and not erros,
        "semana": semana_recente(),
        "bastao": sum(1 for e in eventos if e.get("tipo") == "resultado" and e.get("quem") == "aluno") >= 3,
    }
    return [{"id": i, "titulo": t, "explica": x, "como": c, "feito": feito[i]} for i, t, x, c in PASSOS]
