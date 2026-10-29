# Notas para a Tese

Coisas que quero dizer na tese e na defesa, e decisões que vou tomando
à medida que faço as experiências. As decisões de desenho estão em
[`docs/research_questions.md`](../docs/research_questions.md); aqui
fica o registo do que decidi, quando e porquê.

## Para dizer

### Perguntas ambiciosas

*2026-10-21, sugestão dos orientadores para a defesa.*

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
  Coimbra), de camadas de estradas e trilhos, e das experiências com o
  observador dominante.

Cenários em [Priority and scope](../docs/research_questions.md#priority-and-scope).

### Introdução para um júri de informática

*2026-10, sugestão do orientador.* O júri é de um departamento de
informática e não está por dentro da observação da Terra. A tese (e a
defesa) tem de começar por sensibilizar para o tema: explicar os
conceitos base e os problemas que depois tento resolver.

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
| Poucos observadores: 83% das observações de uma só pessoa | Dados de treino pouco diversos | RQ3; balanceamento do observador |
| Só presenças, sem ausências (Phillips et al., 2009) | Positive-unlabeled learning | Outras plantas como classes |
| Rótulos com ruído: localização imprecisa, píxeis mistos (Ball et al., 2026) | Label noise | Pipeline de preparação dos dados (objetivo 1) |
| Poucos dados | Data efficiency / few labels | RQ2 |
| Observações de anos diferentes das imagens (Ball et al., 2026) | Desfasamento temporal entre dados e rótulos | Ano único 2023; filtro de fogo |
| Pontos vizinhos parecidos inflacionam a exatidão (Karasiak et al., 2022) | Data leakage / autocorrelação | Validação espacial |
| Pior desempenho noutras regiões (Zhu et al., 2026) | Distribution shift | RQ3 |

Ideia para a defesa: um diagrama do pipeline (observação no
iNaturalist → píxel → embedding → classificador → mapa) antes das
perguntas de investigação.

## Decisões

Uma entrada por decisão: data, o que decidi, porquê, e onde está
(notebook, figura ou doc).

### Só *Acacia dealbata*

*2026-10-20, decisão minha (a confirmar com o orientador).*

**O que decidi:** o alvo é a *A. dealbata*. As outras espécies de
*Acacia* ficam fora do treino (opção A). Mais tarde posso testá-las
como classe própria (opção B) ou mapear o género como extensão.

**Porquê:**
- Os dados de especialistas só têm *A. dealbata*: a comparação da
  RQ1 só é justa para esta espécie.
- A proposta pede mapeamento ao nível da espécie (objetivo 3).
- É 66% das observações de *Acacia* (5 254 de 7 943).
- As espécies vêem-se de forma diferente do satélite (manchas densas
  com floração no inverno; árvore misturada na floresta; arbusto das
  dunas).
- Não entram como "outras plantas" porque são *Acacia* e confundiriam
  o modelo.

**Fundamentação:** Domingo et al. (2023) e Martins et al. (2016)
mapearam a *A. dealbata* sozinha.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#species-scope-proposed).
Aplicado a 2026-10-29 no passo 10 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb):
ficam 5 242 observações (5 240 da espécie e 2 da subespécie
*A. dealbata dealbata*); saem 2 621 de outras espécies e 35
identificadas só até ao género ou subgénero. O Observer A fez 90%
delas (83% em todas as *Acacia*).

### Multiclasse também no modelo de especialistas

*2026-10-20, proposta minha (a confirmar com o orientador).*

**O que decidi:** na RQ1, os dois modelos são multiclasse. O de
ciência cidadã já o era (outras plantas do iNaturalist como classes,
decisão da reunião de 21 de outubro). No de especialistas, as ausências
(pontos ao acaso na COS 2023, em classes de vegetação) ficam com a
classe da COS onde caem (p. ex. eucaliptal, pinhal, outra floresta,
agricultura, matos; as classes com poucos pontos juntam-se), em vez de
uma única classe "não *Acacia*". Os dois são avaliados pela
probabilidade de *A. dealbata* nos mesmos pontos de teste. A versão
binária (*A. dealbata* vs. o resto) corre também, como verificação.

