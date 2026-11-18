# Citizen Assist AI - Assistente Digital de Orientação ao Cidadão

O **Citizen Assist AI** é uma solução em Python desenvolvida para simplificar a busca por orientações e serviços públicos essenciais, combinando **inteligência baseada em regras de pontuação**, **estruturas de dados encadeadas manuais** e **perfis cognitivos de acessibilidade**.

---

## 1. Integrantes da Equipe

* **Nome do Integrante 1:** Arthur Vettorazzo de Souza | **RM:** 569445
* **Nome do Integrante 2:** Brayan Barbosa dos Santos | **RM:** 573682
* **Nome do Integrante 3:** Giovanne Gomes Petenuci | **RM:** 574091

---

## 2. Público-Alvo e Problema Escolhido

* **Público-Alvo:** Cidadãos em geral, com foco em idosos, pessoas com baixa alfabetização digital e indivíduos neurodivergentes.
* **Problema:** A burocracia e a dispersão de informações sobre documentos e benefícios públicos geram perda de tempo e ruídos de comunicação.

---

## 3. Objetivos de Desenvolvimento Sustentável (ODS)

* **ODS 10 - Redução das Desigualdades:** Acessibilidade cognitiva por meio dos 4 perfis de acessibilidade (Dinâmico, Guiado, Focado e 100% Voz).
* **ODS 16 - Paz, Justiça e Instituições Eficazes:** Acesso público à informação com transparência e fontes oficiais verificadas.

---

## 4. Como Executar a Aplicação

1. Certifique-se de ter o **Python 3.8+** instalado.
2. Clone o repositório e acesse a pasta raiz:

   ```bash
   git clone https://github.com/giovannegomespetenuci/Citizen-Assist-AI.git
   cd Citizen-Assist-AI
   ```

3. Execute o assistente (não há bibliotecas externas nem etapa de compilação):

   ```bash
   python main.py
   ```

4. Na tela de perfil, escolha de 1 a 4 (ou Enter para o modo Dinâmico). No menu principal, a opção **3 (Gestão de registros e operações)** abre as operações de DSA: listar, consultar por ID, cadastrar, atualizar, excluir, pesquisar e ordenar. Para sair, digite `0` e `0` e informe a nota de facilidade de uso (1 a 5).

## 5. Regra de Pontuação e Busca Inteligente

+3 Pontos: Para cada palavra-chave exata da orientação encontrada na pergunta.

+1 Ponto: Para cada palavra única da pergunta (com 4+ letras) presente no título.

Confiança ALTA: Pontuação $\ge 6$.

Confiança MÉDIA: Pontuação de 3 a 5.

Não Encontrado: Pontuação $< 3$ (o sistema recusa orientações irrelevantes e sugere o uso de palavras-chave mais simples ou navegação por categorias).

## 6. Arquitetura e Estruturas de Dados

Estrutura do Repositório:

```text
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    ├── atendimentos.csv
    └── avaliacoes.json
```

### Estrutura de dados (DSA)

Os registros ficam em uma **lista encadeada simples** implementada pela equipe (`No` e `ListaEncadeada`, em `base_conhecimento.py`). Cada nó guarda uma `Orientacao` em `conteudo` e a referência ao próximo nó em `proximo`; a lista guarda `inicio` e o contador `_tamanho`. Não há ponteiro para o último nó. Operações: `inserir` (no fim), `listar_todos`, `buscar_por_id`, `atualizar_por_id`, `remover_por_id` (trata início, meio, fim e lista de um nó), `pesquisar`, `ordenar_por_id` e `ordenar_por_titulo`.

### Algoritmos de busca e ordenação

* **Busca sequencial por ID:** percorre os nós até achar o id (usada na consulta, no cadastro para recusar ID duplicado, na atualização e na exclusão). Busca binária não compensa em lista encadeada, pois chegar ao meio já custa O(n).
* **Pesquisa por atributo:** percorre todos os nós e verifica se o termo, normalizado (minúsculas, sem acento e sem pontuação), está contido no título, na categoria ou no público-alvo.
* **Ordenação:** Bubble Sort com sinalizador de troca sobre os nós da lista. Troca o **conteúdo** dos nós vizinhos fora de ordem (e não os ponteiros) e repete até uma passada sem trocas. A chave é o `id` ou o título normalizado.

