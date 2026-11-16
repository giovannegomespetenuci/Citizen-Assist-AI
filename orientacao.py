class Orientacao:
    """
    Representa uma orientação individual da base de conhecimento.
    Atende aos campos de PCP, DSA (incluindo público-alvo) e aos quatro
    perfis de acessibilidade.
    """

    def __init__(
        self,
        id_orientacao,
        categoria,
        titulo,
        publico_alvo,
        palavras_chave,
        resposta,
        documentos,
        onde,
        fonte,
        verificado_em,
    ):
        self.id = int(id_orientacao)
        self.categoria = str(categoria)
        self.titulo = str(titulo)
        self.publico_alvo = str(publico_alvo)
        self.palavras_chave = (
            palavras_chave
            if isinstance(palavras_chave, list)
            else [palavras_chave]
        )
        self.resposta = str(resposta)
        self.documentos = (
            documentos if isinstance(documentos, list) else [documentos]
        )
        self.onde = str(onde)
        self.fonte = str(fonte)
        self.verificado_em = str(verificado_em)

    def exibir(self, modo="dinamico"):
        modo = str(modo).lower().strip()
        print("\n" + "=" * 65)
        print(f"[{self.categoria.upper()}] - {self.titulo} (ID: {self.id})")
        print(f"Público-Alvo: {self.publico_alvo}")
        print("=" * 65)

        if modo == "guiado":
            print("\n- Olá! Vamos te orientar passo a passo, de forma simples.")
            print(f"\n- O QUE É:\n {self.resposta}")
            print("\n- O QUE LEVAR (DOCUMENTOS):")
            for documento in self.documentos:
                print(
                    f" - {documento} "
                    "(Dica: Leve o documento original em bom estado)"
                )
            print(f"\n- ONDE IR:\n {self.onde}")
            print(
                f"- Fonte Oficial: {self.fonte} "
                f"(Checado em: {self.verificado_em})"
            )
            print(
                "\n[AVISO] Este assistente é informativo e NÃO substitui "
                "canais oficiais."
            )
        elif modo == "focado":
            print("\n--- MODO FOCADO (PAGINADO - UMA ETAPA POR VEZ) ---")
            print(f"\n[Etapa 1 de 3] SOBRE O SERVIÇO:\n- {self.resposta}")
            input(
                "\n-> Pressione [ENTER] para ver os documentos necessários..."
            )
            print("\n[Etapa 2 de 3] DOCUMENTAÇÃO NECESSÁRIA:")
            for indice, documento in enumerate(self.documentos, 1):
                print(f" {indice}. {documento}")
            input("\n-> Pressione [ENTER] para ver onde ir...")
            print(
                f"\n[Etapa 3 de 3] LOCAL E FONTE:\n"
                f"- Local: {self.onde}\n- Link: {self.fonte}"
            )
            print(
                "\n[AVISO] Este assistente não substitui atendimentos oficiais."
            )
        elif modo == "voz":
            print("\n--- MODO LEITURA DE VOZ (FORMATADO PARA SINTETIZADOR) ---")
            print(
                f"Título: {self.titulo}. Categoria: {self.categoria}. "
                f"Público: {self.publico_alvo}."
            )
            print(
                f"Resumo: {self.resposta}. Documentos necessários: "
                f"{', '.join(self.documentos)}."
            )
            print(
                f"Onde encontrar: {self.onde}. Verificado em "
                f"{self.verificado_em} na fonte {self.fonte}."
            )
        else:
            print(f"\n- Resposta: {self.resposta}")
            print("- Documentos necessários:")
            for documento in self.documentos:
                print(f" - {documento}")
            print(f"- Onde ir: {self.onde}")
            print(
                f"- Fonte Oficial: {self.fonte} "
                f"(verificado em {self.verificado_em})"
            )
            print("- Aviso: este assistente NÃO é um canal oficial.")

        print("=" * 65 + "\n")
