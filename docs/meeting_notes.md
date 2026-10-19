# Reunião com o Orientador — Outubro 2026

> Preparada a 2026-10-17. Reunião de 30 minutos: quatro pontos, por
> ordem de importância. Cada um explica o problema, traz uma proposta
> e termina com o que há a decidir. O resto fica para o fim, só se
> sobrar tempo.

| # | Ponto | Tempo |
|---|---|---|
| 1 | O piloto é um só observador (contexto) | 3 min |
| 2 | Ausências | 10 min |
| 3 | Ano de referência e janela | 7 min |
| 4 | Desenho da RQ2 | 7 min |
| — | Se sobrar tempo | 3 min |

**Ponto de partida:** o piloto são as observações de *Acacia* do
iNaturalist no distrito de Coimbra (7 943 registos, 1992–2026). A
ideia é treinar um classificador que, a partir da imagem de satélite
(Sentinel-2 ou embeddings de um modelo de fundação como o TESSERA),
diga se cada píxel de 10 m tem *Acacia*.

## 1. Abertura: o piloto é um só observador

> "Antes de tudo: quase todos os dados de *Acacia* em Coimbra vêm de
> uma única pessoa. Isso condiciona quase todas as decisões de hoje."

**O que encontrei:**
- Um único observador fez 83% de todos os registos, e 85% dos
  registos dentro da janela proposta (2021–2025, ver ponto 3).
- O pico de 2021 (43% de todos os registos estão nesse ano) é essa
  pessoa: fez 98% dos registos de 2021. Não é o efeito de mais gente
  a usar o iNaturalist, nem um bioblitz.
- Nos anos recentes pesa menos: 35% em 2023 e 31% em 2025.

**Porque importa:** o modelo aprende a partir dos sítios por onde esta
pessoa passou. Se ela percorre sobretudo certos caminhos ou zonas, o
mapa final pode refletir o seu percurso e não a distribuição real da
*Acacia*. Isto é exatamente o enviesamento espacial que a RQ3 estuda.

**Decidir:**
- [ ] O que fazer com este observador?
  - Manter os dados todos como estão.
  - Reduzir o seu peso, p. ex. limitar o número de registos por
    célula da grelha.
  - Usá-lo explicitamente na RQ3 como caso real de enviesamento.

**Mostrar:** [notebook 02](../notebooks/02_citizen_science/acacia_coimbra_pilot_exploration.ipynb)
— observações por ano (pico de 2021), mapa e concentração por
observador.

## 2. Ausências — a decisão com mais consequências

> "O iNaturalist só diz onde a *Acacia* foi vista, nunca onde não
> está. Para treinar um classificador preciso de exemplos negativos.
> Proponho usar observações de outras plantas."

**O problema:** um classificador binário precisa de exemplos
positivos (*Acacia*) e negativos (não-*Acacia*). O iNaturalist só tem
positivos. Os negativos têm de ser construídos — chamam-se
pseudo-ausências ou "fundo".

**As duas opções:**
- **Fundo aleatório:** pontos espalhados ao acaso pela área de estudo.
  É simples, mas as presenças concentram-se em sítios acessíveis
  (estradas, trilhos, periferias), e o fundo não. O modelo pode
  aprender "sítio acessível vs. sítio remoto" em vez de "*Acacia* vs.
  outra vegetação".
- **Fundo de grupo-alvo (proposta):** usar observações iNaturalist de
  outras plantas como negativos. Vêm dos mesmos observadores e dos
  mesmos sítios acessíveis, por isso têm o mesmo enviesamento que as
  presenças. A única diferença que sobra é a espécie, e é isso que o
  modelo tem de aprender. É a técnica proposta por Phillips et al.
  (2009), que melhorou os modelos em 226 espécies.

**O que já verifiquei:**
- Descarreguei as observações de outras plantas em 2021–2025: há
  6 333 presenças e 77 301 pontos de fundo (cerca de 12 por presença).
- Removi registos com coordenadas ofuscadas: o iNaturalist desloca
  de propósito a localização de alguns registos (por privacidade ou
  espécies sensíveis), com erros de quilómetros, o que os torna
  inúteis a 10 m. Foram 43 presenças e 8 242 pontos de fundo.
