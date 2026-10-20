# Reunião com o Orientador — 21 de outubro de 2026

> Só as decisões urgentes. O resto fica para a
> [próxima reunião](meeting_notes_next.md).

## Perguntas de investigação

**Pergunta principal:** quão robustos e eficientes em dados são os foundation models de observação da Terra para mapear plantas invasoras, quando treinados com dados de ciência cidadã?

- **RQ1 — Foundation models vs. abordagem convencional:** em que medida as representações dos foundation models melhoram o mapeamento de plantas invasoras em relação às variáveis espectrais e temporais convencionais, quando treinadas com dados de ciência cidadã, e quanto se perde em comparação com treinar com dados de referência de especialistas?
  - *Na proposta:* objetivo 3 (até que ponto a ciência cidadã permite mapear invasoras com precisão, ao nível da espécie). **Ver ponto 4**.
  - **Explicação**: o TESSERA é melhor, e quanto se perde por usar o iNaturalist em vez de especialistas?

- **RQ2 — Eficiência de dados:** como se comparam os foundation models com a abordagem convencional à medida que há menos dados de ciência cidadã, e importa *quais* observações se retiram — um filtro que melhora a distribuição ou retirar ao acaso, com a mesma quantidade de dados?
  - *Na proposta:* objetivo 2 (usar foundation models para compensar dados de ciência cidadã escassos e com ruído).
  - **Explicação**: ver qual modelo (Sentinel-2 ou TESSERA) aguenta melhor ter poucos dados de ciência cidadã.
    - **Passo 1 — Ao acaso (principal):** treinar os dois modelos com 100%, 50%, 25%, 10%, 5% e 1% dos dados, com várias repetições, e ver qual piora menos. Faço ao acaso porque assim só muda a quantidade.
    - **Passo 2 — Filtro que melhora a distribuição (secundário):** para a mesma quantidade de dados, ver se dados mais bem distribuídos ajudam, e se ajudam mais um modelo do que o outro.
      - **Filtro:** amostragem espacialmente equilibrada. Divido a área em quadrículas de 1 km e escolho uma observação de cada quadrícula à vez, até chegar ao mesmo número do conjunto ao acaso. As quadrículas com muitas observações perdem mais; as com poucas mantêm as suas.
      - **Quais saem e porquê:** sobretudo observações de zonas muito repetidas (provavelmente os percursos da pessoa dominante e as zonas perto de estradas), mostradas num mapa.
      - **Porque não por tipo de paisagem (COS):** a COS já serve para validar e talvez como dados de especialistas, e tem uma classe "Florestas de acácias". O filtro estaria a usar informação sobre a própria resposta.
  - **Nota:** é uma simulação. O mapa final usa sempre todos os dados.
  - [ ] Concorda com a amostragem espacialmente equilibrada como filtro?

- **RQ3 — Enviesamento espacial:** os foundation models amplificam ou atenuam o efeito do enviesamento espacial das observações de ciência cidadã, em comparação com as variáveis convencionais, quando avaliados em regiões geograficamente distintas?
  - *Na proposta:* objetivo 2 (usar foundation models para compensar dados de ciência cidadã escassos e com ruído) e análise de transferibilidade do plano de trabalho.
  - **Explicação**: o TESSERA cai mais ou menos na armadilha de as pessoas irem sempre aos mesmos sítios?
  - **Como:** treinar com as observações da pessoa dominante (todas, limitadas e sem ela), testar noutras regiões e com as observações das outras pessoas, e comparar outras plantas com pontos ao acaso como ausências.

**Ponto de partida:** 7 943 observações de *Acacia* do iNaturalist no distrito de Coimbra, de 1992 a 2026. O modelo olha para a imagem de satélite (Sentinel-2 ou embeddings do TESSERA) e diz, para cada píxel de 10 m, se tem *Acacia*. **83% das observações são de uma só pessoa.**

## 1. Ano das imagens e anos das observações

**O problema:** as imagens são de um ano, mas as observações vão de 1992 a 2026. Se misturar anos, o modelo pode aprender diferenças entre anos em vez da *Acacia*. O efeito do tempo ficou fora da tese, por isso tenho de o manter fixo.

**Proposta:** tudo de 2023 (Sentinel-2, TESSERA, COS/OrtoSat), e só observações de 2021 a 2025 (presenças e ausências).

**Porquê 2023:** o OrtoSat só existe para 2023, e a COS 2023 é a mais recente.

**Porquê 2021–2025:**

| Anos usados | Observações que ficam |
|---|---|
| só 2023 | 3% |
| 2022–2024 | 31% |
| 2021–2025 | 80% |
| 2020–2026 | 93% |

- Com menos anos perde-se 2021, onde está quase metade das
  observações (e quase todas da pessoa dominante).
- A *Acacia* fica no mesmo sítio durante anos. Se foi vista em 2021 ou
  2025, provavelmente estava lá em 2023, a não ser que tenha ardido ou
  sido cortada.

**Fogo:** tiro as observações em zonas que arderam entre o ano da
observação e 2023 (áreas ardidas do ICNF): saem só 2 presenças e 33
outras plantas. Fica como passo fixo de preparação dos dados.

**Alternativa que rejeito:** usar a imagem do ano de cada observação.
O modelo pode aprender o ano em vez da planta, e o ano ficaria
misturado com o sítio, o que estraga a RQ3.

*Se perguntar "porque não um ano mais recente?":* 2 184 presenças
(34,5%) estão em zonas que arderam em 2025; com imagens de 2025
estariam em terreno queimado.

