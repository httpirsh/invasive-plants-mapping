# To do

> Só tarefas confirmadas e importantes. Perguntas para o orientador
> ficam nas [reuniões](meetings/); o raciocínio de cada decisão fica em
> [`thesis/notes.md`](../thesis/notes.md#decisões).

## Agora: relatório intermédio (início de janeiro de 2027)

Âmbito fechado
([thesis/notes.md](../thesis/notes.md#primeira-entrega-relatório-intermédio-início-de-janeiro-de-2027)):
RQ1 só com TESSERA como resultado preliminar; Sentinel-2, RQ2 e RQ3 no
plano de trabalho; sem novas experiências antes da entrega.

- [ ] Decidir o mapeamento dos capítulos de `thesis/document/text/`
  para a forma de relatório intermédio.
- [ ] Rever a estrutura de cada capítulo face aos relatórios de
  referência, à medida que for escrito
  ([thesis/notes.md](../thesis/notes.md#estrutura-do-documento-seguir-um-relatório-de-referência-de-outro-aluno-onde-for-aplicável)).
- [ ] Máscara de segmentação: apresentar as duas regras,
  fundamentadas na literatura, com a comparação planeada na RQ2
  ([thesis/notes.md](../thesis/notes.md#rq2-proposta-mascara)).
- [ ] Ler Phillips et al. (2009) na íntegra.
- [ ] Levar ao orientador as três propostas em fila: nova RQ2 (máscara
  de segmentação), redesenho da RQ3 e formulação das perguntas
  ([próxima reunião](meetings/proxima-reuniao.md)).

## Depois da defesa intermédia

- [ ] Retomar o braço Sentinel-2 da RQ1, depois de decidir como
  reduzir o custo da extração. Só Random Forest e Logistic Regression;
  os diagnósticos de robustez só se o resultado parecer inesperado
  ([thesis/notes.md](../thesis/notes.md#sentinel-2-na-rq1-avançar-já-por-extração-em-pontos-não-raster-completo)).
- [ ] Implementar a zona-tampão na validação espacial do lado dos
  especialistas
  ([thesis/notes.md](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km)).
- [ ] RQ2 (máscara de segmentação): fixar os parâmetros de cada regra
  e correr o desenho que o orientador confirmar
  ([thesis/notes.md](../thesis/notes.md#rq2-proposta-mascara)).
- [ ] RQ3: correr o desenho que o orientador confirmar
  ([thesis/notes.md](../thesis/notes.md#rq3-proposta-redesenho-diagnostico-primeiro)).
- [ ] Validação independente da RQ1 com a classe *Acacia* da COS 2023
  ([docs/methodology.md](methodology.md#validation)).
- [ ] Análise de erro sistemática; precisa da RQ3 e da máscara de
  segmentação ([docs/methodology.md](methodology.md#error-analysis)).
- [ ] Mapa final da área de estudo, com incerteza
  ([docs/methodology.md](methodology.md#final-map)).

Opcional: ablação cumulativa do pipeline de referência
([docs/research_questions.md](research_questions.md#reference-data-pipeline-proposed)).
