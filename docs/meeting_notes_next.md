# Próxima Reunião com o Orientador

> Pontos que não são urgentes para a reunião de 21 de outubro
> ([`meeting_notes_2026-10-21.md`](meeting_notes_2026-10-21.md)).
> As perguntas de investigação estão lá.

## 1. Como fazer a RQ2

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
3. **O fogo fica como limpeza fixa dos dados** (decidido na reunião anterior), e não como
   filtro da RQ2.

**Decidir:**
- [ ] Aprovar a RQ2?
- [ ] Que filtro usar na comparação?
- [ ] Quantas repetições por nível?

## 2. A maioria das observações vem de uma só pessoa

> "Já disse que quase todas as observações vêm de uma só pessoa.
> Falta decidir o que faço com elas. Proponho usá-las na RQ3."

**O que encontrei:**
- Uma só pessoa fez 83% de todas as observações. Entre 2021 e 2025
  (os anos propostos na reunião anterior) fez 85%.
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

## 3. Para informar

O objetivo 1 da proposta fica coberto por um
capítulo metodológico, com cada passo de preparação dos dados medido
por ablação (um passo de cada vez, com Sentinel-2 e com TESSERA, o que
também cobre a parte do "ruído" do objetivo 2).

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

## 4. Outros pontos

Uma pergunta por tema.

- **Espécies:** entre 2021 e 2025: *A. dealbata* 4 145, *A. melanoxylon*
  1 611, *A. longifolia* 417. A proposta pede mapeamento **ao nível da
  espécie**. Proponho o género *Acacia* como alvo principal (mais
  dados) e a *A. dealbata* sozinha como verificação ao nível da
  espécie.
  - [ ] Concorda com género + *A. dealbata*?
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