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
por inteiro — a confirmar antes de citar na tese):
- **MaxEnt já está na bibliografia da tese, noutro papel:** Phillips,
  Anderson & Schapire (2009) — já citado para o *target-group
  background* (ver "Outras plantas como classes, não como ausências")
  — é também o método de referência para modelação de distribuição de
  espécies só com presenças (one-class/presence-only). Pode ser a
  "abordagem" a que o orientador se referiu sem a nomear.
- Li & Guo (2010), "A maximum entropy approach to one-class
  classification of remote sensing imagery", *International Journal of
  Remote Sensing* (doi: 10.1080/01431161003702245) — aplica MaxEnt como
  classificador one-class a imagens de satélite, com melhor exatidão
  que a one-class SVM.
- Rapinel & Hubert-Moy (2021), "One-Class Classification of Natural
  Vegetation Using Remote Sensing: A Review", *Remote Sensing*
  13(10):1892 (doi: 10.3390/rs13101892) — revisão dos métodos OCC para
  vegetação, todos dispensam dados de ausência. **Correção
  (2026-11-06):** esta entrada tinha o nome errado dos autores ("Zhao
  & Zhong"); confirmado via pesquisa (DOAJ, OpenAlex, dblp) que são
  Sébastien Rapinel e Laurence Hubert-Moy.
- Skowronek, Asner & Feilhauer (2017), comparação de Maxent, SVM
  enviesada (biased SVM) e BRT para duas invasoras com espectroscopia
  aérea (não satélite): Maxent e BRT ligeiramente melhores que a SVM
  enviesada.
- Li et al. (2011, IEEE TGRS) — método fundador de PU learning
  (positive-unlabeled) para classificação one-class em deteção remota.
- Artigo de 2025 em *Remote Sensing* (doi: 10.3390/rs17061041) —
  PU learning adversarial para mapear *Pedicularis kansuensis*
  (invasora) com Jilin-1 e **Sentinel-2**: o caso mais próximo do meu
  (invasora + Sentinel-2 + one-class/PU).
- **Contraponto a considerar:** um estudo sobre *Solidago* (vara-de-
  ouro) com Sentinel-2 multitemporal encontrou Random Forest sempre
  melhor que One-Class SVM (1–15 pontos percentuais, F1 0,98 para o
  RF) — não é garantido que one-class supere o multiclasse/binário já
  em curso.

Nenhum destes é sobre *Acacia* nem sobre dados de ciência cidadã; são
pistas para ler, não conclusões. Antes de decidir, falta: ler os
artigos (começar por Phillips et al. 2009, que já tenho, e o de 2025
com Sentinel-2), e perceber se o orientador tinha um método específico
em mente.

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
- Níveis exatos de mistura da curva (p. ex. 10%, 20%, …) e como manter
  um bloco espacial de teste fixo em todos os pontos da curva, dado
  que o observador dominante e os especialistas visitaram zonas
  sobrepostas. Proposta em discussão, não confirmada: reutilizar os 15
  blocos de 10 km já definidos para os polígonos de especialistas,
  escolhendo o conjunto de teste para não ficar só em zona densa de um
  dos lados (ciência cidadã ou especialistas). A comparação acima já
  mostra que reutilizar a grelha de 10 km dos embeddings do piloto
  funciona tecnicamente (85 blocos nessa extensão maior).
- **Confirmar com o orientador o desenho do fundo partilhado** (ponto
  8 acima): 2000 pontos aleatórios uniformes, zona-tampão de 50 m —
  tanto o N como o raio da zona-tampão são escolha minha, sem valor
  específico encontrado na literatura para o raio.
- A RQ3 tinha como candidata "outras plantas como classes vs. fundo ao
  acaso"; sem classes próprias, isto passa a "fundo de outras plantas
  vs. fundo ao acaso" — por rever.

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

### Primeira entrega: relatório intermédio, início de dezembro de 2026

*2026-11-06, informação dada pela Íris (facto do calendário da tese,
não uma decisão de desenho).*

**O que sei:** a minha primeira entrega da tese é um relatório
intermédio (marco a meio do trabalho), a entregar no início de
dezembro de 2026 — não a tese final. Isto está em linha com o género
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

**Decidido (2026-11-06):** a entrega de dezembro **não** vai seguir a
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
de dezembro, para que o capítulo de Resultados apresente a RQ1
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
- Prazo exato de início de dezembro — só foi dito "início de dezembro
  de 2026", sem data exata.

**Onde:** sem notebook/figura própria; afeta diretamente
`thesis/document/text/` e
[`thesis/guidance_example/1768249601_Entrega_intermedia-1.pdf`](guidance_example/1768249601_Entrega_intermedia-1.pdf)
como referência de género.

**Na tese:** ⏳ Ainda não escrita — é a própria entrega que está em
causa; o mapeamento de capítulos fica para quando as experiências da
RQ1 estiverem mais avançadas.