**Porquê:**
- A RQ1 compara a fonte dos rótulos (iNaturalist vs. especialistas).
  Para a diferença vir só daí, a forma da tarefa tem de ser igual nos
  dois modelos.
- Um ponto num polígono de eucaliptal da COS (manchas de pelo menos
  1 ha) diz o que está mapeado ali, não que não há *Acacia*: o mesmo
  argumento das outras plantas.
- A matriz de confusão mostra com que se confunde a *A. dealbata*
  (análise de erros).
- O binário pode dar o mesmo ou melhor com Random Forest. Se der o
  mesmo, a escolha não importa e digo-o; se não, é um resultado.

**Fundamentação:** Ball et al. (2026) classificaram espécies e grupos
de espécies como classes, com embeddings. Não verifiquei outras fontes
para esta escolha.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#other-plants-as-classes-adopted-direction).
Ainda não aplicado: as experiências ficam para depois da análise
exploratória.

### Usar os dados de especialistas, com limpeza

*2026-10-28, decisão minha depois de os ver no QGIS; o uso das
ausências é proposta (a confirmar com o orientador).*

**O que decidi:** os dados de especialistas são de confiança e vão ser
usados. Limpeza: tirar as 11 linhas sem `classifica` e corrigir as 531
geometrias inválidas. Ausências: as que caem em vegetação na COS 2023
(2 823) ficam todas, com a classe da COS; das que caem em edifícios
(2 187) fica só uma amostra pequena, como classe própria.

**Como a COS foi usada:** quem diz se há *A. dealbata* é o rótulo do
professor (`classifica`); a COS não decide isso. Para cada ausência
vi a classe da COS 2023 num ponto dentro do polígono, só para saber
que tipo de sítio é. Daí sai a coluna `use`: `presence`
(`classifica = 1`), `absence_vegetation` (agricultura, florestas,
matos), `absence_artificial` (edifícios, indústria, estradas) e
`absence_other` (água, zonas húmidas, terreno nu). Nada foi apagado:
a coluna só marca; quantas ausências de edifícios entram decide-se ao
preparar os dados de treino.

**Limitação:** a COS mapeia manchas de pelo menos 1 ha. Um segmento
de 75 m² recebe a classe dominante desse hectare, que pode não ser o
que está no próprio segmento (p. ex. uma árvore num jardim fica
"artificial").

**Porquê:**
- Vistos no QGIS, os polígonos estão onde devem. São de 2023, feitos
  no campo e sobre o OrtoSat (resposta do orientador, 2026-10-28).
- A forma estranha vem da segmentação da imagem. As geometrias
  inválidas são contornos que se tocam num canto de píxel; a correção
  não muda a área.
- Se as ausências fossem quase só edifícios, o modelo aprenderia
  "árvore vs. edifício" e não "*A. dealbata* vs. outras plantas", e a
  exatidão sairia inflacionada. Mas também tem de saber que um
  edifício não é acácia, por isso fica uma amostra.

**Onde:** [`notebooks/03_expert_reference/expert_polygons.ipynb`](../notebooks/03_expert_reference/expert_polygons.ipynb)
(secções 5–11).

### Só observações *research*, nos dois lados

*2026-10-29, decisão minha.*

**O que decidi:** no modelo principal, as observações do iNaturalist
são só as *research*, nas presenças e nas outras plantas.
- Presenças de *A. dealbata*: saem as *casual* (1 678) e as
  *needs_id* (123); das 5 242 ficam 3 441.
- Outras plantas: saem 12 458 *casual* e 37 488 *needs_id*; das
  110 576 ficam 60 630.

*Atualizado no mesmo dia:* primeiro apliquei só às presenças; depois
decidi aplicar também às outras plantas, para ser consistente (ver o
último ponto do porquê).

