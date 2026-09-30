import random
import string
from enum import Enum
from typing import Dict, List, Tuple

class Forma(Enum):
    """Formas geométricas disponíveis"""
    CIRCULO = "●"
    QUADRADO = "■"
    TRIANGULO = "▲"
    DIAMANTE = "◆"
    HEXAGONO = "⬡"
    ESTRELA = "★"

class DecodificadorSenhas:
    """
    Decodificador de senhas usando formas geométricas aleatórias.
    Cada caractere é mapeado para uma forma geométrica única.
    """
    
    def __init__(self):
        self.mapa_caracteres_formas: Dict[str, Forma] = {}
        self.mapa_formas_caracteres: Dict[Forma, str] = {}
        self.formas_disponiveis = list(Forma)
        self.caracteres_validos = string.ascii_letters + string.digits + string.punctuation
    
    def gerar_mapa_aleatorio(self, senha: str) -> Dict[str, Forma]:
        """
        Gera um mapa aleatório de caracteres para formas geométricas.
        
        Args:
            senha: Senha a ser decodificada (6 caracteres)
            
        Returns:
            Dicionário mapeando caracteres para formas
        """
        if len(senha) != 6:
            raise ValueError("A senha deve ter exatamente 6 caracteres!")
        
        # Limpar mapas anteriores
        self.mapa_caracteres_formas.clear()
        self.mapa_formas_caracteres.clear()
        
        # Caracteres únicos na senha
        caracteres_unicos = list(set(senha))
        
        # Embaralhar formas disponíveis
        formas_selecionadas = random.sample(self.formas_disponiveis, len(caracteres_unicos))
        
        # Criar mapa
        for char, forma in zip(caracteres_unicos, formas_selecionadas):
            self.mapa_caracteres_formas[char] = forma
            self.mapa_formas_caracteres[forma] = char
        
        return self.mapa_caracteres_formas
    
    def codificar(self, senha: str) -> str:
        """
        Codifica uma senha em formas geométricas.
        
        Args:
            senha: Senha a ser codificada (6 caracteres)
            
        Returns:
            String com formas geométricas
        """
        if len(senha) != 6:
            raise ValueError("A senha deve ter exatamente 6 caracteres!")
        
        self.gerar_mapa_aleatorio(senha)
        
        # Converter cada caractere em sua forma
        senha_codificada = ''.join(
            self.mapa_caracteres_formas[char].value for char in senha
        )
        
        return senha_codificada
    
    def decodificar(self, senha_codificada: str) -> Tuple[str, Dict]:
        """
        Tenta decodificar uma senha codificada em formas geométricas.
        Usa análise de frequência e força bruta para encontrar a senha original.
        
        Args:
            senha_codificada: Senha em formas geométricas
            
        Returns:
            Tupla contendo (senha_original, mapa_usado)
        """
        if len(senha_codificada) != 6:
            raise ValueError("A senha codificada deve ter 6 formas geométricas!")
        
        formas = list(senha_codificada)
        formas_unicas = list(set(formas))
        
        if len(formas_unicas) > len(self.formas_disponiveis):
            raise ValueError("Número de formas inválido!")
        
        # Mapear formas encontradas
        formas_enum = []
        for forma_str in formas:
            for forma in Forma:
                if forma.value == forma_str:
                    formas_enum.append(forma)
                    break
        
        # Tentar combinações possíveis
        caracteres_candidatos = string.ascii_lowercase + string.digits
        formas_unicas_enum = list(set(formas_enum))
        
        # Gerar todas as permutações possíveis
        from itertools import permutations
        
        for perm in permutations(caracteres_candidatos, len(formas_unicas_enum)):
            # Criar mapa de teste
            mapa_teste = dict(zip(formas_unicas_enum, perm))
            
            # Testar se produz uma senha válida
            senha_testada = ''.join(mapa_teste.get(f) for f in formas_enum)
            
            # Retornar primeiro resultado válido
            if self._eh_senha_valida(senha_testada):
                return senha_testada, {forma.value: char for forma, char in mapa_teste.items()}
        
        return None, {}
    
    def _eh_senha_valida(self, senha: str) -> bool:
        """
        Valida se uma senha parece ser válida (critério simples).
        Pode ser expandido com regras mais complexas.
        """
        # Critério básico: contém pelo menos um caractere válido
        return len(senha) == 6 and all(c in self.caracteres_validos for c in senha)
    
    def exibir_mapa(self) -> None:
        """Exibe o mapa atual de caracteres para formas."""
        print("\n📊 Mapa de Caracteres para Formas:")
        print("-" * 40)
        for char, forma in sorted(self.mapa_caracteres_formas.items()):
            print(f"  {char} → {forma.value} ({forma.name})")
        print("-" * 40)
    
    def criar_desafio(self, senha: str) -> Tuple[str, Dict]:
        """
        Cria um desafio de decodificação.
        
        Args:
            senha: Senha a ser ocultada (6 caracteres)
            
        Returns:
            Tupla contendo (senha_codificada, mapa_para_referencia)
        """
        senha_codificada = self.codificar(senha)
        return senha_codificada, dict(self.mapa_caracteres_formas)


# Exemplo de uso
if __name__ == "__main__":
    print("🔐 Decodificador de Senhas com Formas Geométricas\n")
    
    decodificador = DecodificadorSenhas()
    
    # Teste 1: Codificar uma senha
    print("=" * 50)
    print("TESTE 1: Codificar uma senha")
    print("=" * 50)
    
    senha_original = "abc123"
    print(f"Senha original: {senha_original}")
    
    senha_codificada, mapa = decodificador.criar_desafio(senha_original)
    print(f"\nSenha codificada: {senha_codificada}")
    decodificador.exibir_mapa()
    
    # Teste 2: Múltiplos exemplos
    print("\n" + "=" * 50)
    print("TESTE 2: Múltiplos exemplos de codificação")
    print("=" * 50)
    
    exemplos = ["senha1", "test42", "xyz789", "admin5", "pass99"]
    
    for ex_senha in exemplos:
        decodificador_temp = DecodificadorSenhas()
        ex_codificada, ex_mapa = decodificador_temp.criar_desafio(ex_senha)
        print(f"\n📝 Senha: {ex_senha}")
        print(f"   Codificada: {ex_codificada}")
        print(f"   Formas usadas: {len(ex_mapa)}")
    
    # Teste 3: Visualização de todas as formas disponíveis
    print("\n" + "=" * 50)
    print("TESTE 3: Formas geométricas disponíveis")
    print("=" * 50)
    
    for forma in Forma:
        print(f"  {forma.value} - {forma.name}")
