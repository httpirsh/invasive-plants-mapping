# Próxima Reunião com o Orientador — data por marcar

> Fila viva do que levar à próxima reunião. Decisões já tomadas ficam
> em [`thesis/notes.md`](../../thesis/notes.md#decisões); a reunião
> anterior está em [`2026-11-05.md`](2026-11-05.md).

## Resultados a apresentar: curva de redução de esforço (RQ2)

Corri a curva completa (0% a 100% de polígonos de especialistas sobre
a base de ciência cidadã, só com TESSERA, presenças de 2021–2025),
com as presenças de teste separadas por fonte.

- **Teste global** (ciência cidadã e especialistas juntos): o Random
  Forest ganha cerca de 0,005 de ROC-AUC com os primeiros 10%–20% de
  polígonos e não sobe mais (0,902 a 0%, 0,906 a 90%). A Logistic
  Regression sobe 0,031 (0,893 → 0,924). A resposta depende do
  classificador.
- **Só nas presenças de especialistas:** o modelo só com ciência
  cidadã já as ordena bem (ROC-AUC 0,976) e sobe para 0,993 com 90%
  dos polígonos; o Boyce vai no sentido contrário (0,970 → 0,940).
- **A 100%** (só especialistas, sem ciência cidadã) o teste global
  cai para 0,854. A queda vem toda das presenças de teste de ciência
  cidadã (0,812 → 0,677); nas de especialistas fica em 0,994. Não
  quer dizer que o modelo só de especialistas seja pior: o teste de
  ciência cidadã partilha provavelmente o enviesamento do treino.
- **Fundo mais difícil:** contra um fundo só de tipos de floresta, o
  teste global do Random Forest também não muda (0,950 a 0% e 0,952 a
  90%). Esta verificação não está separada por fonte.
- **Composição de habitat:** 55% dos píxeis de especialistas caem na
  classe "floresta de acácias" da COS, contra 17,9% das presenças de
  ciência cidadã. As presenças de especialistas podem ser mais fáceis
  de separar do fundo, o que não é o mesmo que as duas fontes serem
  equivalentes.

Valores por nível:
[thesis/notes.md](../../thesis/notes.md#simplificacao-desenho-2026-11-13).
Raciocínio:
[thesis/notes.md](../../thesis/notes.md#rq2-curva-por-fonte).

*Literatura:* nenhuma nova. A hipótese de que o desempenho sobe com
os dados de especialistas foi escrita depois de ver a curva.

A discutir:

- **Confirmar a leitura:** o ganho é pequeno e pode ser próprio deste
  piloto (uma região, só TESSERA, fundo partilhado ainda não
  confirmado por ele), não uma conclusão sobre o valor dos dados de
  especialistas em geral.
- **Poucas unidades independentes:** os polígonos de teste vêm de 2 a
  4 blocos de 10 km por semente, e as sementes reutilizam blocos.
- **Classificador principal:** mantenho o Random Forest, mas a
  Logistic Regression tem a média de ROC-AUC mais alta só com ciência
  cidadã (0,874 contra 0,836).
- **Unidade de esforço:** medi-o como percentagem de polígonos, não
  por área nem por custo real de campo.
- **Implicação prática:** numa nova recolha de campo, visar habitats e
  locais ainda não cobertos pela ciência cidadã (p. ex. a faixa a
  noroeste do distrito) pode valer mais do que mais polígonos do mesmo
  tipo de mancha.

## Propostas minhas, a confirmar

### Formulação das perguntas: quatro perguntas, centradas na substituição

Reorganizei as perguntas para ficarem no âmbito da proposta de tese e
escrevi-as como pergunta → objetivo geral → objetivos específicos →
hipóteses (H₀/H₁). Concorda com a forma e com os enunciados? Hipóteses
de trabalho ou testes estatísticos formais?

- **Principal:** em que medida as observações de ciência cidadã,
  transformadas em dados de referência e representadas por embeddings
  de foundation models de observação da Terra, podem substituir os
  dados de referência de especialistas no mapeamento de *Acacia
  dealbata* no distrito de Coimbra?
- **RQ1 (dos pontos aos dados de referência):** em que medida os
  filtros de qualidade aplicados às observações de ciência cidadã, e a
  extensão do rótulo de cada observação do píxel observado à mancha de
  vegetação à sua volta, alteram o desempenho do mapeamento?
- **RQ2 (substituição):** em que medida um modelo treinado só com
  observações de ciência cidadã atinge o desempenho de modelos
  treinados com dados de referência de especialistas?
- **RQ3 (representação):** em que medida os embeddings do TESSERA
  melhoram o mapeamento face às features do Sentinel-2, quando
  treinados com dados de ciência cidadã limpos, com todas as
  observações e com poucas?
- **RQ4 (transferibilidade):** em que medida o desempenho do modelo
  treinado com ciência cidadã desce dos locais perto da área amostrada
  para os locais longe dela?
- **O que muda face ao que aprovou:** a pergunta principal passa a
  ser sobre a ciência cidadã substituir os dados de especialistas, em
  vez da comparação TESSERA contra Sentinel-2; a pergunta da curva e a
  da comparação de representações separam-se (RQ2 e RQ3); a máscara e
  os filtros passam a ter pergunta própria (RQ1).
- **Prioridade:** RQ2, RQ1 e RQ4 só precisam do TESSERA; a RQ3
  precisa do Sentinel-2 e fica para o fim.
- **Como meço as hipóteses:** pela diferença de ROC-AUC emparelhada
  por semente (média, desvio-padrão, número de sementes com o mesmo
  sinal), sem limiar de decisão. O Boyce é só reportado.
- **Fica de fora, como limitação declarada:** não testo se os
  foundation models compensam o ruído dos rótulos (a RQ3 usa só dados
  limpos), nem se o modelo separa a *A. dealbata* das outras acácias
  (trabalho futuro).

Objetivos e hipóteses completos:
[research_questions.md](../research_questions.md#main-question-and-objectives).

*Literatura:* nenhuma; é o ajuste das perguntas à proposta de tese, na
forma de um guia de escrita de teses, não uma decisão metodológica.

Origem:
[thesis/notes.md](../../thesis/notes.md#reformulacao-quatro-perguntas);
versão anterior da formulação em
[thesis/notes.md](../../thesis/notes.md#formulacao-pergunta-objetivos-hipoteses).

### RQ1: máscara de segmentação e filtros de qualidade

Proponho que a máscara de segmentação, que disse ser central e que
não pertencia a nenhuma pergunta, seja o centro da RQ1, junto com o
efeito dos filtros de qualidade.

- **Hipóteses:** o desempenho é igual com e sem máscara, ou é
  diferente. Nos dois sentidos: mais píxeis por observação podem
  ajudar, píxeis errados podem prejudicar. O mesmo par para os
  filtros: igual ou diferente com e sem filtros de qualidade.
- **Condições de treino da máscara:** só o píxel observado,
  crescimento de região e superpíxeis, as duas regras sobre os
  embeddings TESSERA.
- **Condições de treino dos filtros:** todos os filtros, ou sem os
  filtros de qualidade (coordenadas escondidas, precisão, grau de
  qualidade). A janela 2021–2025 fica igual nas duas. Sem ablação
  passo a passo, e só com todas as observações.
- **Níveis de dados da máscara:** as 2 465 presenças e uma subamostra
  ao acaso de 150.
- **Resto igual à curva (RQ2)**, só com TESSERA; um conjunto de
  parâmetros fixo por regra.
- **Porque não é uma pergunta sobre reduzir as observações:** todas as
  presenças estão a 2 anos ou menos de 2023, por isso um filtro de
  recência teria pouco para ordenar; e a curva está perto do teto,
  por isso reduzir ao acaso diria pouco e repetiria Ball et al.
  (2026).
- **Fica de fora:** a regra dos polígonos da COS (cobre cerca de 17%
  dos pontos e é circular com a validação independente).
- **Risco a discutir:** não haver diferença mesmo com 150 presenças.

*Literatura:* Rivier et al. (2024) e Raine et al. (2022) para os
superpíxeis; Zhang et al. (2021) para o crescimento de região (crescem
pela confiança de um classificador, não por semelhança à semente). Não
encontrei trabalho que junte propagação de ponto para mancha, ciência
cidadã e embeddings congelados: possível contributo. A comparação com
e sem filtros é adaptada das ablações de um fator de Ball et al.
(2026).

Origem:
[thesis/notes.md](../../thesis/notes.md#rq2-proposta-mascara);
[thesis/notes.md](../../thesis/notes.md#reformulacao-quatro-perguntas).

### RQ4: medir a concentração espacial só com perto contra longe

Em vez de partir do princípio de que o observador dominante é um
enviesamento a corrigir, diagnosticar primeiro se a concentração da
amostragem prejudica o modelo.

- **Experiência:** treinar com ciência cidadã (TESSERA) e avaliar nos
  polígonos de especialistas, perto e longe do ponto de treino mais
  próximo.
- **Produto:** mapa de confiança por dissemelhança aos dados de
  treino.
- **Hipótese:** o desempenho é igual perto e longe, ou é mais baixo
  longe. Uso "concentração" em vez de "enviesamento" porque é o que de
  facto medimos: o observador dominante é fiável e cobre bem a zona
  dele.
- **A pergunta que aprovou** (os foundation models amplificam ou
  atenuam o efeito, face às features convencionais) passa a ser a
  segunda hipótese da RQ3, porque precisa do Sentinel-2: a mesma
  experiência repetida com as features do Sentinel-2.
- **Fica de fora, como trabalho futuro:** a comparação entre o
  observador dominante e os outros, o desbaste espacial, a camada de
  estradas e a segunda região.
- **Dados:** há 429 polígonos do TNE a mais de 1 km de qualquer
  observação.
- **Risco a discutir:** os polígonos de longe são 20 a 40 vezes
  maiores do que os de perto.

*Literatura:* Meyer & Pebesma (2021) para o mapa de confiança;
Ratsakatika et al. (2026, preprint) usam-no com embeddings mas
declaram que a exatidão fora da área não foi testada. Não encontrei
precedente com ciência cidadã concentrada num observador (pesquisa
rápida): possível contributo.

Origem:
[thesis/notes.md](../../thesis/notes.md#rq3-proposta-redesenho-diagnostico-primeiro);
[thesis/notes.md](../../thesis/notes.md#simplificacao-desenho-2026-11-13).

## Para informar

- **Janela temporal das observações (não bloqueante):** uso só
  observações do iNaturalist de 2021–2025, todas tratadas como
  representativas do povoamento de 2023. 2026 fica de fora porque o
  ano estava incompleto no download e por causa da possível rebrota
  depois dos incêndios de 2025. Ficam 2 465 presenças, 90% do
  Observador A.
  *Literatura:* Ball et al. (2026) e Gillespie et al. (2024) tratam
  observações de vários anos como um ano de referência; para a largura
  da janela (± 2 anos) não li nenhuma fonte.
  Origem:
  [thesis/notes.md](../../thesis/notes.md#janela-temporal-2021-2025).
- **Fundo uniforme reconstruído (não bloqueante):** o fundo foi
  reconstruído em 2026-11-13 com a zona-tampão de 50 m à volta das
  2 465 presenças de 2021–2025; mesma semente e mesmo número de
  pontos. O ROC-AUC global coincide a 0,002 com o fundo anterior; o
  Boyce global a 100% passou de 0,930 para 0,969.
  *Literatura:* nenhuma; é proveniência dos dados.
  Origem:
  [thesis/notes.md](../../thesis/notes.md#fundo-uniforme-reconstruido-2465).

## Perguntas

- **Máscara de segmentação, "considerar a área de vegetação mais
  próxima":** quis dizer estender o rótulo à mancha à volta da
  observação, ou só levar o ponto para dentro da vegetação mais
  próxima? Estou a assumir a primeira leitura (origem:
  [thesis/notes.md](../../thesis/notes.md#máscara-de-segmentação-testar-várias-abordagens)).
- **Validação independente da curva (RQ2):** o plano é comparar as
  previsões com a classe "Florestas de acácias" da COS 2023, como
  referência que não vem da ciência cidadã nem dos polígonos de
  especialistas. Confirmar que os polígonos foram feitos sem apoio da
  COS, e que a comparação faz sentido mesmo com 54% dos polígonos
  dentro dessa classe (origem:
  [`data/README.md`](../../data/README.md#acacia-dealbata-expert-reference-polygons)).
- **invasoras.pt:** se as presenças de ciência cidadã ficarem poucas,
  faz sentido juntar observações dessa plataforma? Quem a gere?
  (origem:
  [2026-11-04.md](2026-11-04.md#presenças-de-a-dealbata-7-943--3-000)).
- **Apresentação da Lucie Radová:** faz sentido falar com ela?
  (origem: [2026-11-04.md](2026-11-04.md#3-para-informar)).