**Porquê:**
- *Research* quer dizer que a identificação foi confirmada pela
  comunidade (pelo menos duas pessoas concordam), com foto, data,
  localização e organismo selvagem.
- As nossas *casual* são quase todas observações **sem foto**: 1 670
  das 1 679 do distrito (contagem na API do iNaturalist a
  2026-10-29); só 8 estão marcadas como cultivadas. Ninguém consegue
  confirmar a identificação.
- 98% das *casual* são do Observer A, sobretudo de 2021. Ao tirá-las,
  o peso do Observer A desce de 90% para 87%.
- As *needs_id* têm foto, mas a identificação ainda não foi
  confirmada.
- Mesmo assim ficam 3 441 presenças, o que chega para treinar.
- **A mesma regra nos dois lados:** as outras plantas só servem de
  comparação se forem registadas pelo mesmo processo que as presenças
  (fundo de grupo-alvo, Phillips et al., 2009). Se só as presenças
  fossem *research*, as outras plantas ficavam com os registos sem
  foto do Observer A e com plantas de jardim, e o modelo podia
  aprender como as observações foram feitas em vez da planta.
- Nas outras plantas ainda ficam 17,6 por presença, e continuam nos
  mesmos sítios: 94,5% das quadrículas de 1 km com *A. dealbata* têm
  outras plantas.
- Contra: muitas *needs_id* estão identificadas até ao género, o que
  chegaria para as agrupar em classes. Se faltarem dados numa classe,
  recupero-as.

**Trabalho futuro:** verificação de sensibilidade, treinando com e
sem as *casual* e *needs_id* (nos dois lados ao mesmo tempo), para
ver se os resultados mudam. Se não
mudarem, a escolha não importa e digo-o; se mudarem, é um resultado.
Recuperam-se do ficheiro original.

**Fundamentação:** Gillespie et al. (2024) e Brown et al. (2025)
usaram só observações *research*. Só as *research* são enviadas para
o GBIF, por isso os estudos que usam o iNaturalist através do GBIF
também ficam só com estas. Não encontrei um estudo que compare usar
ou não as *casual* (pesquisa rápida, não exaustiva).

**Onde:** passo 11 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb)
e passo 8 de
[`other_plants_observations.ipynb`](../notebooks/02_citizen_science/other_plants_observations.ipynb);
[`docs/research_questions.md`](../docs/research_questions.md) (tabela
do pipeline, passo 3).

### Precisão da localização: tirar acima de 30 m, manter as sem valor

*2026-10-29, decisão minha (por recomendação, depois de um teste).*

**O que decidi:** nos dois lados (presenças e outras plantas), saem
as observações com `positional_accuracy` conhecida acima de 30 m (3
píxeis). As que não têm valor ficam, marcadas com `accuracy_missing`.
Presenças: 3 441 → 3 276. Outras plantas: 60 630 → 48 125.

**Porquê:**
- A `positional_accuracy` é o raio (m) do círculo onde está a planta.
  Um píxel tem 10 m: com um raio grande, o ponto pode cair no píxel
  errado (rótulo impuro).
- 80% das presenças não têm valor, e quase todas são do Observer A
  (90% das observações dessa pessoa, contra 11% dos outros). "Sem
  valor" não quer dizer "mal localizada": é a forma como esta pessoa
  regista. Tirá-las seria tirar o Observer A.
- **Teste:** que parte de cada grupo cai num acacial da COS 2023 (se
  fossem pontos ao acaso, 2,3%):

  | Precisão | Presenças | % em acacial | % em acacial (só outros observadores) |
  |---|---|---|---|
  | ≤ 10 m | 429 | 20,7% | 10,5% |
  | 10–30 m | 104 | 14,4% | 10,0% |
  | 30–100 m | 91 | 6,6% | 6,7% |
  | > 100 m | 74 | 10,8% | 6,3% |
  | sem valor | 2 743 | 18,6% | 12,2% |

  - As sem valor caem em acaciais quase tanto como as mais precisas:
    ficam.
  - Nos outros observadores, até 30 m dá o mesmo que ≤ 10 m; a partir
    de 30 m desce para cerca de 6,5%, e 30–100 m comporta-se como
    > 100 m. Por isso o limite é 30 m e não 100 m.
