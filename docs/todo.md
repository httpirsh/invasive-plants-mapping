# To do

> Só tarefas confirmadas e importantes. Perguntas para o orientador
> ficam nas [reuniões](meetings/); o raciocínio de cada decisão fica em
> [`thesis/notes.md`](../thesis/notes.md#decisões).

## Agora: relatório intermédio (início de janeiro de 2027)

Âmbito fechado
([thesis/notes.md](../thesis/notes.md#primeira-entrega-relatório-intermédio-início-de-janeiro-de-2027)):
RQ1 (curva de redução de esforço) só com TESSERA como resultado
preliminar; RQ2, RQ3 e RQ4 (Sentinel-2) no plano de trabalho; sem
novas experiências antes da entrega, com exceção da correção da RQ1
abaixo (classificador presence-only). Numeração das perguntas:
[thesis/notes.md](../thesis/notes.md#renumeracao-perguntas-2026-11-13).

- [ ] RQ1: ler Phillips et al. (2006) e Peterson et al. (2008) para
  confirmar a sensitivity a área fixa já usada na seleção de método
  ([thesis/notes.md](../thesis/notes.md#rq1-presence-only)).
- [ ] RQ1: recorrer a curva de redução de esforço e a análise à
  zona-tampão com a regressão logística presença-fundo (`C=10`), em
  leave-one-block-out e com a sensitivity a 10% de área (reescrever
  `experiments/effort_reduction_curve/run.py` e `compare_buffer.py`);
  escrever os números em `docs/research_questions.md`,
  `docs/methodology.md` e no ponto de partida da RQ3
  ([thesis/notes.md](../thesis/notes.md#rq1-presence-only)).
- [ ] Decidir o mapeamento dos capítulos de `thesis/document/text/`
  para a forma de relatório intermédio.
- [ ] Rever a estrutura de cada capítulo face aos relatórios de
  referência, à medida que for escrito
  ([thesis/notes.md](../thesis/notes.md#estrutura-do-documento-seguir-um-relatório-de-referência-de-outro-aluno-onde-for-aplicável)).
- [ ] Máscara de segmentação: apresentar as duas regras,
  fundamentadas na literatura, com a comparação planeada na RQ2
  ([thesis/notes.md](../thesis/notes.md#rq2-proposta-mascara)).
- [ ] Reportar no relatório a análise de sensibilidade da curva da RQ1
  à zona-tampão (300 m e 1 km), ao lado da curva sem tampão
  ([thesis/notes.md](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)).
- [ ] Descarregar à mão o artigo publicado de Dimson et al. (2023)
  ([thesis/notes.md](../thesis/notes.md#lista-de-literatura-releitura-integral-e-limpeza)).
- [ ] Corrigir a entrada `zhu2026` no manuscrito: o autor é Stewart et
  al. ([thesis/notes.md](../thesis/notes.md#lista-de-literatura-releitura-integral-e-limpeza)).
- [ ] Levar ao orientador as propostas em fila (máscara de
  segmentação, redesenho da pergunta da concentração espacial,
  formulação das perguntas) e a reformulação em quatro perguntas
  ([próxima reunião](meetings/2026-11-17.md);
  [thesis/notes.md](../thesis/notes.md#renumeracao-perguntas-2026-11-13)).

## Depois da defesa intermédia

- [ ] Retomar o braço Sentinel-2 (RQ4: comparação com o TESSERA nos
  dois níveis de dados), depois de decidir como reduzir o custo da
  extração. Só a regressão logística presença-fundo (classificador
  da RQ1);
  os diagnósticos de robustez só se o resultado parecer inesperado
  ([thesis/notes.md](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo)).
- [ ] RQ2 (máscara de segmentação): aprovar a extração das janelas
  TESSERA à volta das observações e correr o desenho que o orientador
  confirmar, com a configuração já fixada
  ([thesis/notes.md](../thesis/notes.md#renumeracao-perguntas-2026-11-13)).
- [ ] RQ2 (filtros de grau e de precisão): correr as duas condições,
  com e sem os dois filtros, com todas as observações e só com os
  embeddings já guardados
  ([thesis/notes.md](../thesis/notes.md#renumeracao-perguntas-2026-11-13)).
- [ ] RQ3: contar os polígonos de perto e de longe por semente, correr
  perto contra longe só com TESSERA e fazer o mapa de confiança, no
  desenho que o orientador confirmar
  ([thesis/notes.md](../thesis/notes.md#renumeracao-perguntas-2026-11-13)).
- [ ] Validação independente da curva (RQ1) com a classe *Acacia* da COS 2023
  ([docs/methodology.md](methodology.md#validation)).
- [ ] Análise de erro sistemática; precisa da RQ3 e da máscara de
  segmentação ([docs/methodology.md](methodology.md#error-analysis)).
- [ ] Mapa final da área de estudo, com incerteza
  ([docs/methodology.md](methodology.md#final-map)).

Opcional: ablação cumulativa do pipeline de referência
([docs/research_questions.md](research_questions.md#reference-data-pipeline-proposed)).