### Análise de complexidade (Big-O)

Hipóteses: **n** = número de registros (nós); **L** = comprimento máximo do texto de um campo; a lista não mantém ponteiro para o último nó; custos de leitura e gravação do JSON e de entrada e saída não são considerados.

| Operação | Melhor caso | Pior caso | Espaço extra | Observação |
|---|---|---|---|---|
| Inserção no fim | O(1) | O(n) | O(1) | Lista vazia: O(1). Senão, percorre até o último nó. |
| Busca por ID | O(1) | O(n) | O(1) | Melhor: primeiro nó. Pior: último nó ou ID inexistente. |
| Pesquisa por atributo | O(n·L) | O(n·L) | O(r) | Sempre percorre os n nós e normaliza 3 campos (r = nº de resultados). |
| Atualização | O(1) | O(n) | O(1) | Localiza o nó e troca o `conteudo`. |
| Exclusão | O(1) | O(n) | O(1) | Localiza o nó e religa os ponteiros em O(1). |
| Ordenação por ID (Bubble Sort) | O(n) | O(n²) | O(1) | Melhor: lista já ordenada (uma passada). Pior: ordem inversa (n passadas). |
| Ordenação por título | O(n·L) | O(n²·L) | O(1) | Cada comparação normaliza dois títulos. |
| Carga do JSON (n inserções) | O(n²) | O(n²) | O(n) | Consequência da inserção O(n): 0 + 1 + ... + (n−1) passos. |

A documentação técnica completa de DSA (objetivo, campos dos registros, descrição da lista encadeada, organização do código, instruções de uso, algoritmos e Big-O) e as evidências dos testes estão no arquivo `Testes_e_Demonstrações.docx`, incluído no repositório.

## 7. Resultado dos Testes com Usuários Reais

O assistente foi testado com 3 pessoas externas, somando 10 atendimentos:

Total de Atendimentos: 10

Taxa de Resposta Encontrada: 90.0% (9/10)

Taxa de Acerto (Ajudou o cidadão): 90.0% (9/10)

Tempo Médio por Atendimento: 14.2 segundos

Facilidade de Uso (Média): 4.8 / 5.0

Dúvidas Sem Solução Identificadas: 1 ("Como solicitar isenção do IPTU para idosos")

Melhoria Implementada na Base de Conhecimento:

Com base na dúvida sem solução identificada nos testes, adicionamos formalmente a orientação ID 11: "Solicitar Isenção de IPTU para Idosos e Aposentados" no arquivo data/base_conhecimento.json, incluindo as palavras-chave "isencao iptu", "iptu idoso", "iptu gratis" e "desconto iptu aposentado".

## 8. Fontes Consultadas e Links Oficiais

- [Ministério da Saúde](https://www.gov.br/saude)
- [Governo Digital (CIN / RG)](https://www.gov.br/governodigital/pt-br/identificacao-do-cidadao)
- [Ministério do Trabalho e Emprego (Carteira de Trabalho Digital)](https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho)
- [Receita Federal (CPF)](https://www.gov.br/receitafederal/pt-br/assuntos/meu-cpf)
- [Tribunal Superior Eleitoral (TSE)](https://www.tse.jus.br/servicos-eleitorais/certidoes/certidao-de-quitacao-eleitoral)
- [Ministério do Desenvolvimento e Assistência Social (CadÚnico)](https://www.gov.br/mds/pt-br/acoes-e-programas/cadastro-unico)
- [Agência Nacional de Energia Elétrica (ANEEL) — Tarifa Social](https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-social)
- [Passe Livre Interestadual (ANTT)](https://www.gov.br/pt-br/servicos/obter-passe-livre-interestadual-digital)

## 9. Limitações do Assistente

Atendimento Offline: Depende exclusivamente da base cadastrada em JSON local.

Sensibilidade a Erros Ortográficos Severos: A busca por regras exige que as palavras-chave sejam digitadas com ortografia minimamente legível.

## 10. Link do Vídeo Técnico (YouTube)

URL do Vídeo (Não Listado):