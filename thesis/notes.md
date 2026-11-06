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

**Na tese:** ✅ Esta ordem de prioridade (RQ1 núcleo, RQ2 barato, RQ3
mais exigente) já está em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(secção Research Questions).

**Nota (2026-11-04, minha correção):** a tabela de estado em
`research_questions.md` tinha a RQ1 como "proposed, to confirm", apesar
de esta citação (da mesma reunião que aprovou a RQ3) já a aprovar como
núcleo da tese. Corrigido para "Adopted 2026-10-21", consistente com a
RQ2 e a RQ3.

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

**Na tese:** ✅ Os conceitos base e a tabela de problemas já estão em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(abertura do capítulo e secção Motivation), adaptados ao inglês e ao
desenho atual (fundo em vez de classes, após "Multiclasse abandonado…"
nas Decisões). O diagrama do pipeline ainda não foi feito.

### Outras plantas como classes, não como ausências

*2026-10-30, para a defesa — caso perguntem porque não uso as outras
plantas como "não é acácia".*

> "O iNaturalist só regista presenças: nunca há um registo que diga
> 'aqui não há acácia'. A tentação óbvia é usar uma observação de
> outra planta, por exemplo eucalipto, para dizer 'aqui não há
> acácia'. Não faço isso, porque essa observação só confirma que há
> eucalipto naquele ponto — não que não haja acácia ao lado, ou no
> mesmo píxel. Ninguém verificou isso. Em vez disso, cada observação
> de outra planta vira a sua própria classe positiva ('isto é
> eucalipto'), e o modelo passa a ser multiclasse. A separação entre
> acácia e eucalipto surge de ensinar o modelo a reconhecer as duas
> coisas, não de uma alegação de ausência que os dados não sustentam."

Porque isto é diferente na prática de um "não-acácia" direto:
- Um rótulo "não-acácia" afirma uma ausência que o dado não prova.
- Um rótulo "eucalipto" afirma uma presença que o dado prova; a
  acácia "perder" face ao eucalipto no classificador multiclasse é um
  efeito colateral de aprender a distinguir vegetação, não uma
  alegação direta sobre a acácia.
- Dá matriz de confusão: sei com que a acácia se confunde (eucalipto,
  pinheiro, mato...), não só se o modelo acerta ou erra.
- Não penaliza píxeis mistos, onde a acácia pode genuinamente
  coexistir com a planta observada, mas não fotografada.
- Segue Phillips et al. (2009) — *target-group background*: usar
  observações de outras espécies registadas pelo mesmo
  processo/observadores como "fundo", porque partilham o mesmo viés
  de acessibilidade das presenças de acácia, sem nunca alegar que a
  espécie-alvo está confirmadamente ausente nesses pontos. A COS como
  ausência dos especialistas segue a mesma lógica (ver "Multiclasse
  também no modelo de especialistas" nas Decisões).

**Contraste, se perguntarem se isto é mesmo relevante:** a colega
Lucie Radová, numa apresentação interna que assisti em 2026-10-30
(ainda não publicada, não é artigo nem preprint), propõe exatamente o
oposto nos próximos passos do trabalho dela: usar observações de
outras plantas para *descer* a probabilidade de acácia, ou seja, como
"não-acácia" direto. É um bom contraste para mostrar que a escolha
desta tese não é óbvia nem a única possível — ver a entrada completa,
com a devida ressalva de que é só uma apresentação assistida, em
[`docs/literature.md`](../docs/literature.md).

**Onde:** fundamentação completa em
[`docs/research_questions.md`](../docs/research_questions.md#other-plants-as-classes-adopted-direction)
e nas entradas "Multiclasse também no modelo de especialistas" e
"Outras plantas em 8 grupos; herbáceas só onde são a camada de cima"
nas Decisões, abaixo.

**Na tese:** ❌ Desenho substituído por "Multiclasse abandonado…"
(Decisões, abaixo) — este argumento (outras plantas como classes, não
ausências) já não se aplica tal como está escrito; se for reutilizado
na defesa, tem de ser adaptado para o fundo partilhado.

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

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder). A introdução já nomeia a *A. dealbata* como alvo, sem
justificar o scope.

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

*Atualizado a 2026-11-04:* os polígonos `classifica = 0` dos
especialistas deixam de ser usados (decisão do orientador, ver "Usar
os dados de especialistas"). As classes negativas do modelo de
especialistas passam a vir só de pontos ao acaso na COS 2023; como
escolhê-los está em aberto.

*Substituída a 2026-11-05 (reunião presencial, decisão do orientador):*
o multiclasse é abandonado nos dois modelos — esta decisão fica
histórica. Ver a entrada completa em "Multiclasse abandonado; RQ1
passa a uma curva de redução de esforço (presença vs. fundo)", mais
abaixo.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#other-plants-as-classes-adopted-direction).
Ainda não aplicado: as experiências ficam para depois da análise
exploratória.

**Na tese:** ❌ Decisão histórica, substituída (ver "Multiclasse
abandonado…" mais abaixo) — não entra na tese nesta forma.

### RQ3 aprovada

*2026-10-21, decisão do orientador (na reunião).*

**O que decidi:** a RQ3 (os embeddings amplificam ou atenuam o
enviesamento espacial da ciência cidadã, comparados com o
Sentinel-2?) fica nas perguntas da tese, a seguir à RQ1 e à RQ2.

**Porquê:**
- Há um caso real de enviesamento nos dados: uma pessoa fez 83% de
  todas as observações de *Acacia* (88% das presenças de
  *A. dealbata* depois da limpeza), e 98% do pico de 2021.
- O modelo só aprende com os sítios por onde esta pessoa passou; os
  embeddings podem aprender esse percurso mais facilmente
  (amplificar) ou separar melhor a *Acacia* do que está à volta
  (atenuar). Ainda ninguém testou isto.
- É a pergunta mais cara (precisa de regiões diferentes e de camadas
  de estradas e trilhos), por isso fica em último na prioridade (ver
  "Perguntas ambiciosas" acima).

**Fundamentação:** Dimson et al. (2023): registos de invasoras do
iNaturalist enviesados para estradas e zonas perturbadas; Zhu et al.
(2026) e Yang et al. (2026): embeddings que generalizam pior para
outras regiões; Phillips et al. (2009) para corrigir o enviesamento
com observações dos mesmos observadores.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq3--spatial-sampling-bias).

**Na tese:** ✅ Parcial — o enunciado da RQ3 e a estatística do
observador dominante (83%/88%) já estão em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(secções Motivation e Research Questions); a fundamentação completa
(Dimson, Zhu/Yang) fica para o capítulo de Metodologia.

### Usar os dados de especialistas, com limpeza

*2026-10-28, decisão minha depois de os ver no QGIS. As ausências
mudaram a 2026-11-04, por decisão do orientador: ver "O que mudou".*

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

**O que mudou (2026-11-04, decisão do orientador, por mensagem):**
só conto os polígonos com `classifica = 1`. Os de `classifica = 0`
são áreas de não acácia que não devem entrar no estudo; era por os
estar a usar que apareciam ausências em edifícios. Deixa de haver
ausências dos especialistas e a proposta da amostra de edifícios cai.
Fica em aberto de onde vêm as classes negativas do modelo de
especialistas: a opção que já estava prevista é pontos ao acaso nas
classes de vegetação da COS 2023 (ver "Multiclasse também no modelo
de especialistas").

**Onde:** [`notebooks/03_expert_reference/expert_polygons.ipynb`](../notebooks/03_expert_reference/expert_polygons.ipynb)
(secções 5–10). **Atualizado (2026-11-06):** a secção 6 passa a tirar
também os `classifica = 0` (não só as linhas sem valor); a coluna
`use` (secção 10 antiga) foi removida, já que deixou de haver
ausências para marcar. Ficheiro `expert_polygons_clean.gpkg`
regenerado: 2 470 polígonos (todos `classifica = 1`), ver
[`data/README.md`](../data/README.md#expert-reference-polygons-cleaned-derived).
O notebook consumidor
([`one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb))
foi atualizado para a nova estrutura (deixou de filtrar por
`label == "dealbata"`, coluna que já não existe).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder).

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

**Na tese:** ✅ Parcial — mencionada em resumo na Introdução
("keeping only identification-confirmed (research-grade) records",
secção Contributions); o detalhe completo (números, porquê) fica para
o capítulo de Metodologia.

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

**Na tese:** ✅ Parcial — mencionada em resumo na Introdução
("discarding imprecise locations", secção Contributions); o detalhe
completo (teste, limiar de 30 m) fica para o capítulo de Metodologia.

### Uma observação por píxel; nos conflitos fica a presença

*2026-10-29, decisão minha (o ponto dos conflitos é a versão mínima da
máscara de segmentação, a confirmar com o orientador).*

**O que decidi:**
- **Presenças:** uma por píxel de 10 m (grelha UTM 29N, EPSG:32629).
  Quando há várias, fica a mais próxima de 2023 (em empate, a mais
  recente). 3 276 → 3 000.
- **Conflitos:** nos 443 píxeis com uma *A. dealbata* e outras
  plantas, saem as outras plantas (772) e fica a presença.
- **Outras plantas repetidas:** uma por píxel, decidido depois de as
  agrupar em classes (ver a entrada seguinte). *Mudou a 2026-10-30:*
  antes era "uma por píxel e por classe", mas isso deixava 771 píxeis
  com dois rótulos diferentes.

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

**Na tese:** ✅ Parcial — mencionada em resumo na Introdução
("collapsing repeated observations onto the same pixel", secção
Contributions); o detalhe completo (regra dos conflitos) fica para o
capítulo de Metodologia.

### Outras plantas em 8 grupos; herbáceas só onde são a camada de cima

*2026-10-30, proposta (deixei a escolha ao assistente; a confirmar com
o orientador). Revista no mesmo dia: ver "O que mudou".*

**O que decidi:**
- **8 grupos:** aquáticas, eucalipto, pinheiros e outras coníferas,
  carvalhos, outras invasoras de grande porte, outras árvores, matos e
  arbustos, herbáceas. Cada observação recebe o primeiro grupo cuja
  regra se aplica (por esta ordem):
  - aquática no GIFT → aquáticas;
  - género *Eucalyptus* → eucalipto;
  - conífera (taxonomia do iNaturalist) e árvore no GIFT → pinheiros;
  - género *Quercus* e árvore no GIFT → carvalhos;
  - na lista nacional de invasoras e árvore, arbusto ou planta não
    trepadeira com mais de 2 m → invasoras grandes;
  - árvore no GIFT → outras árvores; arbusto → matos; o resto →
    herbáceas.
- **Musgos, hepáticas e algas saem** (323), pela taxonomia do
  iNaturalist (não vasculares).
- **Herbáceas só nas classes da COS 2023 onde a erva é o que se vê de
  cima:** culturas temporárias, pastagens, montados, dunas e vegetação
  esparsa, zonas húmidas, espaços verdes urbanos. Saem as que estão em
  floresta, matos, edifícios e estradas, vinhas, pomares e olivais,
  estufas e água: 29 644 → 5 967.
- **Uma outra planta por píxel:** fica o grupo mais alto (árvores >
  invasoras grandes > matos > herbáceas > aquáticas), depois a mais
  próxima de 2023. 23 353 → 18 895.
- Resultado: matos 8 145, herbáceas 4 218, invasoras grandes 2 958,
  outras árvores 1 663, carvalhos 802, aquáticas 621, pinheiros 319,
  eucalipto 169. Ficam 6,3 outras plantas por presença.
  *Mudou a 2026-11-03:* os matos debaixo de floresta passaram a sair
  (ver "Matos debaixo de floresta saem" abaixo). Ficam 13 554 (4,5 por
  presença): herbáceas 4 229, invasoras grandes 2 958, matos 2 790,
  outras árvores 1 663, carvalhos 802, aquáticas 624, pinheiros 319,
  eucalipto 169.

**O que mudou (2026-10-30):**
- Primeiro os grupos vinham de listas de géneros feitas à mão. Pedi
  que se baseassem em fontes; passaram a vir do GIFT, da lista
  nacional de invasoras e da taxonomia do iNaturalist. O GIFT
  corrigiu erros das listas manuais (o alecrim e a *Euphorbia
  characias* são arbustos, não herbáceas).
- Primeiro as herbáceas ficavam só em "agricultura e pastagem" (todos
  os códigos 2, 3 e 4 da COS). Perguntei se não bastava tirar as da
  floresta. Não basta: as herbáceas em edifícios (3 523), matos
  (2 361) e pomares e olivais (1 696) dariam píxeis que não são erva.
  Mas a regra antiga também era estrita demais: tirava as das dunas,
  zonas húmidas e jardins, onde a erva é o que se vê. E incluía
  vinhas, pomares, olivais e estufas, que não são erva vista de cima.
  A regra passou a ser por classe da COS, conforme o que cobre o
  píxel.

**Porquê:**
- 1 549 espécies são demasiadas para classes; grupos por forma de
  crescimento separam o que o satélite distingue (copa de árvore,
  mato, erva, água).
- Eucalipto e pinheiro ficam à parte porque são as florestas que
  dominam o distrito. As invasoras grandes ficam à parte porque são as
  plantas mais parecidas com a acácia. 23% das observações de
  eucalipto caem em manchas de acácia da COS: crescem juntos, por isso
  vai ser a confusão mais provável.
- O satélite vê a camada de cima. As pessoas fotografam sobretudo
  plantas pequenas (só 181 eucaliptos em 47 mil observações), e 43%
  das herbáceas estavam debaixo de floresta. Com o rótulo "herbácea",
  um píxel de eucaliptal ensinava o modelo errado; uma erva num
  telhado ensinava que telhados são erva (o mesmo problema que o
  orientador apontou nas ausências dos especialistas em edifícios).
- Pela mesma razão, num píxel com um carvalho e um mato fica o
  carvalho.

**Fundamentação:**
- *Regra da camada de cima:* o sistema de classificação de ocupação
  do solo da FAO (LCCS) decide a forma de vida dominante pela camada
  mais alta ("uppermost canopy"), separa árvores (>5 m) de arbustos
  (<5 m), e diz que árvores esparsas sobre um estrato herbáceo
  fechado não são a forma dominante (Di Gregorio & Jansen, 2000,
  Apêndice A). É por isso que os montados ficam com as herbáceas.
- *Formas de crescimento:* GIFT 3.2 (Weigelt et al., 2020; Denelle et
  al., 2023): 92,7% das observações encontradas pela espécie, 5,9%
  pelo género.
- *Invasoras:* Lista Nacional de Espécies Invasoras, Anexo II do
  Decreto-Lei n.º 92/2019 (só continente). A *Hakea decurrens* subsp.
  *physocarpa* conta como a *H. sericea* da lista: a análise de risco
  da EPPO (2024) concluiu que as populações invasoras de *Hakea*
  amostradas em Portugal são deste táxon, registado durante décadas
  como *H. sericea*.
- *Agrupar espécies em classes:* Ball et al. (2026).
- *Uma por píxel:* Karasiak et al. (2022), como na entrada anterior.
- *Sub-bosque em ciência cidadã:* procurei estudos que tratem
  observações de plantas de sub-bosque ao rotular píxeis de satélite e
  não encontrei nenhum. O mais próximo, Gillespie et al. (2024), treina
  com observações do iNaturalist sobre imagem aérea, mas não verifiquei
  se filtram o sub-bosque. Wolf et al. (2022) viram que mapas de
  traços feitos com o iNaturalist concordam pior em biomas dominados
  por árvores (só li o resumo). Pode ser um contributo metodológico da
  tese.

**Limitações:**
- O GIFT tem erros (diz que a *Hakea decurrens* é trepadeira; por isso
  a regra das trepadeiras não se aplica a árvores e arbustos) e
  classifica algumas espécies de forma diferente da forma local
  (*Quercus coccifera* como árvore). *Smilax aspera* fica nas
  herbáceas porque o GIFT a classifica como "other".
- O limiar de 2 m para invasoras herbáceas grandes (*Cortaderia*,
  *Arundo*, *Phytolacca*) e a tabela de sinónimos são escolhas minhas.
- A lista de classes da COS onde a erva é a camada de cima é a minha
  leitura dos nomes das classes, não uma regra publicada. A COS tem
  unidade mínima de 1 ha: clareiras pequenas perdem-se.
- Os matos também estão sobretudo debaixo de floresta (26% em pinhal,
  21% em eucaliptal, só 13% em matos). *Resolvido a 2026-11-03:* saem
  (ver a entrada abaixo).
- Eucalipto (169) e pinheiros (319) são classes pequenas. Porquê:
  são pouco fotografados (1% e 0,7% das observações de plantas) e o
  filtro *research* tirou a maior parte (67% dos eucaliptos eram
  *casual*, 81% delas do Observer A; hipótese não verificada: registos
  sem foto, como nas acácias). Opções em aberto: recuperar as
  *needs_id* identificadas ao género, juntar ou pesar no treino, ou
  usar a COS para estas classes. Pergunta para o orientador.

**Onde:** passos 11–13 de
[`other_plants_observations.ipynb`](../notebooks/02_citizen_science/other_plants_observations.ipynb);
[`docs/research_questions.md`](../docs/research_questions.md) (secção
"Other Plants as Classes" e tabela do pipeline, passos 8 e 9);
fontes em [`data/README.md`](../data/README.md) (GIFT e lista
nacional de invasoras).

**Na tese:** ❌ Desenho de classes multiclasse, substituído por
"Multiclasse abandonado…" (mais abaixo) — não entra na tese nesta
forma; o sub-bosque debaixo de floresta como candidato a contributo
pode reaparecer de outra forma no pipeline do fundo, por rever.

### Observer A: todas as observações no modelo principal

*2026-11-03, decisão minha.*

**O que decidi:** no modelo principal ficam todas as observações do
Observer A (88% das 3 000 presenças de *A. dealbata*). Não limito o
número por quadrícula na preparação dos dados. Limitá-las ou tirá-las
é a experiência da RQ3 (todas / limitadas / sem as dela), e o modelo
principal é o caso "todas".

**Porquê:**
- Limitar o Observer A é precisamente o que a RQ3 testa. Se o fizesse
  já no modelo principal, a RQ3 ficava sem o caso de comparação.
- As observações repetidas da mesma visita já saíram no passo "uma
  por píxel" (98% das repetidas eram dela).
- Com 88% das presenças, limitar já cortava muitos dados antes de
  saber se o enviesamento muda o resultado.
- Não é uma pergunta para o orientador: a RQ3 já está aprovada, e
  isto é a forma de a pôr em prática.

**Fundamentação:** não verifiquei literatura para esta escolha
concreta; é raciocínio meu, a partir do desenho da RQ3. A motivação
para testar a limitação na RQ3 vem de Phillips et al. (2009) e do
enviesamento descrito por Dimson et al. (2023).

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md)
(tabela do pipeline, passo 10, e
[RQ3](../docs/research_questions.md#rq3--spatial-sampling-bias)).

**Na tese:** ✅ Parcial — a estatística dos 88% já está na Introdução
(tabela Motivation); a decisão de manter todas as observações no
modelo principal fica para o capítulo de Metodologia.

### Matos debaixo de floresta saem

*2026-11-03, decisão minha (a confirmar com a ablação).*

**O que decidi:** para começar, os matos que caem em floresta na COS
2023 (código 5: pinhal, eucaliptal, outras florestas, acacial) saem,
pela mesma regra das herbáceas. Vou testar com e sem esta regra na
ablação; se tirá-los piorar o resultado, volto atrás.
Saem 6 633 matos (pinhal 2 604, eucaliptal 2 087, outras florestas
1 623, acacial 319). Os matos passam de 8 145 para 2 790, e as outras
plantas de 18 895 para 13 554 (4,5 por presença, antes 6,3).

**Porquê:**
- O satélite vê a copa. Um mato fotografado debaixo de um pinhal dá
  um píxel que, de cima, é pinhal; com o rótulo "matos", ensinava o
  modelo que copa de pinheiro é mato.
- Coerência: as herbáceas debaixo de floresta já saíam pela mesma
  razão. Tirar umas e deixar os outros era difícil de defender.
- Esses píxeis confundiam o modelo exatamente nas classes pinheiros
  e eucalipto, e o eucalipto é a confusão mais provável com a acácia.
- Contra: perde-se cerca de dois terços dos matos (6 633 de 10 114),
  que eram a maior classe. E muitos
  pinhais e eucaliptais têm copa aberta; com manchas da COS de pelo
  menos 1 ha, alguns destes matos podiam ser mesmo o que se vê de
  cima. É por isso que fica para testar na ablação.
- Não é uma pergunta para o orientador, mas vou informá-lo.

**Fundamentação:** a regra da camada mais alta da FAO LCCS (Di
Gregorio & Jansen, 2000), como nas herbáceas. Não encontrei estudos
que tirem observações de sub-bosque de ciência cidadã ao rotular
píxeis de satélite (ver a entrada das 8 classes): pode ser um
contributo.

**Onde:** passo 12 de
[`other_plants_observations.ipynb`](../notebooks/02_citizen_science/other_plants_observations.ipynb);
[`docs/research_questions.md`](../docs/research_questions.md) (secção
"Other Plants as Classes" e tabela do pipeline, passo 9).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder); o desenho de base (matos como classe multiclasse) foi
substituído por "Multiclasse abandonado…", por rever se a regra da
camada de cima ainda se aplica ao fundo.

### Máscara de segmentação: sem a direção da câmara; testar várias abordagens

*2026-11-04, decisão do orientador (por mensagem). A regra concreta
está por definir por mim.*

**O que decidi:**
- **Decidido (orientador):** não sigo a ideia de usar a direção da
  câmara ou de separar fotos de grande plano e de paisagem ("acho que
  não vale a pena").
- **Decidido (orientador):** a máscara é um ponto central da tese, e
  vou experimentar várias abordagens.
- **Decidido (orientador):** definir uma regra para considerar a área
  de vegetação mais próxima da observação. Escreveu-o como sugestão
  ("se calhar…?"), mas o que o orientador diz fica como decidido.
  Leio-a como duas coisas que podem ser testadas: (1) levar o ponto à vegetação mais próxima, quando a
  coordenada (onde estava o telemóvel) cai numa estrada ou num
  edifício; (2) estender o rótulo do ponto à mancha à volta, como no
  artigo que indicou (superpíxeis). A segunda é a minha leitura, a
  confirmar.
- **Adotado (meu, a confirmar com o orientador, 2026-11-04):** entre
  as duas leituras acima, fico com a (2) — estender o rótulo à mancha
  à volta — como interpretação de trabalho para desenhar e testar as
  abordagens. Razão: ele escreveu "área de vegetação", não "pixel" ou
  "ponto", e "considerar" essa área sugere usá-la toda, não só realocar
  a coordenada para dentro dela. Continua por confirmar explicitamente
  com ele — pergunta registada em
  [`docs/meetings/proxima-reuniao.md`](../docs/meetings/proxima-reuniao.md).
- **Esclarecido (meu, 2026-11-04):** da candidata dos superpíxeis
  (Rivier et al.), uso só a ideia — superpíxeis + rótulo por maioria
  de voto dos pontos dentro de cada um — aplicada a patches de
  embeddings TESSERA e alimentando o classificador já adotado (frozen
  embeddings + classificador). Não replico o método deles por inteiro
  (eles usam imagem RGB sub-métrica e treinam uma rede de segmentação
  de raiz); ver diferenças em
  [`docs/literature.md`](../docs/literature.md#weak-supervision-from-point-labels).
- **Proposta de parâmetros por omissão para a candidata do crescimento
  de região (meu raciocínio, ainda por testar):** similaridade por
  cosseno; comparar sempre ao pixel-semente, não à média corrente da
  mancha (para não deixar a mancha "andar" para longe do perfil da
  semente); conectividade a 8 vizinhos; raio máximo balizado pelo
  tamanho real dos polígonos "Florestas de acácias" da COS já medidos
  (244 ha / 1 849 polígonos), em vez de um valor inventado; limiar de
  similaridade a definir pela distribuição real de distâncias entre
  cada presença conhecida e os seus vizinhos imediatos (um percentil
  dessa distribuição), em vez de um número fixo à mão. Nenhum destes
  valores foi ainda testado.

**Porquê:**
- O orientador acha que a ideia da câmara não vale a pena.
- A coordenada do iNaturalist nem sempre cai em cima da planta; uma
  regra que leva o ponto à vegetação mais próxima resolve o mesmo
  problema de forma mais direta.
- Por ser central, comparar várias regras pode ser um resultado da
  tese.

**Fundamentação:** o orientador indicou Rivier et al. (2024, IEEE
ICIP), que propaga rótulos de pontos a superpíxeis, e disse que há
mais trabalhos do género. Li o artigo completo (2026-11-03) e procurei
mais trabalhos do género — resumos, números e a comparação com
Gillespie et al. (2024) e Zhang et al. (2021) ficam só em
[`docs/literature.md`](../docs/literature.md#weak-supervision-from-point-labels),
para não duplicar. Conclusão relevante aqui: nenhum trabalho junta
exatamente o nosso caso (poucos pontos de ciência cidadã, embeddings
de foundation models congelados, regra de "vegetação mais próxima");
a técnica em geral não é inédita, mas esta combinação concreta
mantém-se como possível contributo, não prática já estabelecida.

A ideia da câmara veio da apresentação da Lucie Radová (2026-10-30).

**Onde:** [`docs/meetings/2026-11-04.md`](../docs/meetings/2026-11-04.md)
(resposta dos orientadores).

**Na tese:** ✅ Parcial — já referida como candidato a contributo
metodológico na Introdução (secção Contributions: "matching what
citizen scientists tend to photograph… against what the satellite
actually sees"); o desenho concreto e a comparação de abordagens
ficam para o capítulo de Metodologia.

### Baseline do modelo de ciência cidadã pode ser one-class (pergunta sobre os `classifica = 0` sem resposta direta)

*2026-11-03, resposta do orientador por mensagem, a seguimento da
pergunta se os `classifica = 0` podiam servir só para avaliar o modelo
de ciência cidadã.*

**O que respondeu (texto exato):** "O objetivo é o de localizar
*Acacia dealbata*. Para o classificador que vai utilizar como baseline
pode apenas considerar uma classe; existem abordagens para tal. Ou
então constrói o treino manualmente mas não me parece o mais eficiente
pois requer interpretação visual, por exemplo, do OrtoSat. Se quiser
também podemos falar brevemente esta semana." A palavra "treino"
aparece nas duas opções que deu (one-class vs. construir o treino à
mão): a resposta é sobre como **treinar** o classificador baseline sem
ausências confirmadas, não sobre a avaliação que eu tinha perguntado.

**Porquê perguntei:** para avaliar o modelo de ciência cidadã preciso
de locais onde se sabe que não há acácia; os pontos ao acaso da COS
não garantem isso (uma mancha de pinhal pode ter acácia lá dentro). Os
polígonos `classifica = 0` dos especialistas pareciam o único dado com
essa confirmação, mas já tinham sido excluídos do estudo (ver "Usar os
dados de especialistas, com limpeza").

**Em aberto (a resposta não resolve isto):**
- Não diz se os `classifica = 0` são ou não fiáveis — responde a um
  problema relacionado (como treinar sem ausências confirmadas), não à
  pergunta que fiz (usá-los só na avaliação).
- Não é claro o que é "o classificador baseline" aqui: pode ser (a) o
  braço "baseline" da RQ1, já definido em
  [`research_questions.md`](../docs/research_questions.md#rq1--foundation-models-vs-conventional-approaches)
  como o classificador com features do Sentinel-2 (em oposição ao
  "foundation model", com embeddings do TESSERA); ou (b) uma forma
  geral de falar de "o classificador que vou treinar primeiro",
  sem ligação a esse termo específico da tese.
- Não é claro como se concilia com a decisão já tomada de usar os dois
  modelos de RQ1 como multiclasse, com as outras plantas como classes
  (ver "Multiclasse também no modelo de especialistas"): um classificador
  one-class é uma tarefa diferente de um classificador multiclasse.
  **Correção (2026-11-03):** eu tinha escrito aqui que isto era
  "provavelmente sobre a avaliação, não sobre o treino" — está errado.
  A resposta usa a palavra "treino" nas duas opções que dá (one-class
  vs. construir o treino à mão), por isso é sobre o treino do
  classificador baseline, não sobre a avaliação. Continua por
  confirmar se isso significa abandonar o multiclasse nos dois modelos
  principais, ou só no braço Sentinel-2/baseline da RQ1, ou ainda
  construir um terceiro modelo one-class à parte dos dois já desenhados.
- Que abordagem one-class concreta (p. ex. one-class SVM, Isolation
  Forest, modelos de distribuição de espécies) ainda não foi escolhida
  nem pesquisada.
- Por decidir (minha escolha): se aceito falar com o orientador esta
  semana, como ofereceu.

**Resolvido (2026-11-05, reunião presencial):** o orientador esclareceu
em pessoa que a mudança é para abandonar o multiclasse nos dois
modelos principais (ciência cidadã e especialistas), não só no braço
Sentinel-2/baseline da RQ1, como parte de um redesenho maior da RQ1 —
ver a entrada completa em "Multiclasse abandonado; RQ1 passa a uma
curva de redução de esforço (presença vs. fundo)", mais abaixo. O
método concreto para o "one-class" foi escolhido por mim nessa
conversa de seguimento: presença-vs-fundo, não deteção de novidade
pura.

**Fundamentação:** nenhuma referida pelo orientador. Fiz uma primeira
pesquisa (só por resumos/snippets de motor de busca, nenhum artigo lido
por inteiro — a confirmar antes de citar na tese); resumo completo de
cada artigo (Li & Guo 2010, Rapinel & Hubert-Moy 2021, Skowronek/Asner/
Feilhauer 2017, Li/Guo/Elkan 2011, o artigo de 2025 sobre
Jilin-1/Sentinel-2, o contraponto do *Solidago*, etc.) em
[`docs/literature.md#one-class--positive-unlabeled-classification`](../docs/literature.md#one-class--positive-unlabeled-classification),
incluindo a síntese de risco (em todas as comparações encontradas, um
método one-class puro sem fundo foi o pior ou quase o pior). Não achei
nenhum destes sobre *Acacia* nem sobre dados de ciência cidadã; são
pistas para ler, não conclusões.

**Onde:** [`docs/meetings/2026-11-04.md`](../docs/meetings/2026-11-04.md#pergunta-de-seguimento-sobre-classifica--0-para-avaliação-por-mensagem).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder); resolvida por "Multiclasse abandonado…" mais abaixo.

### Validação espacial no lado dos especialistas: zona-tampão, além dos blocos de 10 km

*2026-11-06, minha decisão (unidade assumida, não confirmada pelo
orientador). Pedido de verificação da Íris, a partir de algo dito pelo
orientador na reunião presencial de 2026-11-05 (não registado nessa
altura — ver
[`docs/meetings/2026-11-05.md`](../docs/meetings/2026-11-05.md)).*

**O que o orientador disse (recordado pela Íris, não citação exata):**
na validação do lado dos especialistas, escolher pontos de teste só
aleatoriamente arrisca ficarem ao lado de pontos de treino (vizinhos
próximos), o que infla o desempenho aparente — deu os números "20/30"
como zona-tampão (unidade não confirmada).

**Porquê faz sentido:** os polígonos de especialistas são manchas
contíguas, não pontos dispersos — dividir píxeis individualmente em
treino/teste ao acaso pode colocar um píxel de teste a poucos metros
de um píxel de treino, por vezes no mesmo polígono. As features da
TESSERA/Sentinel-2 são fortemente autocorrelacionadas no espaço a
curta distância, por isso um ponto de teste mesmo ao lado de um ponto
de treino não é realmente "novo" — infla a métrica. Isto é
precisamente o problema descrito por Karasiak et al. (ver abaixo) e
complementa, não substitui, os blocos de 10 km já usados para separar
viés geográfico/do observador a uma escala mais grosseira.

**Investigação feita (2026-11-06):**
- **Literatura (texto completo lido — Mahoney, Johnson & Silge, 2023;
  ver
  [`docs/literature.md#spatial-validation`](../docs/literature.md#spatial-validation)):**
  a distância da zona-tampão **não é uma constante fixa** na
  literatura — deve corresponder ao alcance da autocorrelação espacial
  (dos preditores, da variável-alvo ou dos resíduos do modelo),
  estimado por um variograma empírico (Le Rest et al., 2014, que
  introduziu o SLOO). O mesmo artigo mostra que o bloqueio/clustering
  espacial (mais perto do que já fazemos com os blocos de 10 km) foi
  pelo menos tão robusto quanto a zona-tampão por leave-one-out nas
  simulações deles.
- **Unidade do "20/30":** a biblioteca do próprio Karasiak (Museo
  ToolBox, `SpatialLeaveOneOut`) define a distância da zona-tampão em
  **píxeis**, não metros — o que tornaria "20/30" em 200–300 m (à
  resolução de 10 m da TESSERA), não 20–30 m. Não é uma confirmação
  direta do que o orientador quis dizer, só um indício a favor de
  píxeis.
- **Variograma empírico nos nossos próprios dados (não é de nenhum
  artigo, é cálculo meu — ver
  [`notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb`](../notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb)):**
  a semivariância dos embeddings TESSERA (presenças + fundo, toda a
  extensão do piloto) sobe até cerca de 300–500 m e estabiliza depois
  disso — ou seja, o alcance real da autocorrelação espacial nestes
  dados ronda os 300–500 m, muito mais perto de "20–30 píxeis" do que
  de "20–30 m".

**O que decidi:** assumir "20/30" como metros (zona-tampão de 20–30 m),
sem voltar a perguntar ao orientador, e tirar o ponto da agenda da
próxima reunião.

**Porquê:** a investigação (variograma empírico nos nossos dados,
unidade em píxeis na biblioteca do próprio Karasiak) aponta para
píxeis (200–300 m) como leitura mais provável, não metros — mas gastar
tempo de reunião a confirmar uma unidade de uma zona-tampão não
compensa face ao resto da agenda. Fica registado que isto é uma
suposição minha, não o que o orientador provavelmente quis dizer, para
que a contradição fique visível e não se perca se for preciso revisitar
mais tarde (p. ex. se os resultados da validação parecerem estranhos).

**Fundamentação:** nenhuma — é uma escolha pragmática, não uma decisão
com base em literatura; a literatura e o variograma empírico (ver
"Investigação feita" acima) continuam a apontar na direção oposta
(píxeis, não metros).

**Em aberto:**
- Implementar a zona-tampão de 20–30 m em concreto na divisão
  treino/teste do lado dos especialistas (ainda não feito).
- O variograma usado (~300–500 m) é uma primeira estimativa de área
  larga, não um ajuste de modelo de variograma propriamente dito
  (exponencial/esférico, com intervalo de confiança) — ver limitações
  no notebook. Mantido só como referência, já que a zona-tampão
  adotada (20–30 m) não o segue.

**Onde:**
[`notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb`](../notebooks/04_satellite/tessera_spatial_autocorrelation.ipynb);
[`docs/methodology.md#validation`](../docs/methodology.md#validation);
[`docs/meetings/2026-11-05.md`](../docs/meetings/2026-11-05.md).

**Na tese:** ✅ Parcial — a autocorrelação espacial/validação já é
referida em resumo na Introdução (tabela Motivation, linha Karasiak et
al. 2022); o desenho concreto da zona-tampão fica para o capítulo de
Metodologia.

### Sentinel-2 bruto: via Earth Search (AWS), sem conta, alinhado à grelha da TESSERA

*2026-11-03, minha decisão. Fica só a versão final; ver abaixo as
versões anteriores.*

**O que decidi:** descarregar o Sentinel-2 L2A (ainda em falta em
`data/README.md`) pelo catálogo STAC Earth Search da AWS
(`sentinel-2-l2a`, sem conta nem autenticação), em vez do Copernicus
Data Space ou do Google Earth Engine, as duas opções que o
`data/README.md` já tinha como pendentes. Alinhado píxel a píxel à
grelha da TESSERA (em vez de um bbox à mão), com leitura por janelas
sem descarregar ficheiros inteiros. Resultado: só uma faixa estreita
de teste, não a extensão toda do piloto. Especificação técnica
completa (grelha, reamostragem, bandas, ficheiros):
[`data/README.md`](../data/README.md#sentinel-2-l2a-tessera-grid-2023).

*Revisto duas vezes no mesmo dia antes desta versão: primeiro tile
completo com ficheiros originais; depois, por causa da largura de
banda real (~0,5-1,2 MB/s, tile completo seria 10-16+ h), passei a
recortar; por fim, para alinhar pixel a pixel com a TESSERA, passei a
usar a grelha de um ficheiro GeoTIFF da TESSERA em vez de um bbox meu.*

**Porquê:** o Sentinel-2 era o único dado "em falta" do baseline da
RQ1 (ver `docs/methodology.md`, secção "Baseline"). Tile completo
seria demasiado lento nesta ligação; recortar ao bbox dos dados
rotulados ainda seria lento e não garantia alinhamento píxel a píxel
com a TESSERA — usar a grelha da própria TESSERA resolve as duas
coisas de vez. O teste ficou pequeno (uma faixa, não o distrito todo)
porque o bbox pedido ao `geotessera download` calhou ser pequeno;
fica para alargar depois de confirmar que o pipeline funciona.

**Fundamentação:** a escolha do Sentinel-2 como sensor do baseline já
estava fundamentada (Mouta et al. 2021, Domingo et al. 2023 — ver
`docs/methodology.md`). Não encontrei (nem procurei a fundo) precedente
na literatura especificamente para a via de acesso Earth
Search/STAC/COG com leitura por janelas alinhada à grelha da TESSERA —
é só uma escolha técnica de acesso, não uma decisão metodológica sobre
o que o modelo usa.

**Onde:** [`notebooks/04_satellite/sentinel2_download.ipynb`](../notebooks/04_satellite/sentinel2_download.ipynb),
[`data/README.md`](../data/README.md#sentinel-2-l2a-tessera-grid-2023).

**Na tese:** ⏳ Ainda não escrita (detalhe técnico de acesso a dados;
não é uma decisão metodológica — deve entrar no capítulo de
Metodologia ou em apêndice, se for necessário).

### Multiclasse abandonado; RQ1 passa a uma curva de redução de esforço (presença vs. fundo)

*2026-11-05, reunião presencial. Decisão do orientador (pontos 1 a 4);
ponto 5 é decisão minha, informada por esta conversa. Substitui por
inteiro "Multiclasse também no modelo de especialistas" e resolve
"Baseline do modelo de ciência cidadã pode ser one-class" (ambas
acima).*

**O que decidi:**
1. **Multiclasse abandonado nos dois modelos** (ciência cidadã e
   especialistas): usar outras plantas/COS como classes próprias de
   forma consistente exigiria construir dados de treino à mão
   (interpretação visual, p. ex. do OrtoSat) para ter ausências
   confirmadas, o que o orientador não considera eficiente. Os dois
   modelos passam a ter só *A. dealbata* como alvo.
2. **RQ1 passa a uma experiência de redução de esforço:** em vez de um
   "upper bound" fixo (só especialistas), a experiência começa só com
   ciência cidadã e acrescenta progressivamente dados de especialistas
   (p. ex. 10%, 20%, …) para encontrar o equilíbrio entre desempenho e
   o esforço de recolha no terreno. O ponto 100% especialistas continua
   a existir, como o extremo da curva, não como um braço à parte.
3. **Correr a experiência toda uma vez por representação**, mudando só
   a fonte (TESSERA, depois Sentinel-2), para que a comparação entre
   representações não se confunda com diferenças na curva em si.
4. **Fase 1: só embeddings TESSERA.** O Sentinel-2 fica para uma fase
   posterior.
5. **Testar os dois métodos em paralelo desde o início: one-class
   verdadeiro (deteção de novidade) e presença-vs-fundo.** *Revisto a
   2026-11-06, segunda vez no mesmo dia:* a ideia inicial (só
   presença-vs-fundo) passou primeiro a uma abordagem faseada (one-class
   primeiro, fundo como recurso), e depois — depois da pesquisa de
   literatura (ver "Atualização" abaixo) mostrar que a avaliação
   provavelmente precisa de fundo de qualquer forma, o que esvazia parte
   da vantagem de testar o one-class verdadeiro sozinho primeiro — a
   decisão final é correr os dois desde a primeira experiência, em vez
   de faseado. Decisão minha, a pedido da Íris.
6. **Mistura aditiva na curva de redução de esforço:** a base de
   ciência cidadã fica fixa; os dados de especialistas são
   acrescentados progressivamente por cima (não trocados), por isso o
   N total de treino cresce a cada nível da curva. Reportar sempre o N
   total ao lado da percentagem de especialistas em cada ponto, para
   não esconder o efeito do volume de dados. Decisão minha, confirmada
   pela Íris (2026-11-06).
7. **Método one-class concreto: one-class SVM, não Isolation Forest.**
   Decisão minha, a pedido explícito da Íris ("decide those for
   yourself and start comparing them", 2026-11-06), resolvida por
   comparação direta, não só por literatura — ver "Atualização
   (comparação direta)" abaixo.
8. **Fundo partilhado construído (primeira versão):** 2000 pontos
   aleatórios uniformes na extensão já coberta pelos embeddings TESSERA
   do piloto, excluindo uma zona-tampão de 50 m à volta de cada
   presença confirmada de *A. dealbata* (ciência cidadã e polígonos de
   especialistas). Decisão minha, a pedido explícito da Íris; **ainda
   não confirmada pelo orientador** como o desenho final e partilhado
   para toda a curva — ver "Atualização" abaixo.

**Porquê:**
- A construção manual de ausências confirmadas (alternativa dada pelo
  orientador) não é eficiente face ao volume de dados necessário.
- A redução de esforço responde diretamente ao objetivo 1 da proposta
  (reduzir a dependência de dados de referência caros): a curva mostra
  quanto desempenho se ganha por cada fração adicional de dados de
  especialistas, em vez de um único ponto de comparação.
- Correr tudo uma vez por representação isola o efeito da
  representação (TESSERA vs. Sentinel-2) do efeito da curva de redução
  de esforço.
- TESSERA primeiro porque é o foundation model já acessível (ver "Fase
  1 só TESSERA" no to-do); o Sentinel-2 já está parcialmente testado
  (ver "Sentinel-2 bruto…" acima) mas fica para confirmar o desenho
  antes de repetir tudo.
- Testar os dois em paralelo, não faseado: a pesquisa de literatura
  (ver "Atualização" abaixo) mostra que a avaliação de um modelo só com
  presenças provavelmente precisa de um fundo de qualquer forma (índice
  de Boyce, F-pb/F-cpb — nenhum dos dois dispensa fundo por completo),
  por isso testar o one-class verdadeiro sozinho primeiro já não evita
  por completo o problema do fundo, que tem de ser resolvido de
  qualquer forma. Correr os dois desde já também poupa tempo face a um
  ciclo faseado (testar um, esperar, só depois testar o outro).
- Mistura aditiva: mapeia diretamente a pergunta do orientador ("quanto
  esforço de campo compensa?"); a alternativa (troca, N total fixo)
  respondia a uma pergunta diferente (qualidade dos dados a custo
  fixo), não à redução de esforço.

**Fundamentação:**
- Phillips et al. (2009): *target-group background*, já citado para
  "Outras plantas como classes" — continua relevante se/quando for
  preciso um fundo (ver ponto 7 em "Em aberto").
- Pesquisa de literatura mais completa feita a 2026-11-06 (ver
  "Atualização" abaixo e
  [`docs/literature.md`](../docs/literature.md#one-class--positive-unlabeled-classification)):
  em todas as comparações empíricas encontradas, um método one-class
  verdadeiro sem fundo foi o pior ou quase o pior, sem contraexemplo
  encontrado — mas nenhum dos estudos tem exatamente a nossa
  combinação, por isso não é motivo para desistir do one-class
  verdadeiro, só para não apostar só nele.
- A separação "multiclasse abandonado" / "redução de esforço" / "uma
  vez por representação" / "fase 1 só TESSERA" vem diretamente do que
  o orientador disse na reunião; não tem fundamentação de literatura
  própria para já. A ordem "one-class primeiro, fundo depois" e a
  mistura aditiva são raciocínio meu, a partir desta conversa.

**Atualização (2026-11-06, pesquisa de literatura — ver
[`docs/literature.md`](../docs/literature.md#one-class--positive-unlabeled-classification)
para o detalhe completo, tudo por confirmar a partir de resumos, sem
texto completo lido):**
- Em todas as comparações empíricas encontradas, um método one-class
  verdadeiro sem fundo nenhum (one-class SVM simples, Isolation Forest
  como deteção de anomalias pura) foi o pior ou quase o pior método, e
  não encontrei nenhum contraexemplo. Isto não garante que vá falhar
  para a *A. dealbata* (nenhum destes estudos tem exatamente a nossa
  combinação: embeddings de foundation models congelados, presenças de
  ciência cidadã esparsas e ruidosas, Portugal), mas a literatura não
  dá uma razão positiva para esperar que o one-class verdadeiro ganhe.
- Nenhum método de avaliação para modelos só-com-presenças encontrado
  (índice de Boyce contínuo, F-pb/F-cpb) dispensa dados de fundo por
  completo — todos evitam só a necessidade de ausências *rotuladas*,
  não de fundo. Ou seja: mesmo que o treino do one-class verdadeiro não
  precise de fundo, a avaliação provavelmente vai precisar — o que
  enfraquece parcialmente o motivo original para o testar primeiro
  (evitar o problema do fundo).
- Correção: a entrada "Rapinel & Hubert-Moy (2021)" acima estava
  atribuída erradamente a "Zhao & Zhong" — corrigido.
- **Consequência (2026-11-06):** esta informação levou a rever o ponto
  5 acima — em vez de testar o one-class verdadeiro primeiro e só
  avançar para presença-vs-fundo se corresse mal, os dois métodos
  passam a ser testados em paralelo desde a primeira experiência.

**Atualização (2026-11-06, comparação direta — ver
[`notebooks/07_foundation_models/one_class_method_selection.ipynb`](../notebooks/07_foundation_models/one_class_method_selection.ipynb)):**
- A pedido explícito da Íris ("decide those for yourself and start
  comparing them, so we have a final decision regarding these two
  options"), construí o fundo partilhado (ponto 8 acima) e comparei
  one-class SVM (RBF, `nu` 0.05/0.10/0.20) com Isolation Forest
  (`contamination` auto/0.1), treinados só com embeddings TESSERA de
  presenças de ciência cidadã (2 995 pontos válidos de 3 000), 5
  divisões espaciais diferentes (20% dos 85 blocos de 10 km como
  teste, reaproveitando a mesma grelha dos ficheiros de embeddings do
  piloto), avaliados contra as presenças de teste e o fundo de teste
  com ROC-AUC e o índice de Boyce contínuo (Hirzel et al., 2006).
- **Resultado:** one-class SVM claramente melhor nas duas métricas, em
  todas as divisões espaciais e configurações testadas — ROC-AUC
  ≈0.64–0.65 vs. ≈0.57; índice de Boyce ≈0.6–0.8 vs. ≈0.25 (Isolation
  Forest perto de zero/sem padrão útil). Ver ponto 7 acima.
- **Só um primeiro passo, não um benchmark definitivo:** só o braço de
  ciência cidadã foi testado (não especialistas, não a curva
  completa); os hiperparâmetros não foram afinados por validação
  aninhada, só uma pequena varrimento; o fundo usado (ponto 8) ainda
  não está confirmado pelo orientador como o desenho final.

**Em aberto (ainda por decidir, não resolvido nesta conversa):**
- ~~Níveis exatos de mistura da curva e bloco espacial de teste fixo em
  todos os pontos da curva~~ — feito (2026-11-07), ver
  [Curva de redução de esforço completa: 0%–100%, com fundo e bloco de teste fixos](#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos)
  abaixo. Resultado inesperado: para Random Forest e Logistic
  Regression, acrescentar dados de especialistas de 10% a 90% quase não
  muda o desempenho — só muda a 100% (e para pior na generalização às
  presenças de ciência cidadã).
- **Confirmar com o orientador o desenho do fundo partilhado** (ponto
  8 acima): 2000 pontos aleatórios uniformes, zona-tampão de 50 m —
  tanto o N como o raio da zona-tampão são escolha minha, sem valor
  específico encontrado na literatura para o raio.
- ~~A RQ3 tinha como candidata "outras plantas como classes vs. fundo ao
  acaso"; sem classes próprias, isto passa a "fundo de outras plantas
  vs. fundo ao acaso" — por rever.~~ — revisto (2026-11-06): a
  experiência não dependia do multiclasse, só precisa do fundo de
  outras plantas existir como opção, o que continua a acontecer. O que
  mudou é que o fundo principal já construído para a RQ1 é aleatório
  uniforme, não o de outras plantas — por isso os dois fundos passam a
  mapear diretamente para a pergunta de amplificar/mitigar da RQ3
  (aleatório expõe mais o viés, o de outras plantas corrige-o em
  parte). Ver
  [`docs/research_questions.md`](../docs/research_questions.md#rq3--spatial-sampling-bias).
  Proposta minha, por confirmar com o orientador; a experiência em si
  continua por correr.

**Onde:** [`docs/research_questions.md`](../docs/research_questions.md#rq1--foundation-models-vs-conventional-approaches)
(RQ1 reescrita) e
[`docs/research_questions.md`](../docs/research_questions.md#other-plants-as-classes-adopted-direction)
(fundo em vez de classes);
[`docs/meetings/2026-11-05.md`](../docs/meetings/2026-11-05.md).

**Na tese:** ✅ Parcial — o desenho atual da RQ1 (curva de redução de
esforço, mistura aditiva) já está resumido em
[`thesis/document/text/1-introduction.tex`](document/text/1-introduction.tex)
(secções Research Questions e Contributions); o desenho operacional
completo (níveis da curva, fundo partilhado, one-class vs.
presença-vs-fundo) fica para o capítulo de Metodologia. **Decidido
nesta conversa:** o multiclasse abandonado não desaparece da tese por
completo — ao escrever o capítulo de Metodologia, incluir um parágrafo
breve (não uma secção) explicando porque foi abandonado (custo de
construir ausências confirmadas à mão; literatura sem vantagem clara
do one-class puro sem fundo, ver "Atualização" acima), como
justificação do desenho final, não como histórico extenso.

### Estrutura do documento: seguir um relatório de referência de outro aluno, onde for aplicável

*2026-11-06, decisão minha.*

**O que decidi:** usar
[`thesis/guidance_example/1768249601_Entrega_intermedia-1.pdf`](guidance_example/1768249601_Entrega_intermedia-1.pdf)
(Gonçalo da Silva Lopes dos Santos, "Enhancing Cargo Container License
Plate Recognition Using Visual Language Models", DEI/FCTUC, orientado
por Jacinto Estima e Catarina Silva, janeiro de 2026) como referência
de estrutura para o meu próprio documento, no que for aplicável —
avaliado como um trabalho com boa nota pela Íris.

**Porquê:** ter um exemplo real do mesmo departamento, já avaliado,
ajuda a calibrar o nível de detalhe e a organização esperados, em vez
de inventar a estrutura do zero.

**O que a estrutura do exemplo tem, concretamente:** capa, declaração
de uso de IA, abstract/resumo + palavras-chave em inglês e português,
lista de acrónimos, lista de figuras, lista de tabelas; depois 5
capítulos — (1) Introduction (Context and Motivation, Goals, Document
Structure), (2) Background (conceitos de base do domínio e da área
técnica), (3) State of Art (dividido por sub-tema), (4) Proposed Work
(a parte central, incluindo descrição dos dados e um plano de
trabalho/avaliação de risco para o trabalho que falta), (5) Conclusion
and Future Work; referências no fim.

**Nota importante, para não confundir mais tarde:** apesar do título
dizer "Dissertation", o nome do ficheiro
("Entrega_intermedia") e o conteúdo do capítulo 4 (secções de Work
Plan com Gantt chart e Risk Assessment para o segundo semestre, e um
capítulo 5 que é só "Conclusion and Future Work", sem capítulo de
Resultados) indicam que isto é um **relatório intermédio** (um
marco a meio do trabalho), não uma tese final já defendida. É uma boa
referência para a estrutura dos capítulos iniciais (Introduction,
Background, State of Art) e para o aparato (acrónimos, listas,
declaração de IA), mas não tem um capítulo de Resultados para comparar
com o meu capítulo `4-results.tex` — isso ainda não está resolvido por
este exemplo.

**Comparação com a estrutura atual (`thesis/document/text/`):** já
tenho `1-introduction.tex`, `2-related-work.tex`, `3-methodology.tex`,
`4-results.tex`, `5-conclusion.tex` — à partida mais próxima de uma
tese final do que deste relatório intermédio. Capítulos 1–3 do exemplo
mapeiam razoavelmente para os meus capítulos 1–2; o capítulo 4 do
exemplo (Proposed Work) não mapeia diretamente, porque mistura o que
no meu caso são dois capítulos separados (Metodologia e Resultados).

**Fundamentação:** nenhuma — é uma escolha de estrutura/organização,
não uma decisão metodológica de investigação.

**Em aberto:** rever capítulo a capítulo, à medida que cada um for
escrito, o que vale a pena imitar (p. ex. a secção "Overall Analysis"
no fim do Background, ou a lista de acrónimos) e o que não se aplica
(Work Plan/Gantt/Risk Assessment, próprios de um relatório intermédio).

**Atualização (2026-11-06):** confirmado que a minha primeira entrega
também é um **relatório intermédio** (não a tese final), prevista para
o início de dezembro de 2026 — ver a entrada seguinte, "Primeira
entrega: relatório intermédio, início de dezembro de 2026". Isto torna
a "Nota importante" acima diretamente relevante, não só uma ressalva:
o exemplo passa a ser a referência certa para o género de documento
todo (não só os capítulos iniciais), incluindo a parte de Work
Plan/Risk Assessment que antes parecia não aplicável.

**Onde:** [`thesis/guidance_example/1768249601_Entrega_intermedia-1.pdf`](guidance_example/1768249601_Entrega_intermedia-1.pdf).

**Na tese:** ✅ Parcial — `1-introduction.tex` já existe e mapeia
razoavelmente para os capítulos 1–2 do exemplo (ver "Comparação"
acima); os restantes capítulos (2–5) ainda por escrever/rever à luz
desta referência, agora sabendo que o destino de dezembro é um
relatório intermédio, não a tese final.

### Identidade da tese confirmada: título, mestrado, orientadores, idioma e data da entrega

*2026-11-06, informação dada pela Íris (factos fixos da tese, não
decisões de desenho).*

**O que sei:**
- Mestrado: Mestrado em Inteligência Artificial e Ciência de Dados
  (Master's in Artificial Intelligence and Data Science).
- Título oficial: "Advancing the Mapping of Invasive Alien Plants by
  Combining Citizen Science, Earth Observation Foundation Models and
  Satellite Imagery" (EN) / "Mapeamento de Plantas Exóticas Invasoras
  através da Combinação de Ciência Cidadã, Modelos Fundacionais de
  Observação da Terra e Imagens de Satélite" (PT).
- Orientadores: Professor Jacinto Paulo Simões Estima e Professor
  Diogo André Vicente Amorim Duarte.
- O documento (`thesis/document/`) passa a ser escrito em inglês
  (`\docLanguage{en}` em `0-main.tex`), não em português.
- A data da entrega intermédia passa de início de dezembro de 2026
  para início de janeiro de 2027 (ver "Primeira entrega" abaixo).

**Onde:** `thesis/document/0-main.tex` (bloco CONFIGURATION —
`\titleEN`, `\titlePT`, `\descMScEN/PT`, `\titlePageDescMScEN/PT`,
`\docLanguage`, `\dateEN`, `\datePT`).

**Na tese:** ✅ Feito — capa e página de título
(`frontmatter/1-coverpage.tex`, `frontmatter/2-titlepage.tex`) já
refletem estes dados via `0-main.tex`.

### Primeira entrega: relatório intermédio, início de janeiro de 2027

*2026-11-06, informação dada pela Íris (facto do calendário da tese,
não uma decisão de desenho). Data corrigida de dezembro de 2026 para
janeiro de 2027 em 2026-11-06 (ver entrada anterior).*

**O que sei:** a minha primeira entrega da tese é um relatório
intermédio (marco a meio do trabalho), a entregar no início de
janeiro de 2027 — não a tese final. Isto está em linha com o género
de documento do exemplo de referência (ver entrada anterior), que
também é um relatório deste tipo, do mesmo departamento.

**Porquê isto importa agora:** a estrutura atual de
`thesis/document/text/` (`1-introduction.tex`, `2-related-work.tex`,
`3-methodology.tex`, `4-results.tex`, `5-conclusion.tex`) está desenhada
como uma tese final, com um capítulo de Resultados. Para um relatório
intermédio em dezembro, não vou ter resultados finais da RQ1 (a curva
de redução de esforço ainda não está implementada para o braço de
especialistas — ver
[multiclasse abandonado](#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)
acima). O conteúdo provável para dezembro é mais próximo do capítulo
"Proposed Work" do exemplo (desenho proposto, dados preparados, plano
de trabalho e riscos para o resto da tese) do que de um capítulo de
Resultados fechado.

**Decidido (2026-11-06):** a entrega de janeiro **não** vai seguir a
estrutura final-de-tese tal como está em `thesis/document/text/` —
confirmado por mim. Ainda não decido o mapeamento exato (que capítulo
vira o quê) porque as experiências da RQ1 ainda não estão todas
feitas (só o braço de ciência cidadã foi testado até agora — ver
[multiclasse abandonado](#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)
acima) e isso condiciona quanto fica como "resultado" versus "plano de
trabalho".

**Plano (2026-11-07, esclarecido pela Íris):** o objetivo é terminar as
experiências da RQ1 (curva de redução de esforço completa, nos dois
braços — ciência cidadã e especialistas, com o fundo confirmado e
ambos os métodos, one-class SVM e presença-vs-fundo) antes da entrega
de janeiro, para que o capítulo de Resultados apresente a RQ1
respondida, não um resultado preliminar isolado. Se não for possível
terminar a tempo, o conteúdo recua para resultado preliminar + plano
de trabalho (ver "Em aberto" abaixo).

**Em aberto (por decidir, não resolvido nesta conversa):**
- O mapeamento exato de `thesis/document/text/` para a forma de
  relatório intermédio (p. ex. se `4-results.tex` se torna uma secção
  de resultados preliminares dentro de um capítulo tipo "Proposed
  Work", ou se mantém capítulo próprio mas sem fechar os resultados) —
  fica para decidir quando as experiências da RQ1 estiverem mais
  avançadas.
- Que resultados preliminares (só o braço de ciência cidadã, testado
  até agora — ver
  [notebooks/07_foundation_models/one_class_method_selection.ipynb](../notebooks/07_foundation_models/one_class_method_selection.ipynb))
  é razoável incluir como resultados parciais, versus deixar só como
  "trabalho em curso" no plano de trabalho.
- Prazo exato de início de janeiro — só foi dito "início de janeiro
  de 2027", sem data exata.

**Onde:** sem notebook/figura própria; afeta diretamente
`thesis/document/text/` e
[`thesis/guidance_example/1768249601_Entrega_intermedia-1.pdf`](guidance_example/1768249601_Entrega_intermedia-1.pdf)
como referência de género.

**Na tese:** ⏳ Ainda não escrita — é a própria entrega que está em
causa; o mapeamento de capítulos fica para quando as experiências da
RQ1 estiverem mais avançadas.

### Classificador presença-vs-fundo (ciência cidadã): Random Forest, por agora

*2026-11-06, decisão minha, primeira passagem, não confirmada pelo
orientador.*

**O que decidi:** usar **Random Forest** como classificador por
omissão para o braço presença-vs-fundo da RQ1 (candidatos de
`docs/research_questions.md`: Random Forest, Logistic Regression, rede
neuronal compacta). Comparei Random Forest e Logistic Regression nos
mesmos blocos espaciais (10 km, 5 divisões) e no mesmo fundo
partilhado já usados para escolher o one-class SVM: Random Forest
ROC-AUC 0,842 (dp 0,028), Boyce 0,989 (dp 0,022); Logistic Regression
ROC-AUC 0,878 (dp 0,052), Boyce 0,973 (dp 0,042). Nenhum dos dois
domina nas duas métricas — a Logistic Regression tem o ROC-AUC médio
mais alto mas também mais variável entre divisões; o Random Forest tem
o índice de Boyce mais alto e é mais estável nas duas métricas.

**Porquê Random Forest e não Logistic Regression:** com a diferença de
desempenho pequena e sem vencedor claro, desempatei por (1)
estabilidade entre divisões espaciais, que importa mais aqui do que um
pequeno ganho médio de AUC, dado que o lado dos especialistas só tem
18 blocos de 10 km independentes (corrigido 2026-11-07 — o valor de 15
citado aqui originalmente media a mesma coisa noutro sistema de
coordenadas, ver
[[discrepância-de-15-vs-18-blocos-espaciais-no-lado-dos-especialistas-é-o-sistema-de-coordenadas-não-um-bug]]);
e (2)
fundamentação: o Random Forest já tem cinco citações de apoio em
`docs/research_questions.md`, a Logistic Regression nenhuma. A
Logistic Regression não é descartada, continua a ser reportada como
referência barata de calcular.

**A rede neuronal compacta (terceira candidata) não foi testada** —
decisão de alcance, não de mérito: o objetivo desta passagem era
confirmar que o braço presença-vs-fundo funciona e escolher um
classificador para levar à curva completa, não esgotar os três
candidatos.

**Resultado também confirma a literatura:** os dois classificadores
presença-vs-fundo têm desempenho muito superior ao one-class SVM
testado antes (ROC-AUC ≈0,64–0,65, Boyce ≈0,6–0,8), no mesmo fundo e
divisões — alinhado com a pesquisa de literatura já feita (ver
"Atualização", acima, em "Multiclasse abandonado"), que não encontrou
nenhum caso onde o one-class puro batesse um método com fundo.

**Fundamentação:** candidatos e citações do Random Forest já listados
em `docs/research_questions.md` (Ball et al., 2026; Yang et al., 2026;
Mouta et al., 2021; Domingo et al., 2023; Eskandari et al., 2025); a
Logistic Regression não tem fundamentação de literatura verificada —
está incluída como referência linear simples, não por recomendação de
um artigo específico.

**Em aberto:** confirmar com o orientador; afinação de hiperparâmetros
fica para mais tarde; testar a rede neuronal compacta. ~~Repetir a
comparação no braço de especialistas~~ — feito, ver
[Braço de especialistas: one-class SVM e Random Forest confirmados (100% especialistas)](#braço-de-especialistas-one-class-svm-e-random-forest-confirmados-100-especialistas)
abaixo: a escolha mantém-se, com um desempenho ainda mais claro a
favor do Random Forest no índice de Boyce.

**Onde:** [`notebooks/07_foundation_models/presence_background_citizen_science.ipynb`](../notebooks/07_foundation_models/presence_background_citizen_science.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder).

### Braço de especialistas: one-class SVM e Random Forest confirmados (100% especialistas)

*2026-11-07, decisão minha, primeira passagem, não confirmada pelo
orientador.*

**O que decidi:** aplicar as duas escolhas já feitas no braço de
ciência cidadã — one-class SVM (`nu=0.05`) e Random Forest como
classificador presença-vs-fundo por omissão, com Logistic Regression
como referência — ao braço de especialistas (polígonos `classifica =
1`, sem ciência cidadã), o ponto "100% especialistas" da curva de
redução de esforço. Mesmo fundo partilhado, mesmas métricas (ROC-AUC,
índice de Boyce contínuo), 5 divisões espaciais.

**Resultado:** one-class SVM ROC-AUC 0,911 (dp 0,037), Boyce 0,868 (dp
0,080); Random Forest ROC-AUC 0,990 (dp 0,004), Boyce 0,954 (dp
0,011); Logistic Regression ROC-AUC 0,990 (dp 0,003), Boyce 0,879 (dp
0,086) — as 5 divisões válidas em todos os casos. O mesmo padrão do
braço de ciência cidadã mantém-se: presença-vs-fundo bate o one-class
SVM nas duas métricas; Random Forest bate a Logistic Regression no
índice de Boyce (0,954 vs. 0,879), com muito menos variância (dp 0,011
vs. 0,086), e empata no ROC-AUC. **Random Forest mantém-se como
classificador por omissão para o resto da RQ1.**

**Tudo pontua muito mais alto aqui do que no braço de ciência cidadã**
(p. ex. one-class SVM: 0,911/0,868 aqui vs. 0,654/0,816 lá; Random
Forest: 0,990/0,954 aqui vs. 0,842/0,989 lá — o índice de Boyce fica
parecido, mas o ROC-AUC sobe muito). **Interpretar isto como "o braço
de especialistas é simplesmente mais fácil" seria prematuro (leitura
minha, não confirmada):** as presenças de especialistas são manchas
florestais grandes e contíguas, com embeddings TESSERA internamente
parecidos, enquanto o fundo é aleatório uniforme sobre uso do solo
misto — separar "dentro de uma mancha grande e homogénea de acácia" de
"um ponto qualquer ao acaso no distrito" pode ser um problema
geométrico mais fácil no espaço de embeddings do que separar
observações de ciência cidadã, pontuais e ruidosas, do mesmo fundo,
independentemente de qual dos dois modelos capta melhor a presença de
acácia do ponto de vista ecológico. Fica como hipótese a vigiar quando
a curva misturar as duas fontes, não como conclusão.

**Adaptação nova, só neste braço:** com as presenças de especialistas
concentradas em poucos blocos de 10 km, sortear os blocos de teste a
partir do universo todo (presenças + fundo, como no braço de ciência
cidadã) deixaria a maior parte das divisões sem presenças de teste
suficientes. Os blocos de teste passam a ser sorteados só de entre os
blocos que já têm presenças de especialistas; o fundo de treino/teste
continua a vir do conjunto todo, dividido pelos blocos sorteados.
Decisão minha, não confirmada pelo orientador.

**Correção de contagem:** a junção espacial das presenças de
especialistas com os embeddings do piloto encontrou **18** blocos de
10 km, não os 15 referidos em `docs/research_questions.md` — esse
número descrevia só os 1 849 polígonos dentro do distrito de Coimbra;
a extensão dos embeddings do piloto e esta junção apanham mais alguns
blocos na borda. Por corrigir em `docs/research_questions.md`.

**Fundamentação:** mesma desta secção e da entrada "Multiclasse
abandonado" acima — nenhuma literatura nova consultada para esta
passagem, só a confirmação empírica de que as escolhas já
fundamentadas no braço de ciência cidadã se mantêm aqui.

**Em aberto:** confirmar com o orientador (fundo partilhado, Random
Forest por omissão, e agora também a adaptação dos blocos de teste);
testar a rede neuronal compacta; perceber se o salto de desempenho
reflete uma tarefa mais fácil (hipótese acima) antes de comparar os
dois braços como se fossem diretamente equivalentes; níveis
intermédios da curva (mistura aditiva) ainda por fazer.

**Onde:** [`notebooks/07_foundation_models/expert_arm_classifiers.ipynb`](../notebooks/07_foundation_models/expert_arm_classifiers.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder).

### Curva de redução de esforço completa: 0%–100%, com fundo e bloco de teste fixos

*2026-11-07, decisão minha, primeira passagem, não confirmada pelo
orientador. Pedido explícito da Íris: testar 100%, 10%, 20%, … até
encontrar o equilíbrio entre desempenho e custo de recolha no terreno.*

**O que decidi (desenho dos 3 pontos em aberto, agora resolvidos):**

1. **Unidade de mistura: polígonos, não píxeis.** "X% de especialistas"
   passa a ser X% dos polígonos de especialistas sorteados (com todos
   os seus píxeis), não X% dos píxeis espalhados por todos os
   polígonos — o custo de campo é por local visitado, não por píxel.
2. **Amostragem encaixada (nested):** uma única ordem aleatória fixa
   (seed 0) decide que polígonos "já têm esforço gasto" em cada nível,
   por isso os polígonos de 20% incluem sempre os de 10% — a curva
   mostra esforço a acumular, não uma amostra nova a cada ponto.
3. **Um conjunto de teste fixo por semente, igual em todos os níveis
   da curva:** os blocos de teste são sorteados uma vez por semente
   (não uma vez por nível), a partir dos blocos de 10 km com presenças
   de ciência cidadã ou de especialistas, e mantidos iguais do 0% ao
   100% dentro dessa semente — sem isto, uma mudança de pontuação ao
   longo da curva podia só significar "dados de teste diferentes", não
   "mais dados de especialistas ajudaram". Continua a média de 5
   sementes.
4. **O conjunto de teste inclui sempre as duas fontes**, mesmo a 100%
   (treino só com especialistas) — mostra também se um modelo treinado
   só com dados caros generaliza de volta à distribuição de ciência
   cidadã, não só a mais dados de especialistas.

**Resultado — Random Forest e Logistic Regression praticamente planos
do 0% ao 90%, só mudam a 100%:** Random Forest ROC-AUC 0,879 (0%) →
0,882 (20%) → 0,878 (90%) → 0,801 (100%); Boyce 0,993 (0%) → 0,994
(20%) → 0,983 (90%) → 0,917 (100%) — todos os pontos 10–90% dentro do
ruído de uma semente face ao 0%. Logistic Regression sobe um pouco, de
forma genuína (ROC-AUC 0,873 → 0,896 do 0% ao 90%), mas também cai a
100%. **Acrescentar dados de especialistas entre 10% e 90% não traz
ganho visível para estes dois classificadores; só muda alguma coisa a
100%, e para pior** — a 100% o modelo nunca viu ciência cidadã no
treino, mas continua a ser avaliado contra presenças de ciência
cidadã no teste (ponto 4 acima), e generaliza pior para lá.

**Explicação provável, visível nos próprios números:** em todos os
níveis 10–90%, a ciência cidadã continua a fornecer 85–100% das
presenças de treino (p. ex. a 90%: 2 995 de ciência cidadã vs. 2 504
píxeis de especialistas) — o sinal de ciência cidadã domina o treino o
tempo todo, e um modelo já perto do teto só com ciência cidadã (Boyce
≈0,98–0,99 desde o 0%) tem pouca margem para a fração crescente de
especialistas mudar alguma coisa. Isto também é consistente com
Dimson et al. (2023): as duas fontes têm vieses diferentes, e só
retirar a ciência cidadã por completo (100%) muda o que o modelo
aprende — mudança que aqui prejudica a generalização de volta à
ciência cidadã, não ajuda.

**One-Class SVM é a exceção — melhora mesmo com mais esforço de
especialistas:** ROC-AUC sobe de forma monótona, 0,574 (0%) → 0,655
(70%) → 0,765 (100%) — uma tendência real, não ruído, ainda que fique
sempre bem abaixo dos dois classificadores presença-vs-fundo; o índice
de Boyce para este método é ruidoso (0,63–0,77, dp até 0,30), sem
tendência clara.

**Estes números não são diretamente comparáveis aos 0% e 100% dos
notebooks anteriores** (`one_class_method_selection.ipynb` /
`presence_background_citizen_science.ipynb` para 0%,
`expert_arm_classifiers.ipynb` para 100%) — esses usavam, cada um, o
seu próprio sorteio de blocos de teste (85 blocos para o 0%, só
presenças de especialistas no teste do 100%); aqui todos os níveis são
avaliados contra o mesmo conjunto combinado (ciência cidadã +
especialistas), sorteado só dos 47 blocos que têm alguma das duas
fontes. As pontuações mais baixas aqui (p. ex. Random Forest a 100%:
0,801/0,917 aqui vs. 0,990/0,954 lá) são a consequência direta e
informativa de também exigir generalização à ciência cidadã, não uma
contradição.

**Resposta provisória à pergunta da Íris ("onde está o equilíbrio"):**
com este desenho, **nenhuma quantidade de dados de especialistas
abaixo da substituição total traz uma melhoria visível** — se isto se
confirmar, a implicação prática é que este desenho de RQ1 não
justifica o custo de recolha no terreno, porque a ciência cidadã
sozinha já captura, aqui, praticamente todo o desempenho
presença-vs-fundo alcançável. É o oposto de "mais dados de
especialistas é sempre melhor" e merece escrutínio, não aceitação
automática, antes de virar conclusão.

**Fundamentação:** Dimson et al. (2023) para a diferença de viés entre
fontes (já citado acima); o resto é raciocínio meu a partir dos
números desta experiência, sem literatura nova consultada.

**Em aberto:**
- ~~Pode ser efeito de teto (Boyce já ≈0,98–0,99 no Random Forest a 0%)
  em vez de prova de que os dados de especialistas não valem nada — um
  conjunto de teste mais difícil ou outra métrica podiam revelar
  diferenças que esta não consegue.~~ Testado com um fundo só de tipos
  de floresta — ver [[curva-fundo-so-floresta]] abaixo: a conclusão
  mantém-se (até melhora no Random Forest), não era efeito de teto do
  fundo fácil.
- Esforço medido só como % de polígonos, não ponderado por área ou por
  custo real de campo (deslocação, dificuldade de acesso).
- Rede neuronal compacta ainda não testada; só TESSERA, Sentinel-2 por
  fazer; fundo partilhado ainda não confirmado pelo orientador.
- Confirmar com o orientador antes de tratar isto como resposta final
  à pergunta do equilíbrio custo/desempenho.

**Onde:** [`notebooks/07_foundation_models/effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Resultados/Metodologia,
ainda placeholder).

### Curva de redução de esforço sob um fundo só de floresta: verificação de robustez {#curva-fundo-so-floresta}

*2026-11-07, decisão minha (investigar), não confirmada pelo
orientador. Motivado pela pergunta da Íris "não devíamos ter melhores
resultados com os dados de especialistas? não pode ser um erro?" sobre
o Random Forest já quase no teto (Boyce ≈0,99) a 0% de especialistas.*

**O que decidi:** antes de aceitar "nenhuma quantidade parcial de
dados de especialistas traz ganho visível" como resultado, verifiquei
se é um erro/efeito artificial, não só tranquilizar com explicações.
Quatro verificações, por esta ordem:
1. Revisão de código de `continuous_boyce()` em `src/evaluation.py` —
   sem erro (correlação de Spearman entre janela móvel e razão
   presença/fundo, como em Hirzel et al., 2006).
2. Composição de uso do solo (COS 2023) do fundo partilhado (2 000
   pontos) vs. presenças de ciência cidadã: fundo ~29% não-floresta
   (estradas, agricultura, água) vs. só ~8% nas presenças — desequilíbrio
   real, mas…
3. … reavaliação controlada do Random Forest (0% especialistas, mesmos
   blocos/sementes) contra o fundo completo vs. um subconjunto do
   mesmo fundo restrito a tipos de floresta: ROC-AUC 0,842→0,796, Boyce
   0,989→0,980 — a maior parte da separabilidade sobrevive, não é
   sobretudo um artefacto de composição.
4. Verificação de fuga de dados (`scipy.spatial.cKDTree`): distância
   mínima fundo→presença mais próxima de ciência cidadã = 54,06 m,
   acima da zona-tampão de exclusão de 50 m — zero violações.

Como o passo 3 só tinha testado o ponto 0% isolado, repeti a **curva
completa de 11 pontos** (0–100%) contra um fundo novo, construído de
propósito:
[`forest_only_background_check.ipynb`](../notebooks/07_foundation_models/forest_only_background_check.ipynb)
reconstrói o fundo partilhado (mesma amostragem aleatória uniforme +
zona-tampão de 50 m) acrescentando um filtro de uso do solo COS 2023:
só pontos em eucaliptal, pinhal, "outra floresta" ou matos contam;
excluídos: artificial, agricultura, água/solo nu, **e a classe COS
"floresta de acácias"** (incluir esta como "não-acácia" seria uma
contradição de rótulo, não um teste mais difícil). N = 2 000, igual ao
fundo original, para a comparação ser limpa.

**Resultado:** a conclusão da curva mantém-se — e para o Random Forest
até melhora, não piora, sob o fundo mais difícil.
- **Random Forest:** ROC-AUC sobe em todos os níveis sob o fundo só de
  floresta (0,879→0,934 a 0%; 0,878→0,933 a 90%), curva continua plana
  do 0% ao 90% nos dois fundos. Boyce mantém-se ~0,98–0,99 nos dois. A
  100% (só especialistas no treino), ROC-AUC também sobe (0,801→0,885)
  e Boyce cai pouco (0,917→0,905). **Restringir o fundo a tipos de
  floresta ecologicamente equivalentes não expõe nenhuma fraqueza
  escondida.**
- **Logistic Regression:** mesmo padrão geral, com uma exceção: a 100%
  o Boyce desaba de 0,897 (fundo completo) para 0,567 (só floresta),
  apesar do ROC-AUC continuar a melhorar (0,822→0,870) — fica assinalado
  como nota, não como parte da conclusão principal.
- **One-Class SVM é muito diferente:** ROC-AUC cai para perto do acaso
  a níveis baixos (0,515 a 0%, era 0,574) e o Boyce fica **negativo** a
  0% (-0,039, era 0,628) — sem o fundo "fácil" (não-floresta), o
  classificador one-class deixa de conseguir distinguir acácia de
  outra floresta de forma consistente. Isto sugere fortemente que o
  desempenho moderado deste método ao longo da curva (ROC-AUC
  0,57–0,77) vinha, em boa parte, de reconhecer "isto claramente não é
  vegetação" em vez de aprender algo específico da acácia — risco já
  esperado de um método sem supervisão negativa. A melhoria monótona
  com mais especialistas mantém-se (0,515→0,754, 0% a 100%), mas a
  partir de um nível muito mais baixo.

**Resposta à pergunta da Íris:** não é um erro. As quatro verificações
mais esta repetição completa da curva confirmam que o resultado quase
no teto do Random Forest/Logistic Regression, e a ausência de ganho
visível com dados parciais de especialistas, não são artefacto de um
fundo fácil — sobrevivem (e no Random Forest até melhoram) sob um
fundo muito mais difícil e ecologicamente equivalente. A única
atualização real: a competitividade parcial do One-Class SVM ao longo
da curva parece ter sido, em grande parte, um artefacto da composição
do fundo, específico a esse método — não toca o classificador
presença-vs-fundo proposto por omissão para a RQ1.

**Fundamentação:** raciocínio meu a partir dos números desta
experiência; nenhuma literatura nova consultada para este passo
específico (a distinção presença-vs-fundo com fundo estratificado por
uso do solo segue a prática geral de background sampling de Phillips
et al., já citada noutras entradas, mas não há uma fonte específica
lida para "restringir o fundo à classe de habitat alvo" nesta tese).

**Em aberto:**
- Agrupamento dos códigos COS em "tipo floresta" é escolha minha, não
  confirmada pelo orientador.
- Fundo só de floresta continua com N = 2 000, igualado ao fundo
  original por tamanho, não otimizado/alargado de forma independente.
- Queda de Boyce da Logistic Regression a 100% não foi investigada
  mais a fundo.
- Esta verificação não substitui o fundo partilhado
  ([data/README.md](../data/README.md#tessera-embeddings--rq1-background-pool-2026-11-06)),
  ainda por confirmar com o orientador — só testa a conclusão da curva
  contra uma alternativa mais difícil.

**Onde:** [`notebooks/07_foundation_models/forest_only_background_check.ipynb`](../notebooks/07_foundation_models/forest_only_background_check.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Resultados/Metodologia,
ainda placeholder).

### Redundância dentro dos polígonos de especialistas: diagnóstico

*2026-11-07, decisão minha (investigar), não confirmada pelo
orientador. Seguimento da pergunta "o trabalho dos especialistas foi
inútil? estaremos a perder alguma coisa?" — ver também
[[curva-fundo-so-floresta]]. Descartadas, por agora: revisitar o
multiclasse (reabriria uma decisão já fechada) e a RQ3 (fica para
depois da entrega intermédia); descartada também a hipótese de
correção de falsos positivos (exigiria repor os `classifica = 0`,
já removidos por decisão anterior — ver
[Expert reference polygons](../data/README.md#expert-reference-polygons-cleaned-derived)).*

**O que decidi:** testar se a curva plana (0–90% sem ganho visível)
vem de redundância dentro dos polígonos de especialistas — a mistura é
por polígono, mas o treino continua a usar todos os píxeis de cada
polígono incluído, e píxeis do mesmo polígono podem ser quase
idênticos no espaço de embeddings (mesma mancha, mesmo ano). Três
verificações, sem re-treinar nenhum classificador:
1. Distribuição de píxeis por polígono.
2. Decomposição de variância entre/dentro de polígono (estilo ANOVA)
   com teste de permutação (baralhar que píxel pertence a que
   polígono, mantendo os tamanhos dos grupos, 200 repetições) — para
   separar "homogeneidade real da identidade do polígono" de
   "homogeneidade geral da espécie".
3. Similaridade de cosseno média, dentro do mesmo polígono vs. entre
   polígonos diferentes vs. entre presenças de ciência cidadã (como
   referência de observações genuinamente distintas).

**Resultado:** redundância real e estatisticamente forte, mas os
polígonos são pequenos demais, neste recorte, para isso explicar
sozinho a curva plana.
- Tamanho dos polígonos: mediana 1 píxel, média 1,9, **máximo 9
  píxeis** — não há polígonos grandes a dominar o treino; mesmo assim,
  63,8% dos píxeis vêm de polígonos com 2+ píxeis.
- ICC = 0,881 (fração da variância total explicada pela identidade do
  polígono), muito acima do nulo por permutação (média 0,525, 95º
  percentil 0,538) — acima de 100% das 200 permutações. Confirma
  redundância real da identidade do polígono, não só homogeneidade
  geral da espécie.
- Similaridade de cosseno: dentro do mesmo polígono 0,921 › entre
  polígonos diferentes 0,778 › entre presenças de ciência cidadã
  0,613. **O achado mais inesperado:** mesmo *entre* polígonos
  diferentes (ignorando a redundância interna), os dados de
  especialistas são mais homogéneos entre si (0,778) do que a ciência
  cidadã é entre si (0,613) — os dados de especialistas cobrem, aqui,
  uma gama mais estreita de condições do que a ciência cidadã já
  cobre, possivelmente por estarem concentrados num habitat/zona mais
  homogéneo do distrito-piloto.

**Resposta provisória:** a redundância dentro do polígono existe e é
estatisticamente real, mas como os polígonos são pequenos (máximo 9
píxeis) o efeito prático sobre o tamanho "efetivo" do conjunto de
treino é modesto (no máximo ~1 457 unidades efetivas em vez de 2 771
píxeis, não uma redução drástica) — não parece suficiente para
explicar sozinho a curva plana. A baixa diversidade *entre* polígonos
pode ser tão ou mais relevante, mas fica como achado novo, não
investigado mais a fundo aqui.

**Fundamentação:** decomposição de variância entre/dentro de grupo
(ANOVA de um fator) e teste de permutação são técnicas estatísticas
padrão; não verifiquei uma citação específica para a sua aplicação a
embeddings de sensoriamento remoto agrupados por polígono — raciocínio
meu a partir dos números desta experiência.

**Em aberto:**
- ~~Porque é que os polígonos de especialistas são, como grupo, menos
  diversos entre si do que a ciência cidadã — pode ser cobertura
  geográfica concentrada, não falta de valor dos dados.~~ Resolvido —
  ver "Por que os polígonos de especialistas são menos diversos entre
  si: é habitat, não geografia", abaixo.
- Só testado no recorte-piloto (distrito de Coimbra); pode não
  generalizar a um conjunto maior/mais disperso de polígonos.
- Resultado ainda não confirmado pelo orientador.

**Onde:** [`notebooks/07_foundation_models/expert_polygon_redundancy_check.ipynb`](../notebooks/07_foundation_models/expert_polygon_redundancy_check.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Resultados/Metodologia,
ainda placeholder).

### Por que os polígonos de especialistas são menos diversos entre si: é habitat, não geografia

*2026-11-07, decisão minha (investigar), não confirmada pelo
orientador. Segue diretamente do achado em aberto do diagnóstico
anterior — ver acima.*

**O que decidi:** testar as duas explicações possíveis para os
polígonos de especialistas serem mais homogéneos entre si (cosseno
0,778) do que a ciência cidadã é entre si (0,613): (1) concentração
geográfica — cobrem uma área mais pequena; (2) concentração de
habitat — caem sistematicamente num tipo de paisagem mais estreito.
Teste direto: recalcular a similaridade da ciência cidadã **restrita
só aos blocos de 10 km onde há especialistas**; se subir para perto de
0,778, é geografia; se ficar perto de 0,613, é habitat.

**Resultado — é habitat, não geografia:**
- Ciência cidadã restrita aos 18 blocos com especialistas: similaridade
  0,618 — praticamente igual ao valor no distrito inteiro (0,614), bem
  longe dos 0,778 dos especialistas. Estar na mesma área não torna a
  ciência cidadã tão homogénea quanto os especialistas.
- Composição de uso do solo (COS 2023): **55,0% dos píxeis de
  especialistas caem dentro de polígonos já classificados pela própria
  COS como "floresta de acácias"**, contra só 18,1% da ciência cidadã.
  A ciência cidadã espalha-se por pinhal (32,6%), eucaliptal (20,4%),
  matos (8,5%), artificial (4,7%) e água (0,5%) — contextos quase
  ausentes do lado dos especialistas (0,3% e 0,0% nos dois últimos).
- Mapa: os especialistas formam alguns focos bem separados entre si
  (daí a distância média entre pares ser *maior*, 18,4 km vs. 10,9 km
  da ciência cidadã, apesar de cobrirem só 18 blocos contra 42) — não
  uma zona pequena e concentrada, mas sim poucos locais, cada um muito
  homogéneo internamente. A ciência cidadã cobre uma faixa contígua
  bem mais ampla, incluindo uma região a noroeste do distrito sem
  nenhuma presença de especialista.

**Leitura:** os especialistas documentaram sobretudo manchas de acácia
grandes e já reconhecíveis (sobrepostas à própria classe de uso do
solo "acácia" da COS), enquanto a ciência cidadã já cobre esse mesmo
tipo de contexto *e também* ocorrências mais marginais e variadas
(árvores isoladas, orlas, perto de estradas). Isto explica a curva
plana melhor do que a redundância de píxeis
([[curva-fundo-so-floresta]]): não é que os dados de especialistas não
tenham valor — é que, **como foram amostrados neste piloto**, não
preenchem uma lacuna de diversidade que a ciência cidadã já não cubra.
Resposta à pergunta "o trabalho deles foi inútil?": não — é a prova de
que a ciência cidadã já tem boa cobertura do tipo de habitat que os
especialistas também visaram; não diz nada sobre o valor dos
especialistas para outros tipos de habitat, por delimitação de área, ou
como validação externa. A sobreposição de 55% com a classe "floresta
de acácias" da própria COS é coincidência ecológica — os dados de
especialistas são completamente independentes da COS (confirmado por
mim, 2026-11-07); não é um indício de circularidade entre as duas
fontes.

**Fundamentação:** raciocínio meu a partir dos números desta
experiência; nenhuma literatura nova consultada.

**Em aberto:**
- Achado específico do recorte-piloto; não se sabe se um conjunto de
  especialistas mais disperso (p. ex. cobrindo também a faixa noroeste
  só com ciência cidadã) mudaria a conclusão da curva — implicação
  prática para uma eventual recolha futura: visar habitats/locais
  subrepresentados, não só mais do mesmo tipo.
- Resultado ainda não confirmado pelo orientador.

**Onde:** [`notebooks/07_foundation_models/expert_polygon_geographic_diversity.ipynb`](../notebooks/07_foundation_models/expert_polygon_geographic_diversity.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Resultados/Metodologia,
ainda placeholder).

### Pureza dos rótulos da ciência cidadã: não é a explicação para a curva plana

*2026-11-07, decisão minha (investigar), não confirmada pelo
orientador.*

**O que decidi:** testar se o píxel de 10 m de um ponto do iNaturalist
costuma não estar realmente dominado por *A. dealbata* (erro de GPS,
árvore isolada no meio de outra vegetação) — se isso for frequente,
contamina todos os resultados da ciência cidadã na RQ1, incluindo a
curva plana. Dois testes baratos: (1) onde um ponto cai perto de um
polígono de especialista (verdade de campo independente), que fração
está de facto dentro; (2) em que medida cada presença fica isolada no
espaço de embeddings TESSERA face às outras.

**Resultado:**
- **Teste 1 (verdade de campo, cobertura limitada):** só 21 das 2 995
  presenças (0,7%) caem mesmo dentro de um polígono de especialista;
  alargando a 100 m, chegam a 298, das quais só 7,0% estão de facto
  dentro. Inconclusivo por si só — os polígonos são manchas/segmentos
  específicos, muitos pequenos (≤100 m²), por isso um ponto a 20–80 m
  pode descrever a mesma ocorrência sem ser erro de GPS; e só cobre 10%
  das presenças, nada diz sobre o resto.
- **Teste 2 (distância média às 10 presenças mais próximas em
  embeddings, cosseno):** validado pelo teste 1 — as 21 presenças
  confirmadas dentro de um polígono têm distância mediana bem menor
  (0,053) do que o resto (0,090), e nenhuma delas é sinalizada como
  "outlier" (esperado ao acaso: 5%). As 5% mais isoladas (150
  presenças) não se distinguem por precisão de GPS, mas sim por
  observador: 48% são de observadores não-dominantes, contra só 9,7%
  no resto (~5× mais representados).
- **Importa?** Repetindo o classificador presença-vs-fundo (Random
  Forest, mesmos blocos espaciais, 5 sementes) sem as 150 presenças
  mais isoladas: ROC-AUC 0,842 → 0,843, Boyce 0,992 → 0,995 —
  praticamente inalterado.

**Leitura:** nenhum dos dois testes encontra um problema de pureza em
larga escala. O teste de embeddings identifica um grupo plausível e
modesto de presenças atípicas (concentradas em observadores
ocasionais), mas excluí-las não muda o resultado da ciência cidadã
sozinha. **A pureza dos rótulos não explica a curva plana** — resultado
que complementa, não substitui, o achado de concentração de habitat em
[[por-que-os-polígonos-de-especialistas-são-menos-diversos-entre-si-é-habitat-não-geografia]]
(esse explica por que o lado dos especialistas não acrescenta; este
descarta que o lado da ciência cidadã esteja simplesmente "sujo").

**Fundamentação:** raciocínio meu; nenhuma literatura nova consultada.

**Em aberto:**
- O teste 1 só valida 10% das presenças; nada diz sobre o resto.
- O teste 2 é um proxy (distância em embeddings), não verdade de
  campo — uma mancha legítima mas atípica (pequena, no limite da área
  de distribuição) também pontuaria como "outlier"; ninguém verificou
  visualmente os pontos sinalizados contra ortofoto.
- Resultado ainda não confirmado pelo orientador.

**Onde:** [`notebooks/07_foundation_models/label_purity_check.ipynb`](../notebooks/07_foundation_models/label_purity_check.ipynb).

**Na tese:** ⏳ Ainda não escrita (capítulo de Resultados/Metodologia,
ainda placeholder).

### Discrepância de 15 vs. 18 blocos espaciais no lado dos especialistas: é o sistema de coordenadas, não um bug

*2026-11-07, decisão minha (investigar), não confirmada pelo
orientador.*

**O que decidi:** verificar se a diferença entre os "15 blocos"
reportados em `expert_polygons.ipynb` e os "18 blocos" usados em
`expert_arm_classifiers.ipynb` era só um detalhe de definição (extensão
do distrito vs. extensão do piloto) ou um bug real na divisão
treino/teste, que contaminaria tudo o que depende dela.

**Resultado — é só o sistema de coordenadas:** decompondo a diferença
em três efeitos possíveis, com os mesmos 1 849 polígonos do distrito
em todos os casos:
- **Extensão** (todos os polígonos `classifica = 1` do piloto vs. só os
  do distrito): sem efeito nenhum — os conjuntos de blocos são
  idênticos.
- **Unidade** (píxel a píxel vs. centróide do polígono), mantendo o
  mesmo CRS: sem efeito nenhum.
- **Sistema de coordenadas** (EPSG:3763, usado em `expert_polygons.ipynb`,
  vs. EPSG:32629/UTM 29N, usado em todo o resto do pipeline): isto
  sozinho explica os 15 → 18. Uma grelha de 10 km desenhada numa
  projeção não coincide com uma grelha de 10 km desenhada noutra —
  nenhum polígono muda de sítio, só a contagem de blocos.

**Sem bug na divisão treino/teste:** todos os notebooks que de facto
fazem uma divisão espacial (`one_class_method_selection.ipynb`,
`presence_background_citizen_science.ipynb`,
`expert_arm_classifiers.ipynb`, `effort_reduction_curve.ipynb`,
`forest_only_background_check.ipynb`) trabalham sempre em EPSG:32629,
via `src.embeddings.block_id`/`load_pilot_embeddings` — a mesma grelha
do início ao fim. O "15" foi uma contagem avulsa e só descritiva, feita
em `expert_polygons.ipynb` antes de existir este pipeline por píxel,
numa projeção diferente (EPSG:3763, usada ali só para o trabalho de GIS
e COS) — nunca foi usado para parametrizar nenhuma divisão real.
**O número correto para raciocinar sobre a escassez de blocos do lado
dos especialistas é 18**, coerente com os 42 (ciência cidadã) e 85
(fundo) usados no resto da RQ1, já que os três vêm da mesma função
`block_id` na mesma projeção.

**Correção:** a entrada "[[classificador-presença-vs-fundo-ciência-cidadã-random-forest-por-agora]]"
citava "15 blocos" como parte da razão para preferir o Random Forest
pela estabilidade — devia ler 18; a conclusão (Random Forest) não muda,
18 continua a ser poucos blocos independentes.

**Fundamentação:** raciocínio meu; nenhuma literatura nova consultada.

**Onde:** [`notebooks/07_foundation_models/expert_arm_classifiers.ipynb`](../notebooks/07_foundation_models/expert_arm_classifiers.ipynb)
(secção "Reconciling the '15' vs. '18' block counts").

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder).

### Sentinel-2 na RQ1: avançar já, por extração em pontos, não raster completo

*2026-11-07, decisão minha, não confirmada pelo orientador.*

**O que decidi:** deixar de adiar o braço Sentinel-2 da RQ1. A fase 1
"só TESSERA" (decisão do orientador, 2026-11-05, presencial) era um
faseamento ("primeiro TESSERA, depois Sentinel-2"), não um corte de
âmbito — confirmado em conversa. Como todas as experiências da RQ1
feitas até agora treinam e avaliam em pontos individuais (presenças,
píxeis de especialistas, fundo aleatório), não há necessidade de
descarregar um raster Sentinel-2 completo sobre a extensão toda do
piloto (~100 km × 66 km a 10 m, com 10 bandas × 61 cenas — provavelmente
dezenas a mais de 100 GB): basta extrair as mesmas bandas Sentinel-2
nos mesmos pontos já usados para a TESSERA. Isto reduz o custo em
ordens de grandeza e não perde nada do que a curva precisa agora.

**Porquê:** a pergunta da RQ1, tal como está escrita, é comparativa
("em que medida os foundation models melhoram sobre features
convencionais") — sem o braço Sentinel-2, essa metade fica por
responder. Com o faseamento esclarecido como temporário, não há razão
para continuar a adiar, sobretudo por extração em pontos ser barata.

**Em aberto, antes de implementar:** o conjunto de features
(bandas, índices, composição temporal/sazonal) continua por decidir
— `docs/methodology.md` já marca isto como aberto, fundamentado só em
Ball et al. (2026) e Domingo et al. (2023), ambos ainda por ler na
íntegra (`docs/literature.md`). Não inventar isto sem ler esses
artigos primeiro.

**Fundamentação:** raciocínio meu sobre o custo; a necessidade do
braço Sentinel-2 em si já estava fundamentada em Mouta et al. (2021) e
Domingo et al. (2023) (ver `docs/methodology.md`).

**Onde:** ainda sem notebook — a construir depois de decidido o
conjunto de features.

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder).

### Conjunto de features do Sentinel-2 na RQ1: compósito anual (Ball et al.), fenologia da floração como extensão por ablação (Domingo et al.)

*2026-11-07, proposta minha, aceite em conversa — não confirmada pelo
orientador.*

**O que decidi:** a primeira versão do braço Sentinel-2 usa o
compósito anual à Ball et al. (2026) — mediana anual das 12 bandas
(B01–B12/B8A) de 2023 + NDVI, NDWI (McFeeters) e NBR calculados sobre
essa mediana, nos mesmos pontos já usados para a TESSERA, mascarando
nuvens/sombra por SCL (manter classes 4/5/6/7) e QA60 (bits 10/11) com
`CLOUDY_PIXEL_PERCENTAGE < 60`. As features de fenologia da floração à
Domingo et al. (2023) — composições mensais, métricas de diferença
normalizada (RG/GB/BR/NDVI/NIRG/NIRB) e os deltas pré/pós-floração —
ficam para depois, testadas por ablação (adicionadas ao conjunto
anual, não substituindo-o), seguindo o mesmo padrão cumulativo já
usado no resto da pipeline da RQ1.

**Porquê:** o compósito anual de Ball et al. é o candidato mais
simples e mais barato de implementar primeiro, e não é específico de
espécie — serve como baseline convencional genérico. O conjunto de
Domingo et al., em contraste, foi desenhado especificamente para
*Acacia dealbata* e depende de uma janela de floração encontrada
empiricamente na Galiza (floração em março); aplicá-lo diretamente ao
piloto de Coimbra sem verificar se essa janela se mantém seria inventar
um facto não confirmado. Testar por ablação evita essa escolha prévia:
se o sinal de floração ajudar, aparece na comparação; se a janela
galega não servir para Portugal central, o conjunto anual continua de
pé como baseline.

**Em aberto:** a janela de floração (jan/mar/mai, de Domingo et al.)
pode não se aplicar a Portugal central sem confirmação — ou redescobrir
empiricamente nos próprios dados do piloto, ou tratar como suposição
não verificada se usada sem mais verificação. Também em aberto: se
este conjunto é "o" baseline reportado também em Ball et al. (2026) — o
artigo tem também a variante sazonal (ver `literature.md`), mas qual
delas é a reportada nos números principais do artigo não foi
confirmado (artigo pago, lido só pelo código-fonte dos autores).

**Fundamentação:** Ball et al. (2026) (código-fonte dos autores,
`PatBall1/trentino-trees`, `s1s2annual.js`) e Domingo et al. (2023)
(texto integral, cópia de acesso aberto via repositório da Universidade
de Saragoça) — ver `docs/literature.md` para o resumo de cada um.

**Onde:** ainda sem notebook — este desenho ainda não foi implementado.

**Na tese:** ⏳ Ainda não escrita (capítulo de Metodologia, ainda
placeholder).