- O método só funciona se presenças e fundo vierem do mesmo processo
  de amostragem. Como 85% das presenças são de uma pessoa, verifiquei
  se ela também regista outras plantas. Regista: 33 065 registos, 43%
  do fundo. E em 97% das quadrículas de 1 km onde registou *Acacia*,
  também registou outras plantas. Ou seja, o fundo cobre os mesmos
  sítios que as presenças.
- Mas o contrário não é verdade: só 26% das quadrículas com fundo têm
  *Acacia*. O fundo cobre muito mais território, sobretudo o dos
  outros observadores.

**Ressalvas a assumir:**
- Pseudo-ausências não são ausências reais: um ponto de outra planta
  pode ter *Acacia* ao lado. As métricas medem quão bem o modelo
  separa *Acacia* do fundo, não a exatidão no terreno (ver validação independente, no fim).
- Como o grupo-alvo corrige parte do enviesamento, a escolha do fundo
  muda o que a RQ3 mede. Os resultados têm de dizer sempre qual fundo
  foi usado.

**Decidir:**
- [ ] Aprovar o fundo de grupo-alvo?
- [ ] Fundo de toda a comunidade, ou só os registos de outras plantas
  do observador dominante (mesma pegada, mas menos dados)?

Detalhes que proponho decidir eu e reportar depois: grupo-alvo (todas
as plantas vasculares ou só lenhosas), buffer de exclusão à volta das
*Acacia*, rácio presenças:fundo, e comparar grupo-alvo vs. aleatório
na RQ3.

**Mostrar:** [presences_vs_background.png](../results/figures/meeting_2026-10/presences_vs_background.png)
— presenças vs. fundo, observador dominante vs. restantes.

## 3. Ano de referência e janela temporal

> "Proponho fixar o tempo: todas as imagens de 2023, e só observações
> de 2021 a 2025."

**O problema:** as imagens de satélite e os embeddings são de um ano
concreto, mas as observações vão de 1992 a 2026. Se misturar anos, o
modelo pode aprender diferenças entre anos em vez da *Acacia*. A
análise do desfasamento temporal ficou fora do âmbito, por isso o
tempo tem de ser mantido constante.

**Proposta:**
1. **Ano de referência 2023** para tudo: Sentinel-2, TESSERA e
   COS/OrtoSat.
2. **Janela de observação 2021–2025** (2023 ± 2 anos), aplicada às
   presenças e ao fundo.

**Porquê 2023:** o OrtoSat só existe para 2023 e a COS 2023 é a
edição mais recente.

*Se perguntar "porque não um ano mais recente?":* 2 184 presenças
(34,5%) estão em áreas que arderam em 2025 (≈70 600 ha). Com 2023 o
píxel ainda mostra a vegetação observada; com 2025 (ou TESSERA 2025)
um terço dos rótulos cairia em solo queimado.

**Porquê ±2 anos:**

| Janela | Anos | Dados mantidos |
|---|---|---|
| só 2023 | 2023 | 3% |
| ±1 | 2022–2024 | 31% |
| ±2 | 2021–2025 | 80% |
| ±3 | 2020–2026 | 93% |

- ±1 perde 2021, onde está quase metade dos dados. ±2 é a primeira
  janela que mantém a maior parte.
- A *Acacia* é persistente: forma povoamentos que duram anos. Uma
  observação de 2021 ou 2025 indica que estava lá em 2023, salvo
  perturbação.
- Dizer abertamente: na prática, a janela serve sobretudo para manter
  os dados do observador dominante.

**Salvaguarda:** remover observações em áreas ardidas (ICNF) entre o
ano da observação e 2023, porque aí o píxel de 2023 já não mostra o
que foi observado. Testei: remove só 2 presenças e 33 pontos de fundo.

**Alternativa rejeitada:** associar cada observação à imagem do seu
próprio ano. Parece mais exato, mas as presenças ficariam com anos
misturados enquanto o fundo e o teste ficam noutro, e o modelo pode
aprender o ano em vez da espécie. Além disso, como cada zona foi
visitada em anos diferentes, o ano ficaria ligado à geografia, o que
confunde a RQ3.

