"""Plugin do INTELECTO v2: as ferramentas do kit viram ferramentas do seu Jarvis.

O intelecto acha este plugin pelo entry point `intelecto.plugins` (nome "estudo") e só carrega se você ligar:
  INTELECTO_PLUGINS=estudo   (ou "plugins": ["estudo"] no ~/.intelecto2/config.json)
A matéria é a de ESTUDO_PASTA (ou ~/.estudo-do-seu-jeito). Nenhuma ferramenta roda comando; as que gravam só
acrescentam linhas no diário da matéria.
"""
import asyncio

from .dados import ErroEstudo
from .ferramentas import FERRAMENTAS


def ferramentas(pecas=None):
    from intelecto.ferramentas.base import Ferramenta, Resultado  # só existe com o intelecto instalado

    def fabricar(spec):
        class F(Ferramenta):
            nome = spec["nome"]
            descricao = spec["descricao"]
            parametros = spec["parametros"]

            async def executar(self, **args):
                try:
                    return Resultado(True, await asyncio.to_thread(spec["funcao"], args))
                except (ErroEstudo, KeyError, ValueError) as e:
                    return Resultado(False, f"estudo: {e}")

        F.__name__ = "Estudo_" + spec["nome"]
        return F()

    return [fabricar(s) for s in FERRAMENTAS]
