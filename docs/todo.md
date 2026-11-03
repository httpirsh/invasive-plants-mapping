# To do

> Só tarefas concretas, cada uma com a origem. Os detalhes ficam nas
> [reuniões](meetings/), as decisões em
> [`thesis/notes.md`](../thesis/notes.md#decisões). Marcar com `[x]`
> e limpar as feitas de vez em quando.

## Agora

- [ ] Perguntar aos orientadores porquê não usar os `classifica = 0`
  na avaliação ([reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem))
- [ ] **Máscara de segmentação** (ponto central; [reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem)):
  - [ ] Ler Rivier et al. (2024) e procurar trabalhos do género
  - [ ] Definir uma regra para a área de vegetação mais próxima de
    cada observação
  - [ ] Testar várias abordagens, por exemplo: levar o ponto à
    vegetação mais próxima quando cai numa estrada ou edifício;
    estender o rótulo à mancha à volta (superpíxeis, semelhança dos
    embeddings, polígonos da COS)
  - [ ] Comparar as abordagens (com e sem, na ablação)
- [ ] Decidir se simplifico as classes para árvores e matos
  (sugestão, [reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem))

## Depois da resposta sobre os `classifica = 0`

- [ ] Atualizar `expert_polygons.ipynb`
- [ ] Definir as classes negativas do modelo de especialistas

## Mais tarde

- [ ] Eucalipto e pinheiros: se o modelo correr mal, recuperar pontos
  com pior precisão da localização ([reunião 2026-11-04](meetings/2026-11-04.md#resposta-dos-orientadores-por-mensagem))
- [ ] Ablação: com e sem os matos debaixo de floresta
- [ ] Ver se o Overleaf Premium é necessário
