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
