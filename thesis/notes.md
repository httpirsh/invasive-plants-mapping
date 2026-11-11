# Notas para a Tese

Coisas que quero dizer na tese e na defesa, e o registo do que decidi e
porquê. O estado atual do desenho está em
[`docs/research_questions.md`](../docs/research_questions.md) e
[`docs/methodology.md`](../docs/methodology.md); aqui fica o raciocínio.

Cada entrada segue a mesma forma: quem decidiu, **O que decidi**,
**Porquê**, **Fundamentação**, **Onde**, **Na tese**.

## Para dizer

### Perguntas ambiciosas

*Sugestão dos orientadores para a defesa.*

> "Tenho noção de que as perguntas são ambiciosas. Num cenário ideal,
> com todo o tempo do mundo, chegaria à RQ3. Por isso estão ordenadas
> por prioridade: a RQ1 é o núcleo e tem de ficar completa; a RQ2
> reutiliza o mesmo pipeline e é o passo seguinte; a RQ3 é a mais
> exigente e fica para o fim. Vou ajustando consoante o que os dados e
> o tempo permitirem."

Porque esta ordem se defende:
- A RQ1 sozinha já responde à proposta (objetivos 1 e 3, parte do 2):
  é uma tese completa.
- A RQ2 custa pouco a mais: é a RQ1 com menos dados, com o mesmo modelo
  e o mesmo teste.
- A RQ3 é a mais cara: precisa de regiões diferentes (só tenho
  Coimbra) e das experiências com o observador dominante.

Cenários em [Priority and scope](../docs/research_questions.md#priority-and-scope).

**Na tese:** ✅ Esta ordem de prioridade já está em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(secção Research Questions).

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
| Poucos observadores: 83% das observações de uma só pessoa | Dados de treino pouco diversos | RQ3 |
| Só presenças, sem ausências (Phillips et al., 2009) | Positive-unlabeled learning | Presença vs. fundo (pontos aleatórios) |
| Rótulos com ruído: localização imprecisa, píxeis mistos (Ball et al., 2026) | Label noise | Pipeline de preparação dos dados (objetivo 1) |
| Poucos dados | Data efficiency / few labels | RQ2 |
| Observações de anos diferentes das imagens (Ball et al., 2026) | Desfasamento temporal entre dados e rótulos | Ano único 2023; filtro de fogo |
| Pontos vizinhos parecidos inflacionam a exatidão (Karasiak et al., 2022) | Data leakage / autocorrelação | Validação espacial |
| Pior desempenho noutras regiões (Zhu et al., 2026) | Distribution shift | RQ3 |

Ideia para a defesa: um diagrama do pipeline (observação no
iNaturalist → píxel → embedding → classificador → mapa) antes das
perguntas de investigação.

**Na tese:** ✅ Os conceitos base e a tabela de problemas já estão em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(abertura do capítulo e secção Motivation). O diagrama do pipeline
ainda não foi feito.

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
  AlphaEarth só existe como embeddings; os pesos do TESSERA têm de ser
  pedidos; com poucos rótulos e ruidosos, afinar arrisca ajustar o
  ruído; e o mesmo classificador sobre cada representação isola o
  efeito da representação. Segue Ball et al. (2026), Yang et al.
  (2026) e Brown et al. (2025). Ver
  [Foundation Model Use](../docs/research_questions.md#foundation-model-use-adopted).
- **RQ3: assumir que o observador dominante é um enviesamento.** Só
  conta se o orientador aceitar o redesenho. Questionei a premissa,
  medi (ele é fiável e concentrado numa zona, não necessariamente um
  problema) e propus diagnosticar primeiro. Ver
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
- Uma pessoa fez 83% de todas as observações de *Acacia* (88% das
  presenças de *A. dealbata* depois da limpeza), e 98% do pico de 2021.
- O modelo só aprende com os sítios por onde esta pessoa passou; os
  embeddings podem aprender esse percurso mais facilmente (amplificar)
  ou separar melhor a *Acacia* do que está à volta (atenuar). Ainda
  ninguém testou isto.
- É a pergunta mais cara, por isso fica em último na prioridade.

**Fundamentação:** Dimson et al. (2023): registos de invasoras do
iNaturalist enviesados para estradas e zonas perturbadas; Zhu et al.
(2026) e Yang et al. (2026): embeddings que generalizam pior para
outras regiões; Phillips et al. (2009) para corrigir o enviesamento.

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

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq3--spatial-sampling-concentration).

**Na tese:** ✅ Parcial. O enunciado da RQ3 e a estatística do
observador dominante (83%/88%) já estão em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex);
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
- **Hipóteses:** amplifica (os embeddings guardam contexto da
  paisagem, o modelo aprende a zona amostrada e piora mais do que o
  Sentinel-2 fora dela); atenua (descrevem melhor a planta, piora
  menos); sem efeito (nenhum piora — hipótese que o desenho aprovado
  não previa). As experiências mostram o resultado, não o mecanismo.
