# To do

> Só tarefas confirmadas e importantes — não perguntas em aberto para
> uma reunião (essas ficam só nas [reuniões](meetings/)) nem ideias
> por decidir. Cada tarefa com a origem; os detalhes ficam nas
> reuniões, as decisões em [`thesis/notes.md`](../thesis/notes.md#decisões).
> Marcar com `[x]` e limpar as feitas de vez em quando.

## Agora

- [ ] **Entrega de dezembro de 2026 é um relatório intermédio, não a
  tese final (confirmado)** — `thesis/document/text/` não vai manter a
  forma de tese final para essa entrega; falta decidir o mapeamento
  exato dos capítulos (fica para quando as experiências da RQ1
  estiverem mais avançadas — só o braço de ciência cidadã testado até
  agora)
  ([thesis/notes.md](../thesis/notes.md#primeira-entrega-relatório-intermédio-início-de-dezembro-de-2026))
- [x] Perguntar aos orientadores porquê não usar os `classifica = 0`
  na avaliação — resposta não respondeu diretamente, sugeriu baseline
  one-class em vez disso ([seguimento, reunião 2026-11-04](meetings/2026-11-04.md#pergunta-de-seguimento-sobre-classifica--0-para-avaliação-por-mensagem))
- [x] Pesquisar abordagens one-class / positive-only para o baseline
  do modelo de ciência cidadã — primeira pesquisa feita (só resumos,
  nenhum artigo lido por inteiro; ver pistas em
  [thesis/notes.md](../thesis/notes.md#baseline-do-modelo-de-ciência-cidadã-pode-ser-one-class-pergunta-sobre-os-classifica--0-sem-resposta-direta))
- [ ] Ler Phillips et al. (2009) e o artigo de 2025 sobre PU learning
  com Sentinel-2 (pistas da pesquisa acima)
- [x] Esclarecer com o orientador o que quis dizer com "baseline
  one-class" — resolvido na reunião presencial de 2026-11-05: o
  multiclasse é abandonado nos dois modelos, não só no braço Sentinel-2
  (ver [thesis/notes.md](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo))
- [x] **Reunião (2026-11-05):** aconteceu; só o redesenho da RQ1 foi
  discutido (ver decisão acima) — os restantes itens de
  [docs/meetings/2026-11-05.md](meetings/2026-11-05.md) não chegaram a
  ser abordados e transitaram para
  [docs/meetings/proxima-reuniao.md](meetings/proxima-reuniao.md)
- [x] Escolher o método one-class concreto (one-class SVM vs.
  Isolation Forest) por comparação direta — feito (2026-11-06):
  one-class SVM claramente melhor nas duas métricas (ROC-AUC, índice
  de Boyce), só no braço de ciência cidadã
  ([notebooks/07_foundation_models/one_class_method_selection.ipynb](../notebooks/07_foundation_models/one_class_method_selection.ipynb))
- [x] Construir uma primeira versão do fundo (background) partilhado
  para a RQ1 — feito (2026-11-06): 2000 pontos aleatórios uniformes,
  zona-tampão de 50 m à volta das presenças confirmadas de acácia (não
  pontos estratificados pela COS); **ainda por confirmar com o
  orientador** como desenho final
  ([data/README.md](../data/README.md#tessera-embeddings--rq1-background-pool-2026-11-06))
- [x] Implementar o classificador presença-vs-fundo para o braço de
  ciência cidadã — feito (2026-11-06): Random Forest (ROC-AUC 0.842,
  Boyce 0.989) e Logistic Regression (ROC-AUC 0.878, Boyce 0.973)
  comparados nos mesmos blocos espaciais do one-class; Random Forest
  proposto como classificador por omissão para o resto da RQ1 (minha
  escolha, por agora, não confirmada pelo orientador)
  ([notebooks/07_foundation_models/presence_background_citizen_science.ipynb](../notebooks/07_foundation_models/presence_background_citizen_science.ipynb))
- [x] Implementar os dois classificadores da RQ1 para o **braço de
  especialistas** — feito (2026-11-07): one-class SVM (ROC-AUC 0,911,
  Boyce 0,868) e Random Forest (ROC-AUC 0,990, Boyce 0,954, melhor que
  Logistic Regression no Boyce) confirmam as escolhas feitas no braço
  de ciência cidadã; pontuações bem mais altas aqui, ainda por perceber
  se é tarefa mais fácil ou vantagem real
  ([notebooks/07_foundation_models/expert_arm_classifiers.ipynb](../notebooks/07_foundation_models/expert_arm_classifiers.ipynb))
- [ ] Implementar a zona-tampão de 20–30 m na **validação por divisão
  espacial** (spatial split) do lado dos especialistas, além dos
  blocos de 10 km — unidade assumida por decisão própria (2026-11-06),
  não confirmada pelo orientador
  ([thesis/notes.md](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km))
- [x] Desenhar e implementar a curva de redução de esforço completa da
  RQ1 (0%, 10%, …, 100%) — feito (2026-11-07): mistura por polígono,
  encaixada, bloco de teste espacial fixo por semente em toda a curva.
  **Resultado:** Random Forest e Logistic Regression praticamente
  planos do 0% ao 90%, só pioram a 100% (sem ciência cidadã no treino);
  One-Class SVM melhora de forma monótona com mais especialistas, mas
  fica sempre abaixo dos outros dois. Leitura provisória: nenhuma
  quantidade parcial de dados de especialistas parece justificar o
  custo de recolha, para já — a confirmar com o orientador, pode ser
  efeito de teto
  ([notebooks/07_foundation_models/effort_reduction_curve.ipynb](../notebooks/07_foundation_models/effort_reduction_curve.ipynb))
- [x] Verificar se o resultado "plano" da curva é efeito de teto de um
  fundo fácil — feito (2026-11-07): repetida a curva completa contra um
  fundo só de tipos de floresta (exclui a classe COS de acácia); a
  conclusão mantém-se, Random Forest até melhora sob o fundo mais
  difícil; One-Class SVM piora muito, sugerindo que o seu desempenho
  anterior era em parte artefacto da composição do fundo
  ([notebooks/07_foundation_models/forest_only_background_check.ipynb](../notebooks/07_foundation_models/forest_only_background_check.ipynb))
- [x] Diagnóstico de redundância dentro dos polígonos de especialistas
  — feito (2026-11-07): redundância real e estatisticamente
  forte (ICC 0,881, muito acima do nulo por permutação), mas polígonos
  pequenos (máximo 9 píxeis) limitam o impacto prático; achado novo em
  aberto — polígonos diferentes entre si já são mais homogéneos
  (cosseno 0,778) do que a ciência cidadã é entre si (0,613)
  ([notebooks/07_foundation_models/expert_polygon_redundancy_check.ipynb](../notebooks/07_foundation_models/expert_polygon_redundancy_check.ipynb))
- [x] Explorar porque os polígonos de especialistas são menos diversos
  entre si que a ciência cidadã — feito (2026-11-07): não é geografia
  (ciência cidadã restrita aos mesmos blocos continua tão diversa como
  no distrito inteiro), é habitat — 55% dos píxeis de especialistas
  caem na própria classe "floresta de acácias" da COS, contra só 18%
  na ciência cidadã, que cobre muito mais contextos (pinhal, eucaliptal,
  matos, até estradas). Explica a curva plana melhor do que a
  redundância de píxeis
  ([notebooks/07_foundation_models/expert_polygon_geographic_diversity.ipynb](../notebooks/07_foundation_models/expert_polygon_geographic_diversity.ipynb))
- [ ] Rever o desenho da RQ3 que dependia de "outras plantas como
  classes vs. fundo ao acaso", agora que o multiclasse foi abandonado
  ([research_questions.md](research_questions.md#rq3--spatial-sampling-bias))
- [ ] **Máscara de segmentação** (ponto central; [reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem)):
  - [x] Ler Rivier et al. (2024) e procurar trabalhos do género — feito
    (2026-11-03); nenhum precedente direto para a nossa combinação
    (ver [thesis/notes.md](../thesis/notes.md#máscara-de-segmentação-sem-a-direção-da-câmara-testar-várias-abordagens))
  - [ ] Definir uma regra para a área de vegetação mais próxima de
    cada observação
  - [x] Testar a candidata dos polígonos da COS — feita
    (2026-11-03), numa amostra de 30; só cobre ~13–17% das presenças
    (ver `notebooks/05_data_integration/segmentation_mask.ipynb`)
  - [x] Destravar o acesso aos embeddings TESSERA para Coimbra — feito
    (2026-11-03): a classe `GeoTesseraZarr` (não a `GeoTessera` de
    alto nível) lê a variante `dclimate`, que cobre Portugal, direto
    do Zarr/Icechunk (ver `notebooks/04_satellite/tessera_embeddings.ipynb`)
  - [ ] Candidata do crescimento de região nos embeddings TESSERA —
    testar na amostra de 30, agora que o acesso funciona. Parâmetros
    por omissão propostos (ver
    [thesis/notes.md](../thesis/notes.md#máscara-de-segmentação-sem-a-direção-da-câmara-testar-várias-abordagens)):
    similaridade por cosseno; comparar ao pixel-semente (não à média
    corrente); conectividade a 8 vizinhos; raio máximo balizado pelo
    tamanho real dos polígonos "Florestas de acácias" da COS; limiar
    de similaridade por um percentil da distância real
    presença-vizinho
  - [ ] Candidata dos superpíxeis — usar a mesma patch do TESSERA como
    entrada (ideia de Rivier et al., não o método completo deles —
    ver [thesis/notes.md](../thesis/notes.md#máscara-de-segmentação-sem-a-direção-da-câmara-testar-várias-abordagens));
    precisa de `scikit-image` (ainda não é dependência)
  - [ ] Comparar as abordagens (com e sem, na ablação)
- [x] Testar o download do Sentinel-2 (baseline da RQ1) via Earth
  Search/STAC, alinhado píxel a píxel à grelha da TESSERA — feito
  (2026-11-03), só numa faixa pequena de teste, não a extensão toda
  do piloto (ver [thesis/notes.md](../thesis/notes.md#sentinel-2-bruto-via-earth-search-aws-sem-conta-alinhado-à-grelha-da-tessera))
- [ ] Alargar o download do Sentinel-2 à extensão toda do piloto
  (distrito de Coimbra), com a mesma grelha/abordagem, agora que o
  pipeline está validado
- [x] Ligar o novo projeto Overleaf (acesso dado pelo orientador,
  [reunião 2026-11-04](meetings/2026-11-04.md#2-outras-perguntas)) ao
  repositório — feito (2026-11-04), passos em
  [`README.md`](../README.md#thesis-manuscript-overleaf)
- [x] Atualizar `expert_polygons.ipynb` para tirar os `classifica = 0`
  — feito (2026-11-06): secção 6 passa a só manter `classifica = 1`
  (2 470 polígonos); coluna `use` removida (já não há ausências a
  marcar); `expert_polygons_clean.gpkg` regenerado e o notebook do
  fundo partilhado atualizado para a nova estrutura
  ([data/README.md](../data/README.md#expert-reference-polygons-cleaned-derived))
- [ ] Rever a estrutura de cada capítulo de `thesis/document/text/`
  face ao relatório de referência, à medida que for escrito/revisto
  (não reescrever o que já existe de uma vez)
  ([thesis/notes.md](../thesis/notes.md#estrutura-do-documento-seguir-um-relatório-de-referência-de-outro-aluno-onde-for-aplicável))

## Mais tarde

- [ ] Eucalipto e pinheiros: se o modelo correr mal, recuperar pontos
  com pior precisão da localização ([reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem))
- [ ] Ablação: com e sem os matos debaixo de floresta
