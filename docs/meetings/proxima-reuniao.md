# Próxima Reunião com o Orientador — data por marcar

> Perguntas em aberto que não couberam na reunião de 2026-11-05 (que
> se concentrou no redesenho da RQ1 — ver
> [`2026-11-05.md`](2026-11-05.md#o-que-foi-decidido)) nem foram
> entretanto respondidas por mensagem. Decisões já tomadas ficam em
> [`thesis/notes.md`](../../thesis/notes.md#decisões).

## Por perguntar

- **Regra das herbáceas:** concorda em só contar herbáceas onde são a
  camada de cima nas classes da COS? Já aplicado no pipeline, a
  confirmar (origem:
  [2026-11-05.md](2026-11-05.md#por-perguntar-não-chegou-a-ser-discutido-nesta-reunião)).
- **Uma planta por píxel, fica a mais alta:** concorda? Já aplicado no
  pipeline, a confirmar (mesma origem).
- **invasoras.pt:** se as presenças de ciência cidadã ficarem poucas,
  faz sentido juntar observações dessa plataforma? Quem a gere? (origem:
  [2026-11-04.md](2026-11-04.md#presenças-de-a-dealbata-7-943--3-000),
  passo 4).
- **Segunda região da RQ3 (Covilhã/Fundão):** faz sentido usar a zona
  com 165 polígonos `classifica = 1` e 57 observações *research grade*
  de *A. dealbata* como segunda região? (origem:
  [2026-11-04.md](2026-11-04.md#3-para-informar);
  [`data/README.md`](../../data/README.md#candidate-second-region-for-rq3-found-not-chosen)).
- **RQ3 — mudar a forma de medir (proposta minha):** a pergunta
  mantém-se, mas em vez de partir do princípio de que o observador
  dominante é um enviesamento a corrigir, diagnosticar primeiro:
  (1) treinar com ciência cidadã e avaliar nos polígonos de
  especialistas perto e longe do ponto de treino mais próximo, para
  TESSERA e Sentinel-2; (2) 353 pontos do observador dominante contra
  os 353 dos outros; mapa de confiança por dissemelhança só como
  produto; desbaste só se houver degradação; sem camada de estradas.
  Concorda? Se sim, a segunda região (ponto acima) deixa de ser
  necessária: há 392 polígonos do TNE a mais de 1 km de qualquer
  observação, e 398 no resto do país. Risco a discutir: os polígonos
  de longe são 20 a 40 vezes maiores do que os de perto. *Literatura:* Meyer & Pebesma (2021), método;
  Ratsakatika et al. (2026, preprint) usam-no com embeddings mas
  declaram que a exatidão fora da área não foi testada; não encontrei
  precedente com ciência cidadã concentrada num observador (pesquisa
  rápida) — possível contributo. **E o enunciado:** proponho "Os foundation
  models de observação da Terra amplificam ou atenuam o efeito da
  concentração espacial das observações de ciência cidadã, em
  comparação com features convencionais de satélite, quando o modelo
  é avaliado longe de onde houve amostragem?" — "concentração" em vez
  de "enviesamento", porque é o que de facto medimos (o observador
  dominante é fiável e cobre bem a zona dele), e uma terceira
  hipótese além de amplifica/atenua: sem efeito (origem:
  [thesis/notes.md](../../thesis/notes.md#rq3-proposta-redesenho-diagnostico-primeiro)).
- **Formulação das perguntas (proposta minha):** reescrevi a pergunta
  principal e as três RQ como pergunta → objetivo geral → objetivos
  específicos → hipóteses (H₀/H₁). Concorda com a forma e com os
  enunciados? Hipóteses de trabalho ou testes estatísticos formais?
  - *Principal:* em que medida os foundation models de observação da
    Terra, treinados com observações de ciência cidadã, permitem
    mapear *Acacia dealbata* com menor dependência de dados de
    referência de especialistas do que as features convencionais de
    satélite?
  - *RQ1:* em que medida as representações do TESSERA melhoram o
    mapeamento face às features do Sentinel-2, quando treinadas com
    ciência cidadã, e quanto desempenho se ganha ao acrescentar
    progressivamente dados de especialistas?
  - *RQ2:* qual o efeito da redução das observações, removendo
    primeiro as mais distantes de 2023, no desempenho dos modelos com
    TESSERA face aos modelos com Sentinel-2? (sai "mais fiáveis": já
    é tratado na limpeza)
  - *RQ3:* ver o ponto acima.
  - Objetivos e hipóteses completos:
    [research_questions.md](../research_questions.md#proposed-formulation-question-objectives-hypotheses).
  *Literatura:* nenhuma — é forma de redação, a partir de um guia de
  escrita de teses, não uma decisão metodológica (origem:
  [thesis/notes.md](../../thesis/notes.md#formulacao-pergunta-objetivos-hipoteses)).
- **Apresentação da Lucie Radová:** faz sentido falar com ela? (origem:
  [2026-11-04.md](2026-11-04.md#3-para-informar)).
- **Máscara de segmentação — "considerar a área de vegetação mais
  próxima":** confirmar se quis dizer estender o rótulo à mancha à
  volta da observação, ou só levar o ponto para dentro da vegetação
  mais próxima. Estou a assumir a primeira leitura para já (origem:
  [thesis/notes.md](../../thesis/notes.md#máscara-de-segmentação-sem-a-direção-da-câmara-testar-várias-abordagens)).
- **Validação independente da RQ1 (classe *Acacia* da COS 2023):**
  plano é comparar as previsões da RQ1 com a classe "Florestas de
  acácias" da COS 2023, como referência que não vem nem da ciência
  cidadã nem dos polígonos de especialistas. Confirmar que os
  polígonos de especialistas foram mesmo feitos sem apoio da COS
  (visitas de campo + segmentação/interpretação visual do OrtoSat,
  como já descrito por ele) e que esta comparação faz sentido como
  validação independente, mesmo com 54% dos polígonos já a cair dentro
  dessa classe da COS (origem:
  [`data/README.md`](../../data/README.md#acacia-dealbata-expert-reference-polygons);
  [thesis/notes.md](../../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)).

## Resultados a apresentar: curva de redução de esforço da RQ1

Corrida a curva completa de redução de esforço (0% a 100% de dados de
especialistas sobre a base de ciência cidadã, metodologia fixa em
todos os pontos). Random Forest e Logistic Regression já estão
praticamente no teto só com ciência cidadã (Boyce ≈0,99) e ficam
planos do 0% ao 90% — só pioram a 100%, quando a ciência cidadã é
totalmente substituída. Verificado que não é erro nem artefacto de um
fundo fácil (repetida a curva toda contra um fundo só de tipos de
floresta — o resultado manteve-se, até melhorou no Random Forest).
Explicação encontrada: os polígonos de especialistas, neste piloto,
cobrem sobretudo manchas de acácia já grandes e facilmente
identificáveis (55% caem dentro da própria classe "floresta de
acácias" da COS, apesar de os dados serem completamente independentes
dela), enquanto a ciência cidadã já cobre esse mesmo tipo de caso e
também uma gama muito maior de contextos (pinhal, eucaliptal, matos,
beira de estrada) — não é falta de valor dos dados de especialistas, é
que, como foram amostrados, não preenchem uma lacuna que a ciência
cidadã já não cubra. Detalhe completo em
[thesis/notes.md](../../thesis/notes.md#multiclasse-abandonado-rq1-passa-a-uma-curva-de-redução-de-esforço-presença-vs-fundo)
e notebooks ligados a partir daí.

- **Confirmar:** pode ser efeito de teto específico deste piloto (só
  uma região, só TESSERA, fundo partilhado ainda não confirmado por
  ele) — não uma conclusão definitiva sobre o valor dos dados de
  especialistas em geral.
- **Discutir:** esforço foi medido como % de polígonos, não por área
  nem custo real de campo — rediscutir a unidade.
- **Implicação prática** se houver nova recolha de campo: visar
  habitats/locais ainda não cobertos pela ciência cidadã (p. ex. a
  faixa a noroeste do distrito-piloto) pode valer mais do que mais
  polígonos do mesmo tipo de mancha.
