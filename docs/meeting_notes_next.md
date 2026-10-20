# Próxima Reunião com o Orientador

> Pontos não urgentes. As perguntas de investigação e o contexto estão
> na [reunião de 21 de outubro](meeting_notes_2026-10-21.md).

## 1. Como fazer a RQ2

**O que a RQ2 faz:** treino os dois modelos (Sentinel-2 e TESSERA) com
100%, 50%, 25%, 10%, 5% e 1% dos dados e vejo quanto pioram. É um
teste: o mapa final usa sempre todos os dados. Ter poucos dados é a
razão de a RQ2 existir: se o TESSERA funcionar com poucos dados, serve
para sítios e espécies com poucas observações.

**Porquê tirar ao acaso e comparar com um filtro:**
- Um filtro reduz a quantidade e muda a distribuição ao mesmo tempo;
  sozinho, não separa os dois efeitos.
- Nenhum filtro serve bem sozinho:
  - **Zonas ardidas:** com fogos até 2023 saem só 2 presenças; com
    fogos até 2025 sai 34,5%, mas esses fogos são depois das imagens.
  - **Só observações confirmadas** (*research grade*): reduz, mas não
    melhora a distribuição pelo território.
  - **Uma observação por quadrícula:** melhora a distribuição, mas já
    está na RQ3.

**Proposta:**
1. **Teste principal: tirar dados ao acaso.** Cada nível mais pequeno
   está dentro do maior; repito com vários sorteios e avalio em zonas
   separadas das de treino. Ball et al. (2026) também treinaram com
   partes dos dados (com cerca de 5% chegaram perto do melhor
   resultado), mas com dados de inventário.
2. **Comparação:** com a mesma quantidade de dados, um filtro dá
   melhor resultado do que o acaso? É a parte que não existe na
   literatura, e mostra que observações o filtro tira e porquê.

**Decidir:**
- [ ] Aprovar a RQ2?
- [ ] Que filtro usar na comparação?
- [ ] Quantas repetições por nível?

## 2. A pessoa que fez a maioria das observações

**O que encontrei:**
- Fez 83% de todas as observações, e 85% entre 2021 e 2025.
- 2021 tem 43% de todas as observações, e 98% delas são dela. O pico
  de 2021 não vem de mais gente a usar o iNaturalist.
- Nos anos recentes pesa menos: 35% em 2023 e 31% em 2025.

**Ligação à RQ3:** o modelo só aprende com os sítios por onde esta
pessoa passou, por isso o mapa pode mostrar o percurso dela e não
onde a *Acacia* está. É um caso real para a RQ3: os embeddings sabem
onde há estradas e casas, por isso podem aprender esse percurso mais
facilmente do que o Sentinel-2 (amplificar), ou separar melhor a
*Acacia* do que está à volta (atenuar). Experiência: treinar com
todas as observações, com as dela limitadas, e sem as dela, e testar
nas das outras pessoas e noutras zonas.

**Decidir:**
- [ ] Aprovar a RQ3?
- [ ] No modelo principal: usar todas as observações dela e testar as
  outras opções na RQ3 (proposta), ou limitar já o número por
  quadrícula?

**Mostrar:** [notebook 02](../notebooks/02_citizen_science/acacia_coimbra_pilot_exploration.ipynb)
— observações por ano, mapa e peso de cada observador.

## 3. Para informar

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

## 4. Outros pontos

- **Espécies:** entre 2021 e 2025, *A. dealbata* 4 145,
  *A. melanoxylon* 1 611, *A. longifolia* 417. A proposta pede
  mapeamento ao nível da espécie. Proponho o género *Acacia* como alvo
  principal (mais dados) e a *A. dealbata* sozinha como verificação.
  - [ ] Concorda?
- **Outra fonte de ciência cidadã:** a plataforma invasoras.pt do CFE
  da Universidade de Coimbra (publicada no GBIF). Outras pessoas,
  outra plataforma: mais presenças, ou um teste da RQ3 com
  observadores diferentes.
  - [ ] Vale a pena juntar? Conhece quem a gere?
- **Testar a escolha dos anos:** repetir a RQ1 com 2022–2024,
  2021–2025 e 2020–2026 (com o mesmo número de observações) e ver se o
  melhor modelo continua o mesmo.
  - [ ] É só uma verificação, não um estudo do tempo. Concorda?
