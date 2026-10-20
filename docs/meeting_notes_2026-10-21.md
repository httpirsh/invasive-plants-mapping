# Reunião com o Orientador — 21 de outubro de 2026

> Levo só o que é urgente: as decisões de que preciso para continuar a
> trabalhar já. Primeiro os anos (rápido, dá contexto), depois as
> ausências, o fine-tuning, os dados de especialistas e a área. O
> resto fica para a próxima reunião
> ([`meeting_notes_next.md`](meeting_notes_next.md)).

## Perguntas de investigação

**Pergunta principal:** quão robustos e eficientes em dados são os foundation models de observação da Terra para mapear plantas invasoras, quando treinados com dados de ciência cidadã?

As três perguntas e como se encaixam na proposta:

- **RQ1 — Foundation models vs. abordagem convencional:** em que medida as representações dos foundation models melhoram o mapeamento de plantas invasoras em relação às variáveis espectrais e temporais convencionais, quando treinadas com dados de ciência cidadã, e quanto se perde em comparação com treinar com dados de referência de especialistas?
  - *Na proposta:* responde ao objetivo 3 (até que ponto a ciência cidadã permite mapear com precisão). O modelo treinado com dados de especialistas serve de teto. **Ver ponto 4**.
  - **Explicação**: o TESSERA é melhor, e quanto se perde por usar o iNaturalist em vez de especialistas?

- **RQ2 — Eficiência de dados:** como se comparam os foundation models com a abordagem convencional à medida que há menos dados de ciência cidadã, e importa *quais* observações se retiram — um filtro que melhora a distribuição ou retirar ao acaso, com a mesma quantidade de dados?
  - *Na proposta:* responde ao objetivo 2 (usar foundation models para compensar poucos dados). Retirar ao acaso é o teste principal; o filtro é comparado com o acaso para o mesmo número de dados. Fica para a próxima reunião.
  - **Explicação**: com menos dados, quem aguenta melhor, e importa quais dados ficam?

- **RQ3 — Enviesamento espacial:** os foundation models amplificam ou atenuam o efeito do enviesamento espacial das observações de ciência cidadã, em comparação com as variáveis convencionais, quando avaliados em regiões geograficamente distintas?
  - *Na proposta:* responde ao objetivo 2 (dados de ciência cidadã com erros e enviesados) e à análise de transferibilidade do plano de trabalho. Já se sabe que o enviesamento afeta os modelos; falta saber se os foundation models reagem a ele de forma diferente. Fica para a próxima reunião.
  - **Explicação**: o TESSERA cai mais ou menos na armadilha de as pessoas irem sempre aos mesmos sítios?
  

**Ponto de partida:** tenho 7 943 observações de *Acacia* do iNaturalist no distrito de Coimbra, de 1992 a 2026. Quero treinar um modelo que olhe para a imagem de satélite (Sentinel-2, ou os embeddings do TESSERA) e diga, para cada píxel de 10 m, se tem *Acacia* ou não.
Um facto a dizer logo no início, porque aparece em vários pontos: **83% das observações são de uma só pessoa**. O que fazer com isto fica
para a próxima reunião.

## 1. Ano das imagens e anos das observações

> "Proponho usar imagens de um só ano, 2023, e só observações de 2021 a 2025. Concorda?"

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
preparação dos dados.

**Alternativa que rejeito:** usar, para cada observação, a imagem do
seu próprio ano. Parece mais exato, mas o modelo pode aprender o ano
em vez da planta. E como cada zona foi visitada num ano diferente, o
ano ficaria misturado com o sítio, o que estraga a RQ3.

*Se perguntar "e usar mais anos depois de 2023 (p. ex. 2021–2026)?":*
- A favor: ver uma *Acacia* em 2025 mostra melhor que estava lá em
  2023 do que vê-la em 2021, porque pode ter sido cortada depois.
- Contra: depois dos fogos de 2025, pode ser uma planta nova a
  crescer, que não se parece com a de 2023. E 2026 ainda não acabou.

**Decidir:**
- [ ] Concorda com imagens de 2023 e observações de 2021–2025?

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
  outras plantas, não se acerta no terreno (ver ponto 4).
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

## 3. Fine-tuning ou embeddings fixos

> "A proposta fala em fine-tuning; proponho usar os embeddings fixos.
> E, se for para pedir os pesos do TESSERA, convém pedir já."

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

## 4. Dados de especialistas

> "Para saber quanto se perde com a ciência cidadã preciso de dados de
> especialistas. Ainda não sei quais usar."

**O problema:** a proposta pergunta "até que ponto a ciência cidadã
permite mapear com precisão". Para responder, preciso de saber quanto
se perde face a dados de especialistas. Sem essa comparação, só mostro
quão bons são os foundation models.

**Proposta:** na RQ1, treinar também um modelo com dados de
especialistas e usá-lo como teto.

**O que vi no MAP.INVADER** ([mapinvader.pt](https://mapinvader.pt/timeline/)):
os locais de referência só estão previstos para junho de 2027, e os
mapas (só *A. dealbata*) são de 2026–2028, não de 2023. Ainda não há
dados publicados. A exceção pode ser o trabalho de Soriano et al.
(EARSeL, setembro de 2026), que já mapeou *A. dealbata* no centro de
Portugal com Sentinel, e por isso usou dados de referência.

**Em aberto:**
- [ ] Que dados de especialistas usar? Opções que conheço: os dados de
  referência de Soriano et al. (se puderem ser partilhados, de que ano
  são, e se cobrem Coimbra), ou a classe "Florestas de acácias" da COS
  2023.
- [ ] Com que dados testo, para a comparação ser justa? Talvez o
  OrtoSat 2023, mas só para teste: são imagens de 30 cm, não rótulos,
  por isso eu teria de marcar os pontos à mão. Para treinar seriam
  precisos milhares de pontos e não sou especialista; para testar
  chegam 200–300 pontos, marcados com cuidado (e talvez revistos por
  alguém do projeto). Dúvidas: as imagens são de abril a outubro, sem
  a floração da *A. dealbata*, e só o visualizador (WMS) é público.

## 5. Área de estudo (pergunta rápida)

Começo por Coimbra. As observações cobrem o **distrito**, mas os dados
TESSERA que descarreguei só cobrem o **concelho**. Tenho de descarregar
o TESSERA de 2023, por isso preciso de saber já qual dos dois.

**Decidir:**
- [ ] Distrito ou concelho?

---

As figuras estão em `results/`, que não vai para o Git: os links só
funcionam no meu computador. Para as voltar a gerar, correr o
[notebook 04](../notebooks/04_data_integration/background_and_disturbance_checks.ipynb).