# Próxima Reunião com o Orientador — data por marcar

> Fila viva do que levar à próxima reunião. Decisões já tomadas ficam
> em [`thesis/notes.md`](../../thesis/notes.md#decisões); a reunião
> anterior está em [`2026-11-05.md`](2026-11-05.md).

## Resultados a apresentar: curva de redução de esforço da RQ1

Corri a curva completa (0% a 100% de dados de especialistas sobre a
base de ciência cidadã, só com TESSERA).

- Random Forest e Logistic Regression já estão perto do teto só com
  ciência cidadã (Boyce ≈0,99) e ficam planos do 0% ao 90%. Só pioram
  a 100%, quando a ciência cidadã é totalmente substituída.
- Não é erro nem artefacto de um fundo fácil: repeti a curva contra um
  fundo só de tipos de floresta e o resultado manteve-se (no Random
  Forest até melhorou).
- Explicação encontrada: os polígonos de especialistas cobrem
  sobretudo manchas grandes e reconhecíveis (55% caem na classe
  "floresta de acácias" da COS, apesar de serem independentes dela). A
  ciência cidadã cobre esse caso e também pinhal, eucaliptal, matos e
  beira de estrada. Os dados de especialistas não são inúteis: como
  foram amostrados, não preenchem uma lacuna que a ciência cidadã já
  não cubra.

Detalhe em
[thesis/notes.md](../../thesis/notes.md#curva-de-redução-de-esforço-completa-0100-com-fundo-e-bloco-de-teste-fixos).

A discutir:

- **Confirmar:** pode ser um efeito de teto deste piloto (uma região,
  só TESSERA, fundo partilhado ainda não confirmado por ele), não uma
  conclusão sobre o valor dos dados de especialistas em geral.
- **Unidade de esforço:** medi-o como percentagem de polígonos, não
  por área nem por custo real de campo.
- **Implicação prática:** numa nova recolha de campo, visar habitats e
  locais ainda não cobertos pela ciência cidadã (p. ex. a faixa a
  noroeste do distrito) pode valer mais do que mais polígonos do mesmo
  tipo de mancha.

## Propostas minhas, a confirmar

### RQ3: mudar a forma de medir

A pergunta mantém-se. Em vez de partir do princípio de que o
observador dominante é um enviesamento a corrigir, diagnosticar
primeiro se a concentração da amostragem prejudica o modelo.

- **Experiência 1:** treinar com ciência cidadã e avaliar nos
  polígonos de especialistas, perto e longe do ponto de treino mais
  próximo, para TESSERA e Sentinel-2.
- **Experiência 2:** 353 pontos do observador dominante contra os 353
  dos outros observadores.
- **Produto:** mapa de confiança por dissemelhança aos dados de
  treino.
- **Fica de fora:** a camada de estradas e a segunda região de
  iNaturalist. O desbaste espacial só corre se houver degradação.
- **Dados:** há 392 polígonos do TNE a mais de 1 km de qualquer
  observação, e 398 no resto do país.
- **Risco a discutir:** os polígonos de longe são 20 a 40 vezes
  maiores do que os de perto.
- **Enunciado proposto:** "Os foundation models de observação da Terra
  amplificam ou atenuam o efeito da concentração espacial das
  observações de ciência cidadã, em comparação com features
  convencionais de satélite, quando o modelo é avaliado longe de onde
  houve amostragem?" Uso "concentração" em vez de "enviesamento"
  porque é o que de facto medimos: o observador dominante é fiável e
  cobre bem a zona dele. Acrescento uma terceira hipótese além de
  amplifica e atenua: sem efeito.

*Literatura:* Meyer & Pebesma (2021) para o método; Ratsakatika et al.
(2026, preprint) usam-no com embeddings mas declaram que a exatidão
fora da área não foi testada. Não encontrei precedente com ciência
cidadã concentrada num observador (pesquisa rápida): possível
contributo.

Origem:
[thesis/notes.md](../../thesis/notes.md#rq3-proposta-redesenho-diagnostico-primeiro).

### RQ2: trocar a redução de dados pela máscara de segmentação

Proponho que a RQ2 deixe de ser sobre reduzir as observações e passe
a ser sobre a máscara de segmentação, que disse ser central e que não
pertencia a nenhuma pergunta.

- **Enunciado proposto:** "Em que medida estender o rótulo de cada
  observação de ciência cidadã à mancha de vegetação à sua volta
  altera o desempenho do mapeamento de *A. dealbata*, em comparação
  com treinar só no píxel observado?"
- **Hipóteses:** o desempenho é igual com e sem máscara, ou é
  diferente. Nos dois sentidos: mais píxeis por observação podem
  ajudar, píxeis errados podem prejudicar.
- **Condições de treino:** só o píxel observado, crescimento de região
  e superpíxeis, as duas regras sobre os embeddings TESSERA.
- **Níveis de dados:** as 3 000 presenças e uma subamostra ao acaso
  de 150.
- **Resto igual à RQ1**, só com TESSERA; um conjunto de parâmetros
  fixo por regra.
- **Porque sai a redução de dados:** só 19 das 3 000 presenças estão a
  mais de 4 anos de 2023, por isso o filtro de recência removeria
  sobretudo 2019–2020; e a curva da RQ1 está no teto, por isso reduzir
  ao acaso diria pouco e repetiria Ball et al. (2026).
- **Fica de fora:** a regra dos polígonos da COS (cobre cerca de 17%
  dos pontos e é circular com a validação independente).
- **Risco a discutir:** não haver diferença mesmo com 150 presenças.

*Literatura:* Rivier et al. (2024) e Raine et al. (2022) para os
superpíxeis; Zhang et al. (2025) para o crescimento de região. Não
encontrei trabalho que junte propagação de ponto para mancha, ciência
cidadã e embeddings congelados: possível contributo.

Origem:
[thesis/notes.md](../../thesis/notes.md#rq2-proposta-mascara).

### Formulação das perguntas

Reescrevi a pergunta principal e as três RQ como pergunta → objetivo
geral → objetivos específicos → hipóteses (H₀/H₁). Concorda com a
forma e com os enunciados? Hipóteses de trabalho ou testes
estatísticos formais?

- **Principal:** em que medida os foundation models de observação da
  Terra, treinados com observações de ciência cidadã, permitem mapear
  *Acacia dealbata* com menor dependência de dados de referência de
  especialistas do que as features convencionais de satélite?
- **RQ1:** em que medida as representações do TESSERA melhoram o
  mapeamento face às features do Sentinel-2, quando treinadas com
  ciência cidadã, e quanto desempenho se ganha ao acrescentar
  progressivamente dados de especialistas?
- **RQ2:** o enunciado proposto acima (substitui a pergunta da
  redução de dados).
- **RQ3:** o enunciado proposto acima.

Objetivos e hipóteses completos:
[research_questions.md](../research_questions.md#main-question-and-objectives).

*Literatura:* nenhuma; é forma de redação, a partir de um guia de
escrita de teses, não uma decisão metodológica.

Origem:
[thesis/notes.md](../../thesis/notes.md#formulacao-pergunta-objetivos-hipoteses).

## Perguntas

- **Máscara de segmentação, "considerar a área de vegetação mais
  próxima":** quis dizer estender o rótulo à mancha à volta da
  observação, ou só levar o ponto para dentro da vegetação mais
  próxima? Estou a assumir a primeira leitura (origem:
  [thesis/notes.md](../../thesis/notes.md#máscara-de-segmentação-testar-várias-abordagens)).
- **Validação independente da RQ1:** o plano é comparar as previsões
  com a classe "Florestas de acácias" da COS 2023, como referência que
  não vem da ciência cidadã nem dos polígonos de especialistas.
  Confirmar que os polígonos foram feitos sem apoio da COS, e que a
  comparação faz sentido mesmo com 54% dos polígonos dentro dessa
  classe (origem:
  [`data/README.md`](../../data/README.md#acacia-dealbata-expert-reference-polygons)).
- **Segunda região da RQ3 (Covilhã/Fundão):** só se o redesenho acima
  não for aceite. Faz sentido usar a zona com 165 polígonos
  `classifica = 1` e 57 observações *research grade* como segunda
  região? (origem:
  [`data/README.md`](../../data/README.md#candidate-second-region-for-rq3-found-not-chosen)).
- **invasoras.pt:** se as presenças de ciência cidadã ficarem poucas,
  faz sentido juntar observações dessa plataforma? Quem a gere?
  (origem:
  [2026-11-04.md](2026-11-04.md#presenças-de-a-dealbata-7-943--3-000)).
- **Apresentação da Lucie Radová:** faz sentido falar com ela?
  (origem: [2026-11-04.md](2026-11-04.md#3-para-informar)).