*Se perguntar "e 2021–2026?":* a favor, uma *Acacia* vista em 2025
mostra melhor que estava lá em 2023. Contra, depois dos fogos de 2025
pode ser uma planta nova a crescer, e 2026 ainda não acabou.

**Decidir:**
- [ ] Concorda com imagens de 2023 e observações de 2021–2025?

**Mostrar (só se perguntar pelo ano):** [burned_areas_overlay.png](../results/figures/meeting_2026-10/burned_areas_overlay.png)

## 2. Ausências

**O problema:** o modelo precisa de exemplos com *Acacia* (presenças)
e sem *Acacia* (ausências), mas o iNaturalist só dá presenças. As
ausências têm de ser construídas.

**As duas opções:**
- **Pontos ao acaso:** simples, mas as presenças estão perto de
  estradas e caminhos e os pontos ao acaso não. O modelo pode aprender
  "perto de estrada vs. longe" em vez de "*Acacia* vs. outra planta".
- **Outras plantas do iNaturalist (proposta):** foram registadas pelas
  mesmas pessoas, nos mesmos sítios, por isso a única diferença que
  sobra é a planta. Chama-se fundo de grupo-alvo (Phillips et al.
  2009); melhorou os modelos em 226 espécies.

**O que já verifiquei:**
- 6 333 presenças e 77 301 observações de outras plantas (cerca de 12
  por presença), já sem as observações com localização escondida pelo
  iNaturalist (erros de quilómetros: 43 presenças e 8 242 outras
  plantas).
- A pessoa dominante também regista outras plantas: 33 065
  observações (43%), em 97% das quadrículas de 1 km onde viu
  *Acacia*. Ou seja, as outras plantas cobrem os mesmos sítios.
- Mas cobrem muito mais território: só 26% das quadrículas com
  outras plantas têm *Acacia*.

**Limitações:**
- Outra planta num ponto não prova que não há *Acacia* ao lado. Os
  resultados medem se o modelo separa a *Acacia* das outras plantas,
  não se acerta no terreno (ver ponto 4).
- A escolha das ausências muda o que a RQ3 mede.

**Decidir:**
- [ ] Usar outras plantas do iNaturalist como ausências?
- [ ] De todas as pessoas, ou só da pessoa dominante (mesmos sítios,
  menos dados)?

Decido eu e mostro depois: que plantas entram (todas ou só árvores e
arbustos), a que distância de uma *Acacia* as tiro, quantas ausências
por presença, e se comparo com pontos ao acaso na RQ3.

**Mostrar:** [presences_vs_background.png](../results/figures/meeting_2026-10/presences_vs_background.png)

## 3. Fine-tuning ou embeddings fixos

**O problema:** a proposta diz "fazer fine-tuning dos foundation
models". Eu uso os embeddings fixos com um classificador simples por
cima.

**Proposta:** manter os embeddings fixos e justificar na tese:
- O AlphaEarth só existe como embeddings; não dá para fazer
  fine-tuning.
- Os pesos do TESSERA têm de ser pedidos.
- Com poucos dados e com erros, o fine-tuning arrisca aprender os
  erros.
- O mesmo classificador (ex: Random Forest) em todas as representações isola o efeito da
  representação, que é o que a RQ1 mede. Se eu fizesse com fine tuning, o TESSERA seria treinado de novo e o Sentinel-2 não, então a comparação não seria justa.

Fine-tuning fica como extensão, se houver tempo.

**Decidir:**
- [ ] Aceita embeddings fixos como abordagem principal?
- [ ] Peço já os pesos do TESSERA?

## 4. Dados de especialistas

**O problema:** a RQ1 compara com um modelo treinado com dados de
especialistas (o teto). Sem ele, só mostro quão bons são os
foundation models, não quanto se perde com a ciência cidadã.

**MAP.INVADER** ([mapinvader.pt](https://mapinvader.pt/timeline/)):
os locais de referência só estão previstos para junho de 2027, e os
mapas (só *A. dealbata*) são de 2026–2028, não de 2023. Ainda não há
dados publicados. A exceção pode ser [Soriano et al. (EARSeL, setembro
de 2026)](https://mapinvader.pt/milestones-and-deliverables/), que já mapearam *A. dealbata* no centro de Portugal com
Sentinel, e por isso usaram dados de referência.

**Em aberto:**
- [ ] A minha questão é se temos esses dados de especialistas ou tenho de explorar um pouco mais, e tentar usar os da literatura ou se uso a classe "Florestas de acácias" da COS 2023?
- [ ] Com que dados testo, para a comparação ser justa? Talvez o OrtoSat 2023, só para teste: são imagens, não rótulos, por isso eu marcaria 200–300 pontos à mão (talvez revistos por alguém do projeto). Para treinar seriam precisos milhares. Dúvidas: as imagens são de abril a outubro, sem a floração da *A. dealbata*, e só o visualizador (WMS) é público.

## 5. Área de estudo

As observações cobrem o **distrito**, mas o TESSERA que descarreguei
só cobre o **concelho**. Tenho de descarregar o TESSERA de 2023.

**Decidir:**
- [ ] Distrito ou concelho?

---

As figuras estão em `results/`, que não vai para o Git: os links só
funcionam no meu computador. Para as voltar a gerar, correr o
[notebook 04](../notebooks/04_data_integration/background_and_disturbance_checks.ipynb).
