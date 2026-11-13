# To do

> Só tarefas confirmadas e importantes. Perguntas para o orientador
> ficam nas [reuniões](meetings/); o raciocínio de cada decisão fica em
> [`thesis/notes.md`](../thesis/notes.md#decisões).

## Agora: relatório intermédio (início de janeiro de 2027)

Âmbito fechado
([thesis/notes.md](../thesis/notes.md#primeira-entrega-relatório-intermédio-início-de-janeiro-de-2027)):
RQ1 (curva de redução de esforço) só com TESSERA como resultado
preliminar; RQ2, RQ3 e RQ4 (Sentinel-2) no plano de trabalho; sem
novas experiências antes da entrega. Numeração das perguntas:
[thesis/notes.md](../thesis/notes.md#renumeracao-perguntas-2026-11-13).

- [ ] Decidir o mapeamento dos capítulos de `thesis/document/text/`
  para a forma de relatório intermédio.
- [ ] Rever a estrutura de cada capítulo face aos relatórios de
  referência, à medida que for escrito
  ([thesis/notes.md](../thesis/notes.md#estrutura-do-documento-seguir-um-relatório-de-referência-de-outro-aluno-onde-for-aplicável)).
- [ ] Máscara de segmentação: apresentar as duas regras,
  fundamentadas na literatura, com a comparação planeada na RQ2
  ([thesis/notes.md](../thesis/notes.md#rq2-proposta-mascara)).
- [ ] Descarregar à mão o artigo publicado de Dimson et al. (2023) e
  ler Ma et al. (2026)
  ([thesis/notes.md](../thesis/notes.md#lista-de-literatura-releitura-integral-e-limpeza)).
- [ ] Corrigir a entrada `zhu2026` no manuscrito: o autor é Stewart et
  al. ([thesis/notes.md](../thesis/notes.md#lista-de-literatura-releitura-integral-e-limpeza)).
- [ ] Levar ao orientador as propostas em fila (máscara de
  segmentação, redesenho da pergunta da concentração espacial,
  formulação das perguntas) e a reformulação em quatro perguntas
  ([próxima reunião](meetings/proxima-reuniao.md);
  [thesis/notes.md](../thesis/notes.md#renumeracao-perguntas-2026-11-13)).

## Depois da defesa intermédia

- [ ] Retomar o braço Sentinel-2 (RQ4: comparação com o TESSERA nos
  dois níveis de dados), depois de decidir como reduzir o custo da
  extração. Só Random Forest e Logistic Regression;
  os diagnósticos de robustez só se o resultado parecer inesperado
  ([thesis/notes.md](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo)).
- [ ] Implementar a zona-tampão na validação espacial do lado dos
  especialistas
  ([thesis/notes.md](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)).
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
