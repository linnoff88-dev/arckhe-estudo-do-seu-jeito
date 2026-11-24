# estudo-do-seu-jeito

[![Estudio a tu manera](guia/assets/banner-es.jpg)](https://linnoff88-dev.github.io/

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

**Enséñale a tu hijo (o a tu estudiante) de la manera en que aprende, incluso si no dominas la materia.**

## Qué es

Cuando tu hijo (o tu estudiante) empieza a tener dificultades, quienes quieren ayudar suelen no conocer la materia ni la manera correcta de explicarla. **Estudio a tu manera** es un kit gratuito con una fórmula de 8 pasos. La IA primero te enseña a ti y luego prepara una guía de estudio adaptada a la manera de aprender del estudiante, con esquemas, ejemplos de la vida real y preguntas basadas únicamente en el material de clase. También ayuda a probar, sin ocultar nada, qué manera de estudiar funciona para él. Para usarlo, basta con un chat de IA. Para ir más allá, usa Claude Code o Codex.

📖 Guía (página de presentación + paso a paso): **https://linnoff88-dev.github.io/ ·  
🧪 Ejemplo de la app del estudiante: **https://linnoff88-dev.github.io/ (el ejemplo está en portugués)

## Cómo empezar (copia esto en tu IA)

```text
Lee el kit "Estudio a tu manera" en https://github.com/linnoff88-dev/estudo-do-seu-jeito (el README explica la fórmula de 8 pasos y las instrucciones listas para usar).
Quiero preparar una guía de estudio para [quién], que está en [materia y nivel]. Voy a adjuntar el material: apuntes, guía del profesor, el último examen.
1. Todavía no construyas nada. Primero pregúntame qué necesitas saber: cómo evalúa el profesor, cómo aprende [quién] y qué errores cometió.
2. Dame 2 o 3 opciones para organizar la guía, con los pros y los contras de cada una.
3. Regla fija: todo el contenido y todas las preguntas deben salir únicamente del material que te envíe, e incluir la frase que demuestra la respuesta. Si falta algo, pregúntame.
4. Cuando elija, muéstrame un resumen del plan y espera a que te dé el visto bueno.
```

## La historia que dio origen a la fórmula

Lúcia es madre de cuatro hijos y desde hace 21 años tiene una agencia de marketing con su esposo, en su casa. Su hija mayor, Clara, se fue a estudiar biología marina a una universidad que queda a cinco horas de casa. Clara, que siempre sacaba las mejores notas, empezó a tener dificultades en una materia que le gustaba: mucho contenido en poco tiempo, clases con diapositivas llenas de texto y la regla del profesor de que **fallar una pregunta de un objetivo de aprendizaje significa perder todo el objetivo**.

A Clara no le gustaba la IA. Lúcia no es programadora. Aun así, Lúcia estudió de dos a tres horas al día con Claude para poder enseñarle a su hija, y después preparó una guía de estudio adaptada a la manera de aprender de Clara, que es visual: esquemas para volver a dibujar, ejemplos de la vida real, trampas, preguntas y hojas de resumen para imprimir. La primera versión estuvo lista en un día, con una instrucción de cuatro frases en el chat; después Lúcia pasó a Claude Code para agregar partes interactivas. Cada semana Clara enviaba fotos de sus apuntes, y la guía se actualizaba y se verificaba con el libro. La nota subió más de 10 puntos, de una D alta a casi 80. Todos los objetivos que Clara había perdido en el examen 2 los respondió correctamente en el examen 3.

(Nombres de los personajes cambiados. Las cifras anteriores pertenecen a la historia; **este kit no las midió**. El ejemplo incluido en el kit usa datos inventados.)

## La fórmula en 8 pasos

| # | Paso | En el kit |
|---|---|---|
| 1 | **Quien enseña aprende primero**: estudia el tema en el que el estudiante se equivocó, con la IA explicándolo a partir de la fuente | `estudo tutor`, instrucción 4 |
| 2 | **Entender cómo evalúa el profesor**: qué hace que se pierdan puntos | `professor` en materia.json |
| 3 | **Entender cómo aprende el estudiante**: de forma visual, oral, con ejemplos de la vida real o por escrito | `aluno.jeito` |
| 4 | **Partir de lo que ya respondió mal** | `estudo resultado --origem prova` |
| 5 | **Planear antes de construir**: la IA pregunta lo que no sabe, da opciones y las resume en un plan | instrucciones 1 y 2 → `plano.md` |
| 6 | **Guía por objetivo, solo con lo que está en la fuente**: lectura, recursos visuales, vida real, trampas, preguntas | `estudo adicionar` (rechaza preguntas sin evidencia), `estudo guia` |
| 7 | **Cada semana: material nuevo y verificación** | `estudo semana`, instrucción 5, `estudo respostas` |
| 8 | **Pasar la posta**: el estudiante empieza a usarlo por su cuenta | guia.html → `estudo importar`, instrucción 8 |

`python3 -m estudo passos` muestra el estado de cada paso, calculado a partir de tus datos.

## La prueba de los métodos, a la vista

Nadie sabe de antemano qué método funciona para cada estudiante. El kit los prueba y muestra todo:

1. Antes de estudiar un objetivo, se elige el método y **se anota en el diario junto con el motivo** (`estudo proximo --anotar`). El kit alterna entre los métodos que se ajustan a la manera de aprender del estudiante y un método de control (volver a leer y subrayar), para que la prueba sea justa.
2. El resultado se cuenta para el último método anotado para ese objetivo.
3. «Dominado» sigue la regla del profesor (responder todo correctamente, si así califica).
4. Con menos de 3 objetivos, el método aparece como **«poco dato» (pocos datos)** y nunca como el mejor. Para decir que uno va adelante, hacen falta dos métodos con datos y una diferencia de 20 puntos.
5. El diario (`diario.jsonl`) solo recibe líneas nuevas; nunca borra nada. `estudo diario` muestra todo.

Métodos: observar y volver a dibujar · explicar en voz alta · ejemplo de la vida real · responder preguntas sin consultar · volver a leer y subrayar (control).

## Quién escribe y quién verifica

**El kit no lee fotos ni escribe contenido.** Quien transcribe los apuntes y escribe los objetivos y las preguntas eres tú o la IA (chat, Claude Code, Codex o el cerebro de tu Jarvis). El kit **organiza, verifica y registra**:

- cada pregunta indica de qué fuente proviene y copia el fragmento; el kit busca ese fragmento en el texto de la fuente y **rechaza** la pregunta si no lo encuentra (sin distinguir entre tildes ni mayúsculas);
- señala las respuestas del estudiante que no coinciden con la fuente antes de que se conviertan en material de estudio;
- la IA no inventa preguntas adicionales: si faltan preguntas, falta la fuente.

## Cuatro maneras de usarlo

| Manera | Para quién | Cómo |
|---|---|---|
| **Chat** (cualquier IA) | quien no quiere instalar nada | `python3 -m estudo prompts --idioma es` (8 instrucciones, PT/EN/ES) o copia desde `estudo/prompts/` |
| **App visual** | el estudiante | `guia.html`: se abre en el celular o la computadora, sin internet |
| **Claude Code / Codex** | quien enseña y quiere que el agente haga el trabajo | skill en `skill/estudo-do-seu-jeito/` |
| **Jarvis (INTELECTO v2)** | quien ya tiene el asistente | plugin `estudo`: 6 herramientas |

---

## Instalación técnica

### En 1 minuto

Necesitas Python 3.10 o una versión posterior. No hace falta instalar ningún paquete.

```bash
git clone https://github.com/linnoff88-dev/estudo-do-seu-jeito && cd estudo-do-seu-jeito
python3 -m estudo demo --pasta ~/estudo-demo     # ejemplo con datos inventados
# abre ~/estudo-demo/guia.html en el navegador
python3 -m estudo placar --pasta ~/estudo-demo
```

Para tu materia (los datos quedan en `~/.estudo-do-seu-jeito`, fuera del repositorio):

```bash
python3 -m estudo nova "Biologia"
python3 -m estudo prompts 1                       # planear en el chat
python3 -m estudo semana anotacoes-aula-5.txt     # fuente de la semana
python3 -m estudo adicionar objetivos.json        # rechaza preguntas sin evidencia en la fuente
python3 -m estudo proximo --anotar                # método de cada objetivo, con el motivo
python3 -m estudo guia                            # ~/.estudo-do-seu-jeito/guia.html
python3 -m estudo importar resultados.json        # lo que hizo el estudiante en la app
python3 -m estudo plano-prova --data 2026-12-05
```

Cualquier comando acepta `--json` (para agentes) y `--pasta` (una carpeta por materia).

### Skill en Claude Code

```bash
mkdir -p ~/.claude/skills && cp -r skill/estudo-do-seu-jeito ~/.claude/skills/
```

Después, dentro de la carpeta del kit: «usa la skill estudo-do-seu-jeito y ayúdame a preparar la guía de mi hija».  
Sin la skill, funciona pegando la instrucción 3 (`python3 -m estudo prompts 3`). En Codex: pídele que lea `skill/estudo-do-seu-jeito/SKILL.md` y siga sus instrucciones.

### Plugin de INTELECTO v2 (tu Jarvis)

```bash
pip install git+https://github.com/linnoff88-dev/estudo-do-seu-jeito
INTELECTO_PLUGINS=estudo ESTUDO_PASTA=~/.estudo-do-seu-jeito python3 -m intelecto
```

Herramientas: `estudo_passos`, `estudo_placar`, `estudo_proximo_metodo`, `estudo_registrar_resultado`, `estudo_conferir`, `estudo_plano_prova`. Ninguna ejecuta comandos ni lee fuera de la carpeta de la materia; las que escriben solo agregan líneas al diario. Por Telegram, el estudiante puede escribir «hice 3 de 3 en respiración» y preguntar «¿qué método está funcionando?».

### Cómo está organizado

| Archivo | Qué hace |
|---|---|
| `estudo/dados.py` | carpeta de la materia, materia.json, fuentes, diario (solo agrega) |
| `estudo/verificador.py` | verifica fragmentos en la fuente, opciones, respuestas del estudiante |
| `estudo/experimento.py` | resultados de los métodos, elección del siguiente con el motivo |
| `estudo/formula.py` | los 8 pasos y el estado de cada uno |
| `estudo/plano.py` | plan día a día hasta el examen |
| `estudo/guia_html.py` | la app del estudiante (un único archivo HTML) |
| `estudo/ferramentas.py`, `intelecto_plugin.py` | herramientas para agentes y el plugin de Jarvis |
| `estudo/prompts/{pt,en,es}/` | las 8 instrucciones para el chat |
| `estudo/exemplo/` | la materia de ejemplo (biología, datos inventados) |

Pruebas: `python3 -m pytest -q testes` (42 pruebas: verificación con la fuente, regla de todo el objetivo, resultados con muestras pequeñas, plan sin objetivos olvidados, importación de la app, plugin de INTELECTO y ausencia de una fuente de inspiración en el repositorio).

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Planear en el chat y cerrar el resumen en `plano.md` | `python3 -m estudo prompts 1` y `prompts 2` | 🧠 tú + IA |
| 2 | Crear la materia y completar los datos del profesor y del estudiante | `python3 -m estudo nova "Biologia"` | ⚙️ kit |
| 3 | Quien enseña estudia el punto débil | `python3 -m estudo prompts 4` → `python3 -m estudo tutor --objetivo <id> --minutos 60` | 🧠 tú + IA |
| 4 | Transcribir las fotos de la semana a `fontes/` | `python3 -m estudo prompts 5` → `python3 -m estudo semana aula-5.txt` | 🤖 IA |
| 5 | Objetivos y preguntas con el fragmento de la fuente | `python3 -m estudo adicionar objetivos.json` | 🤖 IA + ⚙️ el kit verifica |
| 6 | Método para cada objetivo, con el motivo | `python3 -m estudo proximo --anotar` | ⚙️ kit |
| 7 | Generar la app del estudiante | `python3 -m estudo guia` | ⚙️ kit |
| 8 | El estudiante estudia y exporta el resultado | `guia.html` → `python3 -m estudo importar resultados.json` | 🧠 estudiante |
| 9 | Ver los resultados y el plan hasta el examen | `python3 -m estudo placar` · `plano-prova --data AAAA-MM-DD` | ⚙️ kit |
| 10 | Verificar las respuestas que completó el estudiante | `python3 -m estudo respostas respostas.json` | ⚙️ kit |

Cada semana se repiten los pasos del 4 al 10. `python3 -m estudo passos` muestra en qué punto estás.

## Límites de esta versión (v0.1)

- La interfaz (comandos y app) está en portugués; las instrucciones están en PT, EN y ES. Puedes usar el comando `prompts` con `--idioma es`.
- El kit no lee imágenes: tú o la IA transcriben las fotos (instrucción 5).
- La verificación encuentra el fragmento en la fuente, pero no garantiza que la fuente sea correcta ni que el fragmento demuestre la respuesta; si ninguna palabra de la respuesta aparece en el fragmento, lo advierte.
- Los resultados comparan objetivos diferentes, que tienen distintas dificultades: son una pista honesta, no un experimento científico.
- Los resultados de la app se guardan en el navegador hasta que los exportas e importas.

## Licencia

MIT.