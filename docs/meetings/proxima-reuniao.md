# Próxima Reunião com o Orientador — data por marcar

> Perguntas em aberto que não couberam na reunião de 2026-11-05 (que
> se concentrou no redesenho da RQ1 — ver
> [`2026-11-05.md`](2026-11-05.md#o-que-foi-decidido)) nem foram
> entretanto respondidas por mensagem. Decisões já tomadas ficam em
> [`thesis/notes.md`](../../thesis/notes.md#decisões).

## Por perguntar

- **Regra das herbáceas:** concorda em só contar herbáceas onde são a
  camada de cima nas classes da COS? Já aplicado no pipeline, a
  confirmar (origem:
  [2026-11-05.md](2026-11-05.md#por-perguntar-não-chegou-a-ser-discutido-nesta-reunião)).
- **Uma planta por píxel, fica a mais alta:** concorda? Já aplicado no
  pipeline, a confirmar (mesma origem).
- **Filtro da RQ2:** "mais recentes" quer dizer 2024–2026, ou as mais
  próximas de 2023? (origem:
  [2026-11-04.md](2026-11-04.md#2-outras-perguntas)).
- **invasoras.pt:** se as presenças de ciência cidadã ficarem poucas,
  faz sentido juntar observações dessa plataforma? Quem a gere? (origem:
  [2026-11-04.md](2026-11-04.md#presenças-de-a-dealbata-7-943--3-000),
  passo 4).
- **Segunda região da RQ3 (Covilhã/Fundão):** faz sentido usar a zona
  com 165 polígonos `classifica = 1` e 57 observações *research grade*
  de *A. dealbata* como segunda região? (origem:
  [2026-11-04.md](2026-11-04.md#3-para-informar);
  [`data/README.md`](../../data/README.md#candidate-second-region-for-rq3-found-not-chosen)).
- **Apresentação da Lucie Radová:** faz sentido falar com ela? (origem:
  [2026-11-04.md](2026-11-04.md#3-para-informar)).
- **Máscara de segmentação — "considerar a área de vegetação mais
  próxima":** confirmar se quis dizer estender o rótulo à mancha à
  volta da observação, ou só levar o ponto para dentro da vegetação
  mais próxima. Estou a assumir a primeira leitura para já (origem:
  [thesis/notes.md](../../thesis/notes.md#máscara-de-segmentação-sem-a-direção-da-câmara-testar-várias-abordagens)).

## Também relevante para esta conversa

A RQ3 dependia de "outras plantas como classes vs. fundo ao acaso"
como candidata a experiência; com o multiclasse abandonado (reunião
2026-11-05), isto passa a "fundo de outras plantas vs. fundo ao
acaso" — por rever antes ou durante esta reunião (ver
[research_questions.md](../research_questions.md#rq3--spatial-sampling-bias)).

## Resultados a apresentar: curva de redução de esforço da RQ1

Corrida a curva completa de redução de esforço (0% a 100% de dados de
especialistas sobre a base de ciência cidadã, metodologia fixa em
todos os pontos). Random Forest e Logistic Regression já estão
praticamente no teto só com ciência cidadã (Boyce ≈0,99) e ficam
planos do 0% ao 90% — só pioram a 100%, quando a ciência cidadã é
totalmente substituída. Verificado que não é erro nem artefacto de um
fundo fácil (repetida a curva toda contra um fundo só de tipos de
floresta — o resultado manteve-se, até melhorou no Random Forest).
Explicação encontrada: os polígonos de especialistas, neste piloto,
cobrem sobretudo manchas de acácia já grandes e facilmente
identificáveis (55% caem dentro da própria classe "floresta de
acácias" da COS, apesar de os dados serem completamente independentes
dela), enquanto a ciência cidadã já cobre esse mesmo tipo de caso e
também uma gama muito maior de contextos (pinhal, eucaliptal, matos,
beira de estrada) — não é falta de valor dos dados de especialistas, é
que, como foram amostrados, não preenchem uma lacuna que a ciência
cidadã já não cubra. Detalhe completo em
[thesis/notes.md](../../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)
e notebooks ligados a partir daí.

- **Confirmar:** pode ser efeito de teto específico deste piloto (só
  uma região, só TESSERA, fundo partilhado ainda não confirmado por
  ele) — não uma conclusão definitiva sobre o valor dos dados de
  especialistas em geral.
- **Discutir:** esforço foi medido como % de polígonos, não por área
  nem custo real de campo — rediscutir a unidade.
- **Implicação prática** se houver nova recolha de campo: visar
  habitats/locais ainda não cobertos pela ciência cidadã (p. ex. a
  faixa a noroeste do distrito-piloto) pode valer mais do que mais
  polígonos do mesmo tipo de mancha.
