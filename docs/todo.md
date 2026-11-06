# To do

> Só tarefas confirmadas e importantes — não perguntas em aberto para
> uma reunião (essas ficam só nas [reuniões](meetings/)) nem ideias
> por decidir. Cada tarefa com a origem; os detalhes ficam nas
> reuniões, as decisões em [`thesis/notes.md`](../thesis/notes.md#decisões).
> Marcar com `[x]` e limpar as feitas de vez em quando.

## Agora

- [ ] **Entrega de início de janeiro de 2027 é um relatório intermédio,
  não a tese final (confirmado)** — data corrigida de dezembro de 2026
  (2026-11-06); `thesis/document/text/` não vai manter a forma de tese
  final para essa entrega; mapeamento exato dos capítulos ainda por
  decidir, para quando as experiências da RQ1 estiverem mais avançadas
  nos dois braços
  ([thesis/notes.md](../thesis/notes.md#primeira-entrega-relatório-intermédio-início-de-janeiro-de-2027))
- [ ] Ler Phillips et al. (2009) e o artigo de 2025 sobre PU learning
  com Sentinel-2 (pistas da pesquisa sobre baselines one-class)
- [ ] Implementar a zona-tampão de 20–30 m na **validação por divisão
  espacial** (spatial split) do lado dos especialistas, além dos
  blocos de 10 km — unidade assumida por decisão própria (2026-11-06),
  não confirmada pelo orientador
  ([thesis/notes.md](../thesis/notes.md#validação-espacial-no-lado-dos-especialistas-zona-tampão-além-dos-blocos-de-10-km))
- [ ] Rever o desenho da RQ3 que dependia de "outras plantas como
  classes vs. fundo ao acaso", agora que o multiclasse foi abandonado
  ([research_questions.md](research_questions.md#rq3--spatial-sampling-bias))
- [ ] **Máscara de segmentação** (ponto central; [reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem)):
  - [ ] Definir uma regra para a área de vegetação mais próxima de
    cada observação
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
- [ ] Alargar o download do Sentinel-2 à extensão toda do piloto
  (distrito de Coimbra), com a mesma grelha/abordagem, agora que o
  pipeline está validado
- [ ] Rever a estrutura de cada capítulo de `thesis/document/text/`
  face ao relatório de referência, à medida que for escrito/revisto
  (não reescrever o que já existe de uma vez)
  ([thesis/notes.md](../thesis/notes.md#estrutura-do-documento-seguir-um-relatório-de-referência-de-outro-aluno-onde-for-aplicável))

## Mais tarde

- [ ] Eucalipto e pinheiros: se o modelo correr mal, recuperar pontos
  com pior precisão da localização ([reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem))
- [ ] Ablação: com e sem os matos debaixo de floresta
