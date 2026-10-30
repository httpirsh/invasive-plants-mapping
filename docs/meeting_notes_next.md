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
    *Literatura:* Rivier et al. (2023/2024) propagaram rótulos de
    pontos a superpíxeis (ainda por ler); Karasiak et al. (2022) para
    a versão de um píxel.
- **Outras plantas como classes:** já apliquei esta proposta
  (47 353 → 18 895 outras plantas, 6,3 por presença). Perguntas por
  ordem de importância:
  1. [ ] **Os 8 grupos:** eucalipto, pinheiros, carvalhos, outras
     árvores, invasoras grandes (*Cortaderia*, *Hakea*, *Arundo*,
     *Ailanthus*…), matos, aquáticas, herbáceas. A forma de
     crescimento vem do GIFT (base de dados de traços), as invasoras
     da lista nacional (DL 92/2019); musgos e algas saem. Concorda,
     com as invasoras grandes como grupo próprio?
     *Literatura:* Ball et al. (2026) classificaram espécies e grupos
     como classes; GIFT (Weigelt et al., 2020; Denelle et al., 2023);
     Decreto-Lei 92/2019, Anexo II; EPPO (2024) para a *Hakea*.
  2. [ ] **Herbáceas só onde a erva é a camada de cima** (culturas,
     pastagens, montados, dunas, zonas húmidas, jardins): 43% estavam
     debaixo de floresta e 12% em edifícios; saem 23 677, ficam 5 967.
     Base: regra da camada de cima da classificação da FAO (LCCS). A
     lista de classes da COS é a minha leitura dos nomes das classes,
     não uma regra publicada. Concorda?
     *Literatura:* FAO LCCS (Di Gregorio & Jansen, 2000): a forma
     dominante é a da camada mais alta; árvores esparsas sobre erva
     fechada não dominam (por isso os montados ficam).
  3. [ ] **Matos debaixo de floresta:** só 13% dos matos estão em
     matos da COS; 26% em pinhal e 21% em eucaliptal. Aplico a mesma
     regra das herbáceas, ou ficam todos (como agora)?
     *Literatura:* a mesma regra da FAO (LCCS) sugere que saiam; não
     encontrei estudos que o façam com ciência cidadã.
  4. [ ] **Classes pequenas: eucalipto (169) e pinheiros (319).**
     - Porquê: são pouco fotografados (1% e 0,7% de todas as
       observações de plantas), e o filtro *research* tirou a maior
       parte: 67% dos eucaliptos eram *casual* (832 de 1 242), 81%
       delas do Observer A.
     - Hipótese (não verificada): como nas acácias, onde quase todas
       as *casual* do Observer A não tinham foto, estes eucaliptos
       também serão registos rápidos sem foto.
     - Opções: (a) recuperar as *needs_id* identificadas ao género
       (até +142 eucaliptos, +176 pinheiros), o que obriga a rever a
       regra do *research* nos dois lados; (b) juntar a "outras
       árvores" ou dar-lhes mais peso no treino; (c) usar a COS para
       estas classes, como nos especialistas, mas aí os rótulos
       deixam de ser de ciência cidadã, o que mexe na RQ1.
     - Qual prefere?
     - *Literatura:* Wolf et al. (2022, só o resumo): os dados do
       iNaturalist representam pior as zonas dominadas por árvores.
       Para (c), Ball et al. (2026) é a base da formulação
       multiclasse com a COS nos especialistas. Para (a) e (b), nada
       verificado.
  5. [ ] **A planta mais alta ganha no píxel:** em 917 píxeis com
     várias outras plantas, fica a mais alta (um carvalho ganha a um
     mato). Concorda?
     *Literatura:* FAO LCCS (camada mais alta); Karasiak et al. (2022)
     (mesmo píxel = mesmo exemplo).
  6. [ ] **Sub-bosque como contributo:** não encontrei estudos sobre o
     que fazer com observações de sub-bosque ao rotular píxeis de
     satélite. Conhece algum? Se não houver, pode entrar como
     contributo metodológico?
     *Literatura:* nenhuma encontrada; o mais próximo é Gillespie et
     al. (2024), iNaturalist com imagem aérea, sem confirmar se
     filtram o sub-bosque.
- **Filtro da RQ2:** as observações de 2024–2026 (1 009 presenças de *A. dealbata*)
  contam como "mais recentes", ou conta a distância a 2023?
  - [ ] Qual?
  *Literatura:* Ball et al. (2026): o desempenho caiu quando imagem e
  rótulos eram de anos diferentes, o que apoia a distância a 2023;
  reduziram os rótulos ao acaso, não por data.

- **Ausências nos dados de especialistas:**
  - [ ] Cruzei as 5 013 ausências (`classifica = 0`) com a COS 2023:
    44% estão em edifícios e indústria, só 3 em água, e 56% (2 823)
    em vegetação (pinhal, agricultura, outra floresta, eucaliptal,
    matos). Proponho usar as de vegetação como ausências e só uma
    amostra pequena das de edifícios, como classe própria.
    Concorda?
    *Literatura:* nenhuma verificada para esta escolha; a classe da
    COS como rótulo segue a formulação multiclasse (Ball et al.,
    2026).

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

**Literatura:** Dimson et al. (2023) encontraram enviesamento para
estradas e zonas perturbadas em registos de invasoras do iNaturalist;
Phillips et al. (2009) para usar outras plantas dos mesmos
observadores; Zhu et al. (2026) e Yang et al. (2026) para embeddings
que generalizam pior para outras regiões.

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
  *Literatura:* Domingo et al. (2023) e Martins et al. (2016)
  mapearam a *A. dealbata* sozinha; Eskandari et al. (2025) o género.
- **Outra fonte de ciência cidadã:** a plataforma invasoras.pt do CFE
  da Universidade de Coimbra (publicada no GBIF). Outras pessoas,
  outra plataforma: mais presenças, ou um teste da RQ3 com
  observadores diferentes.
  - [ ] Vale a pena juntar? Conhece quem a gere?
  *Literatura:* nenhuma verificada; é uma fonte de dados.
- **Overleaf:** para ligar o documento da tese ao repositório (sincronização
  com Git/GitHub) preciso do Overleaf Premium.
  - [ ] A universidade dá acesso ao Premium?

## Para a defesa

Dizer que tenho noção de que as perguntas são ambiciosas e que estão
ordenadas por prioridade. Frase e justificação em
[`thesis/notes.md`](../thesis/notes.md#perguntas-ambiciosas).
