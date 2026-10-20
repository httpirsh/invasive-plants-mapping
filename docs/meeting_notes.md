# Reunião com o Orientador — Outubro 2026

## Perguntas de investigação

Texto completo em [`research_questions.md`](research_questions.md).

**Pergunta principal:** quão robustos e eficientes em dados são os foundation models de observação da Terra para mapear plantas invasoras, quando treinados com dados de ciência cidadã?

As três perguntas e como se encaixam na proposta:

- **RQ1 — Foundation models vs. abordagem convencional:** em que medida as representações dos foundation models melhoram o mapeamento de plantas invasoras em relação às variáveis espectrais e temporais convencionais, quando treinadas com dados de ciência cidadã, e quanto se perde em comparação com treinar com dados de referência de especialistas?
  - *Na proposta:* responde ao objetivo 3 (até que ponto a ciência cidadã permite mapear com precisão). O modelo treinado com dados de especialistas serve de teto. **Ver ponto 0c**.
  - **Explicação**: o TESSERA é melhor, e quanto se perde por usar o iNaturalist em vez de especialistas?


- **RQ2 — Eficiência de dados:** como se comparam os foundation models com a abordagem convencional à medida que há menos dados de ciência cidadã, e importa *quais* observações se retiram — um filtro que melhora a distribuição ou retirar ao acaso, com a mesma quantidade de dados?
  - *Na proposta:* responde ao objetivo 2 (usar foundation models para compensar poucos dados). Retirar ao acaso é o teste principal; o filtro é comparado com o acaso para o mesmo número de dados. **Ver ponto 3**.
  - **Explicação**: com menos dados, quem aguenta melhor, e importa quais dados ficam?

- **RQ3 — Enviesamento espacial:** os foundation models amplificam ou atenuam o efeito do enviesamento espacial das observações de ciência cidadã, em comparação com as variáveis convencionais, quando avaliados em regiões geograficamente distintas?
  - *Na proposta:* responde ao objetivo 2 (dados de ciência cidadã com erros e enviesados) e à análise de transferibilidade do plano de trabalho. Já se sabe que o enviesamento afeta os modelos; falta saber se os foundation models reagem a ele de forma diferente. **Ver ponto 4**.
  - **Explicação**: o TESSERA cai mais ou menos na armadilha de as pessoas irem sempre aos mesmos sítios?


**Ponto de partida:** tenho 7 943 observações de *Acacia* do iNaturalist no distrito de Coimbra, de 1992 a 2026. Quero treinar um modelo que olhe para a imagem de satélite (Sentinel-2, ou os embeddings do TESSERA) e diga, para cada píxel de 10 m, se tem *Acacia* ou não.
Um facto a dizer logo no início, porque aparece em vários pontos: **83% das observações são de uma só pessoa** (ver ponto 4).

*Se perguntar "o que é que isto tem de novo?":* cada parte já foi
estudada sozinha (embeddings vs. Sentinel-2 em espécies florestais;
enviesamento da ciência cidadã em invasoras; embeddings que
generalizam pior para outras regiões). Não encontrei nenhum trabalho
que junte foundation models, plantas invasoras e ciência cidadã, com
o enviesamento avaliado. Os mais próximos: o grupo do TESSERA em
Cambridge, com dados GBIF para habitats (ainda em curso), e um
trabalho em Michigan com invasoras e ciência cidadã, mas a 256 m e sem
foundation models. A novidade está na combinação e nos controlos, não
numa pergunta sozinha.

## 0. Encaixe com a proposta do projeto

> "Comparei as perguntas com a proposta da tese. Há três pontos da
> proposta que precisam de uma decisão para ficarem bem cobertos."

### a) Transformar observações em dados de referência

