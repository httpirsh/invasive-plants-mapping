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

**Onde:** [`notebooks/03_expert_reference/expert_polygons_exploration.ipynb`](../notebooks/03_expert_reference/expert_polygons_exploration.ipynb)
(secções 5–11).
