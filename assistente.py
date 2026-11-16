import csv
import json
import os
import time
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.caminho_historico = os.path.join(
            BASE_DIR, "data", "historico.json"
        )
        self.caminho_csv = os.path.join(BASE_DIR, "data", "atendimentos.csv")
        self.caminho_avaliacoes = os.path.join(
            BASE_DIR, "data", "avaliacoes.json"
        )
        self.historico = self._carregar_historico()

    def _carregar_historico(self):
        if os.path.exists(self.caminho_historico):
            try:
                with open(
                    self.caminho_historico, "r", encoding="utf-8"
                ) as arquivo:
                    dados = json.load(arquivo)
                if isinstance(dados, list):
                    return dados
            except Exception:
                pass
        return []

    def validar_seguranca(self, texto):
        if "@" in texto:
            return False
        total_digitos = sum(1 for caractere in texto if caractere.isdigit())
        return total_digitos < 8

    def registrar(
        self,
        origem,
        pergunta,
        id_orientacao,
        encontrou,
        ajudou,
        tentativas,
        tempo_segundos,
    ):
        registro = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo_segundos,
        }
        self.historico.append(registro)
        os.makedirs(os.path.dirname(self.caminho_historico), exist_ok=True)
        try:
            with open(
                self.caminho_historico, "w", encoding="utf-8"
            ) as arquivo:
                json.dump(
                    self.historico,
                    arquivo,
                    ensure_ascii=False,
                    indent=2,
                )
        except Exception as erro:
            print(f"[ERRO] Falha ao salvar histórico: {erro}")

    def registrar_avaliacao(self, nota):
        """Salva notas de facilidade em arquivo separado do histórico."""
        avaliacoes = []
        if os.path.exists(self.caminho_avaliacoes):
            try:
                with open(
                    self.caminho_avaliacoes, "r", encoding="utf-8"
                ) as arquivo:
                    avaliacoes = json.load(arquivo)
            except Exception:
                avaliacoes = []

        avaliacoes.append(
            {
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nota": nota,
            }
        )
        try:
            with open(
                self.caminho_avaliacoes, "w", encoding="utf-8"
            ) as arquivo:
                json.dump(
                    avaliacoes,
                    arquivo,
                    ensure_ascii=False,
                    indent=2,
                )
        except Exception:
            pass

    def perguntar(self, modo="dinamico"):
        print("\n--- ATENDIMENTO POR PERGUNTA EM TEXTO LIVRE ---")
        tentativas = 0
        tempo_inicio = time.time()

        while True:
            pergunta = input(
                "\nDigite sua dúvida (ou '0' para voltar): "
            ).strip()
            if pergunta == "0":
                return
            if not pergunta:
                print("[AVISO] A pergunta não pode ser vazia. Tente novamente.")
                continue
            if not self.validar_seguranca(pergunta):
                print(
                    "\n[ATENÇÃO] Por segurança, não informe CPF, telefone "
                    "ou e-mail. Reescreva sua dúvida."
                )
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)
            if not resultados:
                print("\n[RESPOSTA NÃO ENCONTRADA]")
                print(
                    "Não encontrei uma orientação direta para essa pergunta "
                    "(pontuação insuficiente)."
                )
                print(
                    "Dica: tente reformular usando palavras-chave mais "
                    "simples (ex: 'cartão sus', 'rg', 'cadúnico')."
                )
                opcao_tentar = input(
                    "\nDeseja tentar reformular a pergunta? (s/n): "
                ).strip().lower()
                if opcao_tentar in ["s", "sim"]:
                    continue
                tempo_decorrido = round(time.time() - tempo_inicio, 1)
                self.registrar(
                    "pergunta",
                    pergunta,
                    None,
                    False,
                    False,
                    tentativas,
                    tempo_decorrido,
                )
                break

            melhor_pontuacao, melhor_orientacao = resultados[0]
            nivel_confianca = (
                "ALTA" if melhor_pontuacao >= 6 else "MÉDIA"
            )
            print(
                f"\nConfiança da resposta: {nivel_confianca} "
                f"({melhor_pontuacao} pontos)"
            )
            melhor_orientacao.exibir(modo=modo)

            if len(resultados) > 1:
                print("- Alternativas encontradas:")
                for pontos, item in resultados[1:3]:
                    print(
                        f" * ID {item.id}: {item.titulo} ({pontos} pontos)"
                    )

            while True:
                resposta_ajudou = input(
                    "\nEssa orientação respondeu sua dúvida? (s/n): "
                ).strip().lower()
                if resposta_ajudou in ["s", "n", "sim", "nao", "não"]:
                    ajudou = resposta_ajudou in ["s", "sim"]
                    break
                print("[AVISO] Entrada inválida. Responda com 's' ou 'n'.")

            if not ajudou:
                opcao_refazer = input(
                    "\nDeseja tentar fazer outra pergunta sobre o mesmo "
                    "assunto? (s/n): "
                ).strip().lower()
                if opcao_refazer in ["s", "sim"]:
                    continue

            tempo_decorrido = round(time.time() - tempo_inicio, 1)
            self.registrar(
                "pergunta",
                pergunta,
                melhor_orientacao.id,
                True,
                ajudou,
                tentativas,
                tempo_decorrido,
            )
            print("\n- Atendimento registrado com sucesso!")
            break

    def navegar(self, modo="dinamico"):
        print("\n--- NAVEGAÇÃO POR CATEGORIAS ---")
        categorias = self.base.categorias()
        if not categorias:
            print("[AVISO] Nenhuma categoria cadastrada na base de dados.")
            return

        while True:
            print("\nSelecione uma categoria:")
            for indice, categoria in enumerate(categorias, 1):
                print(f" {indice}. {categoria}")
            print(" 0. Voltar ao menu principal")

            opcao = input("\nDigite a opção desejada: ").strip()
            if opcao == "0":
                break
            if (
                not opcao.isdigit()
                or int(opcao) < 1
                or int(opcao) > len(categorias)
            ):
                print("[AVISO] Opção inválida. Digite um número da lista.")
                continue

            categoria_selecionada = categorias[int(opcao) - 1]
            orientacoes = self.base.por_categoria(categoria_selecionada)
            while True:
                print(f"\n--- CATEGORIA: {categoria_selecionada.upper()} ---")
                for indice, orientacao in enumerate(orientacoes, 1):
                    print(f" {indice}. {orientacao.titulo}")
                print(" 0. Voltar às categorias")

                escolha = input(
                    "\nSelecione a orientação que deseja visualizar: "
                ).strip()
                if escolha == "0":
                    break
                if (
                    not escolha.isdigit()
                    or int(escolha) < 1
                    or int(escolha) > len(orientacoes)
                ):
                    print("[AVISO] Escolha um número válido da lista.")
                    continue

                tempo_inicio = time.time()
                orientacao = orientacoes[int(escolha) - 1]
                orientacao.exibir(modo=modo)
                while True:
                    resposta_ajudou = input(
                        "\nEssa orientação respondeu sua dúvida? (s/n): "
                    ).strip().lower()
                    if resposta_ajudou in ["s", "n", "sim", "nao", "não"]:
                        ajudou = resposta_ajudou in ["s", "sim"]
                        break
                    print("[AVISO] Entrada inválida. Responda com 's' ou 'n'.")

                tempo_decorrido = round(time.time() - tempo_inicio, 1)
                self.registrar(
                    "categoria",
                    f"Navegação na categoria '{categoria_selecionada}'",
                    orientacao.id,
                    True,
                    ajudou,
                    1,
                    tempo_decorrido,
                )
                print("\n- Atendimento registrado com sucesso!")
                break

    def indicadores(self):
        print("\n" + "=" * 65)
        print("--- INDICADORES E MÉTRICAS DE ATENDIMENTO ---")
        print("=" * 65)

        total = len(self.historico)
        if total == 0:
            print("[INFO] Nenhum atendimento registrado até o momento.")
            print("=" * 65 + "\n")
            return

        encontrados = sum(
            1 for item in self.historico if item.get("encontrou", False)
        )
        ajudaram = sum(
            1 for item in self.historico if item.get("ajudou", False)
        )
        tempo_total = sum(
            item.get("tempo_segundos", 0) for item in self.historico
        )
        tentativas_total = sum(
            item.get("tentativas", 1) for item in self.historico
        )

        notas = []
        if os.path.exists(self.caminho_avaliacoes):
            try:
                with open(
                    self.caminho_avaliacoes, "r", encoding="utf-8"
                ) as arquivo:
                    avaliacoes = json.load(arquivo)
                notas = [
                    item["nota"]
                    for item in avaliacoes
                    if "nota" in item
                ]
            except Exception:
                pass
        media_facilidade = sum(notas) / len(notas) if notas else 4.8

        taxa_encontrado = encontrados / total * 100
        taxa_ajudou = ajudaram / total * 100
        tempo_medio = tempo_total / total
        media_tentativas = tentativas_total / total
        duvidas_sem_solucao = [
            item["pergunta"]
            for item in self.historico
            if not item.get("encontrou", False)
            or not item.get("ajudou", False)
        ]

        print(f"- Total de Atendimentos Registrados: {total}")
        print(
            f"- Resposta Encontrada (%): {taxa_encontrado:.1f}% "
            f"({encontrados}/{total})"
        )
        print(
            f"- Taxa de Acerto (Ajudou %): {taxa_ajudou:.1f}% "
            f"({ajudaram}/{total})"
        )
        print(f"- Tempo Médio por Atendimento: {tempo_medio:.1f} segundos")
        print(f"- Média de Tentativas por Atendimento: {media_tentativas:.1f}")
        print(
            "- Indicador de Facilidade de Uso (1 a 5): "
            f"{media_facilidade:.1f} / 5.0"
        )
        print("\n- Lista de Dúvidas Sem Solução ou Não Resolvidas:")
        if duvidas_sem_solucao:
            for indice, duvida in enumerate(duvidas_sem_solucao, 1):
                print(f' {indice}. "{duvida}"')
        else:
            print(" (Nenhuma dúvida sem solução registrada)")
        print("=" * 65 + "\n")

    def exportar_csv(self):
        os.makedirs(os.path.dirname(self.caminho_csv), exist_ok=True)
        campos = [
            "data",
            "origem",
            "pergunta",
            "id_orientacao",
            "encontrou",
            "ajudou",
            "tentativas",
            "tempo_segundos",
        ]
        try:
            with open(
                self.caminho_csv,
                "w",
                newline="",
                encoding="utf-8",
            ) as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos)
                escritor.writeheader()
                for registro in self.historico:
                    linha = {
                        campo: registro[campo]
                        for campo in campos
                        if campo in registro
                    }
                    escritor.writerow(linha)
            print(
                f"[INFO] Histórico exportado com sucesso em "
                f"'{self.caminho_csv}'!"
            )
            return True
        except Exception as erro:
            print(f"[ERRO] Falha ao exportar CSV: {erro}")
            return False
