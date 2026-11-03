# Próxima Reunião com o Orientador

> Só as perguntas ainda sem resposta. As decisões já tomadas estão em
> [`research_questions.md`](research_questions.md).

## 0. Introdução: o que fiz

Explorei e limpei os três conjuntos de dados, um passo de cada vez,
sem mexer nos ficheiros originais. Todas as observações são tratadas
como 2023, o ano de referência das imagens.

**Presenças de *A. dealbata* (iNaturalist):** 7 943 observações de
*Acacia* → **3 000**. Fiquei só com a *A. dealbata*, só com as
*research* (identificação confirmada), só com precisão da
localização até 30 m (as sem valor ficam), e só uma por píxel de
10 m. O observador principal está anonimizado
("Observer A") e continua a ter 88% das presenças.

**Outras plantas (iNaturalist):** 120 479 observações → **18 895**
(6,3 por presença). Passaram pelos mesmos filtros das presenças, para
o modelo não aprender a forma como foram registadas em vez da planta.
Depois agrupei as espécies em 8 classes pela forma de crescimento,
tirei as que estão no mesmo píxel de uma *A. dealbata*, e fiquei só
com o que o satélite vê de cima (herbáceas fora da floresta, a planta
mais alta em cada píxel).

**Dados de especialistas:** 7 494 polígonos → **7 483**. Tirei os 11
sem rótulo e corrigi as geometrias inválidas. No distrito ficam 1 849
presenças, 2 780 ausências em vegetação e 2 187 em edifícios (vi a
classe da COS 2023 de cada ausência). Proponho usar as de vegetação e
só uma amostra das de edifícios.

#### Se perguntar porquê

**Presenças de *A. dealbata***

| Passo | Porquê | Literatura |
|---|---|---|
| Tirar coordenadas escondidas (43) | com geoprivacidade, o iNaturalist move o ponto para um sítio ao acaso numa célula de vários km | regra do próprio iNaturalist; nenhum artigo |
| Anonimizar o Observer A | a RQ3 precisa de separar esta pessoa, mas a tese não a pode nomear | — |
| Só *A. dealbata* | os especialistas só têm esta espécie (a comparação da RQ1 só é justa assim); a proposta pede a espécie; é 66% das *Acacia*; as espécies vêem-se de forma diferente do satélite | Domingo et al. (2023) e Martins et al. (2016) mapearam a *A. dealbata* sozinha |
| Só *research* | identificação confirmada por pelo menos duas pessoas; as *casual* são quase todas **sem foto** (1 670 de 1 679), e 98% são do Observer A; as *needs_id* ainda não estão confirmadas; ficam 3 441, chega para treinar | Gillespie et al. (2024) e Brown et al. (2025) usaram só *research*; só estas vão para o GBIF. Não encontrei estudo que compare com e sem as *casual* |
| Precisão até 30 m, manter as sem valor | um raio grande põe o ponto no píxel errado (rótulo impuro); as sem valor são do Observer A e o teste com a COS mostra que estão bem localizadas (18,6% em acacial, contra 20,7% das ≤ 10 m e 2,3% ao acaso); acima de 30 m desce para ~6,5% | Ball et al. (2026): rótulos impuros baixam a exatidão. O teste com a COS é meu. A apresentação da Radová (não publicada) aponta no mesmo sentido |
| Uma por píxel de 10 m | o modelo vê píxeis: duas observações no mesmo píxel são o mesmo exemplo; 98% das repetidas eram do Observer A (mesma visita); fica a mais próxima de 2023, o ano das imagens | Karasiak et al. (2022): amostras repetidas e próximas inflacionam a exatidão |
| Marcar zonas ardidas (não tira nada) | se ardeu entre a observação e 2023, o píxel de 2023 já não mostra o que foi visto | Riveiro et al. (2025): a acácia não desaparece com o fogo, o problema é o píxel |

**Outras plantas**

| Passo | Porquê | Literatura |
|---|---|---|
| Como classes, não como "não-acácia" | uma observação de eucalipto prova que há eucalipto, não que não há acácia ao lado; dá matriz de confusão (decisão da reunião de 21 de outubro) | Phillips et al. (2009), *target-group background*; Ball et al. (2026), espécies e grupos como classes |
| Os mesmos filtros das presenças | se só as presenças fossem *research*, as outras plantas ficavam com os registos sem foto e as plantas de jardim, e o modelo aprendia como as observações foram feitas em vez da planta | Phillips et al. (2009): o fundo tem de vir do mesmo processo de amostragem |
| Tirar as que estão num píxel com *A. dealbata* (772) | o mesmo píxel diria "é acácia" e "não é acácia"; fica a presença porque é a planta a mapear | ideia da máscara de segmentação (sua, reunião de 21 de outubro), aqui só a um píxel; Karasiak et al. (2022) |
| 8 grupos pela forma de crescimento | 1 549 espécies são demasiadas; árvore, mato, erva e água vêem-se diferente do satélite; eucalipto e pinheiro são as florestas dominantes; as invasoras grandes são as mais parecidas com a acácia | GIFT (Weigelt et al., 2020; Denelle et al., 2023); DL 92/2019, Anexo II; EPPO (2024) para a *Hakea*; FAO LCCS (Di Gregorio & Jansen, 2000) |
| Herbáceas só onde a erva é a camada de cima | o satélite vê a copa: 43% das herbáceas estavam debaixo de floresta e 12% em edifícios, e ensinavam que copa ou telhado é erva | FAO LCCS (Di Gregorio & Jansen, 2000): a forma dominante é a da camada mais alta. A lista de classes da COS é a minha leitura |
| A mais alta ganha no píxel | pela mesma razão: num píxel com carvalho e mato, de cima vê-se o carvalho | FAO LCCS; Karasiak et al. (2022) |

