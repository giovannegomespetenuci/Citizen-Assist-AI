import os
import re
import sys
from datetime import datetime

from assistente import Assistente
from base_conhecimento import BaseConhecimento
from orientacao import Orientacao


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODOS_ACESSIBILIDADE = {
    "1": ("dinamico", "Modo Dinâmico (Objetivo, bullet points)"),
    "2": ("guiado", "Modo Guiado (Acolhedor, sem jargões, dicas visuais)"),
    "3": ("focado", "Modo Focado (Paginado, um passo por tela)"),
    "4": ("voz", "Modo 100% Voz (Cadenciado para leitores de tela)"),
}

NOMES_MODOS = {
    "dinamico": "Modo Dinâmico",
    "guiado": "Modo Guiado",
    "focado": "Modo Focado",
    "voz": "Modo 100% Voz",
}


def selecionar_perfil():
    print("\n" + "=" * 65)
    print("--- SELEÇÃO DE PERFIL DE ACESSIBILIDADE (ideia.pdf) ---")
    print("=" * 65)
    print(" 1. Modo Dinâmico - Respostas objetivas em tópicos")
    print(" 2. Modo Guiado - Explicações acolhedoras com dicas visuais")
    print(" 3. Modo Focado - Instruções passo a passo (uma tela por vez)")
    print(" 4. Modo 100% Voz - Leitura cadenciada para leitores de tela")

    while True:
        opcao = input(
            "\nEscolha a opção (1-4) [Padrão: 1]: "
        ).strip()
        if not opcao:
            return "dinamico"
        if opcao in MODOS_ACESSIBILIDADE:
            modo_chave, _ = MODOS_ACESSIBILIDADE[opcao]
            return modo_chave
        print("[AVISO] Opção inválida. Digite um número de 1 a 4.")


def validar_data(data_texto):
    """Valida o formato AAAA-MM-DD."""
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", data_texto))


def ler_campo_validado(prompt, validacao_fn, msg_erro):
    """Lê um campo novamente enquanto o valor não passar na validação."""
    while True:
        valor = input(prompt).strip()
        if validacao_fn(valor):
            return valor
        print(f"[ERRO] {msg_erro}")


