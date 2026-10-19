# Reunião com o Orientador — Outubro 2026

> Preparada a 2026-10-17. Reunião de 30 minutos com quatro pontos, do
> mais importante para o menos importante. Cada ponto explica o
> problema, dá uma proposta e diz o que há a decidir. O resto fica
> para o fim, se sobrar tempo.

| # | Ponto | Tempo |
|---|---|---|
| 1 | Ausências | 10 min |
| 2 | Ano das imagens e anos das observações | 7 min |
| 3 | Como fazer a RQ2 | 7 min |
| 4 | A maioria das observações vem de uma só pessoa | 3 min |
| — | Se sobrar tempo | 3 min |

**Ponto de partida:** tenho 7 943 observações de *Acacia* do
iNaturalist no distrito de Coimbra, de 1992 a 2026. Quero treinar um
modelo que olhe para a imagem de satélite (Sentinel-2, ou os
embeddings do TESSERA) e diga, para cada píxel de 10 m, se tem
*Acacia* ou não.

Um facto a dizer logo no início, porque aparece em vários pontos:
**83% das observações são de uma só pessoa** (ver ponto 4).

## 1. Ausências — a decisão mais importante

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

## 2. Ano das imagens e anos das observações

> "Proponho usar imagens de um só ano, 2023, e só observações de 2021
> a 2025."

**O problema:** as imagens de satélite são de um ano, mas as
observações vão de 1992 a 2026. Se misturar anos, o modelo pode
aprender diferenças entre anos em vez da *Acacia*. O efeito do tempo
ficou fora da tese, por isso tenho de o manter fixo.

**Proposta:**
1. **Todas as imagens e mapas de 2023:** Sentinel-2, TESSERA e
   COS/OrtoSat.
2. **Só observações de 2021 a 2025** (2023 mais ou menos 2 anos),
   tanto presenças como ausências.

**Porquê 2023:** o OrtoSat só existe para 2023, e a COS 2023 é a mais
recente.

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
só sai 2 presenças e 33 outras plantas.

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

## 3. Como fazer a RQ2

> "A RQ2 não tira dados ao mapa final. É um teste: treino com cada vez
> menos dados para ver que modelo aguenta melhor. Proponho tirar os
> dados ao acaso e deixar o filtro só como comparação."

**O que a RQ2 faz:** treino os dois modelos (Sentinel-2 e TESSERA) com
100%, 50%, 25%, 10%, 5% e 1% dos dados e vejo quanto pioram. O mapa
final usa sempre todos os dados. Ter poucos dados não é um problema
para a RQ2, é a razão de ela existir: se o TESSERA funcionar com
poucos dados, serve para sítios e espécies com poucas observações.

**O problema da RQ2 como está escrita:** diz que os dados devem ser
reduzidos com um filtro que melhore a distribuição, e não ao acaso.
Nenhum filtro serve bem:
- **Zonas ardidas:** só com fogos até 2023, sai 2 presenças. Com
  fogos até 2025, sai 34,5%, mas esses fogos são depois das imagens e
  não há boa razão para os tirar.
- **Só observações confirmadas** (*research grade*): reduz, mas não
  melhora a distribuição pelo território.
- **Uma observação por quadrícula:** melhora a distribuição, mas já
  está na RQ3.

**Proposta:**
1. **Teste principal: tirar dados ao acaso.** Cada nível mais pequeno
   está dentro do maior. Repito várias vezes com sorteios diferentes e
   avalio em zonas separadas das de treino. É a forma habitual; Ball
   et al. (2026) também treinaram com partes dos dados (com cerca de
   5% chegaram perto do melhor resultado).
2. **Comparação extra:** com a mesma quantidade de dados, um filtro
   dá melhor resultado do que o acaso?
3. **O fogo fica como limpeza fixa dos dados** (ponto 2), e não como
   filtro da RQ2.

**Decidir:**
- [ ] Mudar a RQ2 para tirar dados ao acaso, com o filtro como
  comparação?
- [ ] Se sim, que filtro usar na comparação?
- [ ] Quantas repetições por nível?

## 4. A maioria das observações vem de uma só pessoa

> "Já disse que quase todas as observações vêm de uma só pessoa.
> Falta decidir o que faço com elas."

**O que encontrei:**
- Uma só pessoa fez 83% de todas as observações. Entre 2021 e 2025
  (os anos que proponho usar, ver ponto 2) fez 85%.
- 2021 tem 43% de todas as observações, e 98% delas são dessa pessoa.
  O pico de 2021 não vem de mais gente a usar o iNaturalist.
- Nos anos mais recentes pesa menos: 35% em 2023 e 31% em 2025.

**Porque importa:** o modelo só aprende com os sítios por onde esta
pessoa passou. Se ela anda sempre pelos mesmos caminhos, o mapa pode
mostrar o percurso dela e não onde a *Acacia* está de facto. É
exatamente este problema que a RQ3 estuda.

**Decidir:**
- [ ] O que fazer com as observações desta pessoa?
  - Usar todas.
  - Usar menos, p. ex. no máximo algumas por quadrícula.
  - Usá-las na RQ3 como exemplo real de enviesamento.

**Mostrar:** [notebook 02](../notebooks/02_citizen_science/acacia_coimbra_pilot_exploration.ipynb)
— observações por ano, mapa e peso de cada observador.

## Se sobrar tempo

Uma pergunta por tema; a explicação fica para a próxima reunião.

- **Validação independente:** se treino e teste vêm do mesmo
  iNaturalist, os erros dele ficam escondidos. Opções: a classe
  "Florestas de acácias" da COS 2023 (só manchas com mais de 1 ha) e
  as fotos aéreas OrtoSat 2023 (30 cm, acesso restrito).
  - [ ] Qual usar? Sabe como pedir acesso ao OrtoSat?
- **Área e espécies:** começo por Coimbra. As observações cobrem o
  distrito, mas os dados TESSERA que descarreguei só cobrem o
  concelho. Entre 2021 e 2025: *A. dealbata* 4 145, *A. melanoxylon*
  1 611, *A. longifolia* 417.
  - [ ] Distrito ou concelho? Todas as *Acacia*, ou uma só espécie?
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