- **Experiência 1 — diagnóstico.** Treinar com a ciência cidadã e
  avaliar nos polígonos de especialistas (referência independente),
  perto e longe do ponto de treino mais próximo, em distância
  geográfica, para TESSERA e Sentinel-2. Os mesmos polígonos ficam nas
  mesmas faixas para as duas representações, por isso a comparação é
  direta. Grupo "longe" principal: polígonos do mesmo ficheiro e
  mosaico (TNE) a mais de 1 km de qualquer ponto de ciência cidadã; os
  do resto do país (notTNE) ficam como extensão opcional.
- **Experiência 2 — um observador dedicado contra muitos ocasionais,
  com o mesmo número de pontos:** 353 pontos do Observador A
  (subamostragens repetidas) contra os 353 dos outros, testados perto
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
  necessariamente a dos notebooks), os 2 647 pontos dele ocupam 18 de
  43 blocos e os 353 dos outros ocupam os 43; em contrapartida, 82%
  dos polígonos de especialistas dentro da área da ciência cidadã
  estão a menos de 500 m de um ponto dele (66% para os outros).
- O desenho aprovado avalia "nos registos dos outros observadores"
  (353 pontos, da mesma fonte). Os polígonos de especialistas são
  independentes do iNaturalist.
- Há dados para o teste. Polígonos por distância ao ponto de ciência
  cidadã mais próximo (0–1 / 1–5 / 5–20 / >20 km): TNE dentro do
  distrito 1 677 / 120 / 52 / 0; TNE fora do distrito 3 / 50 / 115 /
  55; notTNE 0 / 0 / 23 / 375. "Perto" = 1 680 polígonos; "longe" no
  mesmo ficheiro = 392; mais 398 no resto do país.
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
- Risco de teto como na RQ1; os 118 pontos dos outros observadores
  fora dos blocos do Observador A são o teste mais difícil de reserva.
- Custo, não verificado: embeddings TESSERA e Sentinel-2 fora da caixa
  do piloto. A comparação depende do braço Sentinel-2, adiado.
- Mapa de confiança: Meyer & Pebesma só testaram regressão com Random
  Forest; aqui indica suporte, não exatidão.

**Fundamentação:** Meyer & Pebesma (2021) para o método; Ratsakatika
et al. (2026, preprint) aplicam-no a um modelo com embeddings mas
declaram como limitação que a exatidão fora da área não foi testada.
Não encontrei precedente com ciência cidadã concentrada num observador
(pesquisa rápida, não revisão): possível contributo. Resumos em
[`docs/literature.md`](../docs/literature.md#spatial-validation). As
contagens são verificação minha, ad-hoc (script não guardado).

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq3--spatial-sampling-concentration).

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
- **Dois níveis de dados:** as 3 000 presenças e uma subamostra ao
  acaso de 150 (5%).
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

1. **O filtro de recência não se aguentava.** A ±1 ano de 2023 estão
   47,1% das presenças, a ±2 anos 82,2%, a ±3 anos 94,5% e a ±4 anos
   99,4%; só 19 estão a mais de 4 anos, e o filtro de perturbação
   encontrou 6 ardidas. "Remover as mais distantes" seria remover
   2019–2020. Além disso misturava quantidade e composição (a quota do
   Observador A cai de 88% para 72% aos 10% dos dados e 63% aos 5%) e
   dava uma só curva, sem repetições.
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
- **Sem a regra da COS:** só cobre cerca de 17% dos pontos, é a que
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
superpíxeis; Zhang et al. (2025) para o crescimento de região. Não
encontrei trabalho que junte propagação de ponto para mancha, pontos
de ciência cidadã e embeddings congelados: possível contributo. Não
fiz pesquisa nova para esta proposta; resumos em
[`docs/literature.md`](../docs/literature.md#weak-supervision-from-point-labels).
As contagens são verificação minha, ad-hoc (scripts não guardados),
sobre `inat_dealbata_clean.csv` e `expert_polygons_clean.gpkg`.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq2--extending-point-labels-to-patches);
regras e testes iniciais em
[Máscara de segmentação](#máscara-de-segmentação-testar-várias-abordagens).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia). O
enunciado da RQ2 na introdução é o aprovado e não muda enquanto o
orientador não responder.

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

**Fundamentação:** Ball et al. (2026): rótulos impuros baixam a
exatidão. O teste com a COS é meu.

**Onde:** passo 12 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb);
tabela do pipeline, passo 2.