def menu_crud_dsa(base):
    while True:
        print("\n" + "=" * 65)
        print("--- GESTÃO DE REGISTROS DA BASE DE DADOS (DSA) ---")
        print("=" * 65)
        print(" 1. Listar todas as orientações")
        print(" 2. Consultar orientação por ID")
        print(" 3. Cadastrar nova orientação (com validação estrita)")
        print(" 4. Atualizar orientação por ID (edição completa)")
        print(" 5. Excluir orientação por ID (com confirmação)")
        print(" 6. Pesquisar por atributo (insensível a acentos)")
        print(" 7. Ordenar lista encadeada (por ID ou por título)")
        print(" 0. Voltar ao menu principal")

        opcao = input("\nSelecione a opção desejada: ").strip()
        if opcao == "0":
            break
        elif opcao == "1":
            todos = base.orientacoes.listar_todos()
            print(f"\n--- LISTAGEM GERAL ({len(todos)} itens) ---")
            if not todos:
                print("[INFO] A lista encadeada está vazia.")
            else:
                for item in todos:
                    print(
                        f" - ID {item.id} | [{item.categoria}] {item.titulo} "
                        f"(Público: {item.publico_alvo})"
                    )
        elif opcao == "2":
            id_texto = ler_campo_validado(
                "Digite o ID (inteiro positivo): ",
                lambda valor: valor.isdigit() and int(valor) > 0,
                "ID inválido.",
            )
            orientacao = base.orientacoes.buscar_por_id(int(id_texto))
            if orientacao:
                orientacao.exibir(modo="dinamico")
            else:
                print(f"[ERRO] Registro com ID {id_texto} não encontrado.")
        elif opcao == "3":
            print("\n--- CADASTRO DE NOVA ORIENTAÇÃO ---")
            id_texto = ler_campo_validado(
                "ID (inteiro positivo único): ",
                lambda valor: (
                    valor.isdigit()
                    and int(valor) > 0
                    and base.orientacoes.buscar_por_id(int(valor)) is None
                ),
                "ID deve ser inteiro positivo e não duplicado.",
            )
            categoria = ler_campo_validado(
                "Categoria: ",
                lambda valor: len(valor) > 0,
                "Categoria não pode ser vazia.",
            )
            titulo = ler_campo_validado(
                "Título: ",
                lambda valor: len(valor) > 0,
                "Título não pode ser vazio.",
            )
            publico_alvo = ler_campo_validado(
                "Público-Alvo (Requisito DSA): ",
                lambda valor: len(valor) > 0,
                "Público-alvo não pode ser vazio.",
            )
            palavras_texto = ler_campo_validado(
                "Palavras-chave (mínimo 3, separadas por vírgula): ",
                lambda valor: len(
                    [
                        palavra.strip()
                        for palavra in valor.split(",")
                        if palavra.strip()
                    ]
                )
                >= 3,
                "Informe pelo menos 3 palavras-chave válidas.",
            )
            palavras_chave = [
                palavra.strip()
                for palavra in palavras_texto.split(",")
                if palavra.strip()
            ]
            resposta = ler_campo_validado(
                "Resposta/Descrição: ",
                lambda valor: len(valor) > 0,
                "Resposta não pode ser vazia.",
            )
            documentos_texto = ler_campo_validado(
                "Documentos (separados por vírgula): ",
                lambda valor: len(valor) > 0,
                "Documentos não podem ser vazios.",
            )
            documentos = [
                documento.strip()
                for documento in documentos_texto.split(",")
                if documento.strip()
            ]
            onde = ler_campo_validado(
                "Local/Canal de Atendimento: ",
                lambda valor: len(valor) > 0,
                "Local não pode ser vazio.",
            )
            fonte = ler_campo_validado(
                "Fonte Oficial (http/https): ",
                lambda valor: valor.startswith("http://")
                or valor.startswith("https://"),
                "Informe uma URL válida com http:// ou https://.",
            )
            data_verificacao = datetime.now().strftime("%Y-%m-%d")
            nova_orientacao = Orientacao(
                int(id_texto),
                categoria,
                titulo,
                publico_alvo,
                palavras_chave,
                resposta,
                documentos,
                onde,
                fonte,
                data_verificacao,
            )
            base.orientacoes.inserir(nova_orientacao)
            base.salvar()
            print(
                f"\n[SUCESSO] Orientação ID {id_texto} cadastrada "
                "e salva com sucesso!"
            )
        elif opcao == "4":
            id_texto = ler_campo_validado(
                "Digite o ID a atualizar: ",
                lambda valor: valor.isdigit() and int(valor) > 0,
                "ID inválido.",
            )
            orientacao_atual = base.orientacoes.buscar_por_id(int(id_texto))
            if not orientacao_atual:
                print(
                    f"[ERRO] Orientação ID {id_texto} não foi encontrada."
                )
                continue

            print(
                f"\nAtualizando ID {orientacao_atual.id} "
                "(Deixe em branco para manter o valor atual):"
            )
            novo_titulo = (
                input(f"Novo Título [{orientacao_atual.titulo}]: ").strip()
                or orientacao_atual.titulo
            )
            nova_categoria = (
                input(f"Nova Categoria [{orientacao_atual.categoria}]: ").strip()
                or orientacao_atual.categoria
            )
            novo_publico = (
                input(
                    f"Novo Público-Alvo [{orientacao_atual.publico_alvo}]: "
                ).strip()
                or orientacao_atual.publico_alvo
            )
            palavras_texto = input(
                "Novas Palavras-chave "
                f"[{', '.join(orientacao_atual.palavras_chave)}]: "
            ).strip()
            novas_palavras = (
                [
                    palavra.strip()
                    for palavra in palavras_texto.split(",")
                    if palavra.strip()
                ]
                if palavras_texto
                else orientacao_atual.palavras_chave
            )
            nova_resposta = (
                input(f"Nova Resposta [{orientacao_atual.resposta}]: ").strip()
                or orientacao_atual.resposta
            )
            documentos_texto = input(
                f"Novos Documentos [{', '.join(orientacao_atual.documentos)}]: "
            ).strip()
            novos_documentos = (
                [
                    documento.strip()
                    for documento in documentos_texto.split(",")
                    if documento.strip()
                ]
                if documentos_texto
                else orientacao_atual.documentos
            )
            novo_local = (
                input(f"Novo Local [{orientacao_atual.onde}]: ").strip()
                or orientacao_atual.onde
            )
            nova_fonte = (
                input(f"Nova Fonte [{orientacao_atual.fonte}]: ").strip()
                or orientacao_atual.fonte
            )
            data_atualizacao = datetime.now().strftime("%Y-%m-%d")
            nova_orientacao = Orientacao(
                orientacao_atual.id,
                nova_categoria,
                novo_titulo,
                novo_publico,
                novas_palavras,
                nova_resposta,
                novos_documentos,
                novo_local,
                nova_fonte,
                data_atualizacao,
            )
            base.orientacoes.atualizar_por_id(
                orientacao_atual.id,
                nova_orientacao,
            )
            base.salvar()
            print(
                f"\n[SUCESSO] Orientação ID {orientacao_atual.id} "
                "atualizada com sucesso na Lista Encadeada!"
            )
        elif opcao == "5":
            id_texto = ler_campo_validado(
                "Digite o ID a excluir: ",
                lambda valor: valor.isdigit() and int(valor) > 0,
                "ID inválido.",
            )
            orientacao = base.orientacoes.buscar_por_id(int(id_texto))
            if not orientacao:
                print(f"[ERRO] ID {id_texto} não encontrado.")
                continue

            confirma = input(
                f"Tem certeza que deseja excluir '{orientacao.titulo}' "
                f"(ID {orientacao.id})? (s/n): "
            ).strip().lower()
            if confirma in ["s", "sim"]:
                if base.orientacoes.remover_por_id(int(id_texto)):
                    base.salvar()
                    print(
                        f"\n[SUCESSO] Registro ID {id_texto} removido "
                        "da Lista Encadeada!"
                    )
            else:
                print("[INFO] Operação de exclusão cancelada.")
        elif opcao == "6":
            termo = input(
                "\nDigite o termo de busca (sem restrição de acentos): "
            ).strip()
            if not termo:
                print("[AVISO] O termo de pesquisa não pode ser vazio.")
                continue
            encontrados = base.orientacoes.pesquisar(termo)
            print(
                f"\n--- RESULTADOS DA PESQUISA POR '{termo}' "
                f"({len(encontrados)} encontrados) ---"
            )
            for item in encontrados:
                print(
                    f" - ID {item.id} | [{item.categoria}] {item.titulo} "
                    f"(Público: {item.publico_alvo})"
                )
        elif opcao == "7":
            if base.orientacoes.esta_vazia():
                print("\n[INFO] A lista encadeada está vazia, nada a ordenar.")
                continue
            print(
                "\nOrdenar por:\n"
                " 1. ID (Crescente)\n"
                " 2. Título (Alfabética)"
            )
            sub_opcao = input("Opção: ").strip()
            if sub_opcao == "1":
                base.orientacoes.ordenar_por_id()
                base.salvar()
                print("\n[SUCESSO] Lista encadeada ordenada por ID!")
            elif sub_opcao == "2":
                base.orientacoes.ordenar_por_titulo()
                base.salvar()
                print("\n[SUCESSO] Lista encadeada ordenada por Título!")
            else:
                print("[AVISO] Opção inválida.")
        else:
            print("[AVISO] Opção inválida. Escolha um número do menu.")


