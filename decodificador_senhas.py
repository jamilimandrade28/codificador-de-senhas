"""Codificador/decodificador de senhas representadas por formas geométricas.

A senha deve ter exatamente seis caracteres. Como as formas são sorteadas,
a chave gerada durante a codificação é necessária para decodificar o código.
"""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass
from enum import Enum


class Forma(str, Enum):
    CIRCULO = "●"
    QUADRADO = "■"
    TRIANGULO = "▲"
    DIAMANTE = "◆"
    HEXAGONO = "⬡"
    ESTRELA = "★"


CARACTERES_VALIDOS = string.ascii_letters + string.digits + string.punctuation
TAMANHO_SENHA = 6


@dataclass(frozen=True)
class Desafio:
    """Código visível e chave necessária para recuperar a senha."""

    codigo: str
    chave: str


class DecodificadorSenhas:
    """Cria e decodifica códigos de seis formas geométricas."""

    def __init__(self) -> None:
        self._aleatorio = secrets.SystemRandom()

    @staticmethod
    def _validar_senha(senha: str) -> None:
        if len(senha) != TAMANHO_SENHA:
            raise ValueError("A senha deve ter exatamente 6 caracteres.")
        if any(caractere not in CARACTERES_VALIDOS for caractere in senha):
            raise ValueError("A senha contém caracteres não suportados.")

    @staticmethod
    def _validar_codigo(codigo: str) -> None:
        if len(codigo) != TAMANHO_SENHA:
            raise ValueError("O código deve ter exatamente 6 formas.")
        formas = {forma.value for forma in Forma}
        if any(forma not in formas for forma in codigo):
            raise ValueError("O código contém uma forma geométrica inválida.")

    def codificar(self, senha: str) -> Desafio:
        """Codifica uma senha e retorna o código junto com sua chave."""
        self._validar_senha(senha)

        # Uma forma é atribuída a cada caractere diferente da senha.
        caracteres = list(dict.fromkeys(senha))
        formas = list(Forma)
        self._aleatorio.shuffle(formas)
        mapa = dict(zip(caracteres, formas))

        codigo = "".join(mapa[caractere].value for caractere in senha)
        # A chave é independente da ordem da senha e pode ser armazenada.
        chave = ";".join(
            f"{forma.value}:{caractere}"
            for caractere, forma in sorted(mapa.items(), key=lambda item: item[1].value)
        )
        return Desafio(codigo=codigo, chave=chave)

    def decodificar(self, codigo: str, chave: str) -> str:
        """Decodifica um código usando a chave retornada por ``codificar``."""
        self._validar_codigo(codigo)
        if not chave.strip():
            raise ValueError("A chave é obrigatória para decodificar o código.")

        mapa: dict[str, str] = {}
        for item in chave.split(";"):
            try:
                forma, caractere = item.split(":", 1)
            except ValueError as erro:
                raise ValueError("Formato de chave inválido.") from erro

            if forma not in {forma_enum.value for forma_enum in Forma}:
                raise ValueError(f"Forma inválida na chave: {forma}")
            if len(caractere) != 1 or caractere not in CARACTERES_VALIDOS:
                raise ValueError("A chave contém um caractere inválido.")
            if forma in mapa or caractere in mapa.values():
                raise ValueError("A chave contém formas ou caracteres repetidos.")
            mapa[forma] = caractere

        try:
            senha = "".join(mapa[forma] for forma in codigo)
        except KeyError as erro:
            raise ValueError("A chave não corresponde a todas as formas do código.") from erro

        self._validar_senha(senha)
        return senha


if __name__ == "__main__":
    decodificador = DecodificadorSenhas()
    senha = input("Digite uma senha de 6 caracteres: ")

    try:
        desafio = decodificador.codificar(senha)
        print(f"\nCódigo: {desafio.codigo}")
        print(f"Chave:  {desafio.chave}")
        print(f"Senha recuperada: {decodificador.decodificar(desafio.codigo, desafio.chave)}")
    except ValueError as erro:
        print(f"Erro: {erro}")