**Dados de especialistas**

| Passo | Porquê | Literatura |
|---|---|---|
| Usá-los | vistos no QGIS estão onde devem; são de 2023, feitos no campo e sobre o OrtoSat (a sua resposta de 28 de outubro) | — |
| Tirar 11 sem rótulo, corrigir 531 geometrias | as inválidas são contornos que se tocam num canto de píxel (vêm da conversão de raster para vetor); a correção não muda a área | — |
| Ausências: as de vegetação, e só uma amostra das de edifícios | com quase só edifícios, o modelo aprendia "árvore vs. edifício" e a exatidão saía inflacionada; mas tem de saber que um edifício não é acácia | nenhuma verificada; a classe da COS como rótulo segue Ball et al. (2026) |

As que ainda não confirmou estão na secção 1.

**Mostrar:** os notebooks em `notebooks/02_citizen_science/` e
`notebooks/03_expert_reference/`. As decisões e a literatura de cada
passo estão em [`thesis/notes.md`](../thesis/notes.md#decisões); as
que ainda estão por confirmar vêm a seguir.

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
  - Ideia extra: em vez de filtrar, dar mais peso às observações mais
    próximas de 2023 (não às mais recentes: uma de 2026 está tão longe
    da imagem como uma de 2020). Também baixava o peso do Observer A
    (2021 tem 43% das observações, 98% dela). Não no modelo principal,
    porque mexe na mesma variável da RQ2: só como verificação extra.
  - [ ] Vale a pena?
  *Literatura:* a mesma, Ball et al. (2026); não verifiquei estudos
  que pesem amostras pela data.

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

## 2. Para informar

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

### Apresentação da Lucie Radová (2026-10-30)

Assisti à apresentação interna dela (Departamento de Matemática, CFE,
orientada pela Cidália Fonte e pelo Diogo Duarte): recalibra um mapa
de probabilidade de *A. dealbata* (Random Forest com Sentinel-2) com
observações *research* do iNaturalist, na mesma zona (tile 29TNE).
Não é artigo nem preprint, por isso só a uso como contexto.

O que tirei para a minha tese:
- **Localização:** a maior parte do desacordo entre pontos e mapa
  vinha do desalinhamento GPS/píxel (mediana de 18% para 51% ao
  aceitar uma vizinhança de 30–50 m). Apoia o filtro de 30 m e a
  máscara de segmentação.
- **O mesmo enviesamento:** um observador fez 85% dos registos de
  *A. dealbata*, numa área maior (aqui, 83%). Se for a mesma pessoa,
  é um apoio independente à RQ3. Os pontos também seguem estradas e
  trilhos, como em Dimson et al. (2023).
- **As mesmas fontes de controlo:** COS 2023 e OrtoSat 2023.
- **Contraste:** ela propõe usar as outras plantas como "não-acácia"
  (para descer a probabilidade). Eu faço o oposto: cada outra planta é
  uma classe própria, porque uma observação de eucalipto não prova que
  não há acácia ao lado (Phillips et al., 2009). Mostra que a minha
  escolha não é a única possível.
- [ ] Conhece o trabalho? Faz sentido falar com ela, para não
  duplicarmos esforço?

## 3. Outros pontos

- **Se achar poucos dados: juntar a invasoras.pt.** Hoje ficam 3 000
  presenças (só *research*). Se achar pouco, a melhor forma de
  acrescentar é a plataforma invasoras.pt do CFE da Universidade de
  Coimbra (publicada no GBIF): outras pessoas e outra plataforma, por
  isso mais presenças sem aumentar o peso do Observer A, e ainda um
  teste da RQ3 com observadores diferentes.
  - Só em último caso: juntar as *casual* com menos peso no treino. São
    quase todas sem foto (1 670 de 1 679) e 98% do Observer A, por isso
    acrescentam mais do mesmo enviesamento; e teriam de entrar também
    nas outras plantas, onde incluem plantas de jardim.
  - [ ] Vale a pena juntar a invasoras.pt? Conhece quem a gere?
  *Literatura:* nenhuma verificada para juntar fontes; é uma fonte de
  dados. Não encontrei estudos que pesem observações do iNaturalist
  pela qualidade (pesquisa rápida).
- **Buffer em ângulo (ideia de outra defesa):** a coordenada do
  iNaturalist é onde estava o telemóvel, não a planta. Em vez de um
  círculo, um setor na direção para onde a câmara apontava, com o
  comprimento conforme o tipo de foto (grande plano: 1–2 m, cabe no
  píxel; paisagem: a planta pode estar a dezenas de metros).
  - A direção da câmara não é utilizável: a API não devolve metadados
    das fotos (verifiquei), e o EXIF que o site mostra só se lê
    raspando a página, que está protegida. Não confirmei se a direção
    é guardada.
  - Fica a parte exequível: classificar as fotos em grande plano ou
    paisagem, e tirar as de paisagem (ou dar-lhes um raio maior).
  - [ ] Percebi bem a ideia? Vale a pena classificar as fotos?
  *Literatura:* d'Andrimont et al. (2021, arXiv:2112.09190) deslocaram
  a posição de fotos de rua 30 m para o lado para onde a câmara
  apontava antes de as ligar às parcelas agrícolas (a mesma ideia, mas
  com fotos de estrada). Não encontrei estudos que corrijam a distância
  entre a câmara e a planta em fotos de ciência cidadã: pode ser um
  contributo.
- **Overleaf:** para ligar o documento da tese ao repositório (sincronização
  com Git/GitHub) preciso do Overleaf Premium.
  - [ ] A universidade dá acesso ao Premium?