**Na tese:** ✅ Parcial. Mencionada em resumo na Introdução; o teste e
o limiar ficam para a Metodologia.

### Uma observação por píxel; nos conflitos fica a presença

*Decisão minha.*

**O que decidi:** uma presença por píxel de 10 m (grelha UTM 29N,
EPSG:32629). Quando há várias, fica a mais próxima de 2023 (em empate,
a mais recente). 3 276 → 3 000. Nos 443 píxeis com uma *A. dealbata* e
outras plantas, ficou a presença (regra do tempo do multiclasse, hoje
sem efeito).

**Porquê:**
- O modelo vê píxeis, não pontos: duas observações no mesmo píxel têm
  o mesmo embedding e são o mesmo exemplo repetido.
- 98% das presenças repetidas eram do Observer A, quase todas do mesmo
  ano (registos repetidos da mesma visita).
- Fica a mais próxima de 2023 porque todas as observações são tratadas
  como 2023.

**Fundamentação:** Karasiak et al. (2022): amostras repetidas e
próximas inflacionam a exatidão.

**Onde:** passo 13 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb);
[`src/grid.py`](../src/grid.py); tabela do pipeline, passo 8.

**Na tese:** ✅ Parcial. Mencionada em resumo na Introdução; o detalhe
fica para a Metodologia.

### Observer A: todas as observações no modelo principal

*Decisão minha.*

**O que decidi:** no modelo principal ficam todas as observações do
Observer A (88% das 3 000 presenças). Não limito o número por
quadrícula na preparação dos dados.

**Porquê:**
- O efeito do Observer A é o que a RQ3 testa. Limitá-lo já no modelo
  principal deixava a RQ3 sem o caso de comparação.
- As observações repetidas da mesma visita já saíram no passo "uma por
  píxel".
- Limitar já cortava muitos dados antes de saber se a concentração
  muda o resultado.

**Fundamentação:** raciocínio meu, a partir do desenho da RQ3.

**Onde:** tabela do pipeline, passo 9;
[RQ3](../docs/research_questions.md#rq3--spatial-sampling-concentration).

**Na tese:** ✅ Parcial. A estatística dos 88% já está na Introdução;
a decisão fica para a Metodologia.

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
    1/15/758 píxeis (mín/mediana/máx). A cauda superior bate no limite
    do raio, sinal de limiar permissivo demais nalguns casos.
  - Superpíxeis (SLIC, `n_segments=100`, `compactness=0,1`, não
    fundamentados): 11/21/45 píxeis. Mais consistente, mas só porque o
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

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq1--foundation-models-vs-conventional-approaches);
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
dos especialistas só tem 18 blocos independentes; e tem cinco citações
de apoio, contra nenhuma da Logistic Regression.

**Fundamentação:** Ball et al. (2026); Yang et al. (2026); Mouta et
al. (2021); Domingo et al. (2023); Eskandari et al. (2025).

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
fontes; o resto é raciocínio meu.

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
  corresponder ao alcance da autocorrelação espacial (Le Rest et al.,
  2014; Mahoney et al., 2023). O bloqueio espacial foi pelo menos tão
  robusto quanto a zona-tampão nas simulações de Mahoney et al.
- A biblioteca de Karasiak (Museo ToolBox) define a distância em
  píxeis, o que daria 200–300 m.
- O variograma dos embeddings TESSERA nos nossos dados estabiliza por
  volta dos 300–500 m (primeira estimativa, não um ajuste formal).

**Fundamentação:** nenhuma para os 20–30 m; é uma escolha pragmática,
e a literatura e o variograma apontam para píxeis.

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

**Em aberto:** a janela de floração para Portugal central; qual das
variantes (anual ou sazonal) é a reportada nos números principais de
Ball et al.

**Fundamentação:** Ball et al. (2026), pelo código-fonte dos autores;
Domingo et al. (2023), texto integral. Resumos em
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
