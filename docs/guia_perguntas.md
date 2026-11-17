# Guia das perguntas de investigação e do que já foi feito

> **Retrato de 2026-11-17, para estudo.** Explica por palavras simples o
> que está nos ficheiros donos e não os substitui. Se alguma coisa aqui
> divergir deles, valem eles:
> [`research_questions.md`](research_questions.md) (perguntas e desenho),
> [`methodology.md`](methodology.md) (validação, métricas, baseline),
> [`thesis/notes.md`](../thesis/notes.md#decisões) (porquê de cada
> decisão) e [`todo.md`](todo.md) (tarefas).
>
> Não tem decisões novas. Todos os números vêm desses ficheiros. A
> 2026-11-17 a RQ1 passou a presence-only (regressão logística
> presença-fundo, sensitivity a área fixa, leave-one-block-out), o
> Random Forest com os seus números (curva, zona-tampão, 0,976) foi
> abandonado e a curva correu no desenho novo. Ver
> [`thesis/notes.md`](../thesis/notes.md#rq1-presence-only) e
> [`thesis/notes.md`](../thesis/notes.md#curva-presence-only).

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
| Presence-only | Só há exemplos de onde a acácia está; nunca se diz ao modelo que um ponto de fundo "não tem acácia". É a tarefa de todas as perguntas |
| Presença-fundo (com fundo não rotulado) | O classificador separa presenças do fundo, mas o fundo entra como "a paisagem em geral", não como ausência. É o que a regressão logística da RQ1 faz |
| One-class puro | Modelo treinado só com presenças, sem nenhum ponto de fundo (Isolation Forest, One-Class SVM). Testado e ficou atrás |
| Embedding (TESSERA) | Um vetor de números por píxel e por ano, produzido por um foundation model a partir das imagens de satélite. Usa-se como vem ("congelado"), sem treinar o modelo que o produz |
| Regressão logística `C=10` | O classificador da RQ1, escolhido na seleção de método de 2026-11-17 (a confirmar com o orientador). O Random Forest foi abandonado porque tratava o fundo como ausência |
| Blocos de 10 km | A área é dividida numa grelha de 10 km. Blocos inteiros ficam para teste, para o modelo não ser testado ao lado de onde treinou |
| Leave-one-block-out | Cada bloco com presenças que cheguem (pelo menos 5) serve de teste exatamente uma vez, com o modelo treinado em todos os outros. Substitui os cinco sorteios de blocos por semente que a curva antiga usava |
| Sensitivity a 10% de área | Ordena-se a paisagem pela nota do modelo; os 10% de área com nota mais alta são a previsão de acácia; a sensitivity é a fração das presenças de teste que cai lá dentro. Acaso = 0,10. É a métrica principal; reporta-se também a curva de 1% a 50% de área |
| ROC-AUC | Probabilidade de o modelo dar nota mais alta a uma presença do que a um ponto de fundo. Passou a secundária: conta uma acácia não registada no fundo como erro, por isso o máximo real fica abaixo de 1 e não se sabe quanto (Phillips et al., 2009) |
| Índice de Boyce | Mede se as presenças ficam mais frequentes à medida que a nota sobe. Esteve perto de 0,99 em quase todos os modelos e não os distinguia. Deixou de ser calculado na curva: cada bloco tem poucos pontos de fundo para as suas janelas |
| Diferença emparelhada | Em cada fold (bloco de teste), a métrica da condição A menos a da condição B. Reporta-se a média, o desvio-padrão e quantos folds sobem ou descem, mais a diferença no resultado agrupado |

## 3. Como ler uma hipótese nesta tese

Cada pergunta tem uma hipótese nula (H₀, "não há diferença") e uma
alternativa (H₁, "há diferença", às vezes com direção).

- **Não há limiar de decisão.** Não se escreve "H₀ rejeitada". Reporta-se
  a diferença emparelhada por fold e descreve-se. A razão: poucos
  blocos independentes não sustentam um teste estatístico formal.
- **Antes ou depois do resultado.** Cada hipótese diz se foi escrita
  antes de se ver o resultado. Só a H₁ da RQ1 foi escrita depois (de
  ver a curva antiga, com o Random Forest).
- **"Sem diferença" tem duas leituras possíveis:** os modelos são
  mesmo iguais, ou a métrica não consegue separá-los. A sensitivity a
  área fixa evita o teto desconhecido do ROC-AUC, mas o seu valor
  absoluto é baixo nos blocos densos em acácia (parte do "fundo" é
  provavelmente acácia e conta como área, não como erro); lê-se a
  comparação entre condições, não o nível. É um risco comum às quatro
  perguntas.

## 4. As quatro perguntas

Ordem: cada pergunta só usa o que as anteriores definem, e a única que
precisa do Sentinel-2 vem no fim.

| | Pergunta, em curto | Estado |
|---|---|---|
| RQ1 | Treinar só com ciência cidadã chega ao desempenho de treinar com dados de especialistas? | Corrida (TESSERA); resultado preliminar, por confirmar com o orientador |
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
- **Validação (desde 2026-11-17): leave-one-block-out** nos 26 blocos
  de 10 km com pelo menos 5 presenças de qualquer das fontes (15 com
  ciência cidadã, 18 com especialistas, 6 com as duas). Em cada fold,
  as presenças das duas fontes do bloco e o fundo do bloco são o
  teste; tudo o resto treina. O mesmo teste em todos os níveis.

**Hipóteses.**

- **H₀:** acrescentar dados de especialistas não muda o desempenho.
- **H₁:** o desempenho sobe com a fração de dados de especialistas.
- **Como se mede:** diferença emparelhada por fold de sensitivity a
  10% de área entre 90% e 0%, mais a diferença no resultado agrupado.
  O teste principal é o agrupado (as duas fontes juntas); só
  especialistas e só ciência cidadã são reportados ao lado.
- **Atenção:** a H₁ foi escrita depois de ver a curva antiga (Random
  Forest). Não é um teste pré-registado.
- **O que cada resultado quereria dizer:** diferença perto de zero
  favorece a leitura de que a ciência cidadã já chega (ou de que a
  métrica não separa); diferença positiva e consistente quer dizer que
  os dados de especialistas ainda acrescentam.

**Métrica (eixo vertical): sensitivity a 10% de área prevista.**

- **O que o modelo faz:** para cada sítio do mapa dá uma **nota** que
  diz quão parecido o sítio é com acácia. Não diz "é" ou "não é"
  acácia: dá só a nota.
- **Que pontos usamos para o avaliar:** no bloco de teste há dois
  tipos de pontos:
  - **sítios onde sabemos que há acácia** (as presenças);
  - **pontos ao acaso na paisagem** (o fundo): eucaliptal, pinhal,
    campo, estrada… Servem só para saber o que são "10% da área": nunca
    são tratados como "sem acácia".
- **A métrica:** ordenam-se os pontos de fundo pela nota; os 10% com
  nota mais alta são a "área prevista de acácia"; a sensitivity é a
  fração das presenças de teste cuja nota entra nessa área. Acaso =
  0,10 (uma presença ao acaso cai nos 10% uma vez em dez).

(Porquê esta métrica e não a ROC-AUC: a ROC-AUC conta uma acácia não
registada no fundo como erro, que é o pressuposto que o orientador
pediu para não fazer; avaliar só com presenças, sem paisagem, também
não serve, porque não distingue modelos — foi testado. A sensitivity a
área fixa nunca rotula o fundo como ausência e mesmo assim penaliza um
modelo que marca tudo como acácia. A literatura desta métrica ainda
está por ler: é raciocínio teu até lá.)

**O que já deu: a seleção do classificador** (ciência cidadã,
TESSERA, 15 blocos com pelo menos 5 presenças, leave-one-block-out,
sensitivity agrupada a 10% de área, melhor configuração de cada modelo
depois de um varrimento pequeno; acaso 0,10):

| Modelo | Família | Sensitivity a 10% |
|---|---|---|
| Regressão logística `C=10` | presença-fundo, fundo não rotulado | **0,410** |
| MaxEnt (linear + quadrática) | presença-fundo, fundo não rotulado | 0,334 |
| One-Class SVM | one-class puro | 0,258 |
| Isolation Forest | one-class puro | 0,188 |
| Autoencoder + Isolation Forest (o ensemble que o orientador nomeou) | one-class puro | 0,163 |
| Autoencoder | one-class puro | 0,140 |

- **Leitura:** todas as presença-fundo batem todos os one-class em
  todas as frações de área; o pedido do orientador (ensemble com
  autoencoder) foi testado e fica perto do acaso. A regressão
  logística é o classificador da curva; o `C=10` é o extremo da grelha
  (menos regularização ajuda aqui), a confirmar na curva.
- **Cautelas:** a melhor configuração foi escolhida nos mesmos folds
  que a reportam (sem validação cruzada aninhada); os 15 blocos são os
  densos em acácia, por isso parte do "fundo" é provavelmente acácia e
  o valor absoluto fica baixo. Só a comparação entre modelos é lida.

**O que deu: a curva** (uma corrida, 2026-11-17; 26 folds, 5 196
presenças de teste; sensitivity agrupada a 10% de área, acaso 0,10):

| Presenças de teste | 0% | 10% | 50% | 90% | Só especialistas |
|---|---|---|---|---|---|
| Agrupadas | 0,531 | 0,604 | 0,681 | 0,692 | 0,701 |
| Só especialistas | 0,637 | 0,775 | 0,910 | 0,933 | 0,983 |
| Só ciência cidadã | 0,411 | 0,408 | 0,421 | 0,417 | 0,381 |

- **Leitura em três frases.** Juntar polígonos de especialistas à
  ciência cidadã melhora muito o reconhecimento das presenças de
  especialistas (17 de 17 folds a subir) e não muda nada no das
  presenças de ciência cidadã (6 folds a subir, 7 a descer). O ganho
  chega cedo: metade com 10% dos polígonos, quase tudo com 50%. O
  modelo só de especialistas é o melhor nas presenças de especialistas
  e o pior nas de ciência cidadã: cada fonte reconhece melhor o que se
  parece com ela.
- **A diferença principal (90% − 0%, agrupada):** +0,161; por fold
  +0,181 (dp 0,221), 18 de 26 folds a subir. Vai no sentido da H₁.
- **É o contrário da curva antiga**, que era plana. Mudaram o
  classificador, a métrica e os folds ao mesmo tempo; qual deles
  explica a mudança não está separado.
- **O que não se lê:** o nível absoluto (parte do fundo dos blocos
  densos é provavelmente acácia); só 17 folds têm píxeis de
  especialistas no teste e a variação entre folds é grande.
- Tabelas em `results/effort_reduction_curve/`; figura e leitura em
  [`effort_reduction_curve.ipynb`](../notebooks/07_foundation_models/effort_reduction_curve.ipynb);
  porquê e cautelas em
  [`thesis/notes.md`](../thesis/notes.md#curva-presence-only).

**O que se sabe dos dados, a ter à frente:** as presenças de
especialistas são mais fáceis de separar do fundo do que as de
ciência cidadã, e são outro habitat: 55,0% dos píxeis de especialistas
caem na classe "Florestas de acácias" da COS 2023, contra 17,9% das
presenças de ciência cidadã. É a hipótese mais provável (não testada)
para a diferença entre as duas fontes de teste.

**Limites a dizer sempre.** Só TESSERA, uma região; polígonos de
especialistas em apenas 18 blocos de 10 km; um fold com 1 154 píxeis
de especialistas pesa muito no resultado agrupado (por isso o por-fold
é reportado ao lado); nada disto foi ainda confirmado pelo orientador.

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
  de 150. O nível pequeno existe para ver se a máscara pesa mais quando
  há poucos dados (o motivo original, "a RQ1 mostrou que o modelo já
  está perto do teto", vinha da curva antiga e deixou de valer).
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
treino. Conjunto de teste (o filtrado), fundo, classificador
(regressão logística presença-fundo), métrica e folds são os da RQ1.
Só TESSERA.

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
- **Ponto de partida:** o modelo só de ciência cidadã dá 0,637 de
  sensitivity a 10% de área nas presenças de especialistas, contra
  0,983 do modelo treinado nelas (curva da RQ1). A RQ3 pergunta se
  esse 0,637 é mais baixo longe das observações.

**Como se mede.**

- **Modelo:** o de 0% da RQ1 (só ciência cidadã), em cada fold.
- **Teste:** os píxeis de especialistas, que este modelo nunca viu no
  treino, com o fundo do bloco a medir a área.
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
fold. O corte de 1 km e o uso dos píxeis de especialistas como
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
abaixo de cerca de 25% dos dados. O mesmo artigo sugere que um
classificador leve pode desfavorecer os embeddings; se isso vale para
a regressão logística da RQ1 não se sabe.

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

- **Tarefa:** classificação presence-only por píxel, *A. dealbata*
  contra um fundo não rotulado. O mapa é a nota prevista em cada
  píxel.
- **Espécie:** só *A. dealbata*. Não se testa se o modelo a distingue
  de outras acácias (limitação declarada).
- **Tempo:** imagens de 2023; ficam só as observações de 2021–2025, e
  todas contam como 2023.
- **Foundation model:** embeddings congelados com um classificador
  leve, não fine-tuning. É um desvio à proposta de tese e tem de ser
  dito como tal.
- **Validação:** leave-one-block-out em blocos de 10 km; métrica
  principal sensitivity a 10% de área. Sem zona-tampão entre treino e
  teste; o efeito do tampão é medido ao lado da curva (secção 6).

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

### Escolha do método

- **Multiclasse abandonado** (decisão do orientador, 2026-11-05):
  exigia construir ausências à mão.
- **Primeira ronda (até 2026-11-17): Random Forest presença-vs-fundo**
  como classificador, avaliado com ROC-AUC e Boyce contra o fundo; o
  one-class SVM tinha perdido nessa avaliação. Abandonado a
  2026-11-17: o orientador contestou a avaliação (assume que o fundo
  não tem acácia), e o Random Forest assume o mesmo no treino, porque
  usa o fundo como ausência.
- **Segunda ronda (2026-11-17): seleção presence-only**, no mesmo
  protocolo para as duas famílias (one-class puro contra presença-fundo
  com fundo não rotulado), com varrimento pequeno de hiperparâmetros.
  Resultado na secção 4: regressão logística `C=10`. A tentativa de
  avaliar literalmente só com presenças (limiar tirado do treino) foi
  feita antes e não distinguia modelos.

### RQ1: a curva e os diagnósticos

- **Curva corrida no desenho novo** (secção 4, RQ1) pelo script
  `experiments/effort_reduction_curve/run.py` (leave-one-block-out nas
  duas fontes, regressão logística, sensitivity a 10% de área, tampão
  opcional por fold). A curva antiga (Random Forest, cinco sementes)
  deixou de ser reportada e as suas pastas foram apagadas; só o fundo
  só de floresta fica como pasta obsoleta.
- **Diagnósticos que ficam, como factos dos dados** (feitos para a
  curva antiga; a curva que explicavam já não existe como resultado):
  - **Redundância dentro dos polígonos:** existe (píxeis do mesmo
    polígono são muito parecidos), mas é modesta: cerca de 1 457
    unidades efetivas em 2 771 píxeis.
  - **Habitat:** os especialistas mapearam sobretudo manchas de
    acacial (55,0% dos píxeis em "Florestas de acácias"); a ciência
    cidadã cobre esse contexto e também pinhal, eucaliptal e matos.
  - **Pureza dos rótulos:** as presenças mais isoladas nos embeddings
    distinguem-se pelo observador; tirá-las do treino não melhorou o
    resultado (medido então com o Random Forest).
  - **Fundo só de floresta:** verificação da curva antiga; não é
    recorrida no desenho novo (obsoleta).
- **Zona-tampão:** medida no desenho novo, com tampões de 300 m e
  1 km por fold (saem do treino os pontos perto de qualquer ponto de
  teste). A sensitivity a 10% de área muda no máximo 0,006 e a
  diferença 90% − 0% não muda; o critério escrito antes cumpre-se nas
  8 comparações às duas distâncias. O tampão não muda a leitura da
  RQ1 e fica reportado ao lado da curva.

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

**Até ao relatório intermédio (início de janeiro de 2027):** as
experiências estão fechadas; a RQ1 entra como resultado preliminar e
RQ2, RQ3 e RQ4 entram no plano de trabalho. Falta escrever, ler a
literatura da métrica (Phillips et al., 2006; Peterson et al., 2008) e
confirmar com o orientador as escolhas da seleção de método e da
curva.

**Depois:** correr a RQ2 (filtros; máscara depois de aprovada a
extração), a RQ3 e o mapa de confiança; retomar o Sentinel-2 para a
RQ4; aplicar a zona-tampão; validar com a classe *Acacia* da COS 2023;
análise de erro; mapa final.

Lista completa e fontes: [`todo.md`](todo.md) e
[próxima reunião](meetings/2026-11-17.md).