**Decidir:**
- [ ] Aprovar 2023 com janela 2021–2025?
- [ ] Janela simétrica, ou assimétrica (p. ex. 2021–2026)?
  - A favor: um registo de 2025 é evidência mais forte de presença em
    2023 do que um de 2021, que pode ter sido cortado ou ardido
    depois.
  - Contra: depois dos fogos de 2025, um registo de 2025–2026 pode ser
    regeneração jovem, que não se parece com o povoamento de 2023. E
    2026 ainda está incompleto.

**Mostrar (só se perguntar pelo ano):** [burned_areas_overlay.png](../results/figures/meeting_2026-10/burned_areas_overlay.png)
— presenças e áreas ardidas 2021–2025.

## 4. Desenho da RQ2 (eficiência de dados)

> "A RQ2 não tira dados ao modelo final. É uma simulação: treino com
> cada vez menos dados para ver que representação aguenta melhor a
> escassez. Proponho fazê-la com subamostragem aleatória e deixar o
> filtro como comparação extra."

**O que a RQ2 faz:** treino os dois modelos (Sentinel-2 e TESSERA) com
100%, 50%, 25%, 10%, 5% e 1% dos dados e comparo como o desempenho cai.
O mapa final continua a usar todos os dados. Ter poucos dados de
ciência cidadã não é um argumento contra a RQ2, é a motivação dela:
se o modelo de fundação aguentar com poucos dados, serve para regiões
e espécies com poucas observações.

**O problema da formulação atual:** a RQ2 adotada pede que a redução
seja feita por um filtro que melhore a distribuição, e não ao acaso.
Nenhum candidato serve bem para isso:
- **Áreas ardidas:** com fogos até 2023 remove só 2 presenças; com
  todos até 2025 remove 34,5%, mas os fogos de 2025 são posteriores às
  imagens e a razão para remover é fraca.
- **Qualidade (*research grade*):** reduz, mas não melhora a
  distribuição espacial.
- **Rarefação espacial:** é o filtro que melhora a distribuição, mas
  já está na experiência da RQ3.

**Proposta:**
1. **Experiência principal: curva de aprendizagem com subamostragem
   aleatória.** Subconjuntos encaixados (cada nível contém o
   seguinte), repetidos com várias sementes e avaliados com validação
   espacial. É o desenho habitual; Ball et al. (2026) também treinaram
   com frações dos dados (com ≈5% chegaram perto do máximo).
2. **Comparação extra:** ao mesmo tamanho, um subconjunto filtrado dá
   melhor resultado do que um aleatório?
3. **O filtro de fogo fica como pré-processamento fixo** (ponto 3), não
   como filtro da RQ2.

**Decidir:**
- [ ] Reformular a RQ2 para subamostragem aleatória como experiência
  principal, com o filtro como comparação?
- [ ] Se sim, que filtro para a comparação: qualidade, ou outro?
- [ ] Quantas repetições por nível?

## Se sobrar tempo

Uma pergunta por tema; a explicação completa fica para a próxima
reunião.

- **Validação independente:** se treino e teste vêm do mesmo
  iNaturalist enviesado, o enviesamento fica escondido. Candidatos: a
  classe "Florestas de acácias" da COS 2023 (só povoamentos ≥ 1 ha) e
  o OrtoSat 2023 (30 cm, acesso restrito).
  - [ ] Que referência usar? Sabe como pedir acesso ao OrtoSat?
- **Área e espécies:** começo por Coimbra; os pilotos usam distrito
  (iNaturalist) e concelho (TESSERA). Na janela: *A. dealbata* 4 145,
  *A. melanoxylon* 1 611, *A. longifolia* 417.
  - [ ] Distrito ou concelho? Género *Acacia* ou uma só espécie?
- **Teste de sensibilidade da janela:** repetir a RQ1 com ±1, ±2 e ±3
  (com o mesmo número de observações) e ver se a ordenação dos modelos
  se mantém.
  - [ ] É uma verificação de robustez, não um estudo do desfasamento
    temporal. Concorda?
- **Tarefa de previsão (já adotada):** classificação binária por
  píxel, treinada nos pontos e aplicada a toda a área.
  - [ ] Confirmar.

---

As figuras estão em `results/`, que não vai para o Git: os links só
funcionam localmente. Para as regenerar, correr
[notebook 04](../notebooks/04_data_integration/background_and_disturbance_checks.ipynb).
