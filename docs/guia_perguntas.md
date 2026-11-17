# Guia das perguntas de investigação e do que já foi feito

> **Retrato de 2026-11-14, para estudo.** Explica por palavras simples o
> que está nos ficheiros donos e não os substitui. Se alguma coisa aqui
> divergir deles, valem eles:
> [`research_questions.md`](research_questions.md) (perguntas e desenho),
> [`methodology.md`](methodology.md) (validação, métricas, baseline),
> [`thesis/notes.md`](../thesis/notes.md#decisões) (porquê de cada
> decisão) e [`todo.md`](todo.md) (tarefas).
>
> Não tem decisões novas. Todos os números vêm desses ficheiros ou de
> `results/effort_reduction_curve/` (execuções de 2026-11-13 e
> 2026-11-14).
>
> **Desatualizado desde 2026-11-17:** o Random Forest presença-vs-fundo
> e os seus números (curva, zona-tampão, 0,976) foram abandonados; a
> RQ1 passou a presence-only (regressão logística presença-fundo,
> sensitivity a área fixa, leave-one-block-out). Ver
> [`thesis/notes.md`](../thesis/notes.md#rq1-presence-only).

## 1. A ideia da tese numa página

**O problema.** Para treinar um classificador de satélite que mapeie
*Acacia dealbata* são precisos exemplos de sítios onde a planta está.
Os melhores exemplos são polígonos desenhados por especialistas, que
custam visitas de campo. O iNaturalist tem milhares de observações
gratuitas, mas são pontos soltos, com erros de posição e de
identificação, e concentradas onde os observadores passam.

**A pergunta principal.** Em que medida as observações de ciência
cidadã, transformadas em dados de referência e representadas por
embeddings de um foundation model, conseguem substituir os dados de
especialistas **como dados de treino** para mapear *A. dealbata* no
distrito de Coimbra?

Três pormenores do enunciado que convém ter presentes:

- **"Em que medida"** pede um grau, não um sim ou não. A resposta é
  uma diferença de desempenho.
- **"Como dados de treino":** os dados de especialistas continuam a
  ser precisos para testar. O que se pergunta é se dá para treinar sem
  eles.
- **"Substituir"** mede-se pela diferença de desempenho entre modelos
  treinados com ciência cidadã e modelos treinados com dados de
  especialistas.

**Estado da formulação.** A pergunta principal, a numeração e a
redação das quatro perguntas abaixo são tuas e estão por confirmar com
o orientador. O que ele aprovou até agora: a ideia da curva (RQ1), uma
pergunta sobre concentração espacial da amostragem (origem da RQ3) e a
máscara de segmentação como ponto central (dentro da RQ2). A
Introdução do manuscrito ainda tem os enunciados que ele aprovou.

## 2. Vocabulário mínimo

| Termo | O que quer dizer aqui |
|---|---|
| Presença | Um píxel de 10 m onde há uma observação de *A. dealbata* (ciência cidadã) ou que cai num polígono de especialista |
| Fundo | 2 000 pontos sorteados ao acaso na área, a mais de 50 m de qualquer presença. Não são ausências confirmadas: são "o que a paisagem tem em geral" |
| Presença vs. fundo | O classificador aprende a distinguir presenças de pontos de fundo. É a tarefa de todas as perguntas |
| Embedding (TESSERA) | Um vetor de números por píxel e por ano, produzido por um foundation model a partir das imagens de satélite. Usa-se como vem ("congelado"), sem treinar o modelo que o produz |
| Random Forest | O classificador principal. A Logistic Regression é reportada como segundo |
| Blocos de 10 km | A área é dividida numa grelha de 10 km. Blocos inteiros ficam para teste, para o modelo não ser testado ao lado de onde treinou |
| Semente | Um sorteio diferente dos blocos de teste. Há cinco. As sementes reutilizam blocos, por isso cinco resultados parecidos não são cinco provas independentes |
| ROC-AUC | Probabilidade de o modelo dar pontuação mais alta a uma presença do que a um ponto de fundo. 0,5 é acaso, 1 é perfeito. Como o fundo pode conter acácia não observada, o máximo real fica abaixo de 1 e não se sabe quanto (Phillips et al., 2009) |
| Índice de Boyce | Mede se as presenças ficam mais frequentes à medida que a pontuação sobe. Está perto de 0,99 em quase todos os modelos, por isso não os distingue. É reportado ao lado do ROC-AUC e nenhuma conclusão assenta só nele |
| Diferença emparelhada | Em cada semente, ROC-AUC da condição A menos o da condição B, nos mesmos blocos de teste. Reporta-se a média, o desvio-padrão e em quantas das cinco sementes o sinal é o mesmo |

## 3. Como ler uma hipótese nesta tese

Cada pergunta tem uma hipótese nula (H₀, "não há diferença") e uma
alternativa (H₁, "há diferença", às vezes com direção).

- **Não há limiar de decisão.** Não se escreve "H₀ rejeitada". Reporta-se
  a diferença emparelhada e descreve-se. A razão: cinco sementes que
  reutilizam blocos não sustentam um teste estatístico formal.
- **Antes ou depois do resultado.** Cada hipótese diz se foi escrita
  antes de se ver o resultado. Só a H₁ da RQ1 foi escrita depois.
- **"Sem diferença" tem duas leituras possíveis:** os modelos são
  mesmo iguais, ou as métricas não conseguem separá-los (ROC-AUC com
  teto desconhecido, Boyce colado a 0,99). É um risco comum às quatro
  perguntas.

## 4. As quatro perguntas

Ordem: cada pergunta só usa o que as anteriores definem, e a única que
precisa do Sentinel-2 vem no fim.

| | Pergunta, em curto | Estado |
|---|---|---|
| RQ1 | Treinar só com ciência cidadã chega ao desempenho de treinar com dados de especialistas? | Medida (TESSERA) |
| RQ2 | Os filtros e a extensão do ponto à mancha mudam o desempenho? | Não corrida |
| RQ3 | O modelo piora longe da zona amostrada? | Não corrida |
| RQ4 | Os embeddings TESSERA são melhores que features Sentinel-2? | Não corrida, depende do Sentinel-2 (parado) |

### RQ1 — Ciência cidadã como substituta dos dados de especialistas

**Pergunta.** Em que medida um modelo treinado só com observações de
ciência cidadã atinge o desempenho de modelos treinados com dados de
referência de especialistas?

**Por palavras simples.** Se eu já tiver as observações do
iNaturalist, quanto ganho por ir buscar polígonos de especialistas? Se
o ganho for pequeno, o esforço de campo pode ser reduzido.

**Como se responde: a curva de redução de esforço.** A ideia é do
orientador (reunião de 2026-11-05); os pormenores são teus.

- Base fixa: as presenças de ciência cidadã (2 464 entram no treino da
  curva, segundo o `run.json`).
- Por cima acrescentam-se polígonos de especialistas: 0%, 10%, …, 90%
  dos 1 457 polígonos com embedding guardado. Os de 20% incluem os de
  10% (ordem encaixada).
- A 100% entram todos os polígonos, e a ciência cidadã continua lá
  (5 235 presenças de treino). A curva é aditiva até ao fim.
- À parte, como ponto de referência, há o modelo **só de
  especialistas** (2 771 píxeis, sem ciência cidadã). É o termo de
  comparação da pergunta principal. Decisão de 2026-11-14, por
  confirmar com o orientador; antes, o "100%" era este modelo.
- O conjunto de teste de cada semente é o mesmo em todos os níveis e
  tem sempre presenças das duas fontes.

**Hipóteses.**

- **H₀:** acrescentar dados de especialistas não muda o desempenho.
- **H₁:** o desempenho sobe com a fração de dados de especialistas.
- **Como se mede:** diferença emparelhada de ROC-AUC entre 90% e 0%.
  O teste principal é o global (as duas fontes juntas); o teste só com
  presenças de especialistas é uma segunda análise, ao lado.
- **Atenção:** a H₁ foi escrita depois de ver a curva. Não é um teste
  pré-registado.
- **O que cada resultado quereria dizer:** diferença perto de zero
  favorece a leitura de que a ciência cidadã já chega (ou de que a
  métrica não separa); diferença positiva e consistente quer dizer que
  os dados de especialistas ainda acrescentam.

**O que deu** (TESSERA, presenças de 2021–2025, média de cinco
sementes, ROC-AUC):

| Treino | Teste global, RF | Só presenças de especialistas, RF | Só presenças de ciência cidadã, RF | Teste global, LR |
|---|---|---|---|---|
| 0% (só ciência cidadã) | 0,902 | 0,976 | 0,812 | 0,893 |
| 20% | 0,907 | 0,988 | 0,810 | 0,917 |
| 90% | 0,906 | 0,993 | 0,801 | 0,924 |
| 100% + ciência cidadã | 0,906 | 0,993 | 0,799 | 0,924 |
| Só especialistas (referência) | 0,854 | 0,994 | 0,677 | 0,873 |

**Métrica (eixo vertical): ROC-AUC.**

- **O que o modelo faz:** para cada sítio do mapa dá uma **nota** de 0
  a 1 que diz quão parecido o sítio é com acácia. Não diz "é" ou "não
  é" acácia: dá só a nota.
- **Que pontos usamos para o avaliar:** na zona de teste há dois tipos
  de pontos:
  - **sítios onde sabemos que há acácia** (as presenças);
  - **pontos ao acaso na paisagem** (o fundo): eucaliptal, pinhal,
    campo, estrada… quase sempre sem acácia.
- **A métrica:** junta-se um sítio com acácia e um ponto de fundo, e
  vê-se se o modelo dá nota mais alta ao sítio com acácia; a ROC-AUC é
  a fração de pares em que acerta (0,5 = tanto faz como atirar uma
  moeda; 1 = acerta sempre).

(Porquê a ROC-AUC: não precisa de escolher um corte do tipo "acima de 0,5 é
acácia"; limitação: o fundo pode ter acácia não registada, por isso nunca
chega a 1 e o máximo possível é desconhecido — Phillips et al., 2009.)

**O gráfico em resumo**
([`curve_by_source.png`](../results/effort_reduction_curve/curve_by_source.png);
eixo horizontal: % de polígonos de especialistas juntos à ciência
cidadã; faixa: variação entre as cinco sementes; marcadores ocos aos
100%: modelo só de especialistas). Lido pela linha do Random Forest:

- **Esquerda (todas as presenças de teste): a linha é quase plana.**
  Juntar especialistas quase não melhora o resultado global. É a
  resposta principal da RQ1.
- **Meio (só presenças de especialistas): fáceis de reconhecer.** Mesmo
  sem nenhum dado de especialista no treino, o modelo já os reconhece
  muito bem; juntá-los melhora só um pouco.
- **Direita (só presenças de ciência cidadã): mais difíceis.** A linha
  fica abaixo das dos outros painéis, e o modelo só de especialistas
  cai bastante: quem treina só com especialistas reconhece pior os
  sítios que os cidadãos fotografam (ver a cautela sobre o teste global, abaixo).
- **Direita: a faixa verde (Logistic Regression) é muito larga.** O
  resultado depende muito da zona testada. Uma das sementes tem muito
  poucas presenças de ciência cidadã no teste; que isto explique a
  variação é uma hipótese provável, não testada.

Diferenças emparelhadas, 90% menos 0%:

- **Random Forest, teste global:** +0,004 (dp 0,005), positiva em
  quatro das cinco sementes. O ganho (cerca de 0,005) aparece logo aos
  10%–20% e não cresce mais.
- **Random Forest, só especialistas:** +0,017 (dp 0,005), positiva nas
  cinco.
- **Logistic Regression, teste global:** +0,031 (dp 0,007), positiva
  nas cinco.

**Como ler isto.**

- **A resposta depende do classificador e das presenças de teste.**
  Com Random Forest no teste global, os dados de especialistas quase
  não acrescentam; com Logistic Regression, ou olhando só para as
  presenças de especialistas, acrescentam um pouco.
- **O modelo só de ciência cidadã ordena bem os sítios mapeados pelos
  especialistas** (0,976, contra 0,994 do modelo só de especialistas).
- **A curva fica plana até ao fim:** de 90% para 100% + ciência
  cidadã nada muda. O valor mais baixo do modelo só de especialistas
  no teste global (0,854) vem de lhe faltar a ciência cidadã: nas
  presenças de especialistas fica igual (0,994 contra 0,993), nas de
  ciência cidadã perde 0,122 (0,677 contra 0,799). Explicação
  provável, não testada: essas presenças partilham o enviesamento de amostragem do
  treino de ciência cidadã, por isso o teste global favorece quem
  treinou com ela. Não quer dizer que o modelo de especialistas seja
  pior.
- **Cautela sobre "equivalência".** O 0,976 pode refletir presenças de
  especialistas mais fáceis de separar do fundo, não fontes
  equivalentes: 55,0% dos píxeis de especialistas caem na classe
  "Florestas de acácias" da COS 2023, contra 17,9% das presenças de
  ciência cidadã. É uma hipótese, apoiada nesta contagem.

**Limites a dizer sempre.** Só TESSERA, uma região; polígonos de
especialistas em apenas 18 blocos de 10 km; cada semente testa em 2 a
4 blocos com polígonos; nada disto foi ainda confirmado pelo
orientador.

### RQ2 — Dos pontos aos dados de referência

**Pergunta.** Em que medida os filtros de grau e de precisão aplicados
às observações, e a extensão de cada rótulo do píxel observado à
mancha de vegetação à volta, mudam o desempenho do mapeamento?

**Por palavras simples.** O pipeline que transforma pontos do
iNaturalist em píxeis rotulados tem escolhas. Duas delas são medidas:
(a) vale a pena rotular a mancha inteira em vez de um só píxel? (b)
vale a pena deitar fora observações menos fiáveis?

**Hipótese a — a máscara (rótulo de píxel ou de mancha).**

- **H₀a:** o desempenho é igual com rótulos só no píxel e com rótulos
  de mancha.
- **H₁a:** é diferente, sem direção fixada. Mais píxeis por observação
  podem ajudar; píxeis errados (a mancha a alastrar para vegetação
  parecida que não é acácia) podem prejudicar.
- **Três condições de treino:** só o píxel observado; **crescimento de
  região** (junta píxeis vizinhos com semelhança de cosseno ≥ 0,90 ao
  píxel observado, até 50 m em cada eixo); **superpíxeis** (SLIC sobre
  os embeddings, segmentos de cerca de 25 píxeis; o rótulo vai para o
  segmento que contém o ponto).
- **Dois níveis de dados:** todas as 2 465 presenças e uma subamostra
  de 150. O nível pequeno existe porque a RQ1 mostrou que com todos os
  dados o modelo já está perto do teto, e aí uma diferença dificilmente
  aparece.
- **Como se mede:** cada regra de máscara contra o treino só com o
  píxel, em cada nível. A comparação entre as duas regras é só
  descritiva.
- **A configuração foi fixada antes de correr** e não vai ser afinada
  nos resultados. Os valores são raciocínio teu, sem fonte.

**Hipótese b — os filtros.**

- **H₀b:** o desempenho é igual com e sem os filtros de grau e de
  precisão.
- **H₁b:** é diferente, sem direção fixada.
- **Duas condições de treino:** com os dois filtros (as 2 465
  presenças) ou sem nenhum (junta 1 120 píxeis de observações que não
  são *research grade* ou têm precisão pior que 30 m).
- **Só com todas as observações**, sem o nível de 150.

**O que fica igual nas duas hipóteses.** Só mudam os rótulos de
treino. Conjunto de teste (o filtrado), fundo, Random Forest, blocos e
sementes são os da RQ1. Só TESSERA.

**Estado.** Não corrida; nenhum resultado de desempenho existe.

- Os filtros podem correr com os embeddings já guardados.
- A máscara precisa de extrair janelas TESSERA à volta das
  observações, que não estão guardadas. Essa extração está por
  aprovar.
- Medido até agora: as contagens de cada passo do pipeline, e o
  tamanho das manchas num protótipo com 30 observações e outros
  parâmetros (só número de píxeis).

**Riscos.** Não haver diferença mesmo com 150; a máscara alastrar para
vegetação errada; a configuração não estar calibrada.

**Possível contributo.** Não foi encontrado nenhum trabalho que junte
propagação de ponto para mancha, pontos só de presença de ciência
cidadã e embeddings de satélite congelados.

### RQ3 — Transferibilidade para longe da zona amostrada

**Pergunta.** Em que medida o desempenho do modelo treinado com
ciência cidadã desce dos locais perto da zona amostrada para os locais
longe dela?

**Por palavras simples.** 90% das presenças são de um só observador,
concentradas em 15 dos 39 blocos com presenças. O modelo funciona onde
ninguém observou?

**Hipóteses** (escritas antes de correr).

- **H₀:** não há diferença de desempenho entre locais perto e longe.
- **H₁:** o desempenho é mais baixo longe (direcional).
- **Já se sabia antes:** pela RQ1, o modelo só de ciência cidadã tem
  0,976 de ROC-AUC nas presenças de especialistas, no conjunto.

**Como se mede.**

- **Modelo:** o de 0% da RQ1 (só ciência cidadã), em cada semente.
- **Teste:** os píxeis de especialistas, que este modelo nunca viu no
  treino, contra o fundo dos blocos de teste.
- **Perto:** polígonos até 1 km da presença de ciência cidadã mais
  próxima (1 251 polígonos, 1 961 píxeis). **Longe:** a mais de 1 km,
  dentro do distrito (205 polígonos, 789 píxeis, entre 1,0 e 8,2 km).
- **Reporta-se** a diferença longe contra perto, **sem atribuir a
  causa à distância**.
- **Produto:** um mapa de confiança (área de aplicabilidade, Meyer &
  Pebesma, 2021) que mostra onde os píxeis são diferentes dos de
  treino.

**Porque não se atribui a causa à distância.** Os polígonos de longe
são diferentes em mais coisas: a área mediana é cerca de 36 vezes
maior (2 788 m² contra 77 m²) e a ocupação do solo não é a mesma.
Manchas grandes são fáceis de detetar, por isso o desempenho pode ser
alto nos dois grupos e não mostrar nada.

**Estado.** Não corrida. Faltam as contagens de perto e longe por
semente. O corte de 1 km e o uso dos píxeis de especialistas como
teste são raciocínio teu, sem fonte.

**Limite.** "Longe" não passa de 8,2 km, por isso o resultado não diz
nada sobre outras regiões.

### RQ4 — Foundation models contra features convencionais

**Pergunta.** Em que medida os embeddings TESSERA melhoram o
mapeamento de *A. dealbata* face a features Sentinel-2, com treino em
dados de ciência cidadã limpos, com todas as observações e com poucas?

**Por palavras simples.** O foundation model vale a pena, ou as bandas
do Sentinel-2 com índices clássicos chegam? E a resposta muda quando
há poucos dados?

**Hipóteses** (escritas antes de correr).

- **H₀:** não há diferença entre os modelos TESSERA e Sentinel-2, em
  nenhum dos dois níveis de dados.
- **H₁:** o TESSERA é melhor, e a diferença é maior com poucos dados
  (direcional).
- **Como se mede:** TESSERA contra Sentinel-2 em cada nível (2 465
  presenças e as mesmas 150 da RQ2). Só muda a representação; tudo o
  resto é o da RQ1.

**A H₁ pode não se confirmar.** Na literatura lida há resultados nos
dois sentidos: em Silva & Gonçalves (2026), um caso português, o
Sentinel-2 bateu o TESSERA; em Koukos et al. (2026) as features
convencionais ficam à frente com todos os dados e o TESSERA à frente
abaixo de cerca de 25% dos dados. O mesmo artigo sugere que o Random
Forest pode desfavorecer os embeddings.

**Estado.** Não corrida, nada medido. Depende do braço Sentinel-2, que
está parado: extrair o Sentinel-2 nos pontos rotulados custou quase
tanto como o raster completo. O conjunto de features já está decidido
(compósito anual de 2023: mediana das 12 bandas, mais NDVI, NDWI e
NBR), por confirmar com o orientador.

**O que não se testa.** Se os embeddings compensam o ruído dos rótulos
(os dois lados treinam em dados limpos). Sem a RQ4, a tese só pode
descrever o desempenho com foundation models, não afirmar que são
melhores.

## 5. O que as quatro perguntas partilham

- **Tarefa:** classificação por píxel, *A. dealbata* contra fundo. O
  mapa é a probabilidade prevista em cada píxel.
- **Espécie:** só *A. dealbata*. Não se testa se o modelo a distingue
  de outras acácias (limitação declarada).
- **Tempo:** imagens de 2023; ficam só as observações de 2021–2025, e
  todas contam como 2023.
- **Foundation model:** embeddings congelados com um classificador
  leve, não fine-tuning. É um desvio à proposta de tese e tem de ser
  dito como tal.
- **Validação:** blocos de 10 km, cinco sementes. Ainda sem
  zona-tampão entre treino e teste (limitação declarada).

## 6. O que já foi feito

### Dados

- **iNaturalist limpo.** Das 5 242 presenças de *A. dealbata* ficam
  2 465:

  | Passo | Ficam |
  |---|---|
  | Só *research grade* | 5 242 → 3 441 |
  | Precisão conhecida até 30 m (sem valor: ficam, marcadas) | 3 441 → 3 276 |
  | Só 2021–2025 | 3 276 → 2 580 |
  | Uma presença por píxel de 10 m | 2 580 → 2 465 |

  Também saíram as observações de coordenadas escondidas, e nenhuma
  presença da janela foi apanhada pelo filtro de áreas ardidas.
  2 227 das 2 465 (90,3%) são do mesmo observador.
- **Polígonos de especialistas explorados e limpos.** 1 849 no
  distrito (244 ha); 1 457 com embedding guardado (2 771 píxeis);
  concentrados em 18 blocos de 10 km.
- **Embeddings TESSERA de 2023** extraídos para o piloto.
- **Fundo:** 2 000 pontos uniformes, mais um fundo só de floresta para
  verificação.
- **Variograma dos embeddings:** a semelhança entre píxeis estabiliza
  entre 500 m e 1 km.
- **Sentinel-2:** caminho de download montado; a extração ficou parada
  pelo custo.
- **Máscara:** protótipo com 30 observações (só tamanhos de mancha).

### Escolha do método (corridas anteriores, com as presenças de todos os anos)

- **One-class testado e descartado.** O one-class SVM perdeu para
  presença vs. fundo nas duas fontes (ciência cidadã: ROC-AUC 0,654
  contra 0,842 do Random Forest).
- **Random Forest escolhido como classificador principal**, por ser
  mais estável entre divisões espaciais. Com os dados de 2021–2025
  esse argumento enfraqueceu, por isso a Logistic Regression passou a
  ser reportada como segundo classificador.
- **Multiclasse abandonado** (decisão do orientador): exigia construir
  ausências à mão.

### RQ1: a curva e os diagnósticos

- **Curva completa corrida** (11 níveis, cinco sementes, dois
  classificadores), agora por um script com entradas e sementes fixas:
  `experiments/effort_reduction_curve/run.py`. Resultados na secção 4.
- **Quatro verificações à curva quase plana**, para afastar erro ou
  artefacto:
  - **Fundo só de floresta:** a curva continua plana e o ROC-AUC até
    sobe (Random Forest a 0%: 0,902 → 0,950). A curva não depende de
    um fundo "fácil". Isto não prova que o fundo uniforme não é
    enviesado.
  - **Redundância dentro dos polígonos:** existe (píxeis do mesmo
    polígono são muito parecidos), mas é insuficiente para explicar.
  - **Habitat:** é a explicação mais apoiada. Os especialistas
    mapearam sobretudo manchas de acacial; a ciência cidadã cobre esse
    contexto e também pinhal, eucaliptal e matos.
  - **Pureza dos rótulos:** tirar do treino as 5% de presenças mais
    isoladas não melhora o resultado (diferença −0,012, dp 0,019).
- **Zona-tampão contada, não aplicada:** a 30 m quase nada sairia do
  treino (17 presenças em 21 507); a 1 km cerca de 8,5%, de forma
  muito desigual entre sementes. O efeito no ROC-AUC não está
  registado.

### Desenho, literatura e documento

- **Perguntas formuladas** como pergunta → objetivo geral → objetivos
  específicos → hipóteses, com o desenho das quatro fechado do teu
  lado.
- **Literatura:** 36 entradas lidas e resumidas em
  [`literature.md`](literature.md). Não foi encontrado nenhum estudo
  que treine o mesmo classificador de satélite com rótulos de ciência
  cidadã e de especialistas para uma planta invasora.
- **Reprodutibilidade:** manifesto dos ficheiros derivados e um
  notebook que reproduz todas as contagens citadas no desenho
  (`design_counts.ipynb`).
- **Manuscrito:** a Introdução está escrita; os outros capítulos são
  esqueletos. Há divergências conhecidas entre a Introdução e o
  desenho atual, listadas em
  [`thesis/notes.md`](../thesis/notes.md#revisao-consistencia-2026-11-13).

## 7. O que falta

**Até ao relatório intermédio (início de janeiro de 2027):** sem novas
experiências. A RQ1 entra como resultado preliminar; RQ2, RQ3 e RQ4
entram no plano de trabalho. Falta escrever, e levar ao orientador a
reformulação em quatro perguntas, a máscara e o redesenho da RQ3.

**Depois:** correr a RQ2 (filtros; máscara depois de aprovada a
extração), a RQ3 e o mapa de confiança; retomar o Sentinel-2 para a
RQ4; aplicar a zona-tampão; validar com a classe *Acacia* da COS 2023;
análise de erro; mapa final.

Lista completa e fontes: [`todo.md`](todo.md) e
[próxima reunião](meetings/2026-11-17.md).
