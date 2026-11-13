# Notas para a Tese

Coisas que quero dizer na tese e na defesa, e o registo do que decidi e
porquê. O estado atual do desenho está em
[`docs/research_questions.md`](../docs/research_questions.md) e
[`docs/methodology.md`](../docs/methodology.md); aqui fica o raciocínio.

Cada entrada segue a mesma forma: quem decidiu, **O que decidi**,
**Porquê**, **Fundamentação**, **Onde**, **Na tese**.

## Para dizer

*Numeração: os pontos desta secção usam as quatro perguntas atuais
(a confirmar com o orientador; ver
[Renumeração das perguntas](#renumeracao-perguntas-2026-11-13)). O
manuscrito ainda tem as três perguntas que ele aprovou.*

### Perguntas ambiciosas

*Sugestão dos orientadores para a defesa.*

> "Tenho noção de que as perguntas são ambiciosas. Por isso estão
> ordenadas de modo que cada uma só usa o que as anteriores definem: a
> RQ1 é o núcleo e já está medida; a RQ2 e a RQ3 reutilizam o modelo
> e os dados da RQ1, só com TESSERA; a RQ4 é a única que depende do
> Sentinel-2 e fica para o fim. Vou ajustando consoante o que os dados
> e o tempo permitirem."

Porque esta ordem se defende:
- A RQ1 sozinha já responde ao objetivo principal da proposta e ao
  objetivo 3: é um resultado completo.
- A RQ2 responde ao objetivo 1 da proposta. A parte dos filtros corre
  com os embeddings já guardados; a máscara precisa de uma extração de
  janelas TESSERA.
- A RQ3 responde à transferibilidade (plano de trabalho 4) dentro do
  distrito, só com TESSERA.
- A RQ4 é a mais cara: precisa do braço Sentinel-2, parado pelo custo
  da extração. Se não correr, perco só a última pergunta.

Cenários em [Scope](../docs/research_questions.md#scope).

**Na tese:** ✅ Parcial. A ordem de prioridade das três perguntas
aprovadas está em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(secção Research Questions); a ordem das quatro perguntas ainda não
foi aplicada.

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
| Só presenças, sem ausências (Phillips et al., 2009) | Positive-unlabeled learning | Presença vs. fundo (pontos aleatórios) |
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
(abertura do capítulo e secção Motivation); a tabela do manuscrito
usa a numeração das três perguntas aprovadas. O diagrama do pipeline
ainda não foi feito. A Introdução ainda cita `zhu2026` para a linha
das outras regiões; a entrada da bibliografia tem o autor errado (é
Stewart et al.) e a fonte certa para essa linha é Yang et al. (2026).
Por corrigir no manuscrito.

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
- **One-class verdadeiro (Isolation Forest e one-class SVM).** Testado
  nos dois braços, perdeu sempre para presença vs. fundo, e sob um
  fundo só de floresta caiu para perto do acaso: sem exemplos
  negativos, reconhecia "isto não é vegetação" e não a acácia. Ficou o
  Random Forest. Ver a mesma entrada.
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
subtema (ver
[Estrutura do documento](#estrutura-do-documento-seguir-um-relatório-de-referência-de-outro-aluno-onde-for-aplicável)).*

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

## Decisões

Agrupadas por tema:

- [Âmbito e perguntas](#decisões-âmbito-e-perguntas)
- [Dados de referência](#decisões-dados-de-referência)
- [RQ1: desenho e resultados](#decisões-rq1-desenho-e-resultados)
- [Validação e Sentinel-2](#decisões-validação-e-sentinel-2)
- [Documento e entrega](#decisões-documento-e-entrega)

Numeração das perguntas: as entradas anteriores a 2026-11-13 usam a
numeração aprovada pelo orientador (RQ1 curva e comparação, RQ2
redução de dados ou máscara, RQ3 concentração). Quatro entradas de
2026-11-13 usam uma numeração intermédia (RQ1 pontos, RQ2 curva),
assinalada em cada uma por um bloco "Revisão". A correspondência com
a atual está em
[Renumeração das perguntas](#renumeracao-perguntas-2026-11-13), cujo
texto usa ainda RQ3 para a comparação com o Sentinel-2 e RQ4 para a
transferibilidade; o bloco "Revisão" dessa entrada troca as duas.

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
âmbito.

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

**Na tese:** ✅ Parcial. O enunciado da RQ3 e a estatística do
observador dominante já estão em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(que diz 88% das presenças limpas; o valor é 90%, por atualizar);
a fundamentação completa fica para a Metodologia.

### RQ3: proposta de redesenho — diagnosticar primeiro se a concentração da amostragem prejudica o modelo {#rq3-proposta-redesenho-diagnostico-primeiro}

*Proposta minha (a confirmar com o orientador). Muda o desenho de uma
pergunta que ele aprovou, por isso não é adotada antes de ele
responder. Na fila da
[próxima reunião](../docs/meetings/proxima-reuniao.md).*

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

**Na tese:** ⏳ Ainda não escrita. O enunciado da RQ3 na introdução
não muda enquanto o orientador não responder.

### Formulação das perguntas como pergunta → objetivo geral → objetivos específicos → hipóteses {#formulacao-pergunta-objetivos-hipoteses}

*Proposta minha (a confirmar com o orientador). Reescreve enunciados
que ele aprovou; os aprovados valem até ele responder. Na fila da
[próxima reunião](../docs/meetings/proxima-reuniao.md).*

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

**Na tese:** ⏳ Ainda não aplicada. Os enunciados em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
são os aprovados.

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

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia). O
enunciado da RQ2 na introdução é o aprovado e não muda enquanto o
orientador não responder.

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

**Na tese:** ⏳ Ainda não aplicada. A Introdução tem os enunciados
aprovados pelo orientador, que não mudam enquanto ele não responder.

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
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb);
`results/rq2_per_source_check/`.

**Na tese:** ⏳ Ainda não aplicada (Introdução com os enunciados
aprovados; Metodologia e Resultados preliminares por escrever).

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
[`docs/meetings/proxima-reuniao.md`](../docs/meetings/proxima-reuniao.md).
Os resultados da curva (RQ1) continuam em
`results/rq2_per_source_check/`, que mantém o nome da numeração da
manhã.

**Na tese:** ⏳ Ainda não aplicada. A Introdução tem os enunciados
aprovados pelo orientador, que não mudam enquanto ele não responder.

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
  [`docs/meetings/proxima-reuniao.md`](../docs/meetings/proxima-reuniao.md).
- **Na tese:** ⏳ Ainda não aplicada, como o resto desta entrada.

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
Contributions); o detalhe fica para a Metodologia.

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

**Na tese:** ✅ Parcial. Mencionada em resumo na Introdução; o teste e
o limiar ficam para a Metodologia.

### Janela temporal das observações: só 2021–2025 {#janela-temporal-2021-2025}

*Decisão minha, de 2026-11-13. O orientador ainda não foi informado;
está como ponto informativo na
[fila da próxima reunião](../docs/meetings/proxima-reuniao.md#para-informar).*

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

**Na tese:** ✅ Parcial. Referida como candidato a contributo na
Introdução (secção Contributions); o desenho e a comparação ficam para
a Metodologia.

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
  o carregamento novo. Os sete ficheiros de
  `results/rq2_per_source_check/` ficaram idênticos byte a byte aos
  anteriores. Nenhum valor mudou.
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
  `results/tables/rq2_sample_150_seed0.csv` (a tratar quando a RQ2
  correr) e `experiments/temporal_window_2021_2025/rerun.py`, que lê
  um ficheiro de presenças que já não existe.

**Fundamentação:** nenhuma literatura consultada; é prática de
reprodutibilidade, raciocínio meu.

**Onde:** [`data/processed_manifest.csv`](../data/processed_manifest.csv);
[`background_pools.ipynb`](../notebooks/05_data_integration/background_pools.ipynb);
`src/background.py`; `src/manifest.py`;
[`data/README.md`](../data/README.md#tessera-embeddings--rq1-background-pool-2026-11-13).

**Na tese:** ⏳ Ainda não escrita. Se entrar, é uma frase sobre
reprodutibilidade na Metodologia.

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

### Classificador presença-vs-fundo (ciência cidadã): Random Forest, por agora

*Decisão minha, não confirmada pelo orientador.*

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

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia).

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

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia).

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

**Na tese:** ⏳ Ainda não escrita (Resultados/Metodologia).

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

**Na tese:** ⏳ Ainda não escrita (Resultados/Metodologia).

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

**Na tese:** ⏳ Ainda não escrita (Resultados/Metodologia).

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

**Na tese:** ⏳ Ainda não escrita (Metodologia/Resultados).

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

**Na tese:** ⏳ Ainda não escrita (Metodologia/Resultados).

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

**Onde:** corridas com o fundo antigo em
`results/temporal_window_2021_2025/` (marcadas em `OBSOLETE.md`);
curva completa com o fundo novo em `results/rq2_per_source_check/`,
feita pela secção 8 de
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).

**Na tese:** ⏳ Ainda não escrita (Metodologia).

**Revisão (2026-11-13, mais tarde no mesmo dia):** a numeração das
perguntas mudou. O que nesta entrada é a "RQ1" (dos pontos aos dados
de referência) passa a ser a RQ2, e a "RQ2" (curva de redução de
esforço) passa a ser a RQ1; a RQ3 e a RQ4 não mudam. Passei a numerar
por ordem de importância, o que também fica mais perto da numeração
que o orientador aprovou. O conteúdo desta entrada não muda. Ver
[Renumeração das perguntas](#renumeracao-perguntas-2026-11-13).

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
[`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb);
`results/rq2_per_source_check/`. As entradas anteriores sobre a curva
descrevem as corridas com todos os anos ou com o fundo antigo.

**Na tese:** ⏳ Ainda não escrita (Resultados preliminares).

**Revisão (2026-11-13, mais tarde no mesmo dia):** a numeração das
perguntas mudou. O que nesta entrada é a "RQ1" (dos pontos aos dados
de referência) passa a ser a RQ2, e a "RQ2" (curva de redução de
esforço) passa a ser a RQ1; a RQ3 e a RQ4 não mudam. Passei a numerar
por ordem de importância, o que também fica mais perto da numeração
que o orientador aprovou. O conteúdo desta entrada não muda; a secção
do notebook que aqui aparece como "secção 8" corresponde hoje às
secções 4 a 7. Ver [Renumeração das perguntas](#renumeracao-perguntas-2026-11-13).

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
Introdução; o desenho da zona-tampão fica para a Metodologia.

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

## Decisões: documento e entrega

### Estrutura do documento: seguir um relatório de referência de outro aluno, onde for aplicável

*Decisão minha.*

**O que decidi:** usar dois relatórios intermédios do mesmo
departamento como referência de estrutura:
[Gonçalo Santos, janeiro de 2026](guidance_example/1768249601_Entrega_intermedia-1.pdf)
e
[Cláudia Torres, janeiro de 2026](guidance_example/Tese_Intermedia____Claudia_Torres.pdf).

**O que têm:** capa, declaração de uso de IA, resumo em inglês e
português, listas de acrónimos, figuras e tabelas; depois Introduction,
Background, State of the Art, Proposed Work (com descrição dos dados,
plano de trabalho e avaliação de risco) e Conclusion and Future Work.
Nenhum tem capítulo de Resultados.

**Estado da arte:** os dois escrevem uma revisão narrativa por
subtema, fechada com uma síntese curta. Nenhum descreve bases de dados
pesquisadas, contagens de triagem ou diagrama PRISMA. O meu capítulo
de trabalho relacionado segue a mesma forma; o
[protocolo de pesquisa](#protocolo-de-pesquisa-da-literatura) fica
como preparação para a defesa, não para o texto.

**Porquê:** exemplos reais do mesmo departamento, já avaliados,
calibram o nível de detalhe esperado.

**Em aberto:** rever capítulo a capítulo, à medida que cada um for
escrito, o que vale a pena imitar.

**Na tese:** ✅ Parcial. `1-introduction.tex` existe; os restantes
capítulos estão por escrever à luz desta referência.

### Lista de literatura: releitura integral e limpeza

*Decisão minha, de 2026-11-11.*

**O que decidi:** reler todas as entradas de `docs/literature.md` a
partir do texto integral, corrigir os resumos e eliminar as que não
apoiam nenhuma decisão.

**Resultado:** ficam 31 entradas. 25 lidas na íntegra; Dimson et al. (2023) só na versão
submetida (o artigo publicado está bloqueado); três só pelo resumo
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

**Na tese:** ⏳ Ainda não aplicada. `references.bib` e a Introdução
ainda têm `zhu2026` com o autor errado.

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