- Eu estava inclinada para 100 m, para não perder dados de ciência
  cidadã. Mas a diferença é pequena: com 30 m saem 165 presenças
  (4,8%), com 100 m sairiam 74 (2,2%).
- A mesma regra nas outras plantas, como na qualidade, para os dois
  lados passarem pelos mesmos filtros.

**Limitações:** é um teste indireto. A COS só mapeia manchas de
acácia com pelo menos 1 ha (só 54% dos polígonos dos especialistas
caem nelas), por isso compara grupos e não confirma cada ponto. Os
grupos com valor são pequenos (74 a 429) e a ordem não é perfeita
(> 100 m acima de 30–100 m).

**Fundamentação:** Ball et al. (2026): rótulos impuros baixam a
exatidão, embora os embeddings tolerem alguma impureza. O teste com a
COS é meu; não verifiquei se outros estudos o usaram.

**Onde:** passo 12 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb)
(teste e filtro) e passo 9 de
[`other_plants_observations.ipynb`](../notebooks/02_citizen_science/other_plants_observations.ipynb);
[`docs/research_questions.md`](../docs/research_questions.md) (tabela
do pipeline, passo 2).

### Uma observação por píxel; nos conflitos fica a presença

*2026-10-29, decisão minha (o ponto dos conflitos é a versão mínima da
máscara de segmentação, a confirmar com o orientador).*

**O que decidi:**
- **Presenças:** uma por píxel de 10 m (grelha UTM 29N, EPSG:32629).
  Quando há várias, fica a mais próxima de 2023 (em empate, a mais
  recente). 3 276 → 3 000.
- **Conflitos:** nos 443 píxeis com uma *A. dealbata* e outras
  plantas, saem as outras plantas (772) e fica a presença.
- **Outras plantas repetidas:** ficam para depois de as agrupar em
  classes; nessa altura, uma por píxel e por classe.

**Porquê:**
- O modelo vê píxeis, não pontos: duas observações no mesmo píxel têm
  o mesmo embedding e são o mesmo exemplo repetido.
- 98% das presenças repetidas eram do Observer A, quase todas do
  mesmo ano (registos repetidos da mesma visita). Mantê-las dava ainda
  mais peso aos sítios dessa pessoa, o que vai contra o que quero
  controlar na RQ3.
- Fica a mais próxima de 2023 porque todas as observações são tratadas
  como 2023: é a que mais provavelmente corresponde à imagem.
- Num conflito, o mesmo píxel diria "é acácia" e "não é acácia". No
  terreno é normal (outras plantas por baixo ou ao lado). Fica a
  presença porque é a planta que quero mapear e foi vista ali. Tirar
  as duas seria mais "limpo", mas perdia 475 presenças (15%).
- Nas outras plantas, as repetidas são sobretudo espécies diferentes
  no mesmo sítio (até 54 num píxel): um píxel com um eucalipto e um
  carvalho tem duas classes, e isso só se sabe depois de agrupar.

**Fundamentação:** Karasiak et al. (2022): amostras repetidas e
próximas inflacionam a exatidão. A ideia de tirar as outras plantas
dentro da mancha de acácia vem do orientador (máscara de segmentação,
reunião de 21 de outubro); aqui só ao nível de um píxel.

**Onde:** passo 13 de
[`acacia_observations.ipynb`](../notebooks/02_citizen_science/acacia_observations.ipynb)
e passo 10 de
[`other_plants_observations.ipynb`](../notebooks/02_citizen_science/other_plants_observations.ipynb);
código da grelha em [`src/grid.py`](../src/grid.py);
[`docs/research_questions.md`](../docs/research_questions.md) (tabela
do pipeline, passo 8).
