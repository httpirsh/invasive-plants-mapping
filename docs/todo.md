# To do

> Só tarefas confirmadas e importantes — não perguntas em aberto para
> uma reunião (essas ficam só nas [reuniões](meetings/)) nem ideias
> por decidir. Cada tarefa com a origem; os detalhes ficam nas
> reuniões, as decisões em [`thesis/notes.md`](../thesis/notes.md#decisões).
> Marcar com `[x]` e limpar as feitas de vez em quando.

## Agora

- [ ] **Âmbito do relatório de janeiro fechado:** RQ1 (só TESSERA,
  ambos os braços) como resultado preliminar; Sentinel-2 declarado
  como risco/plano de trabalho, não resultado em falta; RQ2 e RQ3 só
  no plano de trabalho, sem novas experiências antes da entrega;
  máscara de segmentação apresentada como comparação em curso
  (decisão de âmbito, acordada em conversa, 2026-11-10)
- [ ] **Entrega de início de janeiro de 2027 é um relatório intermédio,
  não a tese final (confirmado)** — data corrigida de dezembro de 2026;
  `thesis/document/text/` não vai manter a forma de tese
  final para essa entrega; mapeamento exato dos capítulos ainda por
  decidir, para quando as experiências da RQ1 estiverem mais avançadas
  nos dois braços
  ([thesis/notes.md](../thesis/notes.md#primeira-entrega-relatório-intermédio-início-de-janeiro-de-2027))
- [ ] Ler Phillips et al. (2009) e o artigo de 2025 sobre PU learning
  com Sentinel-2 (pistas da pesquisa sobre baselines one-class)
- [ ] **Máscara de segmentação, só para janeiro** (ponto central;
  [reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem)):
  apresentar as três candidatas identificadas e fundamentadas na
  literatura (ver
  [`docs/literature.md`](literature.md#weak-supervision-from-point-labels)),
  comparação planeada — sem escolher regra nem correr mais nada agora
  (decisão de âmbito, acordada em conversa, 2026-11-10).
  - [x] Candidata do crescimento de região nos embeddings TESSERA —
    testada na amostra de 30 (parâmetros por omissão, não calibrados:
    similaridade por cosseno ao pixel-semente, 8 vizinhos, raio máximo
    20 px/200 m, limiar 0,90). Resultado: 1/15/758 píxeis (min/mediana/
    máx) — a cauda superior (758, bate no limite do raio) sugere limiar
    permissivo demais nalguns casos
    ([thesis/notes.md](../thesis/notes.md#máscara-de-segmentação-sem-a-direção-da-câmara-testar-várias-abordagens),
    [notebook](../notebooks/05_data_integration/segmentation_mask.ipynb))
  - [x] Candidata dos superpíxeis (SLIC sobre as patches de embeddings
    TESSERA, ideia de Rivier et al., não o método completo deles) —
    testada na mesma amostra de 30; `scikit-image` agora é dependência
    (`requirements.txt`). Resultado: 11/21/45 píxeis — mais consistente,
    mas só porque `n_segments` limita o tamanho máximo por construção,
    não por ser mais exata. Propagação por voto maioritário (a proposta
    real de Rivier et al.) ainda não foi exercitada — esta amostra tem
    um ponto por patch
    ([notebook](../notebooks/05_data_integration/segmentation_mask.ipynb))
- [x] **Pureza dos rótulos da ciência cidadã** — verificado; sem
  problema em larga escala, excluir as presenças mais isoladas em
  embeddings não muda o resultado (ROC-AUC 0,842→0,843, Boyce
  0,992→0,995)
  ([thesis/notes.md](../thesis/notes.md#pureza-dos-rótulos-da-ciência-cidadã-não-é-a-explicação-para-a-curva-plana))
- [x] **Discrepância de 15 vs. 18 blocos espaciais (especialistas)** —
  resolvida; é o sistema de coordenadas, não um bug na divisão
  treino/teste; 18 é o número correto
  ([thesis/notes.md](../thesis/notes.md#discrepância-de-15-vs-18-blocos-espaciais-no-lado-dos-especialistas-é-o-sistema-de-coordenadas-não-um-bug))
- [x] Ler Ball et al. (2026) e Domingo et al. (2023) na íntegra —
  métodos exatos confirmados em [literature.md](literature.md); conjunto
  de features decidido para quando o braço Sentinel-2 for retomado
  (compósito anual à Ball et al., fenologia da floração à Domingo et
  al. testada depois por ablação) — Sentinel-2 está de novo em espera
  ([thesis/notes.md](../thesis/notes.md#conjunto-de-features-do-sentinel-2-na-rq1-compósito-anual-ball-et-al-fenologia-da-floração-como-extensão-por-ablação-domingo-et-al))
- [ ] Rever a estrutura de cada capítulo de `thesis/document/text/`
  face ao relatório de referência, à medida que for escrito/revisto
  (não reescrever o que já existe de uma vez)
  ([thesis/notes.md](../thesis/notes.md#estrutura-do-documento-seguir-um-relatório-de-referência-de-outro-aluno-onde-for-aplicável))

## A fazer só após a defesa intermédia

- [ ] Retomar o braço Sentinel-2 da RQ1 — posto em espera outra vez
  por custo de extração mais alto do que esperado, em vez
  de feito agora. Só Random Forest/Logistic Regression — one-class SVM
  descartado como candidata; os quatro diagnósticos de robustez só se
  o resultado parecer inesperado, não por omissão
  ([thesis/notes.md](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo),
  [thesis/notes.md](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo))
- [ ] Ablação cumulativa do pipeline de referência (recorrer a curva
  depois de cada um dos 10 passos de limpeza) — não começada, adiada
  de propósito para depois de janeiro (decisão de âmbito, acordada em
  conversa, 2026-11-10)
- [ ] Implementar a zona-tampão de 20–30 m na **validação por divisão
  espacial** (spatial split) do lado dos especialistas, além dos
  blocos de 10 km — unidade assumida por decisão própria, não
  confirmada pelo orientador; para janeiro fica só como limitação
  conhecida no relatório, não corrigida (decisão de âmbito, acordada
  em conversa, 2026-11-10)
  ([thesis/notes.md](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km))
- [ ] Fixar os níveis concretos de retenção do filtro de recência da
  RQ2 a partir das contagens já calculadas (99,4%/85,5%/36,6% a
  desde-2019/2021/2023), agora que a recência é definida como
  distância a 2023 — só quando a RQ2 for retomada
  ([thesis/notes.md](../thesis/notes.md#rq2-recência-distância-a-2023))
- [ ] **Máscara de segmentação, depois de janeiro:** comparar
  visualmente as três candidatas no QGIS
  (`data/interim/spatial/qgis/segmentation_mask_sample.gpkg` já tem as
  camadas `mask_cos`, `mask_tessera`, `mask_superpixels` e
  `sample_points`), escolher uma regra, e comparar as abordagens (com
  e sem, na ablação) — adiado de propósito para depois de janeiro
  (decisão de âmbito, acordada em conversa, 2026-11-10)
- [ ] Validação independente da RQ1 com a classe *Acacia* da COS 2023
  (amostra OrtoSat verificada à mão descartada como candidata, mesmo
  motivo de eficiência do multiclasse abandonado) — não começada,
  adiada para depois de janeiro
  ([docs/research_questions.md](research_questions.md#other-open-points),
  [thesis/notes.md](../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo))
- [ ] Análise de erro sistemática (região, uso do solo, densidade de
  observações, observador, qualidade do registo) — precisa de RQ3 e da
  máscara de segmentação, ambas já adiadas; fica para depois de
  janeiro ([docs/methodology.md](../docs/methodology.md#error-analysis))
- [ ] Mapa final (aplicar o modelo a toda a área de estudo, com
  incerteza) — não começado; é trabalho de tese final, confirmado como
  fora de âmbito para o relatório de janeiro
  ([docs/methodology.md](../docs/methodology.md#final-map))