def main():
    print("=" * 65)
    print("CITIZEN ASSIST AI - ASSISTENTE DIGITAL DE ORIENTAÇÃO")
    print("=" * 65)

    caminho_json = os.path.join(BASE_DIR, "data", "base_conhecimento.json")
    base = BaseConhecimento(caminho_json)
    base.carregar()
    assistente = Assistente("Citizen Assist AI", base)
    modo_ativo = selecionar_perfil()

    while True:
        nome_exibicao = NOMES_MODOS.get(modo_ativo, modo_ativo.upper())
        print("\n" + "=" * 65)
        print(f"--- MENU PRINCIPAL | PERFIL ATIVO: {nome_exibicao.upper()} ---")
        print("=" * 65)
        print(" 1. Fazer pergunta ao assistente (Texto livre)")
        print(" 2. Navegar por categorias de serviços")
        print(" 3. Gestão de registros e operações CRUD (DSA)")
        print(" 4. Alternar Perfil de Acessibilidade (ideia.pdf)")
        print(" 5. Ver indicadores de atendimento (PCP)")
        print(" 6. Exportar relatório completo para CSV")
        print(" 0. Sair do sistema")

        opcao = input("\nDigite a opção desejada: ").strip()
        if opcao == "1":
            assistente.perguntar(modo=modo_ativo)
        elif opcao == "2":
            assistente.navegar(modo=modo_ativo)
        elif opcao == "3":
            menu_crud_dsa(base)
        elif opcao == "4":
            modo_ativo = selecionar_perfil()
        elif opcao == "5":
            assistente.indicadores()
        elif opcao == "6":
            assistente.exportar_csv()
        elif opcao == "0":
            print("\n--- AVALIAÇÃO DE EXPERIÊNCIA ---")
            while True:
                nota_texto = input(
                    "Em uma escala de 1 a 5, quão fácil foi utilizar "
                    "o assistente?: "
                ).strip()
                if nota_texto.isdigit() and 1 <= int(nota_texto) <= 5:
                    nota = int(nota_texto)
                    assistente.registrar_avaliacao(nota)
                    print(
                        f"[OBRIGADO] Sua avaliação ({nota}/5) "
                        "foi registrada com sucesso!"
                    )
                    break
                print("[AVISO] Digite uma nota válida entre 1 e 5.")

            assistente.exportar_csv()
            print("\n[INFO] Aplicação encerrada com sucesso. Até logo!\n")
            sys.exit(0)
        else:
            print("[AVISO] Opção inválida. Digite um número de 0 a 6.")


if __name__ == "__main__":
    main()
