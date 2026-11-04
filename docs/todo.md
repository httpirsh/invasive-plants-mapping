# To do

> Só tarefas confirmadas e importantes — não perguntas em aberto para
> uma reunião (essas ficam só nas [reuniões](meetings/)) nem ideias
> por decidir. Cada tarefa com a origem; os detalhes ficam nas
> reuniões, as decisões em [`thesis/notes.md`](../thesis/notes.md#decisões).
> Marcar com `[x]` e limpar as feitas de vez em quando.

## Agora

- [x] Perguntar aos orientadores porquê não usar os `classifica = 0`
  na avaliação — resposta não respondeu diretamente, sugeriu baseline
  one-class em vez disso ([seguimento, reunião 2026-11-04](meetings/2026-11-04.md#pergunta-de-seguimento-sobre-classifica--0-para-avaliação-por-mensagem))
- [x] Pesquisar abordagens one-class / positive-only para o baseline
  do modelo de ciência cidadã — primeira pesquisa feita (só resumos,
  nenhum artigo lido por inteiro; ver pistas em
  [thesis/notes.md](../thesis/notes.md#baseline-do-modelo-de-ciência-cidadã-pode-ser-one-class-pergunta-sobre-os-classifica--0-sem-resposta-direta))
- [ ] Ler Phillips et al. (2009) e o artigo de 2025 sobre PU learning
  com Sentinel-2 (pistas da pesquisa acima); perceber se o orientador
  tinha um método concreto em mente
- [ ] Esclarecer com o orientador o que quis dizer com "baseline
  one-class": só o braço Sentinel-2 da RQ1, ou substituir o
  multiclasse já adotado — e depois registar a resposta
- [ ] **Reunião (2026-11-05):** perguntas combinadas em
  [docs/meetings/2026-11-05.md](meetings/2026-11-05.md)
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
    testar na amostra de 30, agora que o acesso funciona
  - [ ] Candidata dos superpíxeis — usar a mesma patch do TESSERA como
    entrada; precisa de `scikit-image` (ainda não é dependência)
  - [ ] Comparar as abordagens (com e sem, na ablação)
- [ ] Decidir se simplifico as classes para árvores e matos
  (sugestão, [reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem))
- [x] Testar o download do Sentinel-2 (baseline da RQ1) via Earth
  Search/STAC, alinhado píxel a píxel à grelha da TESSERA — feito
  (2026-11-03), só numa faixa pequena de teste, não a extensão toda
  do piloto (ver [thesis/notes.md](../thesis/notes.md#sentinel-2-bruto-via-earth-search-aws-sem-conta-alinhado-à-grelha-da-tessera))
- [ ] Alargar o download do Sentinel-2 à extensão toda do piloto
  (distrito de Coimbra), com a mesma grelha/abordagem, agora que o
  pipeline está validado

## Depois da resposta sobre os `classifica = 0`

- [ ] Atualizar `expert_polygons.ipynb`
- [ ] Definir as classes negativas do modelo de especialistas

## Mais tarde

- [ ] Eucalipto e pinheiros: se o modelo correr mal, recuperar pontos
  com pior precisão da localização ([reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem))
- [ ] Ablação: com e sem os matos debaixo de floresta
