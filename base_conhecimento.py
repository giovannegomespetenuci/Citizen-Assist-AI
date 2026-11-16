import json
import os

from orientacao import Orientacao


ACENTOS = {
    "á": "a",
    "à": "a",
    "ã": "a",
    "â": "a",
    "é": "e",
    "ê": "e",
    "í": "i",
    "ó": "o",
    "õ": "o",
    "ô": "o",
    "ú": "u",
    "ç": "c",
}


def normalizar(texto):
    """
    Remove acentos, pontuação e converte para minúsculas.
    Retorna a string delimitada por espaços nas extremidades para busca
    por palavra inteira.
    """
    if not texto:
        return " "
    texto = str(texto).lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal in "?!.,;:()[]{}-_/\\":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class No:
    def __init__(self, conteudo):
        self.conteudo = conteudo
        self.proximo = None


class ListaEncadeada:
    """Implementação manual de lista encadeada para a disciplina de DSA."""

    def __init__(self):
        self.inicio = None
        self._tamanho = 0

    def __len__(self):
        return self._tamanho

    def esta_vazia(self):
        return self.inicio is None

    def inserir(self, orientacao):
        novo_no = No(orientacao)
        if self.esta_vazia():
            self.inicio = novo_no
        else:
            atual = self.inicio
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = novo_no
        self._tamanho += 1

    def listar_todos(self):
        elementos = []
        atual = self.inicio
        while atual is not None:
            elementos.append(atual.conteudo)
            atual = atual.proximo
        return elementos

    def buscar_por_id(self, id_orientacao):
        atual = self.inicio
        while atual is not None:
            if atual.conteudo.id == id_orientacao:
                return atual.conteudo
            atual = atual.proximo
        return None

    def atualizar_por_id(self, id_orientacao, nova_orientacao):
        """Atualiza um elemento da lista encadeada pelo identificador."""
        atual = self.inicio
        while atual is not None:
            if atual.conteudo.id == id_orientacao:
                atual.conteudo = nova_orientacao
                return True
            atual = atual.proximo
        return False

    def remover_por_id(self, id_orientacao):
        if self.esta_vazia():
            return False

        atual = self.inicio
        anterior = None
        while atual is not None:
            if atual.conteudo.id == id_orientacao:
                if anterior is None:
                    self.inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                self._tamanho -= 1
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def pesquisar(self, termo):
        """Pesquisa atributos ignorando acentos e maiúsculas."""
        termo_normalizado = normalizar(termo).strip()
        resultados = []
        atual = self.inicio
        while atual is not None:
            item = atual.conteudo
            titulo_normalizado = normalizar(item.titulo)
            categoria_normalizada = normalizar(item.categoria)
            publico_normalizado = normalizar(item.publico_alvo)
            if (
                termo_normalizado in titulo_normalizado
                or termo_normalizado in categoria_normalizada
                or termo_normalizado in publico_normalizado
            ):
                resultados.append(item)
            atual = atual.proximo
        return resultados

    def ordenar_por_id(self):
        if self.esta_vazia() or self.inicio.proximo is None:
            return

        trocou = True
        while trocou:
            trocou = False
            atual = self.inicio
            while atual.proximo is not None:
                if atual.conteudo.id > atual.proximo.conteudo.id:
                    atual.conteudo, atual.proximo.conteudo = (
                        atual.proximo.conteudo,
                        atual.conteudo,
                    )
                    trocou = True
                atual = atual.proximo

    def ordenar_por_titulo(self):
        if self.esta_vazia() or self.inicio.proximo is None:
            return

        trocou = True
        while trocou:
            trocou = False
            atual = self.inicio
            while atual.proximo is not None:
                titulo_atual = normalizar(atual.conteudo.titulo)
                titulo_seguinte = normalizar(atual.proximo.conteudo.titulo)
                if titulo_atual > titulo_seguinte:
                    atual.conteudo, atual.proximo.conteudo = (
                        atual.proximo.conteudo,
                        atual.conteudo,
                    )
                    trocou = True
                atual = atual.proximo


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = ListaEncadeada()

    def carregar(self):
        if not os.path.exists(self.caminho):
            print(
                f"[AVISO] Arquivo '{self.caminho}' não encontrado. "
                "Iniciando com base vazia."
            )
            self.orientacoes = ListaEncadeada()
            return False

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                print(
                    "[AVISO] Conteúdo do JSON não é uma lista. "
                    "Iniciando base vazia."
                )
                self.orientacoes = ListaEncadeada()
                return False

            self.orientacoes = ListaEncadeada()
            for item in dados:
                try:
                    orientacao = Orientacao(
                        id_orientacao=item["id"],
                        categoria=item["categoria"],
                        titulo=item["titulo"],
                        publico_alvo=item.get("publico_alvo", "Geral"),
                        palavras_chave=item["palavras_chave"],
                        resposta=item["resposta"],
                        documentos=item["documentos"],
                        onde=item["onde"],
                        fonte=item["fonte"],
                        verificado_em=item["verificado_em"],
                    )
                    self.orientacoes.inserir(orientacao)
                except KeyError as erro:
                    print(
                        "[AVISO] Registro omitido por ausência do campo "
                        f"obrigatório {erro}."
                    )

            print(
                "[INFO] Base carregada! Total de registros válidos: "
                f"{len(self.orientacoes)}"
            )
            return True
        except Exception as erro:
            print(
                f"[AVISO] Falha ao ler o arquivo JSON ({erro}). "
                "Base iniciada como vazia."
            )
            self.orientacoes = ListaEncadeada()
            return False

    def salvar(self):
        dados = []
        for item in self.orientacoes.listar_todos():
            dados.append(
                {
                    "id": item.id,
                    "categoria": item.categoria,
                    "titulo": item.titulo,
                    "publico_alvo": item.publico_alvo,
                    "palavras_chave": item.palavras_chave,
                    "resposta": item.resposta,
                    "documentos": item.documentos,
                    "onde": item.onde,
                    "fonte": item.fonte,
                    "verificado_em": item.verificado_em,
                }
            )

        try:
            pasta = os.path.dirname(self.caminho)
            if pasta:
                os.makedirs(pasta, exist_ok=True)
            with open(self.caminho, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            return True
        except Exception as erro:
            print(f"[ERRO] Falha ao salvar alterações no JSON: {erro}")
            return False

    def categorias(self):
        categorias = set()
        for item in self.orientacoes.listar_todos():
            categorias.add(item.categoria)
        return sorted(list(categorias))

    def por_categoria(self, categoria):
        categoria_normalizada = normalizar(categoria).strip()
        return [
            item
            for item in self.orientacoes.listar_todos()
            if normalizar(item.categoria).strip() == categoria_normalizada
        ]

    def pontuar(self, pergunta, orientacao):
        pergunta_normalizada = normalizar(pergunta)
        pontos = 0

        for palavra_chave in orientacao.palavras_chave:
            palavra_chave_normalizada = normalizar(palavra_chave)
            if palavra_chave_normalizada in pergunta_normalizada:
                pontos += 3

        palavras_pergunta_unicas = {
            palavra
            for palavra in pergunta_normalizada.split()
            if len(palavra) >= 4
        }
        palavras_titulo = set(normalizar(orientacao.titulo).split())
        for palavra in palavras_pergunta_unicas:
            if palavra in palavras_titulo:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        resultados = []
        for item in self.orientacoes.listar_todos():
            pontos = self.pontuar(pergunta, item)
            if pontos >= 3:
                resultados.append((pontos, item))

        n = len(resultados)
        for i in range(n):
            for j in range(0, n - i - 1):
                pontos_atual, orientacao_atual = resultados[j]
                pontos_seguinte, orientacao_seguinte = resultados[j + 1]
                if pontos_atual < pontos_seguinte:
                    resultados[j], resultados[j + 1] = (
                        resultados[j + 1],
                        resultados[j],
                    )
                elif (
                    pontos_atual == pontos_seguinte
                    and orientacao_atual.id > orientacao_seguinte.id
                ):
                    resultados[j], resultados[j + 1] = (
                        resultados[j + 1],
                        resultados[j],
                    )
        return resultados
