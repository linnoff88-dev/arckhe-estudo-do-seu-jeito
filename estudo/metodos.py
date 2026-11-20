"""Os métodos de estudo que o kit sabe testar. Cada um diz o que o aluno faz, para que jeito serve e por quê."""

METODOS = {
    "redesenhar": {
        "nome": "Ver e redesenhar",
        "faz": "Olha o esquema do processo, fecha a página e redesenha de memória; depois compara e corrige.",
        "jeito": ["visual"],
        "porque": "Desenhar de memória obriga a lembrar as etapas na ordem, não só a reconhecê-las.",
    },
    "explicar-falando": {
        "nome": "Explicar em voz alta",
        "faz": "Explica o objetivo para quem ensina (ou para o celular) com as próprias palavras, sem ler.",
        "jeito": ["falado"],
        "porque": "Onde a explicação trava é exatamente o ponto que ainda não entrou.",
    },
    "vida-real": {
        "nome": "Exemplo da vida real",
        "faz": "Liga cada etapa a uma cena do dia a dia e conta a cena antes de responder.",
        "jeito": ["vida-real"],
        "porque": "Uma cena conhecida vira gancho para lembrar a parte abstrata.",
    },
    "pratica-sem-consulta": {
        "nome": "Questões sem consultar",
        "faz": "Responde as questões do objetivo sem olhar nada; só depois confere e lê a explicação do erro.",
        "jeito": ["escrita", "visual", "falado", "vida-real"],
        "porque": "Tentar lembrar (prática de recuperação) fixa mais do que reler.",
    },
    "releitura": {
        "nome": "Reler e grifar (controle)",
        "faz": "Relê a matéria e grifa o importante, do jeito de sempre.",
        "jeito": ["escrita"],
        "porque": "É o jeito de sempre; serve de comparação para ver se os outros fazem diferença.",
    },
}

JEITOS = {
    "visual": "aprende vendo: esquema, cor, desenho",
    "falado": "aprende ouvindo e falando: conversa, explicação",
    "vida-real": "aprende com exemplo concreto do dia a dia",
    "escrita": "aprende lendo e escrevendo, repetindo",
}


def candidatos(jeito: list) -> list:
    """Métodos que combinam com o jeito do aluno, mais o controle (releitura), sempre em ordem fixa."""
    jeito = set(jeito or [])
    nomes = [m for m, d in METODOS.items() if jeito & set(d["jeito"]) and m != "releitura"]
    if not nomes:
        nomes = ["pratica-sem-consulta"]
    return nomes + ["releitura"]
