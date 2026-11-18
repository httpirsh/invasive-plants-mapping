# Notas para a Tese

Coisas que quero dizer na tese e na defesa, e o registo do que decidi e
porquê. O estado atual do desenho está em
[`docs/research_questions.md`](../docs/research_questions.md) e
[`docs/methodology.md`](../docs/methodology.md); aqui fica o raciocínio.

Cada entrada segue a mesma forma: quem decidiu, **O que decidi**,
**Porquê**, **Fundamentação**, **Onde**, **Na tese**. O texto e a
data de uma entrada nunca mudam; o que muda depois entra num bloco
**Revisão** datado no fim da entrada, e o estado atual de cada uma
está no [índice das decisões](#decisões). Os notebooks apagados a
2026-11-17 (`one_class_method_selection`,
`one_class_background_free_evaluation`,
`presence_background_citizen_science`, `expert_arm_classifiers`,
`forest_only_background_check`) continuam ligados nas linhas "Onde"
das entradas antigas; estão no histórico do Git até ao commit
`1ed5b46`.

## Para dizer

*Numeração: os pontos desta secção usam as quatro perguntas atuais
(a confirmar com o orientador; ver
[Renumeração das perguntas](#renumeracao-perguntas-2026-11-13)). O
manuscrito ainda tem as três perguntas que ele aprovou.*

### Perguntas ambiciosas

*Sugestão dos orientadores para a defesa.*

> "Tenho noção de que as perguntas são ambiciosas. Por isso estão
> ordenadas de modo que cada uma só usa o que as anteriores definem: a
> RQ1 é o núcleo, com o protocolo fechado e a curva corrida com o
> classificador presence-only; a RQ2 e a RQ3 reutilizam o modelo
> e os dados da RQ1, só com TESSERA; a RQ4 é a única que depende do
> Sentinel-2 e fica para o fim. Vou ajustando consoante o que os dados
> e o tempo permitirem."

Porque esta ordem se defende:
- A RQ1 sozinha responde ao objetivo principal da proposta e ao
  objetivo 3: é um resultado completo, corrido com o classificador
  escolhido em [RQ1 passa a presence-only](#rq1-presence-only)
  ([curva](#curva-presence-only)).
- A RQ2 responde ao objetivo 1 da proposta. A parte dos filtros corre
  com os embeddings já guardados; a máscara precisa de uma extração de
  janelas TESSERA.
- A RQ3 responde à transferibilidade (plano de trabalho 4) dentro do
  distrito, só com TESSERA.
- A RQ4 é a mais cara: precisa do braço Sentinel-2, parado pelo custo
  da extração. Se não correr, perco só a última pergunta.

Cenários em [Scope](../docs/research_questions.md#scope).

**Na tese:** ✅ Parcial. A ordem de prioridade das quatro perguntas
está em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(secção 1.2 Research Questions and Goals, 2026-11-17); o desenho de
cada uma fica para o Proposed Work.

### Introdução para um júri de informática

*Sugestão do orientador.* O júri é de um departamento de informática e
não está por dentro da observação da Terra. A tese (e a defesa) tem de
começar por explicar os conceitos base e os problemas que depois tento
resolver.

**Conceitos a introduzir:**
- **Observação da Terra e satélites:** o Sentinel-2 fotografa a mesma
  zona a cada poucos dias, com várias bandas (não só RGB), em píxeis de
  10 m. Séries temporais e composições (p. ex. por estação).
- **Mapear uma espécie por satélite:** classificar cada píxel. É
  difícil porque a *Acacia* se parece com outras árvores; o sinal mais
  útil é a floração no inverno (Domingo et al., 2023; Martins et al.,
  2016).
- **Dados de referência:** para treinar e avaliar é preciso saber onde
  a espécie está de facto. Recolhê-los no terreno é caro, que é o
  problema de partida da proposta.
- **Foundation models de observação da Terra e embeddings:** modelos
  pré-treinados em muitas imagens que dão um vetor por píxel (TESSERA,
  AlphaEarth). Analogia para informáticos: como modelos de linguagem
  ou de visão pré-treinados, sobre os quais se treina um classificador
  simples.
- **Ciência cidadã:** pessoas comuns registam observações (iNaturalist)
  com foto, data e localização. São pontos, não mapas, e só dizem onde
  a espécie foi vista.

**Problemas comuns, e onde a tese os trata:**

| Problema | Em termos de informática | Onde é tratado |
|---|---|---|
| Enviesamento espacial: as observações concentram-se perto de estradas e trilhos (Dimson et al., 2023) | Sampling bias / dataset bias | RQ3 |
| Poucos observadores: 90% das 2 465 presenças são de uma só pessoa | Dados de treino pouco diversos | RQ3 |
| Só presenças, sem ausências (Phillips et al., 2009) | Positive-unlabeled learning | Classificador presence-only na RQ1; o fundo entra só como amostra da paisagem, nunca como ausência |
| Rótulos com ruído: localização imprecisa, píxeis mistos (Ball et al., 2026) | Label noise | Pipeline de preparação dos dados; RQ2 (filtros de grau e de precisão, máscara) |
| Poucos dados | Data efficiency / few labels | Nível de 150 presenças na RQ2 e na RQ4 |
| Observações de anos diferentes das imagens (Ball et al., 2026) | Desfasamento temporal entre dados e rótulos | Ano único 2023; filtro de fogo |
| Pontos vizinhos parecidos inflacionam a exatidão (Karasiak et al., 2022) | Data leakage / autocorrelação | Validação espacial |
| Pior desempenho noutras regiões (Yang et al., 2026) | Distribution shift | RQ3, só dentro do distrito |

Ideia para a defesa: um diagrama do pipeline (observação no
iNaturalist → píxel → embedding → classificador → mapa) antes das
perguntas de investigação.

**Na tese:** ✅ Os conceitos base e a tabela de problemas já estão em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(abertura do capítulo e secção 1.1 Context and Motivation, onde os
problemas estão em prosa); os cinco conceitos estão desenvolvidos em
[`thesis/document/text/2-background.tex`](document/text/2-background.tex)
(capítulo escrito a 2026-11-18, uma secção por conceito, mais a 2.5
sobre presence-only e validação espacial); a tabela de problemas está no fim da
secção 1.2, depois dos objetivos, com a numeração das quatro
perguntas atuais (movida e corrigida a 2026-11-18). O
diagrama do pipeline está na secção 1.2, a seguir às quatro perguntas
(Figura `fig:introduction-pipeline`, TikZ, movida a 2026-11-17), com
cada pergunta na etapa em que atua. A motivação da secção 1.1 cita
desde 2026-11-18 o IFN6 (inventário decenal, 8,4 mil ha de
povoamentos de acácia em 2015) e o relatório EFFIS 2024 (fogos
recorrentes), ambos em `docs/literature.md`. A Introdução ainda cita `zhu2026` para a linha
das outras regiões; a entrada da bibliografia já tem o autor certo
(Stewart et al., corrigido a 2026-11-17), mas a fonte certa para essa
linha é Yang et al. (2026). Por corrigir no manuscrito. Duas outras
linhas da tabela já não correspondem ao desenho (fundo e citação de
Ball et al.); ver a
[revisão de consistência](#revisao-consistencia-2026-11-13).

### Metodologias abandonadas

*Para a defesa: o que foi tentado, porque não serviu e o que veio a
seguir. Regras de quanto disto entra no texto: `CLAUDE.md`, "Writing
Abandoned Methodologies".*

- **Multiclasse (outras plantas e classes da COS como classes
  próprias).** Exigia construir ausências confirmadas à mão, por
  interpretação visual, o que o orientador não considerou eficiente.
  Passei a presença vs. fundo, e a RQ1 deixou de ter um "limite
  superior" fixo para passar a uma curva de redução de esforço. Ver
  [Multiclasse abandonado](#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo).
- **One-class puro (Isolation Forest, one-class SVM, PCA e ensemble
  PCA + Isolation Forest).** Testado duas vezes. Primeiro com ROC-AUC
  e Boyce contra o fundo: perdeu sempre para presença vs. fundo e, sob
  um fundo só de floresta, caiu para perto do acaso. O orientador
  contestou essa avaliação (assumia que o fundo não tem acácia) e
  pediu para reabrir; no protocolo novo (leave-one-block-out,
  sensitivity a 10% de área, fundo só como amostra da paisagem), e
  depois de um varrimento de hiperparâmetros nas duas famílias, as
  melhores configurações one-class ficaram abaixo de todas as
  presença-fundo (melhor one-class 0,258 contra 0,410 da regressão
  logística; acaso 0,10). O ensemble autoencoder + Isolation Forest
  que o orientador nomeou foi testado e fica perto do acaso. Ver
  [One-class reaberto](#one-class-reaberto-avaliação-sem-fundo-sensitivity-grelha-espacial-e-ensemble-pca--isolation-forest)
  e [RQ1 passa a presence-only](#rq1-presence-only).
- **Random Forest presença-vs-fundo.** Foi o classificador da curva
  até 2026-11-17. Usa o fundo como classe 0, ou seja, como
  pseudo-ausência (Rapinel & Hubert-Moy, 2021), que é o pressuposto
  que o orientador contestou: não é presence-only. Os números da
  curva, da zona-tampão e do fundo só de floresta obtidos com ele
  ficam como registo, não como resultado. Passou a regressão logística
  presença-fundo, com o fundo como amostra não rotulada. Ver
  [Random Forest](#classificador-presença-vs-fundo-ciência-cidadã-random-forest-por-agora)
  e [RQ1 passa a presence-only](#rq1-presence-only).
- **Afinar o foundation model (fine-tuning).** A proposta da tese pede
  fine-tuning; uso embeddings congelados com um classificador leve. É
  um desvio à proposta, não algo testado e largado. Razões: o
  AlphaEarth só existe como embeddings; o artigo do TESSERA diz que os
  pesos são abertos, mas o repositório restringe o checkpoint
  (verificado em 2026-11-11); no próprio artigo do TESSERA, afinar o
  codificador não trouxe benefício (Feng et al., 2026); com poucos
  rótulos e ruidosos, afinar arrisca ajustar o ruído; e o mesmo
  classificador sobre cada representação isola o efeito da
  representação. Segue Ball et al. (2026), Yang et al. (2026) e Brown
  et al. (2025). Ver
  [Foundation Model Use](../docs/research_questions.md#foundation-model-use-adopted).
- **RQ3: assumir que o observador dominante é um enviesamento** (a
  confirmar com o orientador). Questionei a premissa, medi (ele é
  fiável e concentrado numa zona, não necessariamente um problema) e
  passei a medir primeiro se a concentração prejudica o modelo, perto
  contra longe. Ver
  [proposta de redesenho](#rq3-proposta-redesenho-diagnostico-primeiro).

**Na tese:** ⏳ Ainda não escrita. Ao escrever a Metodologia, um
parágrafo breve sobre estas escolhas como justificação do desenho
final, não como histórico extenso.

### Protocolo de pesquisa da literatura

*Preparação para a defesa: explicar como a literatura foi pesquisada,
se perguntarem. Ainda não executado. Não entra no texto do relatório,
cujo capítulo de trabalho relacionado é uma revisão narrativa por
subtema, como nos relatórios de referência em
`thesis/guidance_example/`.*

Serve para trocar "parece pouco explorado" por uma afirmação
documentada:

1. **Scopus e Web of Science**, com a query guardada, a data e o
   número de resultados:
   ```text
   ("invasive plant*" OR "alien plant*" OR "invasive species")
   AND ("remote sensing" OR "Sentinel-2" OR "satellite")
   AND ("citizen science" OR "iNaturalist" OR "crowdsourc*" OR "GBIF"
        OR "foundation model*" OR "embedding*")
   ```
   Correr também as combinações duas a duas (foundation models +
   espécies; ciência cidadã + deteção remota), para mostrar que a
   interseção das três é pequena.
2. **arXiv e bioRxiv**, 2025–2026: "AlphaEarth", "TESSERA",
   "satellite embedding", combinados com "species", "iNaturalist",
   "invasive". A maior parte do trabalho próximo ainda é preprint.
3. **Triagem:** título/resumo → texto completo, com contagens em cada
   etapa.
4. **Bola de neve:** para trás (referências) e para a frente
   (citações) a partir de Ball 2026, Brown 2025, Feng 2025, Gillespie
   2024 e Dimson 2023.
5. **Alertas:** Google Scholar para "TESSERA embeddings", "AlphaEarth"
   e "iNaturalist remote sensing"; seguir o grupo TESSERA de
   Cambridge.
6. **Tabela de extração** por artigo: tarefa, rótulos (curados ou
   ciência cidadã), representação, validação (aleatória ou espacial),
   enviesamento tratado?, alinhamento temporal tratado?

A lista de leitura atual está em
[`docs/literature.md`](../docs/literature.md).

**Na tese:** não entra no texto; é preparação para a defesa. O
capítulo de trabalho relacionado é uma revisão narrativa.

## Decisões

Agrupadas por tema. Índice com o estado de cada entrada a 2026-11-17
(o detalhe está na linha em itálico de cada entrada e nos seus blocos
"Revisão"; "a confirmar" = proposta minha ainda sem resposta do
orientador):

**[Âmbito e perguntas](#decisões-âmbito-e-perguntas)**
- [Só *Acacia dealbata*](#só-acacia-dealbata) — minha, a confirmar.
- [RQ3 aprovada](#rq3-aprovada) — orientador; a forma de a medir tem
  proposta a confirmar.
- [RQ3: proposta de redesenho](#rq3-proposta-redesenho-diagnostico-primeiro)
  — substituída (2026-11-13) pela simplificação e pela renumeração.
- [Formulação das perguntas](#formulacao-pergunta-objetivos-hipoteses)
  — substituída (2026-11-13); guarda os enunciados aprovados pelo
  orientador.
- [RQ2: a máscara passa a ser a pergunta](#rq2-proposta-mascara) — a
  confirmar; integrada na reformulação (RQ2 = filtros e máscara).
- [Reformulação em quatro perguntas](#reformulacao-quatro-perguntas)
  — a confirmar; a numeração foi substituída pela renumeração.
- [Simplificação do desenho](#simplificacao-desenho-2026-11-13) — a
  confirmar; a numeração foi substituída pela renumeração.
- [Renumeração das perguntas](#renumeracao-perguntas-2026-11-13) — a
  confirmar; numeração e desenho atuais das RQ2 e RQ3.
- [Revisão de consistência de 2026-11-13](#revisao-consistencia-2026-11-13)
  — a confirmar (teste da RQ3, limitação da RQ2); o resto é limpeza
  feita.
- [Pergunta principal: "como dados de treino"](#pergunta-principal-dados-de-treino)
  — a confirmar.

**[Dados de referência](#decisões-dados-de-referência)**
- [Usar os dados de especialistas, com limpeza](#usar-os-dados-de-especialistas-com-limpeza)
  — minha; a exclusão dos `classifica = 0` é do orientador.
- [Só observações *research*](#só-observações-research-nos-dois-lados)
  — minha.
- [Precisão da localização](#precisão-da-localização-tirar-acima-de-30-m-manter-as-sem-valor)
  — minha; teste repetido com 2021–2025 (Revisão de 2026-11-15).
- [Janela temporal 2021–2025](#janela-temporal-2021-2025) — minha;
  dada por resolvida a 2026-11-17.
- [Uma observação por píxel](#uma-observação-por-píxel-nos-conflitos-fica-a-presença)
  — minha.
- [Observer A: todas as observações](#observer-a-todas-as-observações-no-modelo-principal)
  — minha.
- [Máscara de segmentação: testar várias abordagens](#máscara-de-segmentação-testar-várias-abordagens)
  — orientador; a regra concreta está na renumeração (decisão 5).
- [Manifesto de ficheiros derivados](#manifesto-ficheiros-derivados)
  — minha; organização do repositório.

**[RQ1: desenho e resultados](#decisões-rq1-desenho-e-resultados)**
- [Multiclasse abandonado; curva de redução de esforço](#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)
  — orientador (pontos 1 a 4) e minha; o ponto 7 (Random Forest) foi
  superado a 2026-11-17.
- [Random Forest](#classificador-presença-vs-fundo-ciência-cidadã-random-forest-por-agora)
  — superada a 2026-11-17.
- [Braço de especialistas](#braço-de-especialistas-one-class-svm-e-random-forest-confirmados-100-especialistas)
  — minha; os números são do Random Forest e já não contam como
  resultado.
- [One-class reaberto](#one-class-reaberto-avaliação-sem-fundo-sensitivity-grelha-espacial-e-ensemble-pca--isolation-forest)
  — orientador (direção) e minha; a métrica desta entrada foi
  substituída no mesmo dia.
- [RQ1 passa a presence-only](#rq1-presence-only) — minha, a
  confirmar; classificador (regressão logística `C=10`), métrica e
  seleção de método atuais da RQ1.
- [Curva da RQ1 no desenho presence-only](#curva-presence-only) —
  minha, a confirmar; desenho e resultado atuais da curva
  (leave-one-block-out com as duas fontes).
- [Curva completa 0%–100%](#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos)
  — superada em parte (Revisão de 2026-11-17): fica a unidade, a
  ordem encaixada e o teste com as duas fontes; saem as cinco
  sementes e os números do Random Forest.
- [Fundo só de floresta](#curva-fundo-so-floresta) — minha; números do
  Random Forest, não recorrida no desenho novo (obsoleta).
- [Diagnósticos da curva plana](#diagnosticos-curva-plana) — minha;
  ficam como factos dos dados.
- [Limites do Boyce](#metricas-limites-boyce) — minha; ROC-AUC e Boyce
  passaram a métricas secundárias.
- [Fundo partilhado uniforme](#rq1-fundo-uniforme-nao-cos) — minha; o
  fundo passou a amostra da paisagem, nunca ausência.
- [Fundo uniforme reconstruído](#fundo-uniforme-reconstruido-2465) —
  registo de proveniência.
- [Curva por fonte das presenças de teste](#rq2-curva-por-fonte) — a
  confirmar; números do Random Forest, a curva é recorrida.
- [Curva passa a script](#curva-script-experiments) — minha;
  organização do repositório.
- [Fundo de floresta pelo script](#fundo-floresta-script-experiments)
  — minha; organização do repositório.
- [Nível 100% + ciência cidadã](#curva-100-mais-ciencia-cidada) — a
  confirmar; números do Random Forest, a curva é recorrida.

**[Validação e Sentinel-2](#decisões-validação-e-sentinel-2)**
- [Zona-tampão](#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)
  — minha; análise de sensibilidade recorrida no desenho presence-only
  (Revisão de 2026-11-17): o tampão não muda a leitura da RQ1.
- [Sentinel-2 bruto via Earth Search](#sentinel-2-bruto-via-earth-search-aws-sem-conta-alinhado-à-grelha-da-tessera)
  — minha.
- [Sentinel-2 por extração em pontos](#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo)
  — revertida no mesmo dia.
- [Features do Sentinel-2](#conjunto-de-features-do-sentinel-2-na-rq1-compósito-anual-ball-et-al-fenologia-da-floração-como-extensão-por-ablação-domingo-et-al)
  — proposta a confirmar; o classificador do braço passa a ser o da
  RQ1 (Revisão de 2026-11-17).

**[Documento e entrega](#decisões-documento-e-entrega)**
- [Lista de literatura](#lista-de-literatura-releitura-integral-e-limpeza)
  — minha; revisões até 2026-11-17.
- [Identidade da tese](#identidade-da-tese-confirmada-título-mestrado-orientadores-idioma-e-data-da-entrega)
  — facto fixo.
- [Primeira entrega](#primeira-entrega-relatório-intermédio-início-de-janeiro-de-2027)
  — facto do calendário; âmbito meu, com as exceções das Revisões.

Numeração das perguntas. Cada entrada usa a numeração do momento em
que foi escrita:

| Tema | Aprovada pelo orientador | Manhã de 2026-11-13 | Meio do dia | Atual |
|---|---|---|---|---|
| Curva de redução de esforço | RQ1 (parte) | RQ2 | RQ1 | **RQ1** |
| Dos pontos aos dados de referência | RQ2 (redução de dados ou máscara) | RQ1 | RQ2 | **RQ2** |
| Transferibilidade / concentração | RQ3 | RQ4 | RQ4 | **RQ3** |
| TESSERA contra Sentinel-2 | RQ1 (parte) | RQ3 | RQ3 | **RQ4** |

- **Aprovada pelo orientador:** as entradas anteriores a 2026-11-13.
- **Manhã de 2026-11-13:** quatro entradas desse dia (reformulação em
  quatro perguntas, simplificação do desenho, fundo reconstruído,
  curva por fonte), assinaladas por blocos "Revisão".
- **Meio do dia:** o texto da
  [Renumeração das perguntas](#renumeracao-perguntas-2026-11-13).
- **Atual:** o bloco "Revisão" do fim do dia dessa entrada e as
  entradas seguintes.

## Decisões: âmbito e perguntas

### Só *Acacia dealbata*

*Decisão minha (a confirmar com o orientador).*

**O que decidi:** o alvo é a *A. dealbata*. As outras espécies de
*Acacia* ficam fora do treino.

**Porquê:**
- Os dados de especialistas só têm *A. dealbata*: a comparação da RQ1
  só é justa para esta espécie.
- A proposta pede mapeamento ao nível da espécie (objetivo 3).
- É 66% das observações de *Acacia* (5 254 de 7 943).
- As espécies vêem-se de forma diferente do satélite (manchas densas
  com floração no inverno; árvore misturada na floresta; arbusto das
  dunas).

**Fundamentação:** Domingo et al. (2023) e Martins et al. (2016)
mapearam a *A. dealbata* sozinha.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#species-scope-proposed).
Aplicado no passo 10 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb):
ficam 5 242 observações; saem 2 621 de outras espécies e 35
identificadas só até ao género ou subgénero.

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia). A
introdução já nomeia a *A. dealbata* como alvo, sem justificar o
âmbito; a secção 2.1.1 do Background (2026-11-18) descreve a espécie
(floração de inverno, regeneração após fogo), não a escolha do âmbito.

### RQ3 aprovada

*Decisão do orientador (na reunião).*

**O que decidi:** a RQ3 (os embeddings amplificam ou atenuam o
enviesamento espacial da ciência cidadã, comparados com o Sentinel-2?)
fica nas perguntas da tese, a seguir à RQ1 e à RQ2.

**Porquê:**
- Uma pessoa fez 83% de todas as observações de *Acacia* (90% das
  presenças de *A. dealbata* depois da limpeza), e 98% do pico de 2021.
- O modelo só aprende com os sítios por onde esta pessoa passou; os
  embeddings podem aprender esse percurso mais facilmente (amplificar)
  ou separar melhor a *Acacia* do que está à volta (atenuar). Ainda
  ninguém testou isto.
- É a pergunta mais cara, por isso fica em último na prioridade.

**Fundamentação:** Dimson et al. (2023): registos de invasoras do
iNaturalist enviesados para estradas e zonas perturbadas; Yang et al.
(2026): modelos sobre embeddings que perdem exatidão noutra região;
Phillips et al. (2009) para corrigir o enviesamento.

**Correção (2026-11-11, releitura integral):** a fundamentação citava
"Zhu et al. (2026)", que é Stewart et al. (2026), um capítulo sem
experiências que só relata Ma et al. (2026), ainda por ler. Yang et
al. não têm linha de base Sentinel no teste de transferência. Nenhum
trabalho lido mostra embeddings a transferir pior do que features
convencionais: é isso que a RQ3 testa, não um facto de partida.

**Desenho aprovado:**
- Avaliar em regiões de teste geograficamente separadas, com blocos
  espaciais.
- Comparar três conjuntos de treino: observações originais,
  desbastadas espacialmente, e com o observador dominante capado ou
  removido; testar nos registos de outros observadores e noutras
  regiões.
- Construir eixos de enviesamento a partir da distância a estradas e
  trilhos (p. ex. OpenStreetMap) e verificar que valem na área de
  estudo. Não assumir que corrigir o enviesamento melhora o
  desempenho.
- Enunciado: "Do EO foundation-model representations amplify or
  mitigate the effect of spatial sampling bias in citizen-science
  observations, compared with conventional satellite features, when
  evaluated across geographically distinct regions?"

**Estado:** a pergunta mantém-se; proponho mudar a forma de a medir
(ver [proposta de redesenho](#rq3-proposta-redesenho-diagnostico-primeiro)).
Até o orientador responder, o desenho aprovado é este. Desde
2026-11-11, `docs/research_questions.md` mostra só a proposta, marcada
"a confirmar"; se ele não a aceitar, repõe-se este desenho.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq3--transferability-away-from-the-sampled-area).

**Na tese:** ✅ Parcial. A estatística do observador dominante está em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(secção 1.1, que diz 88% das presenças limpas; o valor é 90%, por
atualizar). O enunciado aprovado foi substituído na secção 1.2
(2026-11-17) pela RQ3 atual, a confirmar com o orientador; a
fundamentação completa fica para o Proposed Work.

### RQ3: proposta de redesenho — diagnosticar primeiro se a concentração da amostragem prejudica o modelo {#rq3-proposta-redesenho-diagnostico-primeiro}

*Proposta minha (a confirmar com o orientador). Muda o desenho de uma
pergunta que ele aprovou, por isso não é adotada antes de ele
responder. Na fila da
[próxima reunião](../docs/meetings/2026-11-17.md). Estado:
substituída a 2026-11-13 (Revisão no fim).*

**O que decidi (como proposta):**

- **Enunciado:** "Os foundation models de observação da Terra
  amplificam ou atenuam o efeito da concentração espacial das
  observações de ciência cidadã, em comparação com features
  convencionais de satélite, quando o modelo é avaliado longe de onde
  houve amostragem?" Muda "enviesamento" para "concentração" e
  "regiões geograficamente distintas" para "longe de onde houve
  amostragem".
- **Hipóteses:** amplifica (o modelo com TESSERA piora mais do que o
  Sentinel-2 longe da zona amostrada); atenua (piora menos); sem
  efeito (nenhum piora — hipótese que o desenho aprovado não previa).
  As experiências mostram o resultado, não o mecanismo. Retirei em
  2026-11-11 o mecanismo que tinha escrito para "amplifica" (os
  embeddings guardarem contexto da paisagem): o artigo do TESSERA,
  Stewart et al. (2026) e Ratsakatika et al. (2026) dizem que os
  embeddings TESSERA são calculados por píxel e não codificam a
  paisagem à volta.
- **Experiência 1 — diagnóstico.** Treinar com a ciência cidadã e
  avaliar nos polígonos de especialistas (referência independente),
  perto e longe do ponto de treino mais próximo, em distância
  geográfica, para TESSERA e Sentinel-2. Os mesmos polígonos ficam nas
  mesmas faixas para as duas representações, por isso a comparação é
  direta. Grupo "longe" principal: polígonos do mesmo ficheiro e
  mosaico (TNE) a mais de 1 km de qualquer ponto de ciência cidadã; os
  do resto do país (notTNE) ficam como extensão opcional.
- **Experiência 2 — um observador dedicado contra muitos ocasionais,
  com o mesmo número de pontos:** 238 pontos do Observador A
  (subamostragens repetidas) contra os 238 dos outros, testados perto
  e longe. Hipóteses: profundidade (os pontos do observador dedicado
  dão um modelo igual ou melhor) contra largura (os dos outros dão um
  modelo melhor longe).
- **Produto — mapa de confiança:** dissemelhança ao treino no espaço
  das features (*area of applicability*, Meyer & Pebesma, 2021)
  aplicada a toda a área, para dizer onde o mapa final é apoiado pelos
  dados de treino e onde extrapola. Só como produto, não como eixo da
  comparação entre representações.
- **Fica de fora:** a camada de estradas e trilhos e a segunda região
  de iNaturalist (Covilhã–Fundão, 57 observações). O desbaste espacial
  fica como única correção, e só se a experiência 1 mostrar
  degradação.

**Porquê:**
- O desenho aprovado parte do princípio de que o Observador A é um
  enviesamento a corrigir, mas nunca o medimos. A fiabilidade dele
  (rótulos) já foi verificada; o que é facto é só a concentração
  espacial. Numa grelha de 10 km em EPSG:3763 (minha, não
  necessariamente a dos notebooks), os 2 227 pontos dele ocupam 18 de
  42 blocos e os 238 dos outros ocupam os 42; em contrapartida, 79%
  dos polígonos de especialistas dentro da área da ciência cidadã
  estão a menos de 500 m de um ponto dele (33% para os outros).
- O desenho aprovado avalia "nos registos dos outros observadores"
  (238 pontos, da mesma fonte). Os polígonos de especialistas são
  independentes do iNaturalist.
- Há dados para o teste. Polígonos por distância ao ponto de ciência
  cidadã mais próximo (0–1 / 1–5 / 5–20 / >20 km): TNE dentro do
  distrito 1 641 / 109 / 99 / 0; TNE fora do distrito 2 / 5 / 160 /
  56; notTNE 0 / 0 / 23 / 375. "Perto" = 1 643 polígonos; "longe" no
  mesmo ficheiro = 429; mais 398 no resto do país.
- Em quilómetros perde-se a distinção entre "é longe" e "a paisagem é
  diferente"; aceito, porque a comparação entre representações fica
  direta e o mapa de confiança cobre parte dessa leitura.
- Qualquer resultado é informativo: sem degradação, um observador
  dedicado chega (liga à curva plana da RQ1); com degradação, há
  motivo para testar correções.

**Em aberto (a definir antes de correr):**
- O enunciado proposto só substitui o aprovado se o orientador
  concordar.
- **Tamanho dos polígonos, o principal risco.** Os de perto são
  minúsculos (mediana 0,008 ha no distrito, cerca de um píxel) e os de
  longe 20 a 40 vezes maiores (0,26 ha no TNE fora do distrito, 0,16
  ha no notTNE). Manchas maiores são mais fáceis, o que pode esconder
  degradação. Comparar dentro de classes de tamanho, e ver se sobram
  polígonos suficientes em cada uma.
- "Perto" é onde o modelo treinou (especialistas e Observador A
  visitaram os mesmos sítios): é um limite otimista.
- ROC-AUC e Boyce precisam de pontos de fundo também nas faixas de
  longe, fora do distrito.
- Fixar antes de correr o que conta como "amplifica" e como "atenua".
- Risco de teto como na RQ1; os 69 pontos dos outros observadores
  fora dos blocos do Observador A são o teste mais difícil de reserva.
- Custo, não verificado: embeddings TESSERA e Sentinel-2 fora da caixa
  do piloto. A comparação depende do braço Sentinel-2, adiado.
- Mapa de confiança: Meyer & Pebesma só testaram regressão com Random
  Forest; aqui indica suporte, não exatidão.

**Fundamentação:** Meyer & Pebesma (2021) para o método; Ratsakatika
et al. (2026, preprint) aplicam-no a um modelo com embeddings mas
declaram como limitação que a exatidão fora da área não foi testada.
Da releitura integral (2026-11-11): em Ratsakatika et al. a vantagem
do TESSERA sobre o Sentinel estreita-se com um tampão de 10 km mas
nunca se inverte; em Meyer & Pebesma a área de aplicabilidade é
binária, depende do desenho da validação cruzada, e o mapa contínuo
de erro é um passo à parte com apoio fraco (R² médio 0,21).
Não encontrei precedente com ciência cidadã concentrada num observador
(pesquisa rápida, não revisão): possível contributo. Resumos em
[`docs/literature.md`](../docs/literature.md#spatial-validation). As
contagens são verificação minha, ad-hoc (script não guardado).

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq3--transferability-away-from-the-sampled-area).

**Na tese:** ❌ Superada (ver a Revisão abaixo); a RQ3 atual está na
secção 1.2 da Introdução desde 2026-11-17.

**Revisão (2026-11-13, revisão de consistência):** estado:
substituída. O desenho desta proposta foi reduzido na
[simplificação do desenho](#simplificacao-desenho-2026-11-13) à
experiência perto contra longe e ao mapa de confiança, e a pergunta é
hoje a RQ3 da [renumeração](#renumeracao-perguntas-2026-11-13). O texto acima fica como registo.

### Formulação das perguntas como pergunta → objetivo geral → objetivos específicos → hipóteses {#formulacao-pergunta-objetivos-hipoteses}

*Proposta minha (a confirmar com o orientador). Reescreve enunciados
que ele aprovou; os aprovados valem até ele responder. Na fila da
[próxima reunião](../docs/meetings/2026-11-17.md). Estado:
substituída a 2026-11-13 (Revisão no fim).*

**O que decidi (como proposta):** reescrever a pergunta principal e as
três RQ na estrutura de um guia de escrita de teses (tesify.pt):
pergunta com verbo interrogativo, variáveis e contexto delimitado; um
objetivo geral; cinco objetivos específicos no infinitivo e
mensuráveis; hipóteses em par nula/alternativa. A estrutura é regra
permanente em `CLAUDE.md` ("Formulating Research Questions"). O texto
está em
[`docs/research_questions.md`](../docs/research_questions.md#main-question-and-objectives)
(em inglês, como esse ficheiro e a tese) e em português no ponto da
reunião.

**Porquê:** os enunciados atuais não tinham objetivos nem hipóteses
escritos de forma falsificável, e a pergunta principal não dizia a
espécie, a área nem o termo de comparação. O conteúdo não muda, só a
forma, com duas exceções: a RQ3 usa a redação da
[proposta de redesenho](#rq3-proposta-redesenho-diagnostico-primeiro),
e a RQ2 passa a ser a da
[proposta da máscara de segmentação](#rq2-proposta-mascara), que
substitui a pergunta da redução de dados.

**Enunciados aprovados (registados aqui desde 2026-11-11, quando
`docs/research_questions.md` passou a mostrar só a formulação nova,
marcada "a confirmar"; repõem-se se o orientador não a aceitar):**
- **Principal:** "How robust and data-efficient are Earth Observation
  foundation models for invasive plant mapping when trained with
  citizen-science reference data?" Hipótese: os foundation models
  podem dar representações mais eficientes em dados, mas a vantagem
  pode ser limitada pela qualidade, quantidade e distribuição espacial
  dos dados de ciência cidadã.
- **RQ1:** "To what extent do Earth Observation foundation-model
  representations improve invasive plant mapping over conventional
  spectral-temporal satellite features when trained on citizen-science
  labels, and how much performance is gained by progressively adding
  costlier expert reference data on top of it?"
- **RQ2:** "How does the performance of EO foundation models compare
  with conventional approaches as citizen-science reference data are
  reduced by a filter that keeps the most recent and most reliable
  observations?"
- **RQ3:** ver [RQ3 aprovada](#rq3-aprovada).

**Em aberto:**
- A hipótese H₁b da RQ1 (o desempenho aumenta com a fração de dados de
  especialistas) foi escrita depois de a curva com TESSERA já ter
  saído plana, compatível com H₀b. Dizê-lo na tese.
- Hipóteses de trabalho, não testes estatísticos formais (só cinco
  divisões espaciais); confirmar com o orientador, e escrever o
  critério de decisão de cada uma antes de correr.

**Fundamentação:** guia de escrita (site comercial), não literatura
científica. Serve para a forma, não é para citar.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#main-question-and-objectives);
`CLAUDE.md`.

**Na tese:** ✅ Parcial. A secção 1.2 de
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(2026-11-17) segue esta estrutura: pergunta principal, quatro
perguntas, objetivo geral e objetivos específicos; as hipóteses ficam
para o Proposed Work (4.3.4).

**Revisão (2026-11-13, revisão de consistência):** estado: a
reescrita proposta nesta entrada foi substituída pela
[reformulação em quatro perguntas](#reformulacao-quatro-perguntas) e
pela [renumeração](#renumeracao-perguntas-2026-11-13). Os enunciados aprovados pelo orientador que esta entrada
regista valem até ele responder, e a regra de formulação do
`CLAUDE.md` mantém-se.

### RQ2: proposta — a máscara de segmentação passa a ser a pergunta {#rq2-proposta-mascara}

*Proposta minha, de 2026-11-11 (a confirmar com o orientador).
Substitui uma pergunta que ele aprovou; a aprovada está em
[Formulação das perguntas](#formulacao-pergunta-objetivos-hipoteses) e
vale até ele responder. Substitui também a minha decisão de 2026-11-10
("recência = distância a 2023").*

**O que decidi (como proposta):**

- **Enunciado:** "Em que medida estender o rótulo de cada observação
  de ciência cidadã à mancha de vegetação à sua volta altera o
  desempenho do mapeamento de *A. dealbata*, em comparação com treinar
  só no píxel observado?"
- **Hipóteses:** H₀: o desempenho é igual com e sem máscara. H₁: é
  diferente. Nos dois sentidos de propósito: mais píxeis por
  observação podem ajudar, e píxeis errados podem prejudicar.
- **Três condições de treino:** só o píxel observado, crescimento de
  região e superpíxeis, as duas regras sobre os embeddings TESSERA.
  Duas regras chegam para as "várias abordagens" que o orientador
  pediu: decisão minha, fechada, não é pergunta para ele.
- **Dois níveis de dados:** as 2 465 presenças e uma subamostra ao
  acaso de 150 (6%).
- **Só muda o treino.** Teste, fundo, Random Forest, blocos de 10 km e
  cinco sementes são os da RQ1. Só com TESSERA.
- **Um conjunto de parâmetros fixo por regra**, fundamentado e
  declarado como limitação, sem calibração.
- **Comparação entre as duas regras descritiva**, com o número de
  píxeis que cada uma acrescenta por observação.
- **Fica de fora:** a redução de dados como pergunta, a regra dos
  polígonos da COS, e a comparação das máscaras com os polígonos de
  especialistas.

**Porquê substituir a pergunta da redução de dados:**

1. **O filtro de recência não se aguentava.** Todas as presenças
   estão a 2 anos ou menos de 2023 (3,7% no próprio ano, 57,4% a ±1
   ano), e o filtro de perturbação não encontrou nenhuma ardida.
   "Remover as mais distantes" seria só separar 2021 e 2025 do resto.
   Além disso misturava quantidade e composição e dava uma só curva,
   sem repetições.
2. **A redução ao acaso contribuía pouco.** Resolvia os problemas do
   ponto 1, mas a curva da RQ1 está no teto, por isso o resultado
   provável era "não muda até níveis muito baixos", e repetia Ball et
   al. (2026).
3. **A máscara já era obrigatória e não pertencia a nenhuma
   pergunta.** O orientador disse que é central. Vai no sentido
   contrário de reduzir dados: tira mais de cada observação, que é o
   que a proposta pede (objetivo 1 e a parte de "dados limitados" do
   objetivo 2). O trabalho total diminui, e a RQ2 deixa de depender do
   braço Sentinel-2.

**Porquê este desenho:**

- **Nível de 150 presenças:** com todos os dados o modelo já está no
  teto, e a máscara serve para tirar mais de cada observação; é com
  poucas que pode mostrar efeito. Um nível com propósito, não uma
  curva.
- **Sem a regra da COS:** só cobre cerca de 18% dos pontos, é a que
  tem menos apoio na literatura e fica circular com a validação
  independente, que usa a mesma classe da COS.
- **Sem comparar com os polígonos de especialistas:** 70% dos 1 925
  polígonos na zona das observações são mais pequenos do que um píxel
  de 10 m (mediana 80 m²); cerca de 400 têm mais de 1 000 m² e
  concentram 94% da área. Só 22 pontos de ciência cidadã caem dentro
  de um polígono (17 polígonos), o que dá uma ilustração e não uma
  medida.
- **Só TESSERA:** as duas regras são calculadas sobre os embeddings, e
  a pergunta é sobre os rótulos, não sobre a representação.

**Em aberto:**
- Os valores dos parâmetros de cada regra (os do teste com 30 pontos
  não estão fundamentados).
- O critério de decisão da hipótese, a escrever antes de correr.
- Risco de resultado nulo mesmo com 150 presenças.
- Fuga entre treino e teste: cortar os píxeis da máscara que caiam num
  bloco de teste ou sobre um ponto de fundo.
- A proximidade a 2023 fica como limitação declarada no desenho
  temporal, não testada.

**Fundamentação:** Rivier et al. (2024) e Raine et al. (2022) para os
superpíxeis; Zhang et al. (2021) para o crescimento de região a
partir de rótulos pontuais à escala do Sentinel-2. Da releitura
integral (2026-11-11): Zhang et al. (2021) crescem pela confiança de
um classificador, não por semelhança à semente, e sem raio máximo,
por isso esses dois elementos da minha regra não têm precedente
encontrado; em Raine et al. os superpíxeis sobre features aprendidas
ganham pouco aos de cor; Rivier e Raine usam muitos pontos por imagem,
corretamente colocados. Zhang et al. (2025), que eu citava, saiu da
lista: o crescimento de região só refina a orla de uma mancha já
mapeada. Não encontrei trabalho que junte propagação de ponto para
mancha, pontos de ciência cidadã e embeddings congelados: possível
contributo. Não fiz pesquisa nova para esta proposta; resumos em
[`docs/literature.md`](../docs/literature.md#weak-supervision-from-point-labels).
As contagens são verificação minha, ad-hoc (scripts não guardados),
sobre `inat_dealbata_clean.csv` e `expert_polygons_clean.gpkg`.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq2--from-point-observations-to-reference-data);
regras e testes iniciais em
[Máscara de segmentação](#máscara-de-segmentação-testar-várias-abordagens).

**Na tese:** ✅ Parcial. O enunciado da RQ2 (máscara e filtros) está
na secção 1.2 da Introdução desde 2026-11-17, a confirmar com o
orientador; o desenho fica para o Proposed Work.

### Reformulação em quatro perguntas, centrada na substituição dos dados de especialistas {#reformulacao-quatro-perguntas}

*Decisão minha, de 2026-11-13 (a confirmar com o orientador). Os
enunciados que ele aprovou valem até ele responder e continuam
registados na entrada da
[formulação anterior](#formulacao-pergunta-objetivos-hipoteses).*

**O que decidi:** reorganizar as perguntas para ficarem no âmbito da
proposta de tese (`docs/thesis-proposal.md`).

- **Pergunta principal:** passa a ser sobre a substituição: em que
  medida as observações de ciência cidadã, transformadas em dados de
  referência e representadas por embeddings de foundation models,
  podem substituir os dados de referência de especialistas no
  mapeamento de *A. dealbata* no distrito de Coimbra.
- **Quatro perguntas, numeradas pela ordem dos objetivos da
  proposta:**
  - RQ1, dos pontos aos dados de referência: efeito dos filtros de
    qualidade e da máscara de segmentação (era a RQ2 da máscara, mais
    os filtros).
  - RQ2, ciência cidadã como substituto dos dados de especialistas: a
    curva de redução de esforço (era metade da RQ1).
  - RQ3, foundation models contra features convencionais: TESSERA
    contra Sentinel-2, com todas as observações e com poucas (era a
    outra metade da RQ1).
  - RQ4, transferibilidade para longe da área amostrada (era a RQ3).
- **Prioridade:** RQ2 e RQ1 primeiro; RQ3 e a parte da RQ4 que depende
  do Sentinel-2 depois.
- **Filtros (H₀b da RQ1):** versão barata, com duas condições (sem os
  filtros de qualidade contra todos os filtros), sem ablação passo a
  passo. A janela 2021–2025 é fixa nas duas condições. Assumo que
  "filtros de qualidade" são os passos 1 a 3 do pipeline (coordenadas
  escondidas, precisão, grau de qualidade).
- **Critério de decisão comum:** conta como mudança quando a média das
  diferenças de ROC-AUC por semente é maior do que o seu desvio-padrão
  e tem o mesmo sinal em pelo menos quatro das cinco sementes. O Boyce
  é reportado e não decide.
- **Fica de fora, como limitação declarada:**
  - Ruído: não testo se os foundation models compensam o ruído dos
    rótulos; a RQ3 usa só dados de ciência cidadã limpos.
  - Outras acácias: não testo se o modelo separa a *A. dealbata* das
    outras espécies de *Acacia*; fica como trabalho futuro no
    objetivo 5.

**Porquê:**
- O centro da proposta é reduzir a dependência de dados de referência
  caros usando ciência cidadã; os foundation models são o meio. A
  pergunta principal anterior punha no centro a comparação TESSERA
  contra Sentinel-2, que a proposta não pede explicitamente e que
  depende do braço Sentinel-2, parado.
- A RQ1 anterior juntava duas perguntas com hipóteses separadas.
  Separadas, o resultado da curva deixa de esperar pelo Sentinel-2.
- O objetivo 1 da proposta ("investigar métodos" para transformar os
  pontos) não tinha pergunta; a máscara e os filtros respondem-lhe.
- O ruído e as outras acácias ficam de fora pela quantidade de
  trabalho que já tenho: o teste do ruído depende do Sentinel-2, e o
  âmbito de uma só espécie já está justificado em
  [Só *Acacia dealbata*](#só-acacia-dealbata).

**Fundamentação:** nenhuma literatura consultada. É o ajuste das
perguntas à proposta de tese, na forma do guia de escrita já adotado.
O critério de decisão não tem fonte externa; foi escrito depois de
ver a curva da RQ2 (ver
[RQ2: curva por fonte](#rq2-curva-por-fonte)).

**Em aberto:** o que variam as cinco sementes na RQ4; os parâmetros
das regras da máscara.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#main-question-and-objectives).
As entradas anteriores deste ficheiro usam a numeração antiga (RQ1
curva e comparação, RQ2 máscara, RQ3 concentração).

**Na tese:** ❌ Superada pela renumeração (Revisão abaixo); a versão
atual das quatro perguntas está na secção 1.2 da Introdução desde
2026-11-17.

**Revisão (2026-11-13, mais tarde no mesmo dia):** a numeração das
perguntas mudou. O que nesta entrada é a "RQ1" (dos pontos aos dados
de referência) passa a ser a RQ2, e a "RQ2" (curva de redução de
esforço) passa a ser a RQ1; a RQ3 e a RQ4 não mudam. Passei a numerar
por ordem de importância, o que também fica mais perto da numeração
que o orientador aprovou. Mudou também a hipótese dos filtros: deixa
de ser "passos 1 a 3" e passa a ser só os filtros de grau e de
precisão (passos 2 e 3), para não exigir embeddings novos. O critério
de decisão comum já tinha sido retirado na entrada seguinte. Ver
[Renumeração das perguntas](#renumeracao-perguntas-2026-11-13).

**Revisão (2026-11-13, ao fim do dia):** depois do bloco acima a RQ3
e a RQ4 trocaram: a transferibilidade é a RQ3 e a comparação com o
Sentinel-2 é a RQ4. Ver a [tabela de numeração](#decisões).

**Revisão (2026-11-14):** a pergunta principal passa a dizer que a
ciência cidadã substitui os dados de especialistas "como dados de
treino", porque o desenho continua a usá-los como teste. Ver
[Pergunta principal](#pergunta-principal-dados-de-treino).

### Simplificação do desenho: uma só pergunta com Sentinel-2, sem limiar de decisão {#simplificacao-desenho-2026-11-13}

*Decisão minha, de 2026-11-13 (a confirmar com o orientador). Ajusta
a [reformulação em quatro perguntas](#reformulacao-quatro-perguntas)
e a entrada da [curva por fonte](#rq2-curva-por-fonte), do mesmo dia.*

**O que decidi:**
1. **Só a RQ3 depende do Sentinel-2.** A comparação da descida
   perto–longe entre representações (amplifica ou atenua) passa da
   RQ4 para a RQ3, como segunda hipótese. A RQ4 fica só com TESSERA e
   pode correr sem o Sentinel-2.
2. **RQ4 reduzida** à experiência perto contra longe nos polígonos de
   especialistas e ao mapa de confiança. A comparação entre
   observadores (238 contra 238), o desbaste espacial e a segunda
   região saem do desenho; ficam como trabalho futuro.
3. **Filtros da RQ1 só com todas as observações**, sem o nível de 150
   presenças. A máscara mantém os dois níveis e as duas regras.
4. **Boyce só reportado.** Não vou reimplementá-lo (curva P/E, janela
   móvel), ao contrário do que tinha ficado em
   [Métricas](#metricas-limites-boyce); os limites ficam declarados.
5. **Sem limiar de decisão.** As hipóteses mantêm-se, medidas pela
   diferença de ROC-AUC emparelhada por semente, reportada com média,
   desvio-padrão e número de sementes com o mesmo sinal. Deixo de
   escrever "cumpre" ou "não cumpre". Substitui o critério comum das
   duas entradas acima.
6. **RQ2 curta no design doc**, com os valores aqui em baixo; e o
   notebook da curva passa a ter uma só corrida, com os dados atuais,
   sem as secções da corrida com todos os anos.

**Porquê:**
- Com duas perguntas a depender do Sentinel-2, o risco de ele não
  arrancar atingia metade do plano.
- Os filtros são a parte mais cara da RQ1 (exigem extrair embeddings
  novos) e a que menos responde à proposta.
- O Boyce mudou de 0,930 para 0,969 só com a troca do fundo; não
  justifica mais trabalho numa métrica que não decide.
- O limiar foi escrito depois de ver a curva, dava respostas
  diferentes conforme o nível comparado (falhava aos 90%, passava aos
  20%–50%) e assentava em cinco sementes que reutilizam blocos.
  Reportar as diferenças é mais simples e mais defensável.

**O que se perde:** uma regra de decisão explícita por hipótese; a
resposta sobre o observador dominante; a medição do efeito dos
filtros com poucos dados.

**Valores da curva da RQ2** (TESSERA, presenças de 2021–2025, fundo
novo, uma corrida, média de cinco sementes; RF = Random Forest, LR =
Logistic Regression):

| % polígonos | RF ROC-AUC, global | RF ROC-AUC, só especialistas | RF ROC-AUC, só ciência cidadã | LR ROC-AUC, global | RF Boyce, global | RF Boyce, só especialistas |
|---|---|---|---|---|---|---|
| 0 | 0,902 | 0,976 | 0,812 | 0,893 | 0,995 | 0,970 |
| 10 | 0,906 | 0,986 | 0,810 | 0,910 | 0,995 | 0,963 |
| 20 | 0,907 | 0,988 | 0,810 | 0,917 | 0,995 | 0,958 |
| 30 | 0,907 | 0,990 | 0,807 | 0,920 | 0,998 | 0,957 |
| 40 | 0,907 | 0,991 | 0,806 | 0,921 | 0,985 | 0,960 |
| 50 | 0,907 | 0,992 | 0,805 | 0,923 | 0,993 | 0,952 |
| 60 | 0,906 | 0,991 | 0,802 | 0,923 | 0,993 | 0,949 |
| 70 | 0,908 | 0,992 | 0,807 | 0,923 | 0,995 | 0,959 |
| 80 | 0,907 | 0,992 | 0,804 | 0,923 | 0,978 | 0,958 |
| 90 | 0,906 | 0,993 | 0,801 | 0,924 | 0,993 | 0,940 |
| 100 (só especialistas) | 0,854 | 0,994 | 0,677 | 0,873 | 0,969 | 0,961 |

Diferenças emparelhadas por semente, face a 0%:
- **RF, teste global:** cerca de +0,005 em todos os níveis de 10% a
  90%. Aos 20% é +0,005 (dp 0,003), positiva nas cinco sementes; aos
  90% é +0,004 (dp 0,005), positiva em quatro.
- **RF, só especialistas, aos 90%:** +0,017 (dp 0,005), nas cinco
  sementes. O Boyce desce de 0,970 para 0,940 (em três sementes; igual
  em duas); com 10 janelas toma poucos valores distintos.
- **LR, teste global, aos 90%:** +0,031 (dp 0,007), nas cinco
  sementes.
- **A 100%:** a queda no teste global vem das presenças de teste de
  ciência cidadã (0,812 → 0,677).
- **Fiabilidade:** cada semente testa em 2 a 4 blocos de 10 km com
  polígonos; 9 blocos distintos nas cinco sementes, 6 deles em duas.
  Nas sementes 1 e 3 um só bloco dá 472 dos 523 e dos 557 píxeis de
  teste de especialistas.

**Fundamentação:** nenhuma literatura consultada; são decisões de
âmbito e de forma de reportar.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#secondary-questions);
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).

**Na tese:** ✅ Parcial. A pergunta única (RQ4) está na secção 1.2 da
Introdução desde 2026-11-17; Proposed Work e resultado preliminar por
escrever.

**Revisão (2026-11-13, mais tarde no mesmo dia):** a numeração das
perguntas mudou. O que nesta entrada é a "RQ1" (dos pontos aos dados
de referência) passa a ser a RQ2, e a "RQ2" (curva de redução de
esforço) passa a ser a RQ1; a RQ3 e a RQ4 não mudam. Passei a numerar
por ordem de importância, o que também fica mais perto da numeração
que o orientador aprovou. Mudaram também dois pontos desta entrada. No
ponto 3, os filtros da RQ2 passam a ser só os de grau e de precisão,
com os embeddings já guardados, por isso deixam de exigir extração
nova. No ponto 2, a experiência perto contra longe fica definida com
"longe" só dentro do distrito e com contagens novas. Ver
[Renumeração das perguntas](#renumeracao-perguntas-2026-11-13).

**Revisão (2026-11-13, ao fim do dia):** depois do bloco acima a RQ3
e a RQ4 trocaram: a transferibilidade é a RQ3 e a comparação com o
Sentinel-2 é a RQ4. Ver a [tabela de numeração](#decisões).
No ponto 1, a segunda hipótese (a queda de perto para longe ser igual
nas duas representações) saiu nessa troca; ver a Revisão do fim do dia
na [renumeração](#renumeracao-perguntas-2026-11-13).

### Renumeração das perguntas por ordem de importância; desenho das RQ2 e RQ4 fechado {#renumeracao-perguntas-2026-11-13}

*Decisão minha, de 2026-11-13, por mérito do desenho: proposta (a
confirmar com o orientador). Ajusta a
[reformulação em quatro perguntas](#reformulacao-quatro-perguntas) e a
[simplificação do desenho](#simplificacao-desenho-2026-11-13), do
mesmo dia. Os enunciados que ele aprovou valem até ele responder.*

**O que decidi:**

- **Numeração por ordem de importância.** A pergunta principal, o
  objetivo geral e o conteúdo das quatro perguntas mantêm-se; os
  objetivos específicos 1 e 2 trocam com as perguntas.

  | Aprovada pelo orientador | Numeração da manhã de 2026-11-13 | Nova |
  |---|---|---|
  | RQ1, parte da curva de redução de esforço | RQ2 | **RQ1** |
  | RQ2, redução de dados por filtro (a máscara é proposta minha de 2026-11-11, sem resposta) | RQ1 | **RQ2** |
  | RQ1, parte TESSERA contra Sentinel-2 | RQ3 (H₀a) | **RQ3** (H₀a) |
  | RQ3, concentração espacial da amostragem | RQ4, e RQ3 (H₀b) | **RQ4**, e **RQ3** (H₀b) |

- **O que se reporta, numa frase comum a todas as hipóteses:** a
  diferença emparelhada por semente (média, desvio-padrão, sementes
  com o mesmo sinal). Reporta-se a diferença e não se decide por
  limiar, porque há cinco sementes e elas reutilizam blocos. Cada
  hipótese fica marcada como escrita antes ou depois do resultado: só
  a H₁ da RQ1 é posterior.
- **1. H₀b da RQ2, "filtros de grau e de precisão".** Só os passos 2
  e 3 do pipeline (precisão até 30 m e grau *research*), na versão que
  não exige embeddings novos. A condição "sem filtros" junta os 1 120
  píxeis que já têm embedding guardado; as 2 observações sem embedding
  saem dessa condição. As 12 observações de coordenadas escondidas
  ficam sempre fora, por isso o passo 1 não é medido.
- **2. Máscara (H₀a da RQ2):** depende de extrair as janelas TESSERA
  à volta das observações, que não estão guardadas. Essa extração fica
  por aprovar antes de correr; não extraí nada.
- **3. RQ4:** "longe" são só os polígonos do distrito a mais de 1 km;
  as presenças de teste são todos os píxeis de especialistas, que
  nunca treinam o modelo só de ciência cidadã. As cinco sementes
  variam os blocos de teste, como na RQ1, sem mecanismo novo.
- **4. Contagens da RQ4:** 1 645 polígonos perto e 206 longe (ver
  Contagens). Os valores 1 643 e 429 saem dos docs de desenho. A RQ4
  reporta a diferença sem atribuir a causa à distância.
- **5. Configuração da máscara, uma por regra, fixada antes de correr
  e sem afinar nos resultados:**
  - Crescimento de região: semelhança de cosseno ao píxel observado de
    pelo menos 0,90; 4 vizinhos; no máximo 5 píxeis (50 m) do píxel
    observado em cada eixo, ou seja, no máximo 121 píxeis.
  - Superpíxeis: SLIC numa janela de 41 × 41 píxeis, tamanho médio de
    25 píxeis (67 segmentos), `compactness` 0,1.
  - A conectividade é a do código do notebook (4 vizinhos). A entrada
    [Máscara de segmentação](#máscara-de-segmentação-testar-várias-abordagens)
    diz "8 vizinhos"; vale o notebook, e essa entrada fica como está.
- **6. Regra das hipóteses no `CLAUDE.md`:** "neutral and falsifiable"
  passa a admitir hipóteses enunciadas como diferença reportada,
  quando não se decide por limiar.
- **Leitura de "área de vegetação mais próxima":** extensão do rótulo
  à mancha de vegetação, por confirmar com o orientador.

**Porquê:**

- **Numeração:** a substituição dos dados de especialistas é o centro
  da proposta de tese e o único resultado já medido, por isso é a
  RQ1. A curva volta a ter o número que tem no manuscrito, nas
  entradas antigas deste ficheiro e nos nomes dos dados
  (`rq1_pilot`, `rq1_background`).
- **H₀b sem embeddings novos:** a extração de 20 de outubro foi feita
  antes dos filtros de grau e de precisão, por isso quase todos os
  píxeis que esses filtros retiram já têm embedding. As observações
  de coordenadas escondidas têm a posição baralhada pela plataforma;
  medir esse passo exigiria embeddings novos em sítios errados.
- **"Longe" só no distrito:** os 221 polígonos do TNE fora do distrito
  não têm embedding guardado.
- **Todos os píxeis de especialistas como teste:** se o teste ficasse
  só nos blocos de teste, quase não haveria polígonos "perto", porque
  os pontos de ciência cidadã desses blocos saem do treino.
- **50 m e 25 píxeis:** 50 m é a zona de exclusão do fundo à volta das
  presenças, por isso a regra do crescimento de região não rotula
  como acácia um píxel que possa ser sorteado como fundo; fica muito
  abaixo dos 300–500 m a que o variograma dos embeddings estabiliza.
  25 píxeis é a mesma escala (50 m × 50 m). O limiar 0,90 e a
  `compactness` 0,1 vêm do teste com 30 pontos, onde só vi contagens
  de píxeis, não desempenho.

**Contagens (2026-11-13, feitas ad hoc sobre os ficheiros existentes,
sem script guardado):**

- **Filtros, na janela 2021–2025:** 4 145 observações de
  *A. dealbata*; saem 12 de coordenadas escondidas, 1 437 pelo grau
  (1 334 *casual*, 103 *needs_id*) e 116 pela precisão; ficam 2 580.
  As 1 553 dos dois filtros acrescentam 1 122 píxeis aos 2 465; 1 120
  têm embedding válido no conjunto `tessera_v1.1_2023_rq1_pilot`.
- **Perto e longe:** distância de cada polígono à presença mais
  próxima das 2 465. Até 1 km: 1 645 polígonos (1 643 no distrito).
  A mais de 1 km no distrito: 206, entre 1,0 e 8,2 km (mediana
  4,8 km). A mais de 1 km no TNE fora do distrito: 221. Com embedding
  guardado: 1 252 polígonos perto (1 982 píxeis) e 205 longe (789
  píxeis).
- **Diferença para os valores anteriores:** a contagem antiga (1 643
  perto, 429 longe no mesmo ficheiro) vinha de um script não guardado.
  A de hoje dá 1 645 e 427 no mesmo ficheiro; não sei a causa da
  diferença.
- **Tamanho e ocupação do solo, no distrito:** área mediana de 77 m²
  perto e 2 788 m² longe. Classe da COS 2023: "floresta de acácias"
  55,6% perto e 59,2% longe; pinhal 23,7% e 10,2%. As contagens por
  semente (só com os pontos de treino) ainda não foram feitas.

**O que se perde:** a medição do passo das coordenadas escondidas; os
polígonos de fora do distrito na RQ4, onde "longe" não passa de
8,2 km. Continuam como limitações declaradas: não testo se os
foundation models compensam o ruído dos rótulos, e a incerteza de cada
observação só entra pelo filtro de precisão e pela máscara, não no
modelo.

**Fundamentação:** nenhuma literatura nova consultada. Os valores da
máscara, o corte de 1 km e o desenho das sementes da RQ4 são
raciocínio meu, sem fonte: Rivier et al. (2024) não dão um parâmetro
utilizável neste caso e Zhang et al. (2021) crescem pela confiança de
um classificador, sem raio máximo (resumos em
[`docs/literature.md`](../docs/literature.md#weak-supervision-from-point-labels)).

**Em aberto:** aprovar a extração das janelas TESSERA para a máscara;
as contagens de perto e longe por semente; a resposta do orientador à
reformulação e à leitura de "área de vegetação mais próxima".

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#secondary-questions);
[`docs/meetings/2026-11-17.md`](../docs/meetings/2026-11-17.md).

**Na tese:** ✅ Parcial. As quatro perguntas, com esta numeração e
esta redação, estão na secção 1.2 de
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
desde 2026-11-17 (substituíram os três enunciados aprovados; a
confirmação pelo orientador continua pendente). Hipóteses e desenho
ficam para o Proposed Work.

**Revisão (2026-11-13, ao fim do dia).** Decisão minha, por mérito do
desenho: proposta (a confirmar com o orientador).

- **O que mudou:** a RQ3 e a RQ4 trocam de número, e a comparação com
  o Sentinel-2 fica reduzida a uma hipótese.

  | Nesta entrada | Agora |
  |---|---|
  | RQ3, TESSERA contra Sentinel-2 (H₀a e H₀b) | **RQ4**, só com a comparação direta nos dois níveis de dados (todas as presenças e 150) |
  | RQ4, transferibilidade | **RQ3**, com o mesmo desenho (decisões 3 e 4 acima) |

  Os objetivos específicos 3 e 4 trocam com as perguntas. A RQ1 e a
  RQ2 não mudam.
- **O que saiu:** a segunda hipótese da comparação de representações
  (a queda de perto para longe ser igual com TESSERA e com
  Sentinel-2). A curva de redução de esforço também não é repetida
  com o Sentinel-2.
- **Critério da numeração:** deixa de ser a ordem de importância. Cada
  pergunta só usa o que as anteriores definem, e a única que depende
  do Sentinel-2 vem no fim.
- **Porquê:** quero o Sentinel-2 o mais tarde possível, porque o braço
  está parado pelo custo da extração. Assim a RQ1, a RQ2 e a RQ3
  fazem-se e escrevem-se só com o TESSERA, e se o Sentinel-2 nunca
  correr perco só a última pergunta. Na ordem anterior a RQ3 tinha uma
  hipótese que dependia de uma experiência só definida na RQ4. Tirar
  essa hipótese evita extrair Sentinel-2 também nos píxeis de
  especialistas.
- **O que se perde:** a parte "amplificam ou atenuam" da pergunta
  sobre concentração espacial que o orientador aprovou deixa de ser
  testada; a RQ3 mede a queda só com o TESSERA. Sem a RQ4 a tese não
  pode afirmar que os foundation models melhoram face às features
  convencionais, só descrever o desempenho com eles.
- **Fundamentação:** nenhuma literatura nova consultada; é organização
  das perguntas e âmbito.
- **Onde:** [`docs/research_questions.md`](../docs/research_questions.md#secondary-questions);
  [`docs/meetings/2026-11-17.md`](../docs/meetings/2026-11-17.md).
- **Na tese:** ⏳ Ainda não aplicada, como o resto desta entrada.

**Revisão (2026-11-13, depois da revisão de consistência).** Na
decisão 3, as presenças de teste da RQ3 deixam de ser "todos os píxeis
de especialistas": saem os 21 que são também píxel de uma presença de
ciência cidadã. O resto da entrada não muda. Ver
[Revisão de consistência](#revisao-consistencia-2026-11-13).

**Revisão (2026-11-13, segunda parte da revisão de consistência).**
Três correções ao texto acima, sem mudar o desenho:

- **Variograma:** onde digo que os 50 m ficam "muito abaixo dos
  300–500 m a que o variograma dos embeddings estabiliza", a leitura
  certa é entre 500 m e 1 km (ver a Revisão na
  [zona-tampão](#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)).
  Os 50 m continuam muito abaixo.
- **Limite de 50 m da máscara:** o limite de 5 píxeis é por eixo, por
  isso os cantos da janela de 11 × 11 ficam a 71 m do píxel
  observado. A frase "não rotula como acácia um píxel que possa ser
  sorteado como fundo" só vale ao longo dos eixos; não contei quantos
  pontos de fundo ficam entre 50 m e 71 m de uma presença.
- **Resultados da curva:** estão em `results/effort_reduction_curve/`
  ([script da curva](#curva-script-experiments)).

**Revisão (2026-11-17, mapa da espécie).** Decisão minha. O quinto
objetivo específico ("produzir o mapa de *A. dealbata* da área de
estudo, com mapa de confiança") deixa de ser objetivo e passa a
produto do segundo semestre. **Porquê:** era o único objetivo sem
pergunta nem hipótese associada, e a estrutura adotada liga cada
objetivo específico a uma RQ; o mapa mantém-se porque a proposta pede
classificadores de mapeamento e o mapa de confiança já está desenhado
na RQ3, mas sem verdade de terreno para toda a área só pode ser
apresentado como previsão do modelo, não como mapa validado.
**Fundamentação:** Meyer & Pebesma (2021) para o mapa de confiança; o
resto é raciocínio meu. **Onde:**
[`docs/research_questions.md`](../docs/research_questions.md#main-question-and-objectives);
na tese, 4.1 (Proposed Approach) e o plano do segundo semestre, ainda
não escritos.

### Revisão de consistência de 2026-11-13: ajustes ao desenho e limpeza {#revisao-consistencia-2026-11-13}

*Decisão minha, de 2026-11-13: proposta (a confirmar com o
orientador) no que toca ao desenho da RQ3 e da RQ2; o resto é limpeza
do repositório.*

**O que decidi:**

- **RQ3, conjunto de teste:** ficam de fora os 21 píxeis de
  especialistas que são também píxel de uma presença de ciência
  cidadã. O teste fica com 1 251 polígonos perto (1 961 píxeis) e 205
  longe (789 píxeis), com embedding guardado.
- **RQ2, limitação declarada:** o fundo foi sorteado com zona de
  exclusão de 50 m só à volta das presenças filtradas. Na condição sem
  filtros, um ponto de fundo pode ficar a menos de 50 m de uma
  presença acrescentada; não reconstruo o fundo por isso.
- **RQ1, denominador:** o doc de desenho passa a dizer que as
  percentagens da curva são sobre os 1 457 polígonos com pelo menos um
  píxel com embedding, dos 1 849 do distrito.
- **Números corrigidos nos docs de desenho:** 56% (não 54%) dos
  polígonos do distrito em "Florestas de acácias"; Observador A em 15
  de 39 blocos na grelha das experiências (EPSG:32629), em vez de 18
  de 42 (EPSG:3763); 1 645 polígonos perto, dos quais 1 643 no
  distrito; no passo 1 do pipeline, 43 são observações de *Acacia* de
  todas as espécies; o variograma dos embeddings ainda sobe aos
  400–500 m e estabiliza entre 500 m e 1 km.
- **Notebooks marcados:** `other_plants_observations` como histórico e
  fora da ordem de execução; `segmentation_mask` como protótipo, com
  parâmetros diferentes dos da RQ2. Nenhum foi corrido de novo.
- **`forest_only_background_check`, secção 5:** reescrita com os
  valores das corridas de 2026-11-13.

**Porquê:**

- **21 píxeis:** uma presença de ciência cidadã no mesmo píxel tem o
  mesmo embedding que o píxel de especialistas. Se ela treinar o
  modelo, o teste "perto" inclui píxeis vistos no treino. Os 21 estão
  todos no grupo "perto", em 15 polígonos.
- **Fundo da RQ2:** reconstruir o fundo mudava a curva da RQ1 e exigia
  embeddings novos; a regra de fuga já tira os pontos no mesmo píxel.
- **Números:** os valores anteriores misturavam conjuntos (todos os
  polígonos e só os do distrito) ou grelhas (EPSG:3763 e EPSG:32629).
- **Scripts:** já não corriam. Liam
  `inat_dealbata_clean_2021_2025.csv`, que não existe, e variáveis que
  o notebook da curva deixou de ter.
- **Notebooks:** o desenho atual usa fundo uniforme, não classes de
  outras plantas, e as saídas do `other_plants_observations` são das
  3 000 presenças de todos os anos.

**O que os dados não dizem:** quantos pontos de fundo ficam de facto a
menos de 50 m de uma presença sem filtro; não contei.

**Fundamentação:** nenhuma literatura consultada. Raciocínio meu, sem
fonte, sobre contagens feitas ad hoc nos ficheiros existentes, sem
script guardado.

**Em aberto:** a leitura do variograma no notebook e nas entradas da
[zona-tampão](#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)
e da [renumeração](#renumeracao-perguntas-2026-11-13) ainda diz
300–500 m.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#secondary-questions);
[`docs/methodology.md`](../docs/methodology.md#validation);
[`notebooks/README.md`](../notebooks/README.md);
[`results/README.md`](../results/README.md).

**Na tese:** ⏳ Ainda não escrita (Metodologia).

**Revisão (2026-11-13, segunda parte).** O ponto em aberto (leitura do
variograma) ficou fechado, e fiz mais o seguinte:

- **Variograma:** corrigi a leitura no notebook e acrescentei Revisões
  na [zona-tampão](#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)
  e na [renumeração](#renumeracao-perguntas-2026-11-13).
- **Pureza dos rótulos:** corrigi a célula do teste sem as presenças
  isoladas e voltei a corrê-la; resultado na Revisão dos
  [diagnósticos](#diagnosticos-curva-plana).
- **Numeração:** a [tabela de numeração](#decisões) substitui o parágrafo que lá estava, e as
  entradas com numeração intermédia ganharam uma Revisão.
- **Origem do desenho da curva:** a ata de 2026-11-05 regista a ideia
  do orientador (começar só com ciência cidadã e acrescentar
  especialistas aos poucos, uma vez por representação, TESSERA
  primeiro). A unidade de mistura, a ordem aninhada, o teste fixo e as
  cinco sementes são meus. O `research_questions.md` dizia "Design
  (supervisor)"; passou a separar as duas coisas.
- **Fila da reunião:** acrescentei a "O que muda face ao que aprovou"
  que a curva deixa de ser repetida com o Sentinel-2.
- **Divergências do manuscrito** (não mexi no manuscrito):
  - A tabela de problemas da Introdução diz que o fundo é "built from
    other-species observations"; hoje são pontos aleatórios uniformes.
  - A mesma tabela cita `ball2026` para "imprecise locations and
    mixed pixels"; do que li, Ball et al. tratam parcelas com espécies
    misturadas, não erro de posição.
  - A secção Contributions fala de uma "cumulative ablation" dos
    passos de limpeza; a RQ2 compara só com e sem os filtros de grau e
    de precisão.
  - A mesma secção dá como candidato a contributo o cruzamento entre
    o que os observadores fotografam (plantas de sub-bosque) e o que
    o satélite vê, um passo das outras plantas, sem uso ativo desde
    2026-11-10. A máscara de segmentação não é referida.
  - O capítulo de Resultados diz "no experiment has been run"; a
    curva da RQ1 já correu.
  - Em `references.bib`, `feng2025` está como documento de 2025 (o
    TESSERA saiu no CVPR 2026) e `karasiak2022` como depósito HAL (o
    artigo saiu na *Machine Learning*).

**Na tese (atualizado na segunda parte):** ⏳ Ainda não escrita
(Metodologia). As divergências acima ficam por corrigir quando eu
pedir alterações ao manuscrito. As de `references.bib` foram
corrigidas a 2026-11-17.

**Revisão (2026-11-13, terceira parte).** Duas coisas que as partes
anteriores davam como não contadas ou sem script.

- **Contagens do desenho:** saem agora de
  [`design_counts.ipynb`](../notebooks/05_data_integration/design_counts.ipynb),
  que reproduz todos os valores citados no `research_questions.md`
  (polígonos com embedding, o que os filtros retiram, perto e longe,
  os 21 píxeis partilhados).
- **Máscara, 50 m a 71 m:** 1 dos 2 000 pontos do fundo uniforme cai
  dentro da janela de 11 × 11 de uma presença; nenhum no fundo só de
  floresta. Decisão minha, proposta (a confirmar com o orientador): um
  ponto de fundo que a máscara rotule como acácia sai do fundo dessa
  condição, a aplicar quando a máscara correr. Sem literatura
  consultada; raciocínio meu.
- **Ficheiros derivados:** ver a Revisão em
  [Ficheiros derivados](#manifesto-ficheiros-derivados).

### Pergunta principal: a ciência cidadã substitui os dados de especialistas como dados de treino {#pergunta-principal-dados-de-treino}

*Decisão minha, de 2026-11-14 (a confirmar com o orientador). Ajusta
a pergunta principal da
[reformulação em quatro perguntas](#reformulacao-quatro-perguntas);
os enunciados que ele aprovou valem até ele responder.*

**O que decidi:**
- Acrescentar "as training data" à pergunta principal e ao objetivo
  geral: em que medida as observações de ciência cidadã podem
  substituir os dados de referência de especialistas **como dados de
  treino**.
- Escrever no contexto comum que 90% das presenças são de um
  observador.
- Definir "substituir": é a diferença de desempenho entre modelos
  treinados com ciência cidadã e modelos treinados com dados de
  especialistas. Os dados de especialistas continuam a ser a
  referência de teste.

**Porquê:**
- O desenho continua a precisar dos dados de especialistas para
  testar (teste global da RQ1, teste da RQ3). O que a ciência cidadã
  substitui é o treino; "substituir os dados de especialistas", sem
  mais, prometia mais do que o desenho mostra.
- A proposta de tese diz o mesmo: usar as observações "to create
  training data".
- "Ciência cidadã" neste caso é sobretudo uma pessoa. Fica dito no
  contexto da pergunta, não só nos riscos.

**O que os dados mostram:** 2 227 das 2 465 presenças (90,3%) são do
Observador A (`inat_dealbata_clean.csv`, coluna `observer`).

**Fundamentação:** nenhuma literatura consultada; raciocínio meu, a
partir da proposta de tese e do desenho.

**Impacto:** só a redação. Nenhuma experiência, hipótese ou número
muda. As RQ1 a RQ4 ficam como estão.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#main-question-and-objectives);
`README.md`; `docs/literature.md` (Contribution);
[próxima reunião](../docs/meetings/2026-11-17.md).

**Na tese:** ✅ Parcial. O Abstract
([`6-abstract-EN.tex`](document/frontmatter/6-abstract-EN.tex),
2026-11-17) já usa esta formulação (ciência cidadã a reduzir a
dependência dos dados de especialistas, com a formulação do objetivo da
proposta em vez de "substituir"). A Introdução (secção 1.2,
2026-11-17) tem a pergunta principal com "replace" e a sua leitura
como diferença de desempenho; o Resumo em português já está escrito
(`6-abstract-PT.tex`). A 2026-11-18 a leitura de "replace" na
secção 1.2 passou a "measured on the same held-out locations, which
hold presences from both sources", o parágrafo do fluxo e a figura
da secção 1.2 deixaram de chamar "test reference" aos polígonos de
especialistas, e a secção 2.2.2 do Background diz que as duas fontes
são dados de referência (Revisão abaixo).

**Revisão (2026-11-18).** A frase "os dados de especialistas
continuam a ser a referência de teste" estava errada quando foi
escrita e sai. O teste da RQ1 junta sempre as duas fontes (ponto 4 da
[curva completa](#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos)
e ponto 1 da [curva presence-only](#curva-presence-only)), e os
polígonos de especialistas entram no treino de 0% a 100%. Só a RQ3
testa apenas em píxeis de especialistas, e a RQ2 testa no conjunto
filtrado de ciência cidadã. O que se mantém: "substituir" é a
diferença de desempenho entre treinar com ciência cidadã e treinar com
especialistas. Regra para a redação: as duas fontes são dados de
referência; nenhuma tem um papel fixo de treino ou de teste, e cada
pergunta diz o seu conjunto de teste. Erro apanhado por mim ao ler a
secção 2.2.2 do Background. Corrigido em
[`docs/research_questions.md`](../docs/research_questions.md#main-question-and-objectives)
(contexto comum, "What replace means here") e nas secções 1.2 e
2.2.2 da tese.

## Decisões: dados de referência

### Usar os dados de especialistas, com limpeza

*Decisão minha depois de os ver no QGIS; a exclusão dos
`classifica = 0` é decisão do orientador (por mensagem).*

**O que decidi:** os dados de especialistas são de confiança e são
usados. Contam só os polígonos com `classifica = 1`. Limpeza: tirar as
11 linhas sem `classifica` e os 5 013 `classifica = 0`; corrigir as
geometrias inválidas. Ficam 2 470 polígonos, todos presenças.

**Porquê:**
- Vistos no QGIS, os polígonos estão onde devem. São de 2023, feitos no
  campo e sobre o OrtoSat (resposta do orientador). A forma estranha
  vem da segmentação da imagem; a correção das geometrias não muda a
  área.
- Os `classifica = 0` são áreas de não acácia que não devem entrar no
  estudo (orientador): 44% estão em áreas artificiais, e usá-los faria
  o modelo aprender "árvore vs. edifício". Deixa de haver ausências
  dos especialistas; o lado negativo passou a ser o
  [fundo partilhado](#rq1-fundo-uniforme-nao-cos).

**Revisão (2026-11-18, decisão minha):** a ideia de usar os
`classifica = 0` que caem em vegetação como ausências verificadas só
na avaliação (levada à reunião de 2026-11-17, sem resposta registada)
fica fechada: não se usam em nenhuma fase, nem no treino nem na
avaliação. A exclusão decidida acima mantém-se inteira; a avaliação da
RQ1 passou a presence-only (sensitivity a área fixa, ver
[RQ1 passa a presence-only](#rq1-presence-only)), que não precisa de
ausências. Sem fonte nova; a pergunta deixa de ir ao orientador.

**Como a COS foi usada:** quem diz se há *A. dealbata* é o rótulo do
professor; a classe da COS num ponto dentro do polígono é só
informativa. A COS mapeia manchas de pelo menos 1 ha, por isso um
segmento de 75 m² recebe a classe dominante desse hectare.

**Onde:** [`notebooks/03_expert_reference/expert_polygons.ipynb`](../notebooks/03_expert_reference/expert_polygons.ipynb);
ficheiro e colunas em
[`data/README.md`](../data/README.md#expert-reference-polygons-cleaned-derived).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia).

### Só observações *research*, nos dois lados

*Decisão minha.*

**O que decidi:** no modelo principal, as observações do iNaturalist
são só as *research*. Presenças de *A. dealbata*: saem as *casual*
(1 678) e as *needs_id* (123); das 5 242 ficam 3 441. A mesma regra
foi aplicada às outras plantas (110 576 → 60 630), hoje sem uso ativo.

**Porquê:**
- *Research* quer dizer identificação confirmada pela comunidade (pelo
  menos duas pessoas concordam), com foto, data, localização e
  organismo selvagem.
- As nossas *casual* são quase todas observações sem foto: 1 670 das
  1 679 do distrito (contagem na API do iNaturalist). Ninguém consegue
  confirmar a identificação.
- 98% das *casual* são do Observer A, sobretudo de 2021. Ao tirá-las,
  o peso dele desce de 90% para 87%.
- As *needs_id* têm foto, mas a identificação ainda não foi confirmada.
- Ficam 3 441 presenças, o que chega para treinar.

**Trabalho futuro:** verificação de sensibilidade, treinando com e sem
as *casual* e *needs_id*. Recuperam-se do ficheiro original.

**Fundamentação:** Gillespie et al. (2024) e Brown et al. (2025)
usaram só observações *research*. Só as *research* são enviadas para o
GBIF. Não encontrei um estudo que compare usar ou não as *casual*
(pesquisa rápida).

**Onde:** passo 11 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb);
tabela do pipeline, passo 3.

**Na tese:** ✅ Parcial. Mencionada em resumo na Introdução (secção
Contributions); o que é o *research grade* e o precedente de Gillespie
et al. e Brown et al. estão na secção 2.4.1 do Background
(2026-11-18); a decisão e as contagens ficam para a Metodologia.

### Precisão da localização: tirar acima de 30 m, manter as sem valor

*Decisão minha, depois de um teste.*

**O que decidi:** saem as observações com `positional_accuracy`
conhecida acima de 30 m (3 píxeis). As que não têm valor ficam,
marcadas com `accuracy_missing`. Presenças: 3 441 → 3 276.

**Porquê:**
- A `positional_accuracy` é o raio (m) do círculo onde está a planta.
  Com um raio grande, o ponto pode cair no píxel errado.
- 80% das presenças não têm valor, e quase todas são do Observer A
  (90% das observações dessa pessoa, contra 11% dos outros). "Sem
  valor" é a forma como esta pessoa regista, não "mal localizada".
- **Teste:** que parte de cada grupo cai num acacial da COS 2023 (se
  fossem pontos ao acaso, 2,3%):

  | Precisão | Presenças | % em acacial | % em acacial (só outros observadores) |
  |---|---|---|---|
  | ≤ 10 m | 429 | 20,7% | 10,5% |
  | 10–30 m | 104 | 14,4% | 10,0% |
  | 30–100 m | 91 | 6,6% | 6,7% |
  | > 100 m | 74 | 10,8% | 6,3% |
  | sem valor | 2 743 | 18,6% | 12,2% |

  As sem valor caem em acaciais quase tanto como as mais precisas:
  ficam. Nos outros observadores, até 30 m dá o mesmo que ≤ 10 m; a
  partir de 30 m desce para cerca de 6,5%. Por isso o limite é 30 m e
  não 100 m.
- A diferença de dados é pequena: com 30 m saem 165 presenças (4,8%),
  com 100 m sairiam 74 (2,2%).

**Limitações:** teste indireto. A COS só mapeia manchas de acácia com
pelo menos 1 ha, por isso compara grupos e não confirma cada ponto. Os
grupos com valor são pequenos (74 a 429) e a ordem não é perfeita.

**Fundamentação:** o limiar de 30 m vem do meu teste com a COS.
Filtrar pela incerteza posicional tem precedente em Brown et al.
(2025), com ≤10 m, e Gillespie et al. (2024), com ≤120 m para imagens
de 256 m. Corrigido em 2026-11-11: eu citava Ball et al. (2026), que
não têm dados pontuais nem limiar de precisão posicional.

**Onde:** passo 12 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb);
tabela do pipeline, passo 2.

**Na tese:** ✅ Parcial. Mencionada em resumo na Introdução; o que é a
`positional_accuracy` e os limiares de Brown et al. (10 m) e Gillespie
et al. (120 m) estão na secção 2.4.1 do Background (2026-11-18); o
teste e o limiar de 30 m ficam para a Metodologia.

**Revisão (2026-11-15):** a tabela acima é das 3 441 observações
*research* de todos os anos, porque o filtro dos anos (passo 13) vem
depois deste. Repeti o teste só com as de 2021–2025, que são as usadas
nas experiências, para a tabela da tese ser do conjunto atual. A
decisão não muda.

- **Critério, escrito antes de correr:** manter os 30 m se, nos outros
  observadores, ≤ 10 m e 10–30 m ficassem parecidos e os grupos acima
  de 30 m abaixo deles; e se as sem valor não ficassem claramente
  abaixo das de ≤ 10 m.
- **Resultado** (2 696 observações *research* de 2021–2025, antes do
  filtro de precisão e de uma por píxel; Observer A 88,5%; pontos ao
  acaso 2,3%):

  | Precisão | Presenças | % em acacial | Só outros observadores | % em acacial (só outros) |
  |---|---|---|---|---|
  | ≤ 10 m | 344 | 23,3% | 175 | 10,9% |
  | 10–30 m | 89 | 15,7% | 36 | 13,9% |
  | 30–100 m | 61 | 8,2% | 26 | 7,7% |
  | > 100 m | 55 | 12,7% | 45 | 6,7% |
  | sem valor | 2 147 | 18,0% | 28 | 10,7% |

- **Leitura:** a primeira condição cumpre-se. Nos outros observadores,
  acima de 30 m a proporção continua a descer (7,7% e 6,7%, contra
  10,9% e 13,9%). Para a segunda, o critério não dizia o que é
  "claramente", e isso é uma falha dele. A distância das sem valor às
  de ≤ 10 m aumentou (de 2,1 para 5,3 pontos). Mantenho-as porque
  continuam acima do grupo de 10–30 m (15,7%), que o filtro deixa
  passar, e muito acima do acaso. Esta leitura foi feita depois de
  ver os números.
- **Limitações:** os grupos dos outros observadores são ainda mais
  pequenos (26 a 175); a ordem continua imperfeita (> 100 m, 12,7%,
  acima de 30–100 m, 8,2%).
- **O que não mudou:** o notebook correu de ponta a ponta e os três
  ficheiros que escreve (`inat_dealbata_clean.csv`,
  `acacia_cleaning_counts.csv`, `rq2_sample_150_seed0.csv`) saíram
  iguais byte a byte.
- **Fundamentação:** nenhuma literatura nova.
- **Onde:** passo 12 de
  [`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb),
  logo a seguir à tabela de todos os anos.
- **Na tese:** ⏳ Ainda não escrita (Metodologia, ainda esqueleto); a tabela a usar lá é esta, de 2021–2025.

### Janela temporal das observações: só 2021–2025 {#janela-temporal-2021-2025}

*Decisão minha, de 2026-11-13. Não levada ao orientador: dou-a por
resolvida (2026-11-17).*

**O que decidi:**
- Todas as presenças de *A. dealbata* são tratadas como representativas
  do povoamento de 2023, o ano das variáveis preditoras.
- Para sustentar esse pressuposto, ficam só as observações de
  2021–2025 (2023 ± 2 anos).
- O filtro é um passo da limpeza: depois das validações de cada
  observação (data, coordenadas, espécie, grau de qualidade, precisão
  da localização) e antes de "uma observação por píxel" e da marca de
  fogo.
- Rejeitei 2021–2026 e 2020–2026.

**Porquê:**
- Quanto mais longe de 2023 está a observação, mais fraca é como
  evidência de que o povoamento estava lá em 2023.
- 2026 fica de fora nas duas alternativas rejeitadas: o ano estava
  incompleto no download (2026-09-22), e uma observação depois dos
  incêndios de 2025 pode ser rebrota.

**Contagens:**

| Passo | Antes | Depois | Observador A depois |
|---|---|---|---|
| Sem data | 7 943 | 7 941 | — |
| Coordenadas escondidas | 7 941 | 7 898 | 83,5% |
| Só *A. dealbata* | 7 898 | 5 242 | 90,2% |
| Só *research* | 5 242 | 3 441 | 86,9% |
| Precisão ≤ 30 m ou sem valor | 3 441 | 3 276 | 89,1% |
| Só 2021–2025 | 3 276 | 2 580 | 90,7% |
| Uma por píxel de 10 m | 2 580 | 2 465 | 90,3% |

- Ficam **2 465 presenças**, 2 227 do Observador A (90,3%) e 238 dos
  outros.
- O filtro tira 696 observações: 594 anteriores a 2021 (575 delas de
  2019–2020) e 102 de 2026.
- Nenhuma presença fica com a marca de fogo. 704 presenças (28,6%)
  estão em áreas ardidas em 2025.
- Para o nível de 150 presenças da
  [proposta da RQ2](#rq2-proposta-mascara), o sorteio é
  `sample(150, random_state=0)` sobre o ficheiro limpo (6,1% das
  presenças; 90,7% do Observador A; todas com embedding válido).

**Em aberto:** o efeito da distância a 2023 dentro da janela não é
testado.

**Fundamentação:** tratar observações de vários anos como um ano de
referência tem precedente em Ball et al. (2026) e Gillespie et al.
(2024). Para a largura da janela (± 2 anos) não li nenhuma fonte: é
raciocínio meu. A persistência dos povoamentos também não tem fonte
lida; uma pesquisa rápida em 2026-11-13 não encontrou uma medição
publicada, e Riveiro et al. (2025) só apoia que o fogo não elimina a
espécie.

**Onde:** passo 13 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb);
ficheiro e contagens em
[`data/README.md`](../data/README.md#inaturalist-observations-cleaned-derived);
desenho em
[`docs/research_questions.md`](../docs/research_questions.md#temporal-design-adopted);
sorteio das 150 em `results/tables/rq2_sample_150_seed0.csv` (local,
fora do git).

**Na tese:** ⏳ Ainda não escrita (Metodologia).

### Uma observação por píxel; nos conflitos fica a presença

*Decisão minha.*

**O que decidi:** uma presença por píxel de 10 m (grelha UTM 29N,
EPSG:32629). Quando há várias, fica a mais próxima de 2023 (em empate,
a mais recente). 2 580 → 2 465. Nos píxeis com uma *A. dealbata* e
outras plantas, ficou a presença (regra do tempo do multiclasse, hoje
sem efeito).

**Porquê:**
- O modelo vê píxeis, não pontos: duas observações no mesmo píxel têm
  o mesmo embedding e são o mesmo exemplo repetido.
- 99% das presenças repetidas eram do Observer A, quase todas do mesmo
  ano (registos repetidos da mesma visita).
- Fica a mais próxima de 2023 porque todas as observações são tratadas
  como 2023.

**Fundamentação:** raciocínio meu; não encontrei fonte. Corrigido em
2026-11-11: eu citava Karasiak et al. (2022), mas o artigo trata da
dependência entre treino e teste e nunca fala de amostras repetidas
no mesmo píxel.

**Onde:** passo 14 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb);
[`src/grid.py`](../src/grid.py); tabela do pipeline, passo 8.

**Na tese:** ✅ Parcial. Mencionada em resumo na Introdução; o detalhe
fica para a Metodologia.

### Observer A: todas as observações no modelo principal

*Decisão minha.*

**O que decidi:** no modelo principal ficam todas as observações do
Observer A (90% das 2 465 presenças). Não limito o número por
quadrícula na preparação dos dados.

**Porquê:**
- O efeito do Observer A é o que a RQ3 testa. Limitá-lo já no modelo
  principal deixava a RQ3 sem o caso de comparação.
- As observações repetidas da mesma visita já saíram no passo "uma por
  píxel".
- Limitar já cortava muitos dados antes de saber se a concentração
  muda o resultado.

**Fundamentação:** raciocínio meu, a partir do desenho da RQ3. Apoio
parcial: Dimson et al. (2023) recomendam incluir todos os dados
disponíveis, e Phillips et al. (2009) dizem que descartar registos é
pouco aceitável quando são poucos. Nenhum trata de um observador
dominante. O grupo de Cambridge, que a tabela do pipeline citava,
descreve agrupamento de locais, não de observadores.

**Onde:** tabela do pipeline, passo 9;
[RQ3](../docs/research_questions.md#rq3--transferability-away-from-the-sampled-area).

**Na tese:** ✅ Parcial. A estatística do Observer A já está na
Introdução (que diz 88%; o valor é 90%, por atualizar); a decisão fica
para a Metodologia.

### Máscara de segmentação: testar várias abordagens

*Decisão do orientador (por mensagem). A regra concreta está por
definir por mim.*

**O que decidi:**
- **Orientador:** a máscara é um ponto central da tese, e vou
  experimentar várias abordagens. Definir uma regra para considerar a área de
  vegetação mais próxima da observação.
- **Minha leitura (a confirmar com ele, na fila da próxima reunião):**
  "considerar a área de vegetação" lê-se como estender o rótulo do
  ponto à mancha à volta, e não só levar a coordenada para dentro da
  vegetação mais próxima. Ele escreveu "área", não "píxel" ou "ponto".
- **Três candidatas:** crescimento de região nos embeddings TESSERA;
  superpíxeis sobre os embeddings (ideia de Rivier et al., não o
  método completo deles, que treina uma rede de segmentação sobre
  imagem RGB sub-métrica); polígonos "Florestas de acácias" da COS
  2023 onde o ponto cai dentro de um.
- **Testado numa amostra de 30:**
  - Crescimento de região (cosseno ao píxel-semente, 8 vizinhos, raio
    máximo 20 px/200 m, limiar 0,90; parâmetros não calibrados):
    3/33/962 píxeis (mín/mediana/máx). A cauda superior bate no limite
    do raio, sinal de limiar permissivo demais nalguns casos.
  - Superpíxeis (SLIC, `n_segments=100`, `compactness=0,1`, não
    fundamentados): 10/22/64 píxeis. Mais consistente, mas só porque o
    número de segmentos limita o tamanho por construção. A propagação
    por voto maioritário (a proposta real de Rivier et al.) não foi
    exercitada: a amostra tem um ponto por patch.
- **Para janeiro:** apresentar as regras, fundamentadas, com a
  comparação planeada. Comparar com e sem máscara fica para depois.
- **Atualização (2026-11-11):** proponho que a máscara passe a ser a
  RQ2, com duas regras (crescimento de região e superpíxeis); a dos
  polígonos da COS sai da comparação. Ver
  [proposta](#rq2-proposta-mascara).

**Porquê:**
- A coordenada do iNaturalist nem sempre cai em cima da planta.
- Por ser central, comparar várias regras pode ser um resultado da
  tese.

**Fundamentação:** o orientador indicou Rivier et al. (2024). Li o
artigo e procurei trabalhos do género; resumos e comparação em
[`docs/literature.md`](../docs/literature.md#weak-supervision-from-point-labels).
Nenhum trabalho junta o nosso caso (poucos pontos de ciência cidadã,
embeddings congelados, regra de "vegetação mais próxima"): a técnica
não é inédita, mas esta combinação mantém-se como possível contributo.

**Onde:** [`docs/meetings/2026-11-04.md`](../docs/meetings/2026-11-04.md);
[`notebooks/05_data_integration/segmentation_mask.ipynb`](../notebooks/05_data_integration/segmentation_mask.ipynb).

**Na tese:** ⏳ Ainda não escrita (Metodologia). A Introdução não
refere a máscara; ver a [revisão de consistência](#revisao-consistencia-2026-11-13).

**Revisão (2026-11-13, revisão de consistência):** a linha "Na tese"
dizia que a máscara estava referida na secção Contributions da
Introdução como candidato a contributo. Não está: o candidato que lá
aparece é outro passo (plantas de sub-bosque contra o que o satélite
vê). Corrigi a linha.

### Ficheiros derivados: manifesto de `data/processed/` e construção do fundo num só sítio {#manifesto-ficheiros-derivados}

*Decisão minha, de 2026-11-13. É organização do repositório, não uma
escolha metodológica: o desenho do fundo não muda.*

**O que decidi:**

- **Manifesto.** `data/processed_manifest.csv` tem uma linha por
  ficheiro de `data/processed/` (67: os dois fundos e os 65 blocos do
  piloto), com o hash do ficheiro, a data, quem o construiu, as
  entradas na forma `caminho@sha256`, a semente e os parâmetros.
- **Um só sítio constrói os fundos:**
  `notebooks/05_data_integration/background_pools.ipynb`, com o código
  em `src/background.py`. Saiu dos notebooks de modelação
  (`one_class_method_selection` e `forest_only_background_check`), que
  só construíam o ficheiro se ele não existisse.
- **Regra de reconstrução.** O notebook volta sempre a sortear os
  pontos a partir das entradas atuais. Se forem os guardados, mantém
  os embeddings e só atualiza o manifesto. Se forem outros, pára: são
  precisos embeddings novos, o que é uma leitura remota e só corre
  com uma opção que eu ligo.
- **Quem lê o fundo verifica primeiro.** Os sete notebooks que usam um
  fundo carregam-no com `load_background`, que compara o hash do
  ficheiro e o de cada entrada com o manifesto e pára se algum não
  bater.

**Porquê:** a 2026-11-13 descobri que o fundo uniforme tinha a zona de
exclusão feita à volta das 3 000 presenças de todos os anos, quando as
presenças já eram as 2 465 de 2021–2025
([Fundo uniforme reconstruído](#fundo-uniforme-reconstruido-2465)).
Nenhum notebook deu por isso, porque "só construir se não existir"
reutiliza o ficheiro seja qual for a entrada. A regra "Derived files"
do `CLAUDE.md` proíbe isso; esta é a forma de a cumprir.

**O que verifiquei (2026-11-13):**

- **Fundo uniforme:** os 2 000 pontos sorteados outra vez com a
  semente 42 e as entradas atuais são exatamente os guardados.
- **Fundo só de floresta:** igual, com a semente 0.
- Por isso nenhum dos dois foi reescrito: os hashes são os mesmos de
  antes (`4bb2ee42…` e `2211909f…`) e não houve extração nem
  download.
- **Curva (RQ1):** voltei a correr `effort_reduction_curve.ipynb` com
  o carregamento novo. Os sete ficheiros de resultados ficaram idênticos byte a
  byte aos anteriores. Nenhum valor mudou.
- **Números citados nos docs:** os da curva, o 0,874 contra 0,836 e os
  do fundo de floresta (0,950 e 0,952) batem com os resultados e as
  saídas atuais.

**Limites:**

- Os blocos do piloto foram lidos a 2026-10-20 por um notebook que já
  não existe; as entradas ficam como desconhecidas. Cada embedding
  pertence a um píxel e não depende das presenças escolhidas, por isso
  o manifesto regista só o hash atual.
- O ficheiro dos polígonos é um GeoPackage, cujos bytes podem mudar ao
  ser reescrito com o mesmo conteúdo. Nesse caso a verificação pára, e
  correr `background_pools.ipynb` resolve em segundos, sem extração.
- Os outros seis notebooks ficaram com a célula de carregamento nova e
  as saídas das execuções de 2026-11-13 (depois das 03:50), feitas com
  as mesmas entradas; não voltei a corrê-los.
- Ficam de fora: os downloads de dados brutos "só se não existir"
  (não dependem das presenças), os ficheiros de `data/interim/` (os
  notebooks reescrevem-nos sempre; entram no manifesto como entradas),
  e `results/tables/rq2_sample_150_seed0.csv` (a tratar quando a RQ2
  correr).

**Fundamentação:** nenhuma literatura consultada; é prática de
reprodutibilidade, raciocínio meu.

**Onde:** [`data/processed_manifest.csv`](../data/processed_manifest.csv);
[`background_pools.ipynb`](../notebooks/05_data_integration/background_pools.ipynb);
`src/background.py`; `src/manifest.py`;
[`data/README.md`](../data/README.md#tessera-embeddings--rq1-background-pool-2026-11-13).

**Na tese:** ⏳ Ainda não escrita. Se entrar, é uma frase sobre
reprodutibilidade na Metodologia.

**Revisão (2026-11-13, ao fim do dia):** dois ficheiros que esta
entrada deixava de fora ou com entradas desconhecidas.

- **Amostra de 150 presenças:** já não fica "a tratar quando a RQ2
  correr". É sorteada no fim do `acacia_observations.ipynb`, com
  semente 0, sempre que o ficheiro das presenças é gravado. O ficheiro
  que sai é igual ao que estava guardado, byte a byte.
- **Embeddings do piloto: declarados, não extraídos de novo.** Comecei
  a extraí-los outra vez para os tornar reproduzíveis e cancelei:
  são cerca de 2 h de leitura remota para confirmar valores que já
  tenho. Uso o conjunto tal como foi extraído a 2026-10-20.
  - A escolha dos pontos não se pode refazer: o notebook original não
    está no histórico do Git, e 21 700 dos 29 021 pontos (os negativos
    do desenho antigo) não saem de nenhum ficheiro atual.
  - A lista dos pontos passa a estar versionada
    (`data/tessera_rq1_pilot_points.csv`), e há um notebook que relê
    os embeddings a partir dela.
  - Verificação parcial: os 14 blocos relidos antes de cancelar
    (3 360 pontos) saíram idênticos aos guardados. Os outros 51 não
    foram verificados. O critério que tinha escrito antes de correr
    (aceitar só com os 65 idênticos) não chegou a ser aplicado, e o
    manifesto fica como estava.
- **Onde:** [`data/README.md`](../data/README.md#tessera-embeddings-2023-rq1-pilot-points);
  [`tessera_pilot_embeddings.ipynb`](../notebooks/04_satellite/tessera_pilot_embeddings.ipynb).
- **Na tese:** ⏳ Ainda não escrita; se entrar, é uma frase de limitação na Metodologia (ainda esqueleto).

**Revisão (2026-11-14):** *decisão minha.* Deixo de verificar os
embeddings do piloto e dou o conjunto guardado como certo. Os ficheiros
não tinham como mudar: cada bloco tem o hash no manifesto, e os
notebooks verificam-no antes de ler. Reler a fonte só mostrava que ela
devolve hoje os mesmos valores, o que não muda nenhum resultado. Antes
de parar, duas leituras parciais (13 e 14 de novembro) cobriram 33 dos
65 blocos (11 311 pontos), todos idênticos aos guardados. A lista dos
pontos e o notebook de releitura ficam.

## Decisões: RQ1, desenho e resultados

### Multiclasse abandonado; RQ1 passa a uma curva de redução de esforço (presença vs. fundo)

*Reunião presencial de 2026-11-05. Pontos 1 a 4: decisão do orientador.
Os restantes: decisão minha.*

**O que decidi:**
1. **Multiclasse abandonado nos dois modelos** (ciência cidadã e
   especialistas). Os dois têm só *A. dealbata* como alvo.
2. **RQ1 como curva de redução de esforço:** começa só com ciência
   cidadã e acrescenta progressivamente dados de especialistas, para
   encontrar o equilíbrio entre desempenho e esforço de recolha no
   terreno. O ponto 100% especialistas é o extremo da curva.
3. **A experiência corre uma vez por representação** (TESSERA, depois
   Sentinel-2), para a comparação entre representações não se
   confundir com a curva.
4. **Fase 1: só embeddings TESSERA.**
5. **Mistura aditiva:** a base de ciência cidadã fica fixa e os dados
   de especialistas são acrescentados por cima, por isso o N de treino
   cresce a cada nível. Reportar sempre o N total ao lado da
   percentagem.
6. **Fundo partilhado:** 2 000 pontos aleatórios uniformes na extensão
   dos embeddings do piloto, excluindo 50 m à volta de cada presença
   conhecida. N e raio são escolha minha; não confirmado pelo
   orientador. Ver
   [fundo partilhado](#rq1-fundo-uniforme-nao-cos).
7. **Método: presença vs. fundo com Random Forest.** O one-class
   verdadeiro foi testado em paralelo e descartado (abaixo).

**Porquê:**
- Usar outras plantas ou classes da COS como classes próprias exigiria
  construir ausências confirmadas à mão (interpretação visual, p. ex.
  do OrtoSat), o que o orientador não considera eficiente.
- A redução de esforço responde ao objetivo 1 da proposta: a curva
  mostra quanto desempenho se ganha por cada fração de dados de
  especialistas.
- A mistura aditiva corresponde à pergunta do orientador ("quanto
  esforço de campo compensa?"); trocar dados com N fixo responderia a
  outra pergunta.

**One-class verdadeiro: testado e descartado.**
- Isolation Forest contra one-class SVM, só com presenças de ciência
  cidadã, 5 divisões espaciais: SVM claramente melhor (ROC-AUC
  0,64–0,65 contra 0,57; Boyce 0,6–0,8 contra 0,25).
- One-class SVM contra presença vs. fundo, nos dois braços: perde nas
  duas métricas. Ciência cidadã: 0,654/0,816 (ROC-AUC/Boyce) contra
  0,842/0,989 do Random Forest. Especialistas: 0,911/0,868 contra
  0,990/0,954.
- Sob um [fundo só de floresta](#curva-fundo-so-floresta), o one-class
  SVM cai para perto do acaso (ROC-AUC 0,515, Boyce negativo a 0% de
  especialistas): parte do seu desempenho vinha de reconhecer "isto
  não é vegetação".
- A literatura aponta no mesmo sentido: em todas as comparações
  encontradas, um método one-class sem fundo foi o pior ou quase o
  pior, e nenhum método de avaliação só com presenças dispensa dados
  de fundo.
- **Decidido (2026-11-10):** o one-class SVM não volta a ser testado
  por omissão em braços futuros. Pode ser reaberto como diagnóstico
  pontual se um resultado parecer inesperado.

**Revisão (2026-11-17):** cláusula acima superada nesse ponto. O
orientador pediu, na reunião de 2026-11-17, para reabrir a comparação
one-class, porque a avaliação usada aqui (ROC-AUC e Boyce contra o
fundo) continuava a assumir que o fundo não tem acácia, mesmo
treinando os modelos só com presenças — o pressuposto que um one-class
deveria evitar. Ver
[nova entrada](#one-class-reaberto-avaliação-sem-fundo-sensitivity-grelha-espacial-e-ensemble-pca--isolation-forest).
O resto desta entrada (Random Forest presença-vs-fundo como
classificador principal da RQ1) não muda.

**Outras consequências:**
- **Outras plantas sem uso ativo (2026-11-10).** O conjunto fica
  documentado em
  [`data/README.md`](../data/README.md#inaturalist-observations-cleaned-derived)
  só como dado histórico.
- **Validação independente só com a COS (2026-11-10).** Uma amostra
  verificada à mão no OrtoSat foi riscada pela mesma razão de
  eficiência. Fica a comparação com a classe *Acacia* da COS 2023. A
  COS é independente dos polígonos de especialistas: estes vêm de
  visitas de campo e interpretação visual do OrtoSat, não da COS. Os
  54% de polígonos dentro da classe "Florestas de acácias" são mais
  provavelmente um sinal ecológico do que um artefacto.

**Fundamentação:** a decisão do orientador não tem literatura própria.
Para o one-class: pesquisa por resumos, sem texto completo lido (ver
[`docs/literature.md`](../docs/literature.md#one-class--positive-unlabeled-classification)).
A mistura aditiva é raciocínio meu.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq1--citizen-science-as-a-substitute-for-expert-data);
[`docs/meetings/2026-11-05.md`](../docs/meetings/2026-11-05.md);
[`one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb).

**Na tese:** ✅ Parcial. O desenho da RQ1 (curva, mistura aditiva) já
está resumido em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex);
o desenho operacional fica para a Metodologia, com um parágrafo breve
sobre o multiclasse e o one-class abandonados.

**Revisão (2026-11-13, revisão de consistência):** o ponto 3 (correr
a experiência uma vez por representação, decisão do orientador) deixou
de estar no desenho: na Revisão do fim do dia da [renumeração](#renumeracao-perguntas-2026-11-13) a curva deixa
de ser repetida com o Sentinel-2. É decisão minha e contraria o que
ele decidiu a 2026-11-05, por isso vale como proposta até ele
responder; está na fila da
[próxima reunião](../docs/meetings/2026-11-17.md), em "O que muda
face ao que aprovou".

**Revisão (2026-11-17):** não levei este ponto à reunião de
2026-11-17; dou-o por resolvido como decisão minha. Continua a
contrariar o que o orientador decidiu a 2026-11-05, e ele não
respondeu sobre isto.

**Revisão (2026-11-17, mais tarde no mesmo dia):** o ponto 7
(presença vs. fundo com Random Forest) ficou superado. O Random Forest
usa o fundo como pseudo-ausência e foi abandonado; o classificador da
curva passa a ser a regressão logística presença-fundo, com o fundo
como amostra não rotulada. A frase da primeira Revisão de 2026-11-17
("o resto desta entrada ... não muda") deixou de valer nesse ponto.
Os pontos 1, 2, 4, 5 e 6 mantêm-se. Ver
[RQ1 passa a presence-only](#rq1-presence-only).

### Classificador presença-vs-fundo (ciência cidadã): Random Forest, por agora

*Decisão minha, não confirmada pelo orientador. Superada a
2026-11-17 (Revisão no fim).*

**O que decidi:** Random Forest como classificador único da RQ1. A
Logistic Regression fica como referência barata.

**Resultado (ciência cidadã, blocos de 10 km, 5 divisões, fundo
partilhado):** Random Forest ROC-AUC 0,842 (dp 0,028), Boyce 0,989 (dp
0,022); Logistic Regression ROC-AUC 0,878 (dp 0,052), Boyce 0,973 (dp
0,042). Nenhum domina nas duas métricas.

**Porquê Random Forest:** é mais estável entre divisões espaciais, o
que importa mais do que um pequeno ganho médio de AUC quando o lado
dos especialistas só tem 18 blocos independentes; e tem apoio na
literatura, que a Logistic Regression não tem.

**Fundamentação:** Domingo et al. (2023), Random Forest para
presença/ausência de *A. dealbata*; Yang et al. (2026), sobre
embeddings. Corrigido em 2026-11-11, depois da releitura integral: o
apoio é mais fraco do que as "cinco citações" que eu contava. Em Ball
et al. (2026) o Random Forest é uma linha de base, abaixo de uma rede
pequena, e a Logistic Regression fica muito abaixo (macro F1 0,38
contra 0,55). Em Mouta et al. (2021) é um de oito classificadores
fundidos e fica em terceiro. Eskandari et al. (2025) saiu da lista
(só o resumo é acessível).

**Em aberto:** confirmar com o orientador; afinação de hiperparâmetros.

**Onde:** [`presence_background_citizen_science.ipynb`](../notebooks/07_foundation_models/presence_background_citizen_science.ipynb).

**Na tese:** ❌ Superada pela entrada
[RQ1 passa a presence-only](#rq1-presence-only); a Introdução ainda
não nomeia o classificador, por isso não há texto a corrigir.

**Revisão (2026-11-17): superada.** O Random Forest treinado com o
fundo como classe 0 é um classificador presença/ausência que usa o
fundo como pseudo-ausência (Rapinel & Hubert-Moy, 2021, em
`docs/literature.md`), não um método presence-only. Depois da reunião
de 2026-11-17 decidi que o classificador da RQ1 tem de ser
presence-only; o Random Forest passa a metodologia abandonada, com
esta razão objetiva. Ver
[RQ1 passa a presence-only](#rq1-presence-only). Os números da curva
obtidos com ele ficam válidos como registo do que foi medido, não como
resultado da RQ1.

### Braço de especialistas: one-class SVM e Random Forest confirmados (100% especialistas)

*Decisão minha, não confirmada pelo orientador.*

**O que decidi:** aplicar ao braço de especialistas (polígonos
`classifica = 1`, sem ciência cidadã) as escolhas feitas no braço de
ciência cidadã. Mesmo fundo, mesmas métricas, 5 divisões espaciais.

**Resultado:** one-class SVM ROC-AUC 0,911 (dp 0,037), Boyce 0,868 (dp
0,080); Random Forest 0,990 (dp 0,004) e 0,954 (dp 0,011); Logistic
Regression 0,990 (dp 0,003) e 0,879 (dp 0,086). O padrão mantém-se:
presença vs. fundo bate o one-class SVM, e o Random Forest bate a
Logistic Regression no Boyce com muito menos variância.

**Leitura (minha):** tudo pontua mais alto do que no braço de ciência
cidadã, mas isso não prova que o braço seja "melhor". As presenças de
especialistas são manchas contíguas com embeddings parecidos, e
separá-las de um fundo aleatório pode ser um problema geometricamente
mais fácil.

**Adaptação só neste braço:** os blocos de teste são sorteados só de
entre os blocos com presenças de especialistas (18); sorteá-los do
universo todo deixaria a maior parte das divisões sem presenças de
teste. Os blocos contam-se em EPSG:32629, como em todos os notebooks
com divisão espacial; a mesma grelha em EPSG:3763 dá 15.

**Em aberto:** confirmar com o orientador o fundo, o Random Forest e
esta adaptação.

**Onde:** [`expert_arm_classifiers.ipynb`](../notebooks/07_foundation_models/expert_arm_classifiers.ipynb).

**Na tese:** ❌ Superada no classificador: o Random Forest foi
abandonado a 2026-11-17 e os números desta entrada (ROC-AUC e Boyce
contra o fundo) deixam de contar como resultado; ficam como registo.
Ver [RQ1 passa a presence-only](#rq1-presence-only).

### One-class reaberto: avaliação sem fundo (sensitivity), grelha espacial e ensemble PCA + Isolation Forest

*Reunião com o orientador, 2026-11-17. A reabertura e a direção geral
(grelha espacial, sensitivity em vez de ROC-AUC, ensemble com
autoencoder e isolation forest, por só haver presenças e poucos dados
no braço de ciência cidadã) são decisão dele. A implementação concreta
abaixo é minha, escolhida pela opção mais simples em cada ponto em
aberto, não confirmada pelo orientador.*

**O que decidi:**

1. **Reabrir a comparação one-class** de
   [`one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb),
   descartada a 2026-11-10 (ver Revisão acima): essa comparação treinava
   os modelos só com presenças, mas avaliava-os com ROC-AUC e Boyce
   contra o fundo aleatório — continuava a assumir que o fundo não tem
   acácia.
2. **Métrica: sensitivity em presenças de teste, sem nenhum ponto de
   fundo na avaliação.** Limiar fixado antes de correr: percentil 90
   dos scores de anomalia no treino (10% de contaminação esperada),
   igual para todos os modelos — é o valor já testado em
   `one_class_method_selection.ipynb` (`contamination=0.1`/`nu=0.10`),
   não um valor novo.
3. **Divisão espacial: reaproveitar a grelha de 10 km já usada**
   (85 blocos cobrindo presenças e fundo), em leave-one-block-out sobre
   os blocos com presenças de ciência cidadã, em vez de uma grelha nova
   4x4 e em vez do sorteio aleatório de 20% em 5 sementes já usado
   nesse notebook. Mais simples de implementar (código já existe para
   os blocos) e mais exaustivo do que o sorteio (cada bloco serve de
   teste exatamente uma vez).
4. **Autoencoder = reconstrução por PCA**, com componentes suficientes
   para 90% da variância das presenças de treino, em vez de uma rede
   neuronal. É a forma mais simples de autoencoder (equivalência
   PCA/autoencoder linear, Baldi & Hornik, 1989) e a mais adequada a
   poucos dados: uma rede neuronal precisaria de mais dados para
   aprender uma reconstrução útil, o que contraria a própria razão
   dada para sugerir um autoencoder.
5. **Ensemble = média dos scores estandardizados (z-score)** do
   Isolation Forest e do erro de reconstrução do PCA, com o mesmo
   limiar do ponto 2 aplicado ao score combinado. Combinação mais
   simples, sem pesos a afinar.
6. **Âmbito: só o braço de ciência cidadã** (onde está o problema de
   poucos dados); o braço de especialistas não é refeito.

**Porquê:** o orientador pediu a reabertura e deu a razão (só
presenças, poucos dados, risco de haver acácia não registada no
fundo); os pontos 2 a 6 seguem a instrução de decidir sempre pela
opção mais simples quando o desenho exato não foi especificado.

**Resultado:** 39 blocos de 10 km têm pelo menos uma presença; só 15
têm 5 ou mais (o mesmo piso de 5 já usado no notebook anterior) e
servem de fold de teste, cada um uma vez (entre 7 e 819 presenças de
teste por fold). Sensitivity média (dp) nos 15 folds: Isolation Forest
0,916 (0,068); ensemble PCA + Isolation Forest 0,876 (0,119); One-Class
SVM 0,849 (0,110); PCA 0,815 (0,158). Como o limiar é o percentil 10
dos próprios scores de treino, 0,90 é o valor esperado quando um bloco
de teste se parece com os de treino; só o Isolation Forest fica nesse
nível ou acima, por isso é o que generaliza melhor entre os 15 blocos
nesta corrida — o ensemble não melhora sobre o Isolation Forest sozinho
(o PCA, com mais variância, puxa-o para baixo). Corrida única, sem
afinação de hiperparâmetros; não comparável aos números de ROC-AUC/Boyce
do notebook anterior (métrica, divisão espacial e uso do fundo são
todos diferentes).

**Não decidido:** isto não muda, por si só, o classificador principal
da curva da RQ1 (continua o Random Forest presença-vs-fundo).

**Fundamentação:** Baldi & Hornik (1989) para a equivalência entre PCA
e um autoencoder linear. O resto (limiar de 10%, leave-one-block-out,
média estandardizada no ensemble) é raciocínio meu, sem literatura
própria procurada para esta combinação específica — nenhuma das
comparações one-class já lidas
([`docs/literature.md`](../docs/literature.md#one-class--positive-unlabeled-classification))
testa isolation forest com autoencoder em ensemble.

**Em aberto:**
- Confirmar com o orientador que a implementação (grelha reaproveitada
  em vez de 4x4, PCA em vez de rede neuronal, limiar de 10%)
  corresponde ao que tinha em mente.
- Hiperparâmetros não afinados (um só valor de contaminação/`nu`); só
  um passe, como o notebook anterior.

**Calendário:** exceção ao âmbito fechado do relatório intermédio —
corre antes da entrega de janeiro de 2027, porque corrige a avaliação
da própria RQ1. Ver
[Revisão em "Primeira entrega"](#primeira-entrega-relatório-intermédio-início-de-janeiro-de-2027).

**Onde:** [`docs/meetings/2026-11-17.md`](../docs/meetings/2026-11-17.md);
[`one_class_background_free_evaluation.ipynb`](../notebooks/07_foundation_models/one_class_background_free_evaluation.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia). A métrica
desta entrada (sensitivity com limiar tirado do treino) foi
substituída no mesmo dia; ver a Revisão abaixo e
[RQ1 passa a presence-only](#rq1-presence-only).

**Revisão (2026-11-17, mesmo dia): a leitura do resultado estava
errada.** Com o limiar tirado do percentil 10 dos scores de treino, a
sensitivity mede só se as presenças de teste se parecem com as de
treino; não mede se o modelo distingue acácia do resto da paisagem. Um
modelo que dá scores quase iguais a tudo fica perto de 0,90 em
qualquer bloco. Logo, "o Isolation Forest generaliza melhor" não é
suportado por estes dados — pode só significar que os seus scores são
pouco informativos (foi o que pior separou presenças do fundo no teste
antigo, ROC-AUC 0,57). O que esta corrida mostra é que uma avaliação
literalmente só com presenças não discrimina modelos. A métrica passa a
sensitivity a uma fração fixa de área prevista, em
[RQ1 passa a presence-only](#rq1-presence-only); o notebook tem a
leitura corrigida na secção 4.

### RQ1 passa a presence-only: seleção entre one-class puro e presença-fundo, sensitivity a área fixa, leave-one-block-out {#rq1-presence-only}

*Decisão minha de 2026-11-17, na sequência da reunião do mesmo dia. O
orientador pediu um modelo só com presenças, grelha espacial e
sensitivity; que o Random Forest atual não cumpre isso, e o desenho
concreto abaixo, são meus, a confirmar com ele nos pontos assinalados.*

**O que decidi:**

1. **O classificador principal da RQ1 passa a ser presence-only.** O
   Random Forest presença-vs-fundo usa o fundo como pseudo-ausência
   (ver Revisão na
   [entrada do Random Forest](#classificador-presença-vs-fundo-ciência-cidadã-random-forest-por-agora)),
   que é o pressuposto que o orientador contestou.
2. **Dois sentidos de presence-only entram na seleção de método, no
   mesmo protocolo:** (a) one-class puro, sem fundo no treino —
   Isolation Forest, One-Class SVM, PCA e o ensemble PCA + Isolation
   Forest, o que o orientador nomeou; (b) presença-fundo com o fundo
   como amostra *não rotulada* da paisagem — MaxEnt ou PU-learning,
   método concreto por escolher. O vencedor passa a classificador da
   curva. Medir os dois responde ao que ele pediu (a) e ao que a
   literatura lida aponta (b).
3. **Protocolo único:** leave-one-block-out nos blocos de 10 km com
   pelo menos 5 presenças (15 no braço de ciência cidadã), como em
   `one_class_background_free_evaluation.ipynb`.
4. **Métrica principal: sensitivity a uma fração fixa de área
   prevista.** Ordena-se a paisagem pelo score; os X% de área com
   score mais alto são a previsão de acácia; a sensitivity é a fração
   das presenças de teste que cai lá dentro. Reporta-se a curva
   sensitivity × área de 5% a 30% e um número principal numa fração
   fixada antes de correr — **a fração ainda não está fixada.**
   ROC-AUC e Boyce passam a secundárias, com a ressalva já
   documentada.
5. **O fundo entra na avaliação só como amostra da paisagem**, para
   saber o que são X% de área; nunca é rotulado como ausência, por
   isso uma acácia não registada no fundo não conta como erro. Em (b)
   entra também no treino, como não rotulado.
6. **A curva da RQ1 é recorrida com o classificador vencedor.** Até
   lá, os números atuais ficam marcados nos docs como obtidos com o
   Random Forest.

**Porquê:** a objeção do orientador ("não assumir que não há acácia no
fundo") não se resolve só com a métrica — o Random Forest assume-o no
treino, e a ROC-AUC assume-o na avaliação (cada ponto de fundo com
score alto conta como falso positivo). Avaliar literalmente só com
presenças também não serve: a corrida de hoje mostrou que não
discrimina modelos. A sensitivity a área fixa é a única forma que
encontrei de cumprir as duas coisas: nunca rotular fundo como ausência
e penalizar um modelo que marca tudo como acácia.

**Fundamentação:** Rapinel & Hubert-Moy (2021): fundo com classificador
presença/ausência = pseudo-ausências, confusão em 42% dos estudos.
Phillips et al. (2009): fundo como amostra não rotulada da paisagem.
Deng et al. (2018), Mack & Waske (2017), Li & Guo (2010), Li, Guo &
Elkan (2011, só resumo): métodos (b) batem one-class puros em todas as
comparações lidas. Hirzel et al. (2006): mesma lógica
presença-vs-disponível do Boyce. **Para a métrica, não li:** julgo que
é a lógica da taxa de omissão contra área prevista (Phillips et al.,
2006) e da ROC parcial (Peterson et al., 2008) — a confirmar antes de
a tratar como estabelecida; até lá é raciocínio meu com fontes por
ler. Para a seleção (a) contra (b) neste desenho não encontrei
precedente lido.

**Em aberto:**
- Confirmar com o orientador: que (b) é aceitável como presence-only;
  que usar o fundo para medir área é aceitável; a grelha reaproveitada
  em vez de 4x4; a fração de 10%.
- Ler Phillips et al. (2006) e Peterson et al. (2008).
- MaxEnt (`elapid`, não instalado) como alternativa à regressão
  logística em (b), se o orientador o preferir.

**Fixado antes de correr (2026-11-17, opção mais simples em cada
ponto):** fração de área principal 10% (escolha minha, sem fonte; a
curva 5–30% é reportada); método (b) = regressão logística L2
presença-vs-fundo, `class_weight="balanced"`, sem afinação; a amostra
da paisagem é o fundo do próprio bloco de teste (15–40 pontos), e a
métrica é calculada por ordenação dentro do bloco e agrupada sobre as
2 464 presenças fora-de-fold; critério: vence o candidato com a maior
sensitivity agrupada a 10%, diferenças abaixo de 0,02 resolvidas pelo
menor desvio-padrão entre folds; o Random Forest entra só como
referência.

**Resultado (2026-11-17,
[`presence_only_method_selection.ipynb`](../notebooks/07_foundation_models/presence_only_method_selection.ipynb)):**
sensitivity agrupada a 10% de área (acaso = 0,10): regressão logística
(b) **0,365**; Random Forest (referência) 0,321; One-Class SVM 0,230;
Isolation Forest 0,165; ensemble PCA + Isolation Forest 0,156; PCA
0,120. Por fold (média, dp): 0,406 (0,165); 0,351 (0,154); 0,271
(0,130); 0,159 (0,117); 0,145 (0,125); 0,089 (0,087).

- **Decisão pelo critério (primeira corrida; ver Revisão abaixo): a
  regressão logística presença-fundo é o classificador da curva da
  RQ1.** Bate o melhor one-class por 0,135,
  em todas as frações de 5% a 30%. O ensemble que o orientador nomeou
  fica perto do acaso. Concorda com todas as comparações lidas em
  `docs/literature.md`.
- **Eixo antigo contra novo, no mesmo protocolo:** o Random Forest
  fica abaixo da regressão logística (0,321 contra 0,365; à frente em
  5 blocos, atrás em 8, empate em 2). Os dois presença-fundo estão
  próximos; a distância grande é para a família one-class.
- **Valores absolutos baixos — hipóteses, não testadas:** os 15 blocos
  são os densos em acácia, por isso parte do fundo deles é
  provavelmente acácia ou vegetação parecida, que a métrica conta como
  área e não como erro; e ordenar dentro de um bloco é mais difícil do
  que a ROC-AUC global, que ganha com as diferenças entre blocos. Só a
  comparação entre modelos é lida, não o nível.
- Uma corrida, sem afinação; resolução de ~3% por presença, suavizada
  pela agregação.

**Revisão (2026-11-17, segunda corrida, mesmo notebook):** instalei o
`elapid` (acrescentado a `requirements.txt`) e juntei dois candidatos
(b), com o critério inalterado: **MaxEnt** só com variáveis lineares
(com *hinge* e produtos, 128 dimensões dariam milhares de variáveis
para ~2 300 presenças) e **biased SVM** (SVC RBF,
`class_weight="balanced"`, presenças contra fundo dos blocos de
treino). O PU-learning de Elkan & Noto não corre à parte: o seu score é
uma reescala monótona do classificador presença-vs-não-rotulado, logo
numa métrica por ordenação dá o mesmo que a regressão logística
(raciocínio meu; Elkan & Noto, 2008, não lido). Resultado a 10% de
área: **biased SVM 0,368**, regressão logística 0,365, Random Forest
0,321, MaxEnt 0,294; os one-class como antes. Por fold (média, dp):
0,404 (0,149); 0,406 (0,165); 0,351 (0,154); 0,348 (0,146).

- **A decisão passa, pelo critério, para o biased SVM:** os dois
  primeiros estão dentro da margem de 0,02 (0,003 de diferença) e o
  desempate pelo desvio-padrão dá o SVM. Lido sem o critério, é um
  empate: por fold o SVM está à frente em 7 blocos, atrás em 5,
  empatado em 3. A regressão logística é mais simples e muito mais
  barata (a curva treina com até ~21 500 presenças); se o orientador a
  preferir, estes números não o contrariam. Levo-lhe os dois.
- **O resultado robusto é o de família:** todos os (b) batem todos os
  (a) em todas as frações; o melhor one-class fica 0,138 abaixo do
  vencedor.
- O MaxEnt linear é o mais fraco dos (b) a 10% e iguala os outros a
  partir de 15%; com variáveis lineares está perto de uma regressão
  logística regularizada, por isso não se esperava grande diferença;
  parâmetros por omissão, não afinados.

**Revisão (2026-11-17, mais tarde no mesmo dia; decisão minha):**
dois cortes na lista de modelos e uma limpeza.

- **O biased SVM sai.** Fui eu que o acrescentei na segunda corrida,
  sem fonte lida (o nome vem do PU-learning, Liu et al., 2003, não
  lido; no notebook é só um SVC RBF presenças contra fundo com
  `class_weight="balanced"`), para a comparação (a)/(b) ter um kernel
  de cada lado. Empatou com a regressão logística (0,003) e é muito
  mais caro para a curva. Sem ele, **a regressão logística vence o
  critério sem desempate** (0,365 contra 0,294 do MaxEnt) e é o
  classificador da curva; a opção mais simples, como pedido na
  reunião.
- **O Random Forest sai de todos os ficheiros de estado atual.** Não
  é um presence-only: usa o fundo como pseudo-ausência, logo todos os
  seus números (curva, zona-tampão, 0,976 da RQ3, verificação de fundo
  só-floresta) deixam de valer como resultados e foram retirados de
  `docs/research_questions.md`, `docs/methodology.md` e
  `docs/todo.md` em vez de ficarem marcados; as pastas
  `results/effort_reduction_curve*` levam `OBSOLETE.md` e os
  notebooks que o usaram ficam com nota no topo. A linha "ref. Random
  Forest" do notebook de seleção também sai na próxima corrida. Os
  diagnósticos da curva plana (redundância, habitat, pureza) ficam
  como factos dos dados; a curva que explicavam já não existe.
- **Também o braço Sentinel-2 (RQ4)** deixa de prever "Random Forest e
  regressão logística": passa a usar só o classificador da RQ1
  (Revisão na entrada do Sentinel-2).
- **Em aberto:** se o PCA (e com ele o ensemble PCA + Isolation
  Forest, que respondia ao pedido do orientador) sai da lista; depende
  de decidir primeiro se há forma de melhorar os one-class. O notebook
  é recorrido uma vez, quando a lista fechar.

**Revisão (2026-11-17, terceira corrida; notebook reescrito e corrido
uma só vez, com critérios fixados antes):** para fechar a lista,
corri um varrimento pequeno nas duas famílias, nos mesmos 15 folds
(28 configurações): Isolation Forest (`max_samples`, `max_features`),
One-Class SVM (`nu` × gamma), PCA a 20 dimensões antes de cada um,
autoencoder 128–32–128 (`MLPRegressor`) no lugar do PCA e os ensembles
autoencoder/PCA + Isolation Forest; do lado (b), regressão logística
(`C` 0,01 a 10) e MaxEnt (linear ou linear + quadrática × multiplicador
de regularização 0,5 / 1,5 / 4). Um texto que recebi recomendava
MaxEnt afinado (via `maxnet` + ENMeval) com validação por blocos,
Boyce, AUC e fração de área prevista: a avaliação é a que já tínhamos,
e a afinação é o que faltava; a parte do ensemble biomod2 (MaxEnt + RF
+ BRT) não segue, por usar pseudo-ausências e por serem mais modelos.
Critérios escritos antes: (1) se nenhum one-class chegar a 0,30 a 10%
de área, a lista one-class fecha com Isolation Forest e One-Class SVM;
(2) melhor regressão logística contra melhor MaxEnt, margem 0,02 a
favor da regressão. Ressalva declarada: a melhor configuração é
escolhida nos mesmos folds que a reportam, nas duas famílias; sem CV
aninhada.

- **Resultado a 10% de área (melhor configuração de cada modelo):**
  regressão logística `C=10` **0,410** (por fold 0,415, dp 0,161);
  MaxEnt linear + quadrática, multiplicador 4, 0,334 (0,357; 0,127);
  One-Class SVM `nu=0,2`, gamma 2× 0,258; PCA20 → One-Class SVM 0,233;
  Isolation Forest `max_features=0,5` 0,188; ensemble autoencoder +
  IF 0,163; autoencoder 0,140.
- **Decisão (critério 1): o PCA, o autoencoder e os ensembles saem.**
  Nenhum one-class chega a 0,30; o varrimento moveu-os pouco (OCSVM
  0,230 → 0,258; IF 0,165 → 0,188). O autoencoder não linear fica
  perto do acaso como o PCA, e o ensemble com o Isolation Forest não
  bate o Isolation Forest sozinho. O pedido do orientador (ensemble
  autoencoder + isolation forest) fica testado e registado aqui; a
  lista one-class da RQ1 é Isolation Forest e One-Class SVM.
- **Decisão (critério 2): a regressão logística, `C=10`, é o
  classificador da curva**, 0,076 acima do melhor MaxEnt. O `C=10` é
  o extremo da grelha (o número sobe monotonamente com menos
  regularização: 0,326 / 0,348 / 0,365 / 0,410); não explorei mais,
  porque a escolha é feita nos folds de teste e a resolução por bloco é
  grosseira. A confirmar na curva ou no braço de especialistas antes de
  dizer mais do que "menos regularização ajuda aqui".
- O resultado de família mantém-se: as melhores configurações de (b)
  batem as melhores de (a) em todas as frações de área.
- O MaxEnt só ganhou com variáveis quadráticas sob regularização forte;
  com regularização fraca as quadráticas prejudicam (0,239 a 10%).
- As duas corridas anteriores (com Random Forest e biased SVM) ficam só
  nesta entrada; o notebook foi reescrito e tem uma única corrida.

**Revisão (2026-11-17, leitura das fontes da métrica; decisão minha):**
li Phillips et al. (2006), Peterson et al. (2008) e Elkan & Noto
(2008), que acima estavam "por ler" ou "não lido".

- **A sensitivity a área fixa deixa de ser raciocínio meu com fontes
  por ler.** É o teste de "equalized predicted area" de Phillips et
  al. (2006, §2.6.1): a omissão depende da área prevista, por isso
  dois modelos só se comparam a área igual; eles fixam a área pelo
  modelo rival, eu fixo-a à partida. O eixo "proporção da área
  prevista", em vez de comissão sobre ausências, é o que Peterson et
  al. (2008) adotam na ROC parcial, com a diferença de que fixam a
  tolerância de omissão e não a área, e dizem, sem o implementar, que
  limitar a área prevista também faria sentido. Nenhum dos dois
  recomenda uma fração: **os 10% continuam a ser escolha minha.**
- **Elkan & Noto (2008, lema 1)** confirma a equivalência de
  ordenação entre PU-learning e presença-vs-fundo que usei para não
  correr o PU-learning à parte, no cenário de um só conjunto de
  treino. Para o cenário caso-controlo (presenças e fundo amostrados à
  parte, o nosso) o artigo só diz que a prevalência não é
  identificável; estender-lhe a equivalência de ordenação continua a
  ser raciocínio meu.
- Li, Guo & Elkan (2011) e Li & Guo (2010) passaram de "só resumo" a
  lidos na íntegra e confirmam o que o resumo dizia; Mack & Waske
  (2017) fica só pelo resumo.
- Resumos em
  [`docs/literature.md`](../docs/literature.md#evaluating-presence-only-models-without-confirmed-absences);
  estado atualizado em
  [`docs/methodology.md`](../docs/methodology.md#evaluation).

**Impacto a jusante (tudo a recorrer ou a marcar):** curva da RQ1
(`results/effort_reduction_curve/`, números em
`docs/research_questions.md`), análise de sensibilidade à zona-tampão
(calculada em ROC-AUC do Random Forest), valor "0,976" que a RQ3
assume como ponto de partida, secções Validation/Evaluation/Baseline de
`docs/methodology.md`, resumo do desenho na Introdução do manuscrito
(a Introdução não nomeia o classificador nem a métrica — verificado por
grep; nada a corrigir lá por agora).

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq1--citizen-science-as-a-substitute-for-expert-data);
[`docs/methodology.md`](../docs/methodology.md#evaluation);
[`docs/meetings/2026-11-17.md`](../docs/meetings/2026-11-17.md);
[`presence_only_method_selection.ipynb`](../notebooks/07_foundation_models/presence_only_method_selection.ipynb).

**Na tese:** ✅ Parcial. Os conceitos (one-class contra presença-fundo,
fundo como amostra não rotulada e não como ausência, avaliação a área
prevista igual segundo Phillips et al. 2006 e Peterson et al. 2008)
estão na secção 2.5.1 do Background (2026-11-18). A 2.5.1 diz
também (mesmo dia) que o MaxEnt e o PU-learning explícito caem na
família presença-fundo (Phillips et al. 2006; lema 1 de Elkan & Noto
2008), que os one-class puros perderam em todas as comparações lidas
(Deng et al. 2018; Li & Guo 2010; Li, Guo & Elkan 2011; Mack & Waske
2017), com a razão de Elkan & Noto, e que o fundo só mede a área na
avaliação. **Mack & Waske (2017) é citado só pelo resumo** (texto
completo com paywall; tese do autor na FU Berlin por descarregar à
mão): a tese afirma apenas o que o resumo diz, as três famílias
comparadas, o biased SVM em primeiro, o one-class SVM atrás, e mau
desempenho do melhor método em muitas tarefas, sem números. A seleção
de método, o critério, os resultados (0,410 contra 0,334, 0,258 e
0,188), o MaxEnt corrido e perdido, a ressalva de que a extensão do
lema de Elkan & Noto ao caso-controlo é raciocínio meu, e o Random
Forest como metodologia abandonada (razão do ponto 1) ficam para o
Proposed Work.

### Curva da RQ1 no desenho presence-only: leave-one-block-out com as duas fontes, sensitivity a 10% de área {#curva-presence-only}

*Decisão minha (2026-11-17), a confirmar com o orientador. Reescreve
`experiments/effort_reduction_curve/run.py` e `compare_buffer.py` para
o desenho da entrada [#rq1-presence-only](#rq1-presence-only); o que
muda face à [curva completa](#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos)
está na Revisão dessa entrada.*

**O que decidi:**
1. **Folds: leave-one-block-out sobre os blocos de 10 km com pelo
   menos 5 presenças de qualquer das fontes** (ciência cidadã ou
   píxeis de especialistas): 26 blocos, 15 com ciência cidadã, 18 com
   especialistas, 6 com as duas. Em cada fold, as presenças das duas
   fontes do bloco e o fundo do bloco são o teste; tudo o resto
   treina. Polígonos que cruzam a fronteira do bloco (9 em 1 457)
   dão os píxeis do bloco ao teste e os outros ao treino, como antes.
2. **Classificador:** regressão logística presença-fundo, `C=10`, o
   escolhido na seleção de método; escala ajustada em presenças +
   fundo de treino.
3. **Métrica:** sensitivity a 10% de área prevista, calculada como na
   seleção de método (área necessária por presença contra o fundo do
   bloco de teste); reportada agrupada sobre todas as presenças
   retidas (cada uma conta uma vez) e por fold (blocos com peso
   igual), com a curva 1%–50%. ROC-AUC por fold como secundária. **O
   Boyce deixa de ser calculado na curva:** um bloco tem 5–41 pontos
   de fundo, poucos para as dez janelas do índice.
4. **Condições:** as mesmas de antes (0% a 100% em passos de 10, 100%
   = só especialistas, e "100% + ciência cidadã"), ordem encaixada dos
   polígonos com seed 0. Comparação principal: 90% − 0% no teste
   agrupado, diferença emparelhada por fold (média, dp, folds a
   subir/descer) e diferença agrupada; especialistas e ciência cidadã
   em separado ao lado.
5. **Tampão:** continua opção do script, agora por fold; critério da
   análise de sensibilidade na Revisão da
   [entrada do tampão](#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km).

**Porquê:** o mesmo protocolo da seleção de método, estendido aos
especialistas pela regra mais simples (o bloco é a unidade; entra como
fold se tiver presenças que cheguem de uma das fontes). Evita sortear
blocos de teste por semente e a reutilização de blocos entre
sementes, que impedia ler a concordância entre sementes como evidência
independente. Os 5 de mínimo são o mesmo limiar da seleção. Um fold
com 1 154 píxeis de especialistas (56_443) pesa muito no agrupado; por
isso o por-fold é reportado ao lado.

**Fundamentação:** nenhuma nova; o limiar de 5 e a regra dos folds são
raciocínio meu. Própria da avaliação: ver [#rq1-presence-only](#rq1-presence-only).

**Impacto a jusante:** `results/effort_reduction_curve/`,
`_buffer_300m/`, `_buffer_1000m/` e `_buffer_comparison/` são
regenerados com tabelas novas (`per_fold.csv`, `summary.csv`,
`pooled_curve.csv`, `paired_differences.csv`); o notebook
`effort_reduction_curve.ipynb` tem de ser reescrito para as ler;
`forest_only_background_check.ipynb` fica obsoleto (o fundo só de
floresta não é recorrido).

**Resultado (2026-11-17, uma corrida, sem afinação;
`results/effort_reduction_curve/`, `run.json` com os hashes das
entradas):** 26 folds, 5 196 presenças retidas (2 767 píxeis de
especialistas em 17 folds, 2 429 de ciência cidadã em 19).
Sensitivity agrupada a 10% de área (acaso 0,10):

| Presenças de teste | 0% | 10% | 50% | 90% | 100% + CC | Só especialistas |
|---|---|---|---|---|---|---|
| Agrupadas | 0,531 | 0,604 | 0,681 | 0,692 | 0,691 | 0,701 |
| Só especialistas | 0,637 | 0,775 | 0,910 | 0,933 | 0,935 | 0,983 |
| Só ciência cidadã | 0,411 | 0,408 | 0,421 | 0,417 | 0,413 | 0,381 |

- **Comparação principal, 90% − 0%, agrupada:** +0,161 no agrupado;
  por fold +0,181 (dp 0,221), 18 folds a subir, 6 a descer, 2
  empatados. **Só especialistas:** +0,296; por fold +0,335 (dp 0,148),
  17 de 17 a subir. **Só ciência cidadã:** +0,006; por fold +0,011 (dp
  0,111), 6 a subir, 7 a descer, 6 empatados.
- **A curva sobe cedo e satura:** a 10% dos polígonos já se ganha
  quase metade (+0,072 agrupado; +0,138 em especialistas), a 50%
  quase tudo; de 50% a 90% muda menos de 0,025 em todos os testes. O
  padrão repete-se nas frações de 5%, 20% e 30% de área.
- **"100% + ciência cidadã" contra 90%:** −0,001 (empate). Contra o
  modelo só de especialistas: nas presenças de especialistas −0,048
  (0 folds a subir, 12 a descer, 5 empatados); nas de ciência cidadã
  +0,032 (10 a subir, 5 a descer).
- **O modelo só de especialistas reconhece pior a ciência cidadã:**
  0,381 a 10% de área, abaixo de todos os níveis com ciência cidadã no
  treino; a 50% de área, 0,722 contra 0,837 do modelo de 0%.
- **Por fold, a subida vem dos blocos com píxeis de especialistas no
  teste:** nos 9 folds só com ciência cidadã a diferença 90% − 0%
  média é −0,052; nos 7 só com especialistas, +0,396; nos 10 com as
  duas fontes, +0,241. O fold 56_443 tem 42% dos píxeis de
  especialistas de teste (1 154 de 2 767) e dá +0,198, perto da média
  por fold: não é ele que puxa o agrupado.
- **ROC-AUC por fold (secundária):** agrupado 0,827 (0%) → 0,882
  (90%) → 0,833 (só especialistas); especialistas 0,877 → 0,974 →
  0,988; ciência cidadã 0,766 → 0,779 → 0,674. Mesma leitura.

**Leitura:**
- **A resposta à RQ1 muda face à curva do Random Forest** (plana em
  ROC-AUC, [curva completa](#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos)):
  os dados de especialistas acrescentam muito ao reconhecimento das
  presenças de especialistas e nada ao das presenças de ciência
  cidadã. O resultado vai no sentido da H₁ no teste agrupado e nos
  especialistas, e no sentido da H₀ na ciência cidadã. Três coisas
  mudaram ao mesmo tempo (classificador, métrica e folds); qual delas
  explica a diferença não está separado.
- **"Substituir" depende do que se quer mapear:** só com ciência
  cidadã, 0,637 nas presenças de especialistas contra 0,983 do modelo
  treinado nelas; nas presenças de ciência cidadã, o modelo de
  especialistas é o pior. Cada fonte reconhece melhor o que se parece
  com ela. O 0,637 é o ponto de partida da RQ3.
- **Hipóteses para a diferença entre fontes (não testadas):** as
  presenças de especialistas são manchas de acacial (55,0% em
  "Florestas de acácias", contra 17,9% da ciência cidadã,
  [diagnósticos](#diagnosticos-curva-plana)), um contexto que a ciência
  cidadã cobre pouco; e a métrica ordena dentro do bloco, onde a
  composição do treino pesa mais do que numa ROC-AUC global que ganha
  com as diferenças entre blocos.
- **Cautelas:** só 17 folds têm píxeis de especialistas no teste (7
  deles sem ciência cidadã) e o desvio-padrão por fold é grande
  (0,22); a H₁ foi escrita depois de ver a curva antiga; `C=10` é o
  extremo da grelha da seleção; o nível absoluto não se lê (parte do
  fundo dos blocos densos é provavelmente acácia). Sem tampão entre
  treino e teste: ver a Revisão da
  [entrada do tampão](#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km).

**Onde:** [`run.py`](../experiments/effort_reduction_curve/run.py);
[`compare_buffer.py`](../experiments/effort_reduction_curve/compare_buffer.py);
[`src/evaluation.py`](../src/evaluation.py) (`needed_area`);
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb)
(lê e desenha).

**Na tese:** ⏳ Ainda não escrita (Metodologia e Resultados da RQ1).

### Curva de redução de esforço completa: 0%–100%, com fundo e bloco de teste fixos

*Decisão minha, não confirmada pelo orientador.*

**O que decidi (desenho):**
1. **Unidade de mistura: polígonos, não píxeis.** O custo de campo é
   por local visitado.
2. **Amostragem encaixada:** uma ordem aleatória fixa (seed 0) decide
   que polígonos entram em cada nível; os de 20% incluem os de 10%.
3. **Um conjunto de teste fixo por semente, igual em todos os níveis,**
   sorteado dos blocos de 10 km com presenças de alguma das duas
   fontes (47). Média de 5 sementes.
4. **O teste inclui sempre as duas fontes,** mesmo a 100%.

**Resultado:**
- **Random Forest e Logistic Regression planos do 0% ao 90%.** Random
  Forest: ROC-AUC 0,879 (0%) → 0,882 (20%) → 0,878 (90%) → 0,801
  (100%); Boyce 0,993 → 0,994 → 0,983 → 0,917. A Logistic Regression
  sobe um pouco (ROC-AUC 0,873 → 0,896 do 0% ao 90%) e também cai a
  100%. A 100% o modelo nunca viu ciência cidadã no treino e
  generaliza pior para ela.
- **One-class SVM melhora com mais especialistas** (ROC-AUC 0,574 →
  0,655 → 0,765), mas fica sempre abaixo dos outros dois.

**Explicação provável:** em todos os níveis 10–90%, a ciência cidadã
fornece 85–100% das presenças de treino, e o modelo já está perto do
teto só com ela. As verificações abaixo confirmam que não é erro nem
artefacto, e apontam a
[concentração de habitat](#diagnosticos-curva-plana)
como explicação.

**Resposta provisória à pergunta do equilíbrio:** com este desenho,
nenhuma quantidade de dados de especialistas abaixo da substituição
total traz melhoria visível. Merece escrutínio antes de virar
conclusão.

**Nota:** estes números não são comparáveis aos 0% e 100% dos notebooks
anteriores, que usavam cada um o seu sorteio de blocos de teste.

**Em aberto:**
- Esforço medido só como % de polígonos, não por área nem por custo
  real de campo.
- Só TESSERA; fundo ainda não confirmado pelo orientador.
- Confirmar com o orientador antes de tratar como resposta final.

**Fundamentação:** Dimson et al. (2023) para a diferença de viés entre
fontes, como analogia: dizem que os enviesamentos são "muitas vezes"
inversos (não em todas as espécies), e lá as duas fontes amostraram
sítios diferentes, enquanto aqui especialistas e Observador A
visitaram os mesmos. Só li a versão submetida, não o artigo
publicado. O resto é raciocínio meu.

**Onde:** [`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).

**Na tese:** ⏳ Ainda não escrita (Resultados/Metodologia). O desenho
(polígonos como unidade, amostragem encaixada, teste fixo) mantém-se;
os números desta entrada são do Random Forest e não entram como
resultado. A curva é recorrida com o classificador de
[RQ1 passa a presence-only](#rq1-presence-only).

**Revisão (2026-11-14):** a curva ganha um nível "100% especialistas
+ ciência cidadã" no fim da parte aditiva; o "100%" desta entrada (só
especialistas) passa a ser um ponto de referência à parte. O resto do
desenho não muda. Ver
[nível 100% + ciência cidadã](#curva-100-mais-ciencia-cidada).

**Revisão (2026-11-17):** *superada em parte* pela
[curva no desenho presence-only](#curva-presence-only): os pontos 1, 2
e 4 (polígonos como unidade, ordem encaixada, teste com as duas
fontes) mantêm-se; o ponto 3 (um conjunto de teste sorteado por
semente, cinco sementes) é substituído por leave-one-block-out. Os
resultados desta entrada foram obtidos com o Random Forest
presença-vs-fundo e deixam de ser reportados
([#rq1-presence-only](#rq1-presence-only)).

### Curva de redução de esforço sob um fundo só de floresta: verificação de robustez {#curva-fundo-so-floresta}

*Decisão minha (investigar), não confirmada pelo orientador. Motivada
pela dúvida "não devíamos ter melhores resultados com os dados de
especialistas? não pode ser um erro?".*

**O que decidi:** verificar se a curva plana é erro ou artefacto.
1. Revisão de `continuous_boyce()` em `src/evaluation.py`: sem erro.
2. Composição do fundo: cerca de 29% não-floresta (estradas,
   agricultura, água) contra 8% nas presenças.
3. Random Forest a 0% contra o fundo completo e contra o subconjunto
   de floresta: ROC-AUC 0,842 → 0,796, Boyce 0,989 → 0,980. A maior
   parte da separabilidade sobrevive.
4. Fuga de dados: distância mínima fundo→presença = 54,06 m, acima da
   zona-tampão de 50 m.
5. Curva completa repetida contra um fundo novo só de floresta
   (eucaliptal, pinhal, outra floresta, matos; excluída a classe
   "floresta de acácias", que seria contradição de rótulo), N = 2 000.

**Resultado:** a conclusão mantém-se.
- **Random Forest:** ROC-AUC sobe em todos os níveis (0,879 → 0,934 a
  0%; 0,878 → 0,933 a 90%; 0,801 → 0,885 a 100%); a curva continua
  plana; Boyce cerca de 0,98–0,99.
- **Logistic Regression:** mesmo padrão, exceto a 100%, onde o Boyce
  cai de 0,897 para 0,567. Não investigado.
- **One-class SVM:** ROC-AUC 0,515 a 0% (era 0,574) e Boyce −0,039
  (era 0,628). Sem o fundo "fácil", deixa de distinguir acácia de
  outra floresta.

**Em aberto:** o agrupamento dos códigos COS em "tipo floresta" é
escolha minha. Esta verificação não substitui o fundo partilhado.

**Fundamentação:** raciocínio meu; sem literatura nova.

**Onde:** [`forest_only_background_check.ipynb`](../notebooks/07_foundation_models/forest_only_background_check.ipynb).

**Na tese:** ❌ Superseded. Os valores (Random Forest, ROC-AUC e Boyce
contra o fundo) deixam de contar como resultado a 2026-11-17 e a
verificação não foi recorrida no desenho presence-only
([RQ1 passa a presence-only](#rq1-presence-only),
[curva presence-only](#curva-presence-only)); a pasta
`results/effort_reduction_curve_forest_only/` fica marcada como
obsoleta. Se entrar no texto, é uma frase nas metodologias abandonadas.

**Revisão (2026-11-13):** os valores do **Resultado** acima e o
ponto 3 são da execução de 2026-11-07, anterior à janela 2021–2025 e
ao fundo uniforme reconstruído; já não são os atuais. A conclusão
mantém-se, com outros tamanhos: no Random Forest o ROC-AUC passa de
0,902 para 0,950 a 0%, de 0,906 para 0,952 a 90% e de 0,854 para 0,919
a 100%; na Logistic Regression o Boyce a 100% é 0,727 (não 0,567); no
one-class SVM o ROC-AUC a 0% é 0,504 e o Boyce 0,197 (não negativo).
O ponto 3 (0,842 → 0,796) não foi repetido com os dados atuais. A
verificação passou a ser calculada pelo script da curva. Tabela
completa e motivo:
[Verificação com fundo só de floresta](#fundo-floresta-script-experiments).

### Diagnósticos da curva plana: redundância, habitat e pureza {#diagnosticos-curva-plana}

*Decisão minha (investigar), não confirmada pelo orientador.*

**O que decidi:** testar três explicações para a curva plana da RQ1.

**Resultado:**
- **Redundância dentro dos polígonos: real, mas insuficiente.**
  Polígonos pequenos (mediana 1 píxel, máximo 9). ICC = 0,881, contra
  0,525 no nulo por permutação (200 repetições). Similaridade de
  cosseno: 0,921 dentro do mesmo polígono, 0,778 entre polígonos,
  0,613 entre presenças de ciência cidadã. Efeito prático modesto:
  cerca de 1 457 unidades efetivas em vez de 2 771 píxeis.
- **Habitat: é a explicação.** Restringir a ciência cidadã aos 18
  blocos com especialistas não muda a sua similaridade (0,618 contra
  0,614), por isso não é geografia. 55,0% dos píxeis de especialistas
  caem na classe "floresta de acácias" da COS, contra 18,1% da ciência
  cidadã, que se espalha por pinhal (32,6%), eucaliptal (20,4%), matos
  (8,5%), artificial (4,7%) e água (0,5%). Os especialistas formam
  poucos focos separados, cada um homogéneo por dentro; a ciência
  cidadã cobre uma faixa contígua mais ampla, incluindo uma zona a
  noroeste sem nenhum polígono.
- **Pureza dos rótulos: não é a explicação.** 21 das 2 995 presenças
  caem dentro de um polígono de especialista; das 298 a menos de
  100 m, 7,0% estão dentro (inconclusivo por si só). As 5% de
  presenças mais isoladas nos embeddings (150) distinguem-se pelo
  observador (48% de observadores não dominantes, contra 9,7% no
  resto); sem elas, ROC-AUC 0,842 → 0,843 e Boyce 0,992 → 0,995.

**Leitura:** os especialistas documentaram sobretudo manchas grandes e
reconhecíveis; a ciência cidadã cobre esse contexto e também
ocorrências mais variadas. Os dados de especialistas não são inúteis:
como foram amostrados neste piloto, não preenchem uma lacuna que a
ciência cidadã já não cubra. Implicação para uma recolha futura: visar
habitats e locais sub-representados.

**Em aberto:** achado específico do piloto, não confirmado pelo
orientador. O teste de pureza com polígonos só cobre 10% das
presenças, e o isolamento nos embeddings é um proxy: ninguém verificou
os pontos sinalizados contra ortofoto.

**Fundamentação:** raciocínio meu; ANOVA de um fator e teste de
permutação são técnicas padrão, a aplicação a embeddings é minha.

**Onde:** [`expert_polygon_redundancy_check.ipynb`](../notebooks/07_foundation_models/expert_polygon_redundancy_check.ipynb),
[`expert_polygon_geographic_diversity.ipynb`](../notebooks/07_foundation_models/expert_polygon_geographic_diversity.ipynb),
[`label_purity_check.ipynb`](../notebooks/07_foundation_models/label_purity_check.ipynb).

**Na tese:** ⏳ Ainda não escrita (Resultados/Metodologia). Os três
diagnósticos ficam como factos dos dados; a curva que explicavam
(Random Forest) já não existe como resultado
([RQ1 passa a presence-only](#rq1-presence-only)).

**Revisão (2026-11-13, revisão de consistência):** a célula do teste
sem as presenças isoladas tinha um erro: tirava-as também do conjunto
de teste, por isso as duas variantes não eram avaliadas nas mesmas
presenças. Corrigi (o filtro só atua no treino) e voltei a correr, com
as presenças de 2021–2025 e o fundo atual.

- **Resultado:** ROC-AUC 0,835 com todas as presenças e 0,826 sem as
  124 mais isoladas (5%) no treino. Diferença emparelhada por semente:
  −0,009 (dp 0,014), negativa nas cinco sementes (−0,035 numa, cerca
  de −0,003 nas outras). Boyce 0,981 e 0,983.
- **Leitura:** tirar estas presenças não melhora o resultado, por isso
  a conclusão mantém-se: a pureza não explica a curva. A pequena
  descida pode vir de o teste ainda conter presenças sinalizadas, que
  o modelo filtrado não viu (hipótese, não testada).
- **Critério:** escrito antes de correr: manter a leitura se a
  diferença média fosse menor que o seu desvio-padrão entre sementes.
- **O que fica:** os valores 0,842 → 0,843 acima são da corrida com
  todos os anos e com o erro. O sinal de "isolada" é calculado com
  todas as presenças, incluindo as dos blocos de teste.

**Revisão (2026-11-14):** fechei a limitação que tinha ficado na
Revisão anterior. O sinal de "isolada" passa a ser calculado também
dentro de cada semente, só com as presenças de treino, numa terceira
linha da mesma célula.

- **Resultado:** ROC-AUC 0,824, contra 0,835 com todas as presenças.
  Diferença emparelhada −0,012 (dp 0,019), negativa nas cinco sementes
  (−0,045 numa). Boyce 0,978.
- **Leitura:** igual à da variante anterior (−0,009). Tirar as
  presenças isoladas do treino não melhora o resultado; a conclusão
  mantém-se.
- **Critério:** escrito antes de correr, o mesmo da Revisão anterior.

### Métricas: limites do índice de Boyce tal como está calculado {#metricas-limites-boyce}

*Decisão minha, de 2026-11-11, depois de ler Hirzel et al. (2006) na
íntegra.*

**O que decidi:** manter ROC-AUC e Boyce nos resultados já corridos,
sem alterar o código antes da entrega, e declarar os limites do Boyce
sempre que o reportar.

**Porquê:**
- O índice é uma correlação de ordens: não distingue curvas
  monótonas. Um valor perto de 1 diz só que as presenças ficam mais
  frequentes quando a pontuação sobe. Boyce ≈0,99 em todos os modelos
  não os ordena.
- `continuous_boyce()` em `src/evaluation.py` usa dez janelas
  adjacentes de um décimo do intervalo observado de pontuações. É a
  forma de classes fixas, não a janela móvel sobre [0, 1] do artigo.
  Com dez valores a correlação anda em degraus grossos: 0,99 está a
  cerca de uma troca de 1.
- Hirzel et al. não dão orientação para valores perto do teto; nos
  dados deles o máximo foi 0,61.

**Em aberto:** reportar a própria curva P/E e a sua variação entre
divisões espaciais, como o artigo recomenda; passar à janela móvel.
As duas coisas mudam números já reportados, por isso ficam para
depois da entrega.

**Fundamentação:** Hirzel et al. (2006), texto integral. A leitura do
código é minha.

**Onde:** [`src/evaluation.py`](../src/evaluation.py);
[`docs/methodology.md`](../docs/methodology.md#evaluation).

**Na tese:** ⏳ Ainda não escrita (Metodologia/Resultados). Desde
2026-11-17 ROC-AUC e Boyce são métricas secundárias; a principal é a
sensitivity a área fixa ([RQ1 passa a presence-only](#rq1-presence-only)).

### RQ1: fundo partilhado de pontos aleatórios uniformes {#rq1-fundo-uniforme-nao-cos}

*Decisão minha, não confirmada pelo orientador; não é pergunta
pendente para ele.*

**O que decidi:** o fundo partilhado da RQ1 são pontos aleatórios
uniformes com zona-tampão de 50 m.

**Porquê:** a
[verificação com um fundo só de floresta](#curva-fundo-so-floresta)
mostra que a conclusão principal não depende do fundo: mantém-se e até
melhora; só o one-class SVM piora.

**Correção:** o fundo uniforme não se fundamenta em Phillips et al.
(2009), que defende o oposto (fundo de grupo-alvo). A fundamentação
real é a verificação empírica.

**Segunda correção (2026-11-11, depois de ler Phillips et al. na
íntegra):** a verificação empírica não chega para afastar o
enviesamento do fundo. Phillips et al. mostram que, avaliado com
presenças contra fundo aleatório, o modelo de fundo aleatório parece
melhor por construção (AUC 0,820 contra 0,717 do grupo-alvo), e que o
ganho do grupo-alvo só aparece com dados independentes de
presença-ausência. O teste com fundo só de floresta mostra que a
curva plana não depende de um fundo fácil, não que o fundo uniforme
seja não enviesado. O fundo uniforme fica como escolha minha, com
esta limitação declarada. A favor: Rapinel & Hubert-Moy (2021)
recomendam fundo sobre toda a paisagem, mas sem excluir a vizinhança
das presenças, ao contrário do meu tampão de 50 m. Phillips et al.
notam ainda um caso em que a correção deles falha: uma planta
pioneira ligada à perturbação, mais comum junto a estradas.

**Política para os diagnósticos (2026-11-10):** os quatro diagnósticos
da curva plana (fundo só de floresta, redundância, habitat, pureza)
não se repetem por omissão em cada braço novo. Só se o resultado
parecer inesperado.

**Em aberto:** dizer a ressalva do one-class SVM sempre que os números
desse método forem reportados.

**Fundamentação:** raciocínio meu, a partir da verificação de
robustez.

**Onde:** [`forest_only_background_check.ipynb`](../notebooks/07_foundation_models/forest_only_background_check.ipynb).

**Na tese:** ⏳ Ainda não escrita (Metodologia/Resultados). Desde
2026-11-17 o fundo entra só como amostra da paisagem, nunca como
ausência (ponto 5 de [RQ1 passa a presence-only](#rq1-presence-only));
o conjunto de pontos é o mesmo.

### Fundo uniforme reconstruído a partir das 2 465 presenças {#fundo-uniforme-reconstruido-2465}

*Registo de 2026-11-13. Decisão minha (o fundo continua por confirmar
com o orientador).*

**O que aconteceu:** em 2026-11-13, às 03:59, o
`background_points.npz` foi reconstruído pelo
`one_class_method_selection.ipynb`, que só o constrói quando o
ficheiro não existe. Os dois ficheiros de fundo anteriores (uniforme e
só de floresta) tinham desaparecido; a causa é desconhecida. O de
floresta foi reconstruído às 04:28 pelo
`forest_only_background_check.ipynb` e é igual ao anterior, byte a
byte (mesmo sha256).

**O que decidi:** o fundo uniforme em uso é o novo. A entrada da
[janela temporal](#janela-temporal-2021-2025) diz que mantive os
fundos antigos; isso deixou de ser verdade para o uniforme a partir
desta data.

**O que mudou no fundo uniforme:** só a zona-tampão de 50 m, agora à
volta das 2 465 presenças de 2021–2025 em vez das 3 000 de todos os
anos. Código, semente (42) e número de pontos (2 000) são os mesmos.
Verifiquei que o ficheiro atual se reproduz exatamente a partir da
semente e do ficheiro de presenças atual. Do antigo só resta o
checksum, por isso não comparei os dois ponto a ponto.

**Efeito nos resultados (curva 2021–2025, Random Forest):** o ROC-AUC
global coincide a 0,002 entre os dois fundos (0,903 e 0,902 a 0%;
0,855 e 0,854 a 100%). O Boyce global a 100% não: 0,930 com o fundo
antigo, 0,969 com o novo.

**Fundamentação:** nenhuma literatura consultada; é um registo de
proveniência.

**Onde:** curva completa com o fundo novo feita pela secção 8 de
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).

**Na tese:** ⏳ Ainda não escrita (Metodologia). O "efeito nos
resultados" acima é em Random Forest e já não conta como resultado
([RQ1 passa a presence-only](#rq1-presence-only)); a proveniência do
fundo mantém-se.

**Revisão (2026-11-13, mais tarde no mesmo dia):** a numeração das
perguntas mudou. O que nesta entrada é a "RQ1" (dos pontos aos dados
de referência) passa a ser a RQ2, e a "RQ2" (curva de redução de
esforço) passa a ser a RQ1; a RQ3 e a RQ4 não mudam. Passei a numerar
por ordem de importância, o que também fica mais perto da numeração
que o orientador aprovou. O conteúdo desta entrada não muda. Ver
[Renumeração das perguntas](#renumeracao-perguntas-2026-11-13).

**Revisão (2026-11-13, ao fim do dia):** depois do bloco acima a RQ3
e a RQ4 trocaram: a transferibilidade é a RQ3 e a comparação com o
Sentinel-2 é a RQ4. Ver a [tabela de numeração](#decisões).
A curva com o fundo novo está hoje em
`results/effort_reduction_curve/`
([script da curva](#curva-script-experiments)).

### RQ2: curva por fonte das presenças de teste, critério e leitura do resultado {#rq2-curva-por-fonte}

*Decisão minha, de 2026-11-13 (a confirmar com o orientador). RQ2 na
[numeração nova](#reformulacao-quatro-perguntas); a curva era a RQ1.*

**O que decidi:**
- Correr a curva completa (11 níveis, cinco sementes, Random Forest e
  Logistic Regression) numa só corrida, com as presenças de 2021–2025
  e o [fundo novo](#fundo-uniforme-reconstruido-2465), separando as
  presenças de teste por fonte.
- **Teste principal:** o global (ciência cidadã e especialistas
  juntos), como no desenho da curva. As presenças de especialistas
  sozinhas são uma segunda análise, reportada ao lado.
- **Critério:** a diferença emparelhada por semente entre 90% e 0%,
  pelo critério comum. Foi escrito, tal como a H₁, depois de ver a
  curva plana: não é um teste pré-registado.
- **Random Forest continua a ser o classificador principal** e a
  Logistic Regression passa a ser reportada como segundo classificador,
  não como referência barata.
- Deixar de descrever a curva como "plana" sem mais.

**O que deu (valores em
[`docs/research_questions.md`](../docs/research_questions.md#rq1--citizen-science-as-a-substitute-for-expert-data)):**
- No teste global, o Random Forest ganha cerca de 0,005 de ROC-AUC
  logo aos 10%–20% de polígonos e não sobe mais. Aos 90% não cumpre o
  critério; aos 20%–50% cumpre. O resultado depende do nível
  comparado; mantive 90% contra 0% para não ajustar o critério ao
  resultado.
- Só nas presenças de especialistas, o ROC-AUC do Random Forest sobe
  de 0,976 para 0,993 e cumpre o critério; o Boyce vai no sentido
  contrário.
- A Logistic Regression sobe 0,031 no teste global. A resposta
  depende do classificador.
- A queda a 100% vem toda das presenças de teste de ciência cidadã.

**Porquê:**
- O teste global mistura dois níveis muito diferentes (0,976 nos
  especialistas, 0,812 na ciência cidadã, no modelo de 0%), por isso
  a média escondia um ganho pequeno nos especialistas.
- As presenças de teste de ciência cidadã partilham provavelmente o
  enviesamento de amostragem do treino, por isso o teste global
  favorece os modelos treinados com ciência cidadã. A queda a 100%
  não quer dizer que o modelo só de especialistas seja pior.
- O ROC-AUC mais alto nos especialistas pode refletir presenças mais
  fáceis de separar do fundo, não equivalência entre as fontes.
- O Random Forest foi escolhido em 4 de novembro com as 3 000
  presenças de todos os anos, antes da curva. Com 2021–2025 a
  Logistic Regression continua com a média mais alta a 0% (0,874
  contra 0,836) e o argumento da estabilidade enfraquece (dp 0,041
  contra 0,055; era 0,028 contra 0,052).
- A consistência entre sementes não é evidência independente: as
  sementes reutilizam blocos (9 blocos distintos com polígonos em
  cinco sementes, 6 deles em duas).
- O Boyce mudou de 0,930 para 0,969 (global, 100%) só com a troca do
  fundo, enquanto o ROC-AUC coincidiu a 0,002: confirma que não deve
  decidir.

**Fundamentação:** nenhuma literatura nova consultada. O critério não
tem fonte externa. Os limites do Boyce estão em
[Métricas](#metricas-limites-boyce).

**Em aberto:** os diagnósticos da curva (fundo só de floresta,
redundância, pureza) não foram separados por fonte.

**Onde:** secção 8 de
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).
As entradas anteriores sobre a curva
descrevem as corridas com todos os anos ou com o fundo antigo.

**Na tese:** ⏳ Ainda não escrita (Resultados preliminares). Os
números são do Random Forest e da Logistic Regression em ROC-AUC
contra o fundo; desde 2026-11-17 não contam como resultado e a curva
é recorrida ([RQ1 passa a presence-only](#rq1-presence-only)).

**Revisão (2026-11-13, mais tarde no mesmo dia):** a numeração das
perguntas mudou. O que nesta entrada é a "RQ1" (dos pontos aos dados
de referência) passa a ser a RQ2, e a "RQ2" (curva de redução de
esforço) passa a ser a RQ1; a RQ3 e a RQ4 não mudam. Passei a numerar
por ordem de importância, o que também fica mais perto da numeração
que o orientador aprovou. O conteúdo desta entrada não muda; a secção
do notebook que aqui aparece como "secção 8" corresponde hoje às
secções 4 a 7. Ver [Renumeração das perguntas](#renumeracao-perguntas-2026-11-13).

**Revisão (2026-11-13, ao fim do dia):** depois do bloco acima a RQ3
e a RQ4 trocaram: a transferibilidade é a RQ3 e a comparação com o
Sentinel-2 é a RQ4. Ver a [tabela de numeração](#decisões).
O critério comum que esta entrada aplica foi retirado no ponto 5 da
[simplificação do desenho](#simplificacao-desenho-2026-11-13): onde
está "cumpre" ou "não cumpre", vale só a diferença reportada. Os
resultados estão hoje em `results/effort_reduction_curve/`
([script da curva](#curva-script-experiments)).

### Curva de redução de esforço: o cálculo passa a script em `experiments/` {#curva-script-experiments}

*Decisão minha, de 2026-11-13. É organização do repositório, segundo o
critério de [`experiments/README.md`](../experiments/README.md); o
desenho da curva não muda.*

**O que decidi:**

- **O cálculo da curva (RQ1) sai do notebook.** Passa a
  `experiments/effort_reduction_curve/run.py`, com a configuração
  fixa no topo (níveis, sementes 1 a 5, semente 0 da ordem dos
  polígonos, 20% de blocos de teste, os dois classificadores) e o
  código das secções 1 a 6 do notebook, sem alterar a lógica.
- **Saída fixa:** `results/effort_reduction_curve/`, com as cinco
  tabelas de antes, uma nova com o N nominal por nível
  (`nominal_levels.csv`) e um `run.json` com a configuração, o commit
  e os hashes das quatro entradas (presenças, polígonos, embeddings do
  piloto e fundo). O anterior só registava as presenças e o fundo.
- **O notebook só lê e desenha.**
  `notebooks/07_foundation_models/effort_reduction_curve.ipynb` fica
  com o propósito, as tabelas lidas dos resultados, a figura e a
  leitura da curva. Ao abrir compara os hashes do `run.json` com os
  ficheiros atuais e avisa se os resultados forem de outras entradas.

**Porquê:** a curva é o resultado que vai para os docs e para a tese e
volta a correr sempre que os dados mudam. Num notebook, o resultado
depende de que células foram corridas e por que ordem; num script com
entradas, sementes e pasta de saída fixas, uma tabela vem de uma só
execução, como pede a regra de reprodutibilidade do `CLAUDE.md`.

**O que verifiquei (2026-11-13):**

- As cinco tabelas escritas pelo script são idênticas byte a byte às
  que o notebook escrevia. Nenhum valor mudou.
- A figura gerada pelo notebook a partir das tabelas novas tem o mesmo
  hash da anterior.
- As contagens que o notebook imprimia (46 blocos candidatos, 9 blocos
  de teste por semente, 9 dos 18 blocos com polígonos num conjunto de
  teste, 1 265 píxeis de teste distintos em 2 122) vêm agora do
  `run.json` e são as mesmas.

**Limites e o que fica de fora:**

- `forest_only_background_check.ipynb` continua a ser um notebook com
  o código da curva duplicado. É o candidato seguinte; não o movi.
- Esse notebook compara o fundo de floresta com valores do fundo
  uniforme escritos à mão numa célula (por exemplo 0,879 de ROC-AUC
  global do Random Forest a 0%), que não são os da curva atual
  (0,902). Não corrigi; os docs citam só os valores do fundo de
  floresta (0,950 e 0,952), que são os atuais.
- As contagens feitas à mão a 2026-11-13 (filtros; polígonos perto e
  longe) continuam sem script.

**Fundamentação:** nenhuma literatura consultada; é prática de
reprodutibilidade, raciocínio meu.

**Onde:** [`experiments/effort_reduction_curve/run.py`](../experiments/effort_reduction_curve/run.py);
`results/effort_reduction_curve/`;
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).

**Na tese:** ⏳ Ainda não escrita. Se entrar, é uma frase sobre
reprodutibilidade na Metodologia.

**Revisão (2026-11-13, mais tarde no mesmo dia):** dois pontos desta
entrada deixaram de ser verdade. O script passou a ter também o
one-class SVM, numa tabela à parte (`one_class_per_seed.csv`), e uma
opção para o fundo; as tabelas da curva continuam idênticas. E os
dois primeiros limites ficaram resolvidos:
`forest_only_background_check.ipynb` já não tem o código da curva
duplicado nem valores escritos à mão. Ver
[Verificação com fundo só de floresta](#fundo-floresta-script-experiments).

### Verificação com fundo só de floresta: passa a ler duas execuções do script da curva {#fundo-floresta-script-experiments}

*Decisão minha, de 2026-11-13. É organização do repositório, na
sequência de [a curva passar a script](#curva-script-experiments); o
desenho da verificação não muda.*

**O que decidi:**

- **Um script, dois fundos.**
  `experiments/effort_reduction_curve/run.py` aceita
  `--background uniform` (por omissão, a curva da RQ1, em
  `results/effort_reduction_curve/`) ou `--background forest_only`
  (a verificação, em `results/effort_reduction_curve_forest_only/`).
  A única diferença entre as duas execuções é o ficheiro de fundo.
- **O one-class SVM entra no script.** A verificação compara três
  métodos e o script só tinha dois. O one-class SVM (`rbf`, `nu` 0,05)
  treina nas mesmas presenças em cada nível, é avaliado só no teste
  global e fica numa tabela à parte (`one_class_per_seed.csv`), nas
  duas execuções. As tabelas da curva não o incluem.
- **O notebook só lê e desenha.**
  `forest_only_background_check.ipynb` deixou de ter o código da curva
  duplicado: lê as duas pastas, verifica os hashes das entradas,
  monta a comparação e guarda a figura em
  `results/effort_reduction_curve_forest_only/`.
- **O texto de leitura do notebook ficou como estava**, de
  2026-11-07, com uma nota no início com os valores atuais.

**Porquê:** o notebook comparava o fundo de floresta com valores do
fundo uniforme escritos à mão numa célula, que eram de uma curva
anterior. Com as duas execuções a saírem do mesmo script e das mesmas
entradas, os dois lados da comparação são sempre da mesma versão dos
dados.

**O que verifiquei (2026-11-13):**

- **Fundo uniforme:** as seis tabelas e a figura de
  `results/effort_reduction_curve/` ficaram idênticas byte a byte às
  anteriores. Só o `run.json` mudou (tem dois campos novos).
- **Fundo de floresta:** os valores do script são iguais, às três
  casas decimais, aos que o notebook mostrava antes (33 linhas:
  3 métodos, 11 níveis).
- **Mudou a comparação**, como esperado, porque o lado do fundo
  uniforme passou a ser o da curva atual.

**Valores atuais (teste global, média de 5 sementes, fundo uniforme →
fundo de floresta):**

| Método | Métrica | 0% | 90% | 100% |
|---|---|---|---|---|
| Random Forest | ROC-AUC | 0,902 → 0,950 | 0,906 → 0,952 | 0,854 → 0,919 |
| Random Forest | Boyce | 0,995 → 0,995 | 0,993 → 0,988 | 0,969 → 0,902 |
| Logistic Regression | ROC-AUC | 0,893 → 0,958 | 0,924 → 0,962 | 0,873 → 0,905 |
| Logistic Regression | Boyce | 0,966 → 0,938 | 0,971 → 0,906 | 0,841 → 0,727 |
| One-class SVM | ROC-AUC | 0,574 → 0,504 | 0,693 → 0,650 | 0,831 → 0,814 |
| One-class SVM | Boyce | 0,668 → 0,197 | 0,918 → 0,655 | 0,885 → 0,534 |

**O que isto muda nas entradas anteriores:** os valores da entrada da
verificação de 2026-11-07 (por exemplo 0,879 → 0,934 no Random Forest
a 0%, Boyce de 0,567 na Logistic Regression a 100%, Boyce de −0,039 no
one-class SVM a 0%) são dessa execução, anterior à janela 2021–2025 e
ao fundo uniforme reconstruído. O sentido de cada conclusão é o mesmo
com os valores atuais: a curva do Random Forest continua plana e com
ROC-AUC mais alto no fundo de floresta, e o one-class SVM continua a
perder com esse fundo. O Boyce do one-class SVM a 0% já não é
negativo, mas varia muito entre sementes (desvio-padrão 0,723).

**Limites:** a leitura continua a ser no teste global; a verificação
separada por fonte das presenças de teste não foi lida, embora o
script já escreva essas tabelas para o fundo de floresta.

**Fundamentação:** nenhuma literatura consultada; raciocínio meu.

**Onde:** [`experiments/effort_reduction_curve/run.py`](../experiments/effort_reduction_curve/run.py);
`results/effort_reduction_curve_forest_only/`;
[`forest_only_background_check.ipynb`](../notebooks/07_foundation_models/forest_only_background_check.ipynb).

**Na tese:** ⏳ Ainda não escrita (Resultados/Metodologia).

**Revisão (2026-11-13, à noite):** repeti as duas execuções do script
(fundo uniforme e só de floresta) sobre o commit `43d7ede`, sem
alterações por gravar. Critério escrito antes de correr: as tabelas
tinham de sair iguais byte a byte. Saíram: as oito tabelas de cada
pasta são idênticas às anteriores, e só o `run.json` mudou, porque
regista agora esse commit em vez do `cc81a3f` com alterações por
gravar. Vale também para a entrada do
[script da curva](#curva-script-experiments).

### Curva da RQ1: nível "100% especialistas + ciência cidadã"; o "só especialistas" fica como referência à parte {#curva-100-mais-ciencia-cidada}

*Decisão minha, de 2026-11-14 (a confirmar com o orientador). Ajusta
o desenho da
[curva completa](#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos).*

**O que decidi:**
- A parte aditiva da curva passa a acabar num nível novo, **100% dos
  polígonos de especialistas mais a base inteira de ciência cidadã**.
- O modelo **só de especialistas** (o antigo "100%") fica, mas como
  ponto de referência à parte, desenhado separado da curva.
- A comparação principal da RQ1 não muda: 90% contra 0%, no teste
  global. O nível novo é reportado ao lado.

**Porquê:** do 90% para o 100% mudavam duas coisas ao mesmo tempo:
entravam mais 10% dos polígonos e saía toda a ciência cidadã. O último
troço da curva não era comparável aos outros, e a queda no teste
global a 100% (0,906 → 0,854) lia-se como se os especialistas
piorassem o modelo. Vem quase toda das presenças de teste de ciência
cidadã (0,801 → 0,677). Com o nível novo, a curva aditiva fica
contínua até ao fim. O "só especialistas" continua a ser preciso,
porque é o termo de comparação da pergunta principal (substituir os
dados de especialistas como dados de treino).

**Origem do "100% sem ciência cidadã":** está registado nesta lista
como parte da decisão do orientador de 2026-11-05 (ponto 2 da
[entrada do multiclasse](#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)),
mas a [ata dessa reunião](../docs/meetings/2026-11-05.md) só diz
"começar só com ciência cidadã e acrescentar progressivamente dados de
especialistas". Não sei se a saída da ciência cidadã no fim foi dita
por ele. O ponto "só especialistas" mantém-se, por isso nada do que
ele possa ter dito se perde.

**Critério, escrito antes de correr:**
- **Implementação:** o nível novo sai do mesmo script, numa tabela à
  parte. As tabelas que já existem têm de sair iguais byte a byte; se
  não saírem, paro e não uso os números novos.
- **O que se reporta:** diferença emparelhada de ROC-AUC por semente
  (média, dp, sementes com o mesmo sinal), com o Boyce ao lado, Random
  Forest e Logistic Regression, nos três conjuntos de teste (global,
  só especialistas, só ciência cidadã), em três comparações: nível
  novo menos 0%, nível novo menos 90% e nível novo menos "só
  especialistas".
- **Sem hipótese nova e sem limiar.** Não escrevo uma expectativa de
  sentido para o nível novo; reporta-se a diferença.
- O one-class SVM não é avaliado no nível novo (só serve à verificação
  com fundo de floresta).

**Fundamentação:** nenhuma literatura consultada; raciocínio meu. Não
procurei precedente para curvas de mistura de fontes com um ponto
final aditivo e um de substituição.

**Impacto:** `experiments/effort_reduction_curve/run.py` (nível novo);
`results/effort_reduction_curve/` (tabela nova; as outras não podem
mudar); [`docs/research_questions.md`](../docs/research_questions.md#rq1--citizen-science-as-a-substitute-for-expert-data)
(desenho e resultado da RQ1);
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb)
(figura). As pastas do fundo só de floresta e da zona-tampão não são
corridas de novo e ficam sem o nível novo.

**Na tese:** ⏳ Ainda não escrita (Metodologia e Resultados
preliminares, ainda esqueletos). O desenho do nível novo mantém-se;
os números são do Random Forest e da Logistic Regression em ROC-AUC e
desde 2026-11-17 não contam como resultado
([RQ1 passa a presence-only](#rq1-presence-only)).

**O que deu (corrida de 2026-11-14, `results/effort_reduction_curve/`,
commit `5add326`):**

- **Critério de implementação cumprido:** as sete tabelas que já
  existiam saíram iguais byte a byte às da corrida de 2026-11-13. Só
  mudou o `run.json`; as duas tabelas novas são
  `plus_cs_per_seed.csv` e `plus_cs_paired_differences.csv`.
- **N de treino nominal do nível novo:** 1 457 polígonos (2 771
  píxeis) mais 2 464 presenças de ciência cidadã, 5 235 no total.

ROC-AUC, média de cinco sementes; diferença emparelhada (dp; sementes
a subir/a descer):

| Classificador, teste | 100% + CC | menos 0% | menos 90% | menos só especialistas |
|---|---|---|---|---|
| RF, global | 0,906 | +0,004 (0,006; 3/2) | −0,000 (0,002; 3/2) | +0,051 (0,016; 5/0) |
| RF, só especialistas | 0,993 | +0,017 (0,006; 5/0) | +0,000 (0,000; 4/1) | −0,001 (0,000; 0/5) |
| RF, só ciência cidadã | 0,799 | −0,013 (0,017; 2/3) | −0,002 (0,005; 2/3) | +0,122 (0,062; 5/0) |
| LR, global | 0,924 | +0,031 (0,007; 5/0) | +0,000 (0,000; 2/3) | +0,050 (0,026; 5/0) |
| LR, só especialistas | 0,988 | +0,061 (0,012; 5/0) | +0,001 (0,000; 5/0) | −0,008 (0,002; 0/5) |
| LR, só ciência cidadã | 0,836 | −0,004 (0,014; 2/3) | −0,001 (0,001; 1/4) | +0,122 (0,075; 5/0) |

Boyce do RF no teste global: 0,995 no nível novo, igual ao de 0% e
de 90%.

**Leitura:**
- **A curva aditiva fica plana até ao fim.** Do 90% para o 100% + CC
  nada muda (diferenças de 0,000 a 0,002). A queda que se via a 100%
  vinha de tirar a ciência cidadã, não de acrescentar especialistas.
- **Contra o modelo só de especialistas:** nas presenças de
  especialistas, juntar a ciência cidadã quase não custa (RF −0,001,
  LR −0,008, mas a descer nas cinco sementes); nas presenças de
  ciência cidadã ganha +0,122. Que isto venha de o teste de ciência
  cidadã partilhar o enviesamento do treino continua a ser hipótese,
  não testada.
- A comparação principal (90% contra 0%) e a sua leitura não mudam.

## Decisões: validação e Sentinel-2

### Validação espacial no lado dos especialistas: zona-tampão, além dos blocos de 10 km

*Decisão minha (unidade assumida, não confirmada pelo orientador), a
partir de algo que ele disse na reunião de 2026-11-05.*

**O que o orientador disse (recordado, não citação exata):** escolher
pontos de teste só ao acaso arrisca ficarem ao lado de pontos de
treino, o que infla o desempenho. Deu os números "20/30" como
zona-tampão, sem unidade.

**O que decidi:** validação por blocos espaciais de 10 km, o método
usado em todas as experiências. No lado dos especialistas, acrescentar
uma zona-tampão, assumida como 20–30 m, sem voltar a perguntar. Ainda
não implementada: para janeiro fica como limitação conhecida.

**Porquê:** os polígonos são manchas contíguas, por isso um píxel de
teste pode ficar a poucos metros de um de treino. Gastar tempo de
reunião a confirmar a unidade não compensa. Fica registado que a
leitura mais provável é outra:
- A literatura diz que a distância não é uma constante: deve
  corresponder ao alcance da autocorrelação espacial, estimado dos
  dados (Le Rest et al., 2014; Karasiak et al., 2022; Mahoney et al.,
  2023), e subestimá-lo é o lado perigoso (Le Rest et al.).
- A biblioteca de Karasiak (Museo ToolBox) define a distância em
  píxeis, o que daria 200–300 m; o tampão do próprio artigo foi cerca
  de 19,7 km, tirado de um correlograma.
- O variograma dos embeddings TESSERA nos nossos dados estabiliza por
  volta dos 300–500 m (primeira estimativa, não um ajuste formal).

**Fundamentação:** nenhuma para os 20–30 m; é uma escolha pragmática,
e a literatura e o variograma apontam para distâncias maiores.

**Correção (2026-11-11, releitura integral):** eu tinha escrito que o
bloqueio espacial foi pelo menos tão robusto quanto a zona-tampão nas
simulações de Mahoney et al. Não é isso que mostram: o melhor
resultado é de blocos combinados com um tampão de exclusão, e blocos
sem tampão não são reportados. Karasiak et al. e Ratsakatika et al.
dizem o mesmo (em Ratsakatika, PR-AUC 0,84 sem tampão contra 0,73 com
10 km). Os blocos de 10 km sem tampão entre treino e teste ficam como
limitação conhecida, nos dois braços e não só no dos especialistas.

**Onde:** [`tessera_spatial_autocorrelation.ipynb`](../notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb);
[`docs/methodology.md`](../docs/methodology.md#validation).

**Na tese:** ✅ Parcial. A validação espacial é referida em resumo na
Introdução; o conceito (fuga por autocorrelação, blocos, tampão ao
alcance medido, Karasiak, Le Rest, Mahoney, Ratsakatika) está na
secção 2.5.2 do Background (2026-11-18); o desenho da zona-tampão e o
variograma ficam para a Metodologia.

**Revisão (2026-11-13, revisão de consistência):** li mal o
variograma. Pela tabela do notebook, a semivariância quase não muda
entre 200–300 m e 300–400 m (1,72 e 1,74), volta a subir aos
400–500 m (2,00) e fica entre 2,0 e 2,2 a partir dos 500 m. Estabiliza
entre 500 m e 1 km, não aos 300–500 m.

- **Consequência:** aos 200–300 m a semivariância está a cerca de 80%
  do patamar, e aos 20–30 m a cerca de 40%. O variograma deixa de
  apoiar a leitura de "20/30" como píxeis; as duas leituras ficam
  abaixo do alcance.
- **A decisão não muda:** tampão por implementar, declarado como
  limitação.
- **Limites:** médias por classe de distância, sem modelo ajustado;
  as duas primeiras classes têm 61 e 48 pares.

**Revisão (2026-11-14):** contei quanto um tampão retiraria, sem o
implementar. Nas cinco divisões da curva, pontos de treino a menos de
uma dada distância de qualquer ponto de teste (soma das cinco
sementes):

| Fonte | Pontos de treino | ≤ 30 m | ≤ 300 m | ≤ 1 km |
|---|---|---|---|---|
| Ciência cidadã | 9 774 | 3 | 142 | 754 (7,7%) |
| Especialistas | 11 733 | 14 | 303 | 1 067 (9,1%) |
| Fundo | 8 631 | 0 | 5 | 130 (1,5%) |

- **Leitura:** com blocos de 10 km, um tampão de 20–30 m quase não
  retira nada (17 presenças em 21 507). A 300 m retira cerca de 2% e
  a 1 km, o alcance do variograma, cerca de 8,5%, mas de forma muito
  desigual: na semente 5 são 630 dos 2 182 píxeis de especialistas e
  380 das 1 581 presenças de ciência cidadã; na semente 2 são 29 e 2.
- **O que os dados não dizem:** se retirar estes pontos muda o
  ROC-AUC. Não repeti a curva com tampão; continua a ser limitação
  declarada, agora com número.
- **Para o orientador:** a unidade do "20/30" só pesa se forem
  píxeis ou mais; em metros o tampão não muda quase nada.
- **Onde:** secção 5 de
  [`design_counts.ipynb`](../notebooks/05_data_integration/design_counts.ipynb);
  [`docs/methodology.md`](../docs/methodology.md#validation).

**Revisão (2026-11-14, efeito medido):** *decisão minha.* Repeti a
curva da RQ1 com um tampão de 300 m e de 1 km entre treino e teste,
como exceção que aprovei ao "sem novas experiências antes de janeiro".
Muda o que estava decidido ("tampão por implementar, declarado como
limitação"): o tampão fica implementado como opção do script, o efeito
fica medido, e a limitação passa a análise de sensibilidade.

**O que decidi:** o desenho continua sem tampão. Os tampões de 300 m e
de 1 km são reportados ao lado da curva como análise de sensibilidade.

**Como foi medido:** em cada semente saem do treino todos os pontos
(ciência cidadã, especialistas e fundo) a menos dessa distância de
qualquer ponto de teste. O conjunto de teste é o mesmo nas três
condições. Sem tampão, o script reproduz as tabelas da curva byte a
byte. Os pontos retirados coincidem com a contagem da revisão anterior.

**Critério, escrito antes de correr com tampão:** em cada comparação,
a diferença de ROC-AUC face à curva sem tampão, emparelhada por
semente, tem média menor em módulo do que o seu desvio-padrão entre as
cinco sementes. O tampão não muda a leitura da RQ1 só se as 16
comparações cumprirem: níveis 0%, 90% e 100% e a diferença 90% − 0%,
para os dois classificadores, no teste global e só nas presenças de
especialistas. Declarei também, sem poder de decisão, o valor absoluto
da diferença, o sinal de 90% − 0% e a repetição sem a semente 5.

**Resultado (ROC-AUC, média das cinco sementes; d = com tampão − sem
tampão, média ± desvio-padrão):**

| Classificador, teste | Nível | Sem tampão | d 300 m | d 1 km |
|---|---|---|---|---|
| RF, global | 0% | 0,9018 | −0,0022 ± 0,0024 | −0,0075 ± 0,0078 |
| RF, global | 90% | 0,9061 | −0,0009 ± 0,0025 | **−0,0065 ± 0,0057** |
| RF, global | 100% | 0,8543 | −0,0001 ± 0,0015 | −0,0019 ± 0,0060 |
| RF, global | 90% − 0% | +0,0043 | +0,0014 ± 0,0043 | +0,0010 ± 0,0059 |
| RF, especialistas | 0% | 0,9761 | −0,0004 ± 0,0021 | −0,0007 ± 0,0036 |
| RF, especialistas | 90% | 0,9927 | +0,0005 ± 0,0006 | −0,0004 ± 0,0007 |
| RF, especialistas | 100% | 0,9936 | +0,0002 ± 0,0008 | 0,0000 ± 0,0012 |
| RF, especialistas | 90% − 0% | +0,0165 | +0,0009 ± 0,0020 | +0,0003 ± 0,0038 |
| LR, global | 0% | 0,8930 | −0,0015 ± 0,0015 | −0,0052 ± 0,0079 |
| LR, global | 90% | 0,9236 | −0,0006 ± 0,0008 | **−0,0039 ± 0,0027** |
| LR, global | 100% | 0,8732 | −0,0004 ± 0,0006 | +0,0007 ± 0,0074 |
| LR, global | 90% − 0% | +0,0306 | +0,0009 ± 0,0010 | +0,0013 ± 0,0061 |
| LR, especialistas | 0% | 0,9270 | −0,0012 ± 0,0018 | −0,0016 ± 0,0081 |
| LR, especialistas | 90% | 0,9869 | −0,0004 ± 0,0004 | **−0,0019 ± 0,0011** |
| LR, especialistas | 100% | 0,9960 | −0,0001 ± 0,0002 | −0,0009 ± 0,0011 |
| LR, especialistas | 90% − 0% | +0,0599 | +0,0009 ± 0,0017 | −0,0002 ± 0,0085 |

- **300 m:** critério cumprido nas 16 comparações.
- **1 km:** não cumprido, 13 de 16. Falham as três a negrito, todas no
  nível 90% e todas a descer. As quatro diferenças 90% − 0% cumprem.
- **O que a RQ1 reporta (90% − 0%):** mantém o sinal nas quatro
  comparações e nas duas distâncias, e muda no máximo 0,0014. Em RF
  global as sementes a favor passam de 4 para 3; nas outras três
  continuam a ser as 5.
- **Semente 5** (27% das presenças de treino retiradas a 1 km): dá
  34%, 35% e 12% da soma das diferenças nas três comparações que
  falham, e as três falham também sem ela. Sem a semente 5 cumprem 15
  de 16 a 300 m e 12 de 16 a 1 km.
- **Boyce (só reportado):** a maior alteração é em LR, só
  especialistas, a 100%, de 0,782 para 0,938 com 1 km.

**Porquê:**
- A conclusão da RQ1 não depende do tampão, por isso não compensa
  repetir a curva canónica, a verificação com fundo só de floresta e o
  que partilha as divisões antes de janeiro.
- Os níveis absolutos de ROC-AUC sem tampão ficam ligeiramente
  otimistas (até 0,0075 a 1 km), e isso tem de ficar dito ao lado da
  curva. O critério falhou a 1 km, por isso não chega declarar a
  limitação.
- Não adoto 300 m como desenho. O tampão é parte da avaliação, não do
  modelo: escolher a distância que dá o ROC-AUC mais alto é circular,
  porque é o que a fuga espacial também produziria. A distância que os
  dados apoiam é o alcance do variograma, entre 500 m e 1 km.

**O que os dados não dizem:** se a descida a 1 km vem de menos
proximidade ou de menos dados de treino; a experiência não separa as
duas coisas. As sementes reutilizam blocos, por isso a concordância
entre elas não é evidência independente.

**Fundamentação:** a recomendação de blocos com tampão e a distância
pelo alcance da autocorrelação são as já citadas nesta entrada (Le
Rest et al., 2014; Karasiak et al., 2022; Mahoney et al., 2023;
Ratsakatika et al., 2026). Para o critério e para reportar como análise
de sensibilidade em vez de adotar no desenho não procurei literatura:
raciocínio próprio.

**Onde:** [`run.py`](../experiments/effort_reduction_curve/run.py)
(`--buffer-m`) e
[`compare_buffer.py`](../experiments/effort_reduction_curve/compare_buffer.py);
tabelas em `results/effort_reduction_curve_buffer_300m/`,
`..._buffer_1000m/` e `..._buffer_comparison/`;
[`docs/methodology.md`](../docs/methodology.md#validation).

**Na tese:** ⏳ Ainda não escrita. A análise de sensibilidade pertence
à Metodologia (validação) e aos resultados da RQ1; o resultado a
reportar é o da Revisão de 2026-11-17 (desenho presence-only), não o
do Random Forest.

**Revisão (2026-11-17, desenho presence-only):** a medição acima foi
feita com o Random Forest e os cinco sorteios, e deixa de ser
reportada. O tampão continua opção de `run.py`, agora por fold
(saem do treino os pontos a menos da distância de qualquer ponto de
teste do bloco retido). **Critério, escrito antes de correr:** em cada
comparação, a diferença de sensitivity a 10% de área face à curva sem
tampão, emparelhada por fold, tem média menor em módulo do que o seu
desvio-padrão entre os 26 folds (ou é zero em todos). O tampão não
muda a leitura da RQ1 só se as 8 comparações cumprirem: 0%, 90%, 100%
e 90% − 0%, no teste agrupado e só nas presenças de especialistas.
Reporto também, sem poder de decisão, a diferença nos valores
agrupados e o ROC-AUC.

**Resultado (2026-11-17, `results/effort_reduction_curve_buffer_comparison/`;
sensitivity a 10% de área, d = com tampão − sem tampão, média ± dp por
fold, 26 folds):**

| Teste | Nível | Sem tampão (agrupado) | d 300 m | d 1 km |
|---|---|---|---|---|
| Agrupado | 0% | 0,531 | −0,001 ± 0,006 | −0,006 ± 0,019 |
| Agrupado | 90% | 0,692 | −0,001 ± 0,004 | −0,006 ± 0,014 |
| Agrupado | Só especialistas | 0,701 | +0,001 ± 0,004 | −0,003 ± 0,012 |
| Agrupado | 90% − 0% | +0,161 | −0,001 ± 0,007 | +0,001 ± 0,020 |
| Especialistas | 0% | 0,637 | −0,003 ± 0,009 | −0,006 ± 0,020 |
| Especialistas | 90% | 0,933 | −0,001 ± 0,003 | −0,004 ± 0,012 |
| Especialistas | Só especialistas | 0,983 | −0,000 ± 0,001 | −0,002 ± 0,004 |
| Especialistas | 90% − 0% | +0,296 | +0,002 ± 0,009 | +0,002 ± 0,022 |

- **Critério cumprido nas 8 comparações, às duas distâncias.** O
  tampão não muda a leitura da RQ1.
- **Sentido:** a 1 km os níveis descem quase todos (por fold, 6 a 8
  folds a descer contra 1 a 2 a subir, no agrupado), até 0,006; a
  diferença 90% − 0% não muda (agrupada: 0,161 → 0,169 a 300 m e
  0,189 a 1 km, o sinal e a ordem de grandeza ficam).
- **Quanto sai do treino:** a 300 m, 0,4% das presenças de ciência
  cidadã e 0,6% dos píxeis de especialistas (máximo por fold 5%); a
  1 km, 2,0% e 1,8% (máximo 23% e 21%, nos folds 56_444 e 57_444); o
  fundo quase nada (0,2%).
- **ROC-AUC (só reportada):** diferenças até 0,003.
- **O que os dados não dizem:** se a descida a 1 km vem de menos
  proximidade ou de menos dados de treino, como antes. A fuga por
  fronteira de bloco, a existir, pesa menos de 0,01 na sensitivity a
  10% de área.
- **Onde:** [`compare_buffer.py`](../experiments/effort_reduction_curve/compare_buffer.py);
  secção 7 de
  [`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).

### Sentinel-2 bruto: via Earth Search (AWS), sem conta, alinhado à grelha da TESSERA

*Decisão minha.*

**O que decidi:** descarregar o Sentinel-2 L2A pelo catálogo STAC
Earth Search da AWS (sem conta), alinhado píxel a píxel à grelha da
TESSERA, com leitura por janelas. Resultado: só uma faixa estreita de
teste, não a extensão do piloto. Especificação em
[`data/README.md`](../data/README.md#sentinel-2-l2a-tessera-grid-2023).

**Porquê:** o mosaico completo seria demasiado lento nesta ligação
(10–16 h ou mais), e usar a grelha da TESSERA garante o alinhamento.

**Fundamentação:** escolha técnica de acesso, não metodológica. O
Sentinel-2 como sensor do baseline está fundamentado em Mouta et al.
(2021) e Domingo et al. (2023).

**Onde:** [`sentinel2_download.ipynb`](../notebooks/04_satellite/sentinel2_download.ipynb).

**Na tese:** ⏳ Ainda não escrita (detalhe técnico; Metodologia ou
apêndice, se for preciso).

### Sentinel-2 na RQ1: avançar já, por extração em pontos, não raster completo

*Decisão minha, revertida no mesmo dia.*

**O que tentei:** deixar de adiar o braço Sentinel-2, extraindo as
bandas só nos pontos já usados para a TESSERA, em vez de um raster
completo.

**Porque foi revertida:** medida, a extração por pontos não é mais
barata. Os cerca de 31 000 pontos cobrem quase toda a extensão, por
isso a leitura toca quase todos os blocos dos ficheiros. Amostrar
2 000 pontos numa banda de uma cena demorou 37 s; multiplicado por 12
bandas e dezenas de cenas, é inviável. O acesso a este bucket também
está anormalmente lento neste ambiente.

**O que decidi:** o braço Sentinel-2 volta a ficar em espera, como na
indicação original do orientador. Falta decidir como reduzir o custo
(menos cenas, resolução mais grosseira ou outro ambiente).

**Onde:** sem notebook.

**Na tese:** ⏳ Ainda não escrita. Para janeiro, o Sentinel-2 é
declarado como risco no plano de trabalho.

### Conjunto de features do Sentinel-2 na RQ1: compósito anual (Ball et al.), fenologia da floração como extensão por ablação (Domingo et al.)

*Proposta minha, não confirmada pelo orientador.*

**O que decidi:** a primeira versão do braço Sentinel-2 usa o
compósito anual de Ball et al. (2026): mediana anual das 12 bandas de
2023, mais NDVI, NDWI (McFeeters) e NBR, com máscara de nuvens por SCL
(classes 4/5/6/7) e QA60, e `CLOUDY_PIXEL_PERCENTAGE < 60`. As features
de fenologia da floração de Domingo et al. (2023) entram depois, por
ablação, acrescentadas ao conjunto anual.

**Porquê:** o compósito anual é o mais simples e não é específico de
espécie. O conjunto de Domingo et al. depende de uma janela de
floração encontrada na Galiza (março); aplicá-lo a Coimbra sem
verificar seria assumir um facto não confirmado.

**Em aberto:** a janela de floração para Portugal central.

**Da releitura integral (2026-11-11):** a variante reportada nos
números principais de Ball et al. é a sazonal, e sempre com
Sentinel-1; a anual fica abaixo (F1 ponderado 0,745 contra 0,803). O
meu braço é só Sentinel-2 e anual, por isso é uma linha de base mais
fraca do que a deles. Martins, Mouta e Domingo encontram todos o
sinal em meses específicos ou em diferenças entre eles, o que dá mais
peso à ablação da floração.

**Fundamentação:** Ball et al. (2026), pelo código-fonte dos autores e
pelo texto integral; Domingo et al. (2023), texto integral. Resumos em
[`docs/literature.md`](../docs/literature.md).

**Onde:** sem notebook; ainda não implementado.

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia).

**Revisão (2026-11-17):** a escolha de "Random Forest e regressão
logística" para o braço Sentinel-2 fica superada: o Random Forest
presença-vs-fundo foi abandonado na RQ1 (usa o fundo como
pseudo-ausência), e o braço passa a usar só o classificador
presence-only escolhido na RQ1, a regressão logística presença-fundo
([#rq1-presence-only](#rq1-presence-only)).

## Decisões: documento e entrega

### Lista de literatura: releitura integral e limpeza

*Decisão minha, de 2026-11-11.*

**O que decidi:** reler todas as entradas de `docs/literature.md` a
partir do texto integral, corrigir os resumos e eliminar as que não
apoiam nenhuma decisão.

**Resultado:** ficam 31 entradas. 25 lidas na íntegra; Dimson et al.
(2023) só na versão submetida (o artigo publicado está bloqueado);
três só pelo resumo
(Li, Guo & Elkan 2011; Li & Guo 2010; Mack & Waske 2017); duas não
publicadas (grupo de Cambridge, apresentação da Radová).

**Eliminadas (10):**
- Liu et al. 2026 (Tighnari v2): só servia a regra dos polígonos da
  COS.
- Wölk et al. 2026: outro problema, e inacessível.
- Cardoso et al. 2024: fotografias ao nível do solo, não satélite.
- Skowronek et al. 2017, Zhu, Samat et al. 2025, Zagajewski et al.
  2024 e Li & Guo 2014: não testam um método one-class verdadeiro, ou
  são de uma métrica que não uso.
- Lucas et al. 2026 (atóis): o braço Sentinel-2 é de 2024–2025 contra
  embeddings de 2023, por isso não apoia o ano de referência único.
- Eskandari et al. 2025: só o resumo é acessível; género *Acacia*,
  imagens de junho.
- Zhang et al. 2025 (timberline): o crescimento de região só refina a
  orla de uma mancha já mapeada.

**Identificações corrigidas:** "Zhu et al. 2026" é Stewart, Fang,
Corley & Zhu; "Gonçalves et al. 2026" é Silva & Gonçalves, um preprint
do Porto em que o Sentinel-2 ganha aos embeddings; o artigo do
goldenrod é Malinowski et al. 2025; o TESSERA saiu no CVPR 2026.

**O que mudou na fundamentação:** cada correção está na entrada da
decisão respetiva (precisão posicional, uma observação por píxel,
Observer A, Random Forest, fundo uniforme, validação espacial,
features do Sentinel-2, RQ2, RQ3, Boyce).

**Em aberto:** descarregar à mão o artigo publicado de Dimson et al.;
ler Ma et al. (2026), a fonte primária da frase sobre transferência
espacial; a entrada `zhu2026` do manuscrito tem o autor errado.

**Onde:** [`docs/literature.md`](../docs/literature.md).

**Na tese:** ✅ Parcial (2026-11-17). Em `references.bib`, `zhu2026`
tem agora os autores certos (Stewart, Fang, Corley & Zhu) e `feng2025`
e `karasiak2022` as versões publicadas. Falta a Introdução: ainda cita
`zhu2026` para a linha da transferência para outras regiões, que
devia citar Yang et al. (2026) (ver a [revisão de consistência](#revisao-consistencia-2026-11-13)).

**Revisão (2026-11-14):** pesquisa web para testar os gaps e cinco
entradas novas. Ficam 36 entradas.

- **Pesquisa:** doze consultas web, sem Scopus nem Web of Science
  (não tenho acesso por aqui). O
  [protocolo](#protocolo-de-pesquisa-da-literatura) continua por
  executar. Não apareceu nenhum estudo que treine o mesmo
  classificador de satélite com rótulos de ciência cidadã e com
  rótulos de especialistas para uma planta invasora, nem embeddings
  de foundation models aplicados a invasoras.
- **Lidas na íntegra (texto extraído do PDF ou da página; figuras só
  pelas legendas):** Ma et al. (2026, manuscrito do arXiv, não o
  artigo publicado); Koukos et al. (2026, preprint); Fonte et al.
  (2020); Milanesi et al. (2020); Raine et al. (2026, versão do
  arXiv).
- **O que mudou na fundamentação:**
  - *Transferência espacial:* a frase "nenhum compara as duas
    representações sob transferência" deixou de ser verdade. Ma et
    al. comparam: o AlphaEarth transfere pior na regressão de
    produtividade e de forma mista na classificação. Não cobre
    espécies nem o TESSERA.
  - *RQ2, máscara:* Raine et al. (2026) já propagam pontos por
    semelhança em features congeladas de um foundation model. O "sem
    precedente" fica mais estreito: um só ponto, só de presença, com
    limiar, conectividade e raio, em embeddings de satélite.
  - *RQ2, filtros:* Fonte et al. (2020) medem o efeito de filtrar
    dados voluntários de treino. Os filtros melhoraram sempre os
    dados de treino e só numa das duas áreas o mapa.
  - *RQ3:* Milanesi et al. (2020) não analisam a concentração num
    observador; o "sem precedente" mantém-se.
  - *RQ4:* Koukos et al. (2026) apoiam os dois níveis de dados
    (features convencionais à frente com todos os dados, TESSERA à
    frente abaixo de cerca de 25%). Trazem também um risco: com
    Random Forest a distância a favor das features convencionais é
    de 8,4 pontos, contra 1,1 com uma rede neuronal.
  - *RQ1:* o gap mantém-se. Fonte et al. não treinam nenhum
    classificador com dados de especialistas para comparar.
- **Por ler:** Di Cecco et al. (2021, "Observing the Observers",
  fechado); o pacote AlphaSDM (CRAN); a literatura de informação
  geográfica voluntária como dados de treino para além de Fonte et
  al. (2020).
- **Tarefa fechada:** ler Ma et al. (2026). Falta o artigo publicado.

**Revisão (2026-11-14, trabalhos dos orientadores):** duas entradas
novas, de trabalhos dos meus orientadores. Ficam 38 entradas.

- **Porquê:** Fonte et al. (2020) tem o Prof. Duarte como coautor e
  cita trabalhos do Prof. Estima. Fui ver a lista de publicações dos
  dois (ORCID e CiênciaVitae) para saber o que da linha deles serve as
  minhas perguntas.
- **Lidas na íntegra (texto extraído do PDF; figuras só pelas
  legendas) e acrescentadas:** Duarte et al. (2022), transferência
  entre duas regiões de Portugal de modelos treinados com
  OpenStreetMap, que apoia a RQ3; Fonte et al. (2017), revisão da
  qualidade de dados voluntários, que enquadra os filtros da RQ2 (o
  acordo entre voluntários mede fiabilidade, não exatidão).
- **Lidas e deixadas de fora:** Antoniou et al. (2016), fotografias
  georreferenciadas de Londres sem classificador nem dados de
  referência; Duarte et al. (2023), comparação da COS 2018 com o
  WorldCover, cujo limite útil (unidade mínima de 1 ha) já está na
  entrada de Fonte et al. (2020). Não mudam nenhuma decisão.
- **O que se mantém:** nenhum dos quatro analisa um contribuidor
  dominante nem compara treino voluntário com treino de especialistas;
  os gaps da RQ1 e da RQ3 ficam como estavam.
- **Por ler:** três trabalhos do grupo de que só vi o título e que
  pedi na [próxima reunião](../docs/meetings/2026-11-17.md)
  (floração da *A. dealbata* na Lousã, avaliação de uma classe rara,
  segmentação fracamente supervisionada de invasoras); See et al.
  (2016) e Fonte et al. (2024), públicos mas não obtidos.

**Revisão (2026-11-17):** não pedi os três trabalhos do grupo na
reunião de 2026-11-17; dou o ponto por resolvido e ficam fora da
lista por ler.

**Revisão (2026-11-17, leitura do que faltava):** lidos na íntegra
Phillips et al. (2006, cópia do autor via Internet Archive), Peterson
et al. (2008, cópia na WHOI), Elkan & Noto (2008, PDF do autor), Li,
Guo & Elkan (2011) e Li & Guo (2010, cópias na página do Guo na UC
Merced); figuras só pelas legendas. Ficam 41 entradas: 35 lidas na
íntegra; 3 noutra versão (Dimson 2023, Ma 2026, Raine 2026); 1 só
resumo (Mack & Waske 2017: a *Remote Sensing Letters* está paga e o
repositório da FU Berlin com a tese do autor bloqueou o acesso
automático); 2 não publicadas. O artigo publicado de Dimson et al.
continua bloqueado por aqui (Wiley) e o de Ma et al. (Elsevier) não
foi obtido; o de Raine et al. (IEEE) não foi tentado. O que mudou na
fundamentação está na
[entrada da RQ1 presence-only](#rq1-presence-only) (Revisão de
2026-11-17, leitura das fontes da métrica). Verifiquei também a
consistência de `docs/literature.md` com o desenho atual: só a nota da
secção one-class apontava ainda para a entrada do multiclasse; passou
a apontar para a entrada presence-only.

### Identidade da tese confirmada: título, mestrado, orientadores, idioma e data da entrega

*Factos fixos da tese, não decisões de desenho.*

- Mestrado em Inteligência Artificial e Ciência de Dados.
- Título: "Advancing the Mapping of Invasive Alien Plants by Combining
  Citizen Science, Earth Observation Foundation Models and Satellite
  Imagery" / "Mapeamento de Plantas Exóticas Invasoras através da
  Combinação de Ciência Cidadã, Modelos Fundacionais de Observação da
  Terra e Imagens de Satélite".
- Orientadores: Professor Jacinto Paulo Simões Estima e Professor
  Diogo André Vicente Amorim Duarte.
- O documento é escrito em inglês.

**Onde:** `thesis/document/0-main.tex` (bloco CONFIGURATION).

**Na tese:** ✅ Feito. Capa e página de título já refletem estes
dados.

### Primeira entrega: relatório intermédio, início de janeiro de 2027

*Facto do calendário; âmbito decidido por mim em 2026-11-10.*

**O que sei:** a primeira entrega é um relatório intermédio, no início
de janeiro de 2027 (sem data exata), não a tese final.

**Âmbito para janeiro:**
- RQ1 só com TESSERA, nos dois braços, como resultado preliminar.
- Sentinel-2 declarado como risco e plano de trabalho, não como
  resultado em falta.
- RQ2 e RQ3 só no plano de trabalho.
- Máscara de segmentação apresentada como comparação em curso.
- Sem novas experiências nem código antes da entrega.

**Em aberto:** o mapeamento de `thesis/document/text/` (hoje com forma
de tese final, com capítulo de Resultados) para a forma de relatório
intermédio.

**Onde:** [`docs/todo.md`](../docs/todo.md).

**Na tese:** ⏳ Ainda não escrita; é a própria entrega que está em
causa.

**Revisão (2026-11-13, revisão de consistência):** dois pontos do
âmbito acima deixaram de corresponder ao que fiz.

- **"Sem novas experiências nem código":** a 13 de novembro voltei a
  correr a curva com as presenças de 2021–2025, passei-a a script e
  reconstruí o fundo. A regra vale daqui em diante, com duas exceções
  que aprovei no mesmo dia: voltar a correr a célula corrigida do
  `label_purity_check` (feito) e repetir a curva depois de um commit,
  para o `run.json` registar o commit certo.
- **"RQ2 e RQ3 só no plano de trabalho":** na numeração atual são a
  RQ2, a RQ3 e a RQ4; a RQ1 (curva, só TESSERA) é o resultado
  preliminar. Ver a [tabela de numeração](#decisões).

**Revisão (2026-11-17):** nova exceção a "sem novas experiências nem
código", pela mesma razão da de 2026-11-13: a comparação one-class
reaberta a pedido do orientador
([`thesis/notes.md`](#one-class-reaberto-avaliação-sem-fundo-sensitivity-grelha-espacial-e-ensemble-pca--isolation-forest))
corrige a avaliação da própria RQ1 que vai no relatório de janeiro, por
isso corre antes da entrega e não fica para "Depois da defesa
intermédia".