**O problema:** é o primeiro objetivo da proposta ("transformar
observações pontuais em dados de referência, tendo em conta a
incerteza e a qualidade"). Não é uma pergunta de investigação
própria.

**Proposta:** tratar os passos que transformam pontos do iNaturalist
em píxeis com rótulo como um **contributo medido**, não como simples
limpeza. Muitos já estão feitos ou propostos: localizações escondidas
(feito), anos, fogo, ausências. Faltam dois:
- **Precisão da localização:** tirar observações com incerteza grande
  face a um píxel de 10 m.
- **Pureza do rótulo:** uma foto de uma acácia sozinha num jardim não
  é um píxel de acácia. Verificar numa amostra com COS/OrtoSat.

Depois, medir quanto cada passo muda o resultado da RQ1 (juntar um
passo de cada vez). Assim a limpeza passa a ser um resultado.

**Decidir:**
- [ ] Fica como contributo metodológico (capítulo próprio), ou como
  uma pergunta de investigação à parte?

### b) Fine-tuning ou embeddings fixos

**O problema:** a proposta diz "fazer fine-tuning dos foundation
models". Eu uso os embeddings fixos com um classificador simples por
cima, o que não é fine-tuning.

**Proposta:** manter os embeddings fixos e dizer na tese que é uma
escolha:
- O AlphaEarth só existe como embeddings, não dá para fazer
  fine-tuning.
- Os pesos do TESSERA têm de ser pedidos.
- Com poucos dados e com erros, o fine-tuning arrisca aprender os
  erros.
- Usar o mesmo classificador em todas as representações isola o
  efeito da representação, que é o que a RQ1 mede.

Fine-tuning fica como extensão, se houver tempo.

**Decidir:**
- [ ] Aceita embeddings fixos como abordagem principal?
- [ ] Vale a pena pedir já os pesos do TESSERA?

### c) Comparar com dados de especialistas

**O problema:** a proposta pergunta "até que ponto a ciência cidadã
permite mapear com precisão". Para responder, preciso de saber quanto
se perde face a dados de especialistas. Sem essa comparação, só mostro
quão bons são os foundation models.

**Proposta:** na RQ1, treinar também um modelo com dados de
especialistas e usá-lo como teto.

**Decidir:**
- [ ] O MAP.INVADER tem dados de referência de *Acacia* que eu possa
  usar?
- [ ] Se não, uso pontos da classe "Florestas de acácias" da COS 2023?
  (Cuidado: se a COS também servir de teste, treino e teste têm de vir
  de zonas separadas.)

## 1. Ano das imagens e anos das observações

> "Proponho usar imagens de um só ano, 2023, e só observações de 2021 a 2025."

**O problema:** as imagens de satélite são de um ano, mas as observações vão de 1992 a 2026. Se misturar anos, o modelo pode aprender diferenças entre anos em vez da *Acacia*. O efeito do tempo ficou fora da tese, por isso tenho de o manter fixo.

**Proposta:**
1. **Todas as imagens e mapas de 2023:** Sentinel-2, TESSERA e COS/OrtoSat.
2. **Só observações de 2021 a 2025** (2023 mais ou menos 2 anos), tanto presenças como ausências.

**Porquê 2023:** o OrtoSat só existe para 2023, e a COS 2023 é a mais recente.

*Se perguntar "porque não um ano mais recente?":* 2 184 presenças
(34,5%) estão em zonas que arderam em 2025. Em 2023 essas zonas ainda
tinham a vegetação observada. Com imagens de 2025, um terço das
presenças estaria em terreno queimado.

**Porquê 2021–2025:**

| Anos usados | Observações que ficam |
|---|---|
| só 2023 | 3% |
| 2022–2024 | 31% |
| 2021–2025 | 80% |
| 2020–2026 | 93% |

- Com menos anos perde-se 2021, onde está quase metade das
  observações.
- A *Acacia* fica no mesmo sítio durante anos. Se foi vista em 2021 ou
  2025, provavelmente estava lá em 2023, a não ser que tenha ardido ou
  sido cortada.
- Dizer com franqueza: na prática, estes anos servem sobretudo para
  manter as observações da pessoa dominante.

**Cuidado com o fogo:** tirar as observações em zonas que arderam
entre o ano da observação e 2023, porque aí a imagem de 2023 já não
mostra o que foi visto. Testei com os mapas de área ardida do ICNF:
só saem 2 presenças e 33 outras plantas. Fica como passo fixo de
preparação dos dados (um dos passos do ponto 0a).

**Alternativa que rejeito:** usar, para cada observação, a imagem do
seu próprio ano. Parece mais exato, mas o modelo pode aprender o ano
em vez da planta. E como cada zona foi visitada num ano diferente, o
ano ficaria misturado com o sítio, o que estraga a RQ3.

**Decidir:**
- [ ] Aprovar imagens de 2023 e observações de 2021–2025?
- [ ] Ou usar mais anos depois de 2023 (p. ex. 2021–2026)?
  - A favor: ver uma *Acacia* em 2025 mostra melhor que estava lá em
    2023 do que vê-la em 2021, porque pode ter sido cortada depois.
  - Contra: depois dos fogos de 2025, pode ser uma planta nova a
    crescer, que não se parece com a de 2023. E 2026 ainda não acabou.

**Mostrar (só se perguntar pelo ano):** [burned_areas_overlay.png](../results/figures/meeting_2026-10/burned_areas_overlay.png)
— presenças e zonas ardidas de 2021 a 2025.

## 2. Ausências — a decisão mais importante dos dados

> "O iNaturalist só diz onde a *Acacia* foi vista, nunca onde não
> está. Para treinar o modelo preciso de exemplos sem *Acacia*.
> Proponho usar observações de outras plantas."

**O problema:** o modelo precisa de exemplos com *Acacia* (presenças)
e sem *Acacia* (ausências). O iNaturalist só dá presenças. As
ausências têm de ser inventadas; chamam-se pseudo-ausências ou
"fundo".

**As duas opções:**
- **Pontos ao acaso:** espalhar pontos pela área ao acaso. É simples,
  mas as presenças estão perto de estradas e caminhos, e os pontos ao
  acaso não. O modelo pode aprender "perto de estrada vs. longe" em
  vez de "*Acacia* vs. outra planta".
- **Outras plantas do iNaturalist (proposta):** usar observações de
  outras plantas como ausências. Foram feitas pelas mesmas pessoas,
  nos mesmos sítios, por isso a única diferença que sobra é a planta.
  Chama-se fundo de grupo-alvo (Phillips et al. 2009); melhorou os
  modelos em 226 espécies.

**O que já verifiquei:**
- Entre 2021 e 2025 há 6 333 presenças e 77 301 observações de outras
  plantas, cerca de 12 por cada presença.
- Tirei as observações com localização escondida. O iNaturalist muda
  de propósito a localização de algumas (por privacidade ou espécies
  protegidas), com erros de quilómetros. Foram 43 presenças e 8 242
  outras plantas.
- Este método só funciona se as presenças e as outras plantas vierem
  dos mesmos sítios. Por isso verifiquei se a pessoa que domina as
  presenças também regista outras plantas. Regista: 33 065
  observações, 43% do total. E em 97% das quadrículas de 1 km onde ela
  viu *Acacia*, também registou outras plantas.
- Mas as outras plantas cobrem muito mais território: só 26% das
  quadrículas com outras plantas têm *Acacia*.

**Limitações a dizer:**
- Uma observação de outra planta não prova que não há *Acacia* ali
  ao lado. Os resultados medem se o modelo separa a *Acacia* das
  outras plantas, não se acerta no terreno (ver "Validação
  independente", no fim).
- A escolha das ausências muda o que a RQ3 mede. Tenho de dizer
  sempre qual usei.

**Decidir:**
- [ ] Usar outras plantas do iNaturalist como ausências?
- [ ] Usar as outras plantas de todas as pessoas, ou só as da pessoa
  dominante (mesmos sítios, mas menos dados)?

Detalhes que proponho decidir eu e mostrar depois: que plantas entram
(todas ou só árvores e arbustos), a que distância de uma *Acacia* tirar
outras plantas, quantas ausências por presença, e se comparo com
pontos ao acaso na RQ3.

**Mostrar:** [presences_vs_background.png](../results/figures/meeting_2026-10/presences_vs_background.png)
— presenças e outras plantas, para a pessoa dominante e para as
restantes.

## 3. Como fazer a RQ2

> "A RQ2 não tira dados ao mapa final. É um teste: treino com cada vez
> menos dados para ver que modelo aguenta melhor. Proponho tirar os
> dados ao acaso e comparar com um filtro para a mesma quantidade de
> dados."

**O que a RQ2 faz:** treino os dois modelos (Sentinel-2 e TESSERA) com
100%, 50%, 25%, 10%, 5% e 1% dos dados e vejo quanto pioram. O mapa
final usa sempre todos os dados. Ter poucos dados não é um problema
para a RQ2, é a razão de ela existir: se o TESSERA funcionar com
poucos dados, serve para sítios e espécies com poucas observações.

**Porquê tirar ao acaso e comparar com um filtro:**
- Um filtro reduz a quantidade e muda a distribuição ao mesmo tempo;
  sozinho, não consigo separar os dois efeitos.
- Nenhum filtro serve bem sozinho:
  - **Zonas ardidas:** só com fogos até 2023, saem 2 presenças. Com
    fogos até 2025, sai 34,5%, mas esses fogos são depois das imagens
    e não há boa razão para os tirar.
  - **Só observações confirmadas** (*research grade*): reduz, mas não
    melhora a distribuição pelo território.
  - **Uma observação por quadrícula:** melhora a distribuição, mas já
    está na RQ3.

**Proposta:**
1. **Teste principal: tirar dados ao acaso.** Cada nível mais pequeno
   está dentro do maior. Repito várias vezes com sorteios diferentes e
   avalio em zonas separadas das de treino. É a forma habitual; Ball
   et al. (2026) também treinaram com partes dos dados (com cerca de
   5% chegaram perto do melhor resultado), mas com dados de
   inventário, não de ciência cidadã.
2. **Comparação: com a mesma quantidade de dados, um filtro dá
   melhor resultado do que o acaso?** Esta parte é a que não existe
   na literatura, e permite mostrar que observações o filtro tira e
   porquê.
3. **O fogo fica como limpeza fixa dos dados** (ponto 1), e não como
   filtro da RQ2.

**Decidir:**
- [ ] Aprovar a RQ2?
- [ ] Que filtro usar na comparação?
- [ ] Quantas repetições por nível?

## 4. A maioria das observações vem de uma só pessoa

> "Já disse que quase todas as observações vêm de uma só pessoa.
> Falta decidir o que faço com elas. Proponho usá-las na RQ3."

**O que encontrei:**
- Uma só pessoa fez 83% de todas as observações. Entre 2021 e 2025
  (os anos que proponho usar, ver ponto 1) fez 85%.
- 2021 tem 43% de todas as observações, e 98% delas são dessa pessoa.
  O pico de 2021 não vem de mais gente a usar o iNaturalist.
- Nos anos mais recentes pesa menos: 35% em 2023 e 31% em 2025.

**Porque importa:** o modelo só aprende com os sítios por onde esta
pessoa passou. Se ela anda sempre pelos mesmos caminhos, o mapa pode
mostrar o percurso dela e não onde a *Acacia* está de facto. É
exatamente este problema que a RQ3 estuda.

**Ligação à RQ3:** é um caso real para testar se os foundation
models amplificam ou atenuam o enviesamento. Os embeddings sabem onde
há estradas e casas, por isso podem aprender o percurso desta pessoa
ainda mais facilmente do que o Sentinel-2 (amplificar). Ou podem
separar melhor a *Acacia* do que está à volta (atenuar). Experiência:
treinar com todas as observações, com as dela limitadas, e sem as
dela, e testar nas observações das outras pessoas e noutras zonas.

**Decidir:**
- [ ] Aprovar a RQ3?
- [ ] O que fazer com as observações desta pessoa no modelo
  principal?
  - Usar todas.
  - Usar menos, p. ex. no máximo algumas por quadrícula.
  - Usar todas no modelo principal e testar as outras opções na RQ3
    (proposta).

**Mostrar:** [notebook 02](../notebooks/02_citizen_science/acacia_coimbra_pilot_exploration.ipynb)
— observações por ano, mapa e peso de cada observador.

## Se sobrar tempo

Uma pergunta por tema; a explicação fica para a próxima reunião.

- **Validação independente:** se treino e teste vêm do mesmo
  iNaturalist, os erros dele ficam escondidos. Opções: a classe
  "Florestas de acácias" da COS 2023 (só manchas com mais de 1 ha) e
  as fotos aéreas OrtoSat 2023 (30 cm, acesso restrito). Se a COS
  também der os dados de especialistas (ponto 0c), têm de ser zonas
  separadas.
  - [ ] Qual usar? Sabe como pedir acesso ao OrtoSat?
- **Área e espécies:** começo por Coimbra. As observações cobrem o
  distrito, mas os dados TESSERA que descarreguei só cobrem o
  concelho. Entre 2021 e 2025: *A. dealbata* 4 145, *A. melanoxylon*
  1 611, *A. longifolia* 417. A proposta pede mapeamento **ao nível da
  espécie**. Proponho o género *Acacia* como alvo principal (mais
  dados) e a *A. dealbata* sozinha como verificação ao nível da
  espécie.
  - [ ] Distrito ou concelho? Concorda com género + *A. dealbata*?
- **Outra fonte de ciência cidadã:** a plataforma invasoras.pt do CFE
  da Universidade de Coimbra (publicada no GBIF). Outras pessoas,
  outra plataforma: pode dar mais presenças, ou servir para testar a
  RQ3 com observadores diferentes.
  - [ ] Vale a pena juntar? Conhece quem a gere?
- **Testar a escolha dos anos:** repetir a RQ1 com 2022–2024,
  2021–2025 e 2020–2026 (com o mesmo número de observações) e ver se o
  melhor modelo continua a ser o mesmo.
  - [ ] É só para confirmar que a escolha dos anos não muda as
    conclusões, não um estudo do tempo. Concorda?
- **O que o modelo faz (já decidido):** diz *Acacia* sim/não para
  cada píxel; treina nos pontos observados e depois corre em toda a
  área.
  - [ ] Confirmar.

---

As figuras estão em `results/`, que não vai para o Git: os links só
funcionam no meu computador. Para as voltar a gerar, correr o
[notebook 04](../notebooks/04_data_integration/background_and_disturbance_checks.ipynb).