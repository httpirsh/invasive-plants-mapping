# Próxima Reunião com o Orientador

> Só as perguntas ainda sem resposta. As decisões já tomadas estão em
> [`research_questions.md`](research_questions.md).

## 1. Esclarecer decisões

- **Máscara de segmentação:** falou nela quando referi os buffers.
  Percebi assim: em vez de um círculo fixo à volta de cada *Acacia*,
  delimitar a mancha real (os píxeis vizinhos parecidos com o píxel
  observado, até um raio máximo). A mancha serve para tirar as outras
  plantas que caem dentro dela e para usar todos os seus píxeis como
  *Acacia* no treino. A tarefa continua a ser classificação por píxel.
  - [ ] É isto? Se sim, como delimitar a mancha: semelhança dos
    embeddings, superpíxeis, ou polígonos da COS quando existem?
    (Para já apliquei a versão de um píxel: as outras plantas no
    mesmo píxel de uma *A. dealbata* saem, 772 em 443 píxeis.)
- **Outras plantas como classes:** proponho 5–10 grupos (p. ex.
  eucalipto, pinheiros, carvalhos, outras árvores, arbustos,
  herbáceas).
  - [ ] Concorda com esta divisão?
- **Filtro da RQ2:** as observações de 2024–2026 (1 009 presenças de *A. dealbata*)
  contam como "mais recentes", ou conta a distância a 2023?
  - [ ] Qual?

- **Ausências nos dados de especialistas:**
  - [ ] Cruzei as 5 013 ausências (`classifica = 0`) com a COS 2023:
    44% estão em edifícios e indústria, só 3 em água, e 56% (2 823)
    em vegetação (pinhal, agricultura, outra floresta, eucaliptal,
    matos). Proponho usar as de vegetação como ausências e só uma
    amostra pequena das de edifícios, como classe própria.
    Concorda?

## 2. A pessoa que fez a maioria das observações

**O que encontrei:**
- Fez 83% de todas as observações.
- 2021 tem 43% de todas as observações, e 98% delas são dela. O pico
  de 2021 não vem de mais gente a usar o iNaturalist.
- Nos anos recentes pesa menos: 35% em 2023 e 31% em 2025.

**Ligação à RQ3:** o modelo só aprende com os sítios por onde esta
pessoa passou, por isso o mapa pode mostrar o percurso dela e não
onde a *Acacia* está. É um caso real para a RQ3: os embeddings sabem
onde há estradas e casas, por isso podem aprender esse percurso mais
facilmente do que o Sentinel-2 (amplificar), ou separar melhor a
*Acacia* do que está à volta (atenuar). Experiência: treinar com
todas as observações, com as dela limitadas, e sem as dela, e testar
nas das outras pessoas e noutras zonas.

**Decidir:**
- [ ] Aprovar a RQ3?
- [ ] No modelo principal: usar todas as observações dela e testar as
  outras opções na RQ3 (proposta), ou limitar já o número por
  quadrícula?

**Mostrar:** [notebook 02](../notebooks/02_citizen_science/acacia_observations.ipynb)
— observações por ano, mapa e peso de cada observador.

## 3. Para informar

O objetivo 1 da proposta (transformar observações de ciência cidadã
em dados de referência) fica coberto por um capítulo metodológico, com
cada passo de preparação dos dados medido por ablação (um passo de
cada vez, com Sentinel-2 e com TESSERA, o que também cobre a parte do
"ruído" do objetivo 2).

*Se perguntar "o que é que isto tem de novo?":* cada parte já foi
estudada sozinha (embeddings vs. Sentinel-2 em espécies florestais;
enviesamento da ciência cidadã em invasoras; embeddings que
generalizam pior para outras regiões). Não encontrei nenhum trabalho
que junte foundation models, plantas invasoras e ciência cidadã, com
o enviesamento avaliado. Os mais próximos: o grupo do TESSERA em
Cambridge, com dados GBIF para habitats (ainda em curso), e um
trabalho em Michigan com invasoras e ciência cidadã, mas a 256 m e sem
foundation models. A novidade está na combinação e nos controlos.

## 4. Outros pontos

- **Espécies:** em todos os anos, *A. dealbata* 5 241,
  *A. melanoxylon* 1 884, *A. longifolia* 512. Proponho só a
  *A. dealbata*: os dados de especialistas só têm esta espécie, a
  proposta pede mapeamento ao nível da espécie, e é 66% das
  observações. As outras *Acacia* ficam fora do treino; mais tarde,
  talvez como classe própria.
  - [ ] Concorda?
- **Outra fonte de ciência cidadã:** a plataforma invasoras.pt do CFE
  da Universidade de Coimbra (publicada no GBIF). Outras pessoas,
  outra plataforma: mais presenças, ou um teste da RQ3 com
  observadores diferentes.
  - [ ] Vale a pena juntar? Conhece quem a gere?
- **Overleaf:** para ligar o documento da tese ao repositório (sincronização
  com Git/GitHub) preciso do Overleaf Premium.
  - [ ] A universidade dá acesso ao Premium?

## Para a defesa

Dizer que tenho noção de que as perguntas são ambiciosas e que estão
ordenadas por prioridade. Frase e justificação em
[`thesis/notes.md`](../thesis/notes.md#perguntas-ambiciosas).
