# Video Spec Kit

🇺🇸 [Read in English](README.md)

**Especifique antes de escrever o prompt.** Transforme uma ideia vaga de vídeo
gerado por IA em uma especificação clara, estruturada e versionada — e compile
essa especificação em prompts ajustados para cada modelo de vídeo.

```
$video Uma mulher anda de bicicleta por Tóquio à noite, sob chuva forte.
```

→ duas perguntas certeiras → uma scene spec, um storyboard, uma shot spec, um
prompt para Wan, um prompt para LTX e configurações de geração reproduzíveis.
Você gera o clipe na sua própria ferramenta, descreve o que viu, e o kit ajuda
a corrigir **uma variável por vez**.

> O Video Spec Kit **não** gera vídeo. Ele é um conjunto de skills em Markdown,
> schemas, templates e adapters de modelo que rodam dentro do agente de código
> que você já usa. Sem backend, sem API, nada pago obrigatório.

Já tem um roteiro? Cole um trecho do roteiro em vez de uma ideia —
`$video-screenplay` transforma o trecho em shots e prompts sem inventar história.

---

## Sumário

- [O problema](#o-problema)
- [A proposta](#a-proposta)
- [Filosofia](#filosofia)
- [Instalação](#instalação)
- [Início rápido](#início-rápido)
- [Exemplo](#exemplo)
- [A partir de um roteiro](#a-partir-de-um-roteiro)
- [Fluxo de trabalho](#fluxo-de-trabalho)
- [Estrutura de arquivos](#estrutura-de-arquivos)
- [Agentes suportados](#agentes-suportados)
- [Modelos suportados](#modelos-suportados)
- [Criar um adapter](#criar-um-adapter)
- [Criar um preset](#criar-um-preset)
- [Idiomas](#idiomas)
- [Contribuindo](#contribuindo)
- [Roadmap](#roadmap)
- [Como este projeto foi feito](#como-este-projeto-foi-feito)
- [Licença](#licença)

---

## O problema

Escrever prompts para um modelo de vídeo costuma ser assim: escreve um
parágrafo, gera (minutos de GPU), algo sai errado, reescreve o parágrafo
inteiro, gera de novo. Depois de dez tentativas:

- você não sabe qual mudança consertou o quê — nem o que quebrou;
- o modelo preencheu ao acaso tudo que você não especificou (câmera, luz, figurino…);
- o prompt que funcionou no Wan não funciona no LTX;
- a personagem fica diferente em cada clipe;
- você não consegue reproduzir o melhor resultado da semana passada porque não anotou a seed.

## A proposta

Tratar o vídeo como software construído a partir de uma especificação:

1. **Esclarecer** só as decisões que mudam o vídeo por completo.
2. **Especificar** a cena em YAML estruturado — a fonte da verdade.
3. **Planejar** o tempo (storyboard) e o shot (câmera, lente, enquadramento, início/fim).
4. **Compilar** a especificação em um prompt por modelo, com um *prompt adapter*.
5. **Gerar** na sua ferramenta (ComfyUI, uma CLI, qualquer uma).
6. **Revisar** o que você viu e receber um diagnóstico ligado aos campos da spec.
7. **Iterar** com um experimento controlado: uma mudança, mesma seed, diff registrado.

```
IDEIA → CLARIFY → SCENE SPEC → STORYBOARD → SHOT SPEC → PROMPT DO MODELO
      → (você gera) → REVIEW → ITERATE
```

Inspirado na filosofia do Spec Kit do GitHub (desenvolvimento orientado a
especificação), aplicada a vídeo — sem depender dele.

## Filosofia

1. Especifique antes de escrever o prompt.
2. Separe a intenção da sintaxe do modelo.
3. Esclareça só o que importa.
4. Prefira especificações estruturadas.
5. Prompts são artefatos compilados.
6. Preserve a continuidade.
7. Mude uma variável por vez.
8. Registre os experimentos.
9. Torne a geração reproduzível.
10. Continue agnóstico em relação ao modelo.

Cada princípio e como o kit o implementa: [docs/philosophy.md](docs/philosophy.md) (em inglês).

## Instalação

Você precisa de:

- **git**, e
- **um agente de código** capaz de ler e escrever arquivos numa pasta — Codex,
  Claude Code, Gemini CLI, OpenCode ou qualquer outro (planos gratuitos e
  modelos locais funcionam; veja [Agentes suportados](#agentes-suportados)).

```bash
git clone https://github.com/<sua-org>/video-spec-kit.git
cd video-spec-kit
```

Só isso. Sem pacotes, sem build. Extras opcionais:

- `pip install pyyaml jsonschema` → `python tools/validate.py` valida suas specs.
- VS Code + extensão YAML → validação de schema em tempo real enquanto você
  edita (configurada em `.vscode/settings.json`).

## Início rápido

1. Abra o agente **na pasta do repositório**:

   ```bash
   codex        # ou: claude · gemini · opencode
   ```

2. Descreva o seu vídeo:

   | Agente | Digite |
   |--------|--------|
   | Codex | `$video Uma samurai caminha por Tóquio sob chuva forte à noite.` |
   | Claude Code, Gemini CLI | `/video Uma samurai caminha por Tóquio sob chuva forte à noite.` |
   | OpenCode | `Use a skill video: uma samurai caminha por Tóquio sob chuva forte à noite.` |
   | Qualquer outro agente | `Leia .agents/skills/video/SKILL.md e siga: uma samurai caminha…` |

   Escreva em qualquer idioma — o agente faz as perguntas no seu idioma e
   mantém as specs e os prompts em inglês.

3. Responda às (poucas) perguntas. O agente grava seus arquivos em
   `projects/<nome>/scenes/scene-001/v001/` e mostra os prompts.

4. Cole `prompts/wan.txt` (ou `ltx.txt`) na sua ferramenta de vídeo, use as
   configurações de `generation-config.yaml` e anote a seed.

5. Conte ao agente o que você viu:

   ```
   $video a câmera ficou ótima, mas o rosto dela muda no meio do vídeo
   ```

   Ele escreve um review, propõe uma única mudança e, quando você responde
   "sim", cria a `v002` só com essa mudança.

## Exemplo

[`examples/tokyo-rain/`](examples/tokyo-rain/) é uma execução completa e
versionada: ideia → clarify → spec → storyboard → shot → prompts Wan + LTX →
generation config → review → experimento v002 → review.
Comece pelo [walkthrough](examples/tokyo-rain/walkthrough.md).

O mesmo shot compilado para dois modelos (os prompts ficam em inglês):

**Wan** (`v001/prompts/wan.txt`, 134 palavras, começa pelo shot, usa negative prompt)

> Medium tracking shot at eye level. A Japanese woman in her late 20s with a
> short black bob, wearing a translucent yellow raincoat over a charcoal hoodie,
> dark jeans and white sneakers, carrying a small red backpack, rides a bicycle
> steadily through heavy rain, tired but determined, … The camera tracks
> alongside her from the left at her speed, keeping her centered. …

**LTX** (`v001/prompts/ltx.txt`, 174 palavras, começa pela ação, em ordem cronológica)

> A woman rides a bicycle steadily through heavy rain along a narrow Tokyo side
> street at night. She is a Japanese woman in her late 20s with a short black
> bob, … Her legs pedal at a steady rhythm and her upper body leans slightly
> forward against the rain. …

E o experimento que corrigiu o rosto (`v002/iteration.md`):

```diff
  timeline.beats[1].description:
-   She glances toward the camera for a moment, then looks back at the road ahead …
+   She keeps her eyes on the road ahead and leans slightly into the pedals …
```

Seed, modelo e configurações inalterados → o resultado pode ser atribuído a essa única linha.

## A partir de um roteiro

```
$video-screenplay --duration 5

INT. COZINHA - NOITE

Maria entra lentamente na cozinha.
A luz da geladeira aberta ilumina seu rosto.
Ela percebe um copo quebrado no chão.

MARIA
João?

Um barulho vem do corredor.
Maria congela.
```

A skill:

- interpreta sluglines (`INT.`/`EXT.`), local, horário, personagens, ações,
  diálogos, parentéticos, transições e indicações de câmera;
- separa o que é **visível** do que não é (pensamentos, memórias, sons);
- mantém os beats na ordem do roteiro;
- avisa que 5 beats visuais não cabem em um clipe de 5 segundos e oferece
  **dividir**, **reduzir** ou **aumentar a duração**;
- depois que você escolhe "dividir", grava três cenas comuns (entrada na luz da
  geladeira · insert do copo quebrado · chamado, barulho e congelamento) com
  prompts para Wan e LTX.

`"João?"` é preservado exatamente como está, mas não é falado pelo modelo; o
barulho é apenas uma pista sonora (motiva a reação, nunca vira imagem); e
ninguém aparece no corredor, porque João só é mencionado.

Quando o roteiro traz uma informação interna — por exemplo, *"Carlos se lembra
de tudo que o pai disse"* —, a skill não a transforma literalmente em imagem.
Ela decide se isso já está evidente nos outros beats, se dá para mostrar só com
atuação sutil (registrado como suposição) ou se precisa perguntar a você como
representar: close e mudança de expressão, flashback, objeto ligado à memória
ou nenhuma representação explícita.

Também funciona como `$video_from_screenwright` e `$video-from-screenplay`.

> **Sobre o nome:** a skill foi pedida como `video_from_screenwright`, mas
> *screenwright* não é um termo usado em inglês (roteiro é *screenplay*;
> roteirista é *screenwriter*), e nomes de skill só aceitam letras minúsculas,
> números e hífens. Por isso o nome canônico é `video-screenplay`, e
> `video_from_screenwright` continua funcionando como alias.

Guia: [docs/screenplay.md](docs/screenplay.md) (em inglês) · exemplos:
[shot único](examples/screenplay-rooftop/walkthrough.md),
[três shots, PT-BR](examples/screenplay-kitchen/walkthrough.md).

## Fluxo de trabalho

A maioria das pessoas só usa **`video`**. Ele roda o pipeline inteiro e
encaminha o seu feedback. As outras skills dão controle fino:

| Skill | Para quê |
|-------|----------|
| `video` | Orquestrador: ideia → arquivos; feedback → review → iteração. |
| `video-clarify` | Encontra as ambiguidades que importam e pergunta só essas (CRÍTICAS vs OPCIONAIS). |
| `video-character` | Personagens reutilizáveis, com trava de consistência e uma âncora de prompt repetida literalmente. |
| `video-scene` | Escreve a `scene-spec.yaml`, a fonte da verdade, com proveniência em cada valor. |
| `video-storyboard` | Primeiro frame, 1 a 3 beats com tempo, último frame. |
| `video-shot` | Câmera, lente, movimento, enquadramento; aplica presets/personagens; detecta conflitos. |
| `video-prompt` | Compila para um modelo: `$video-prompt wan`, `$video-prompt ltx`. |
| `video-review` | Diagnostica uma geração a partir da sua descrição. |
| `video-iterate` | Nova versão, uma mudança, mesma seed, diff registrado. |
| `video-screenplay` | Trecho de roteiro → análise visual → divisão em shots → scene specs → prompts. Aliases: `video_from_screenwright`, `video-from-screenplay`. |

Detalhes: [docs/workflow.md](docs/workflow.md) ·
como os prompts são compilados: [docs/prompt-compiler.md](docs/prompt-compiler.md) (em inglês).

### Você sempre sabe o que disse e o que o agente escolheu

Todo valor numa spec tem proveniência:

```yaml
provenance:
  user:     [camera.movement, environment.weather, environment.time_of_day]
  inferred: [camera.movement_detail, presets.lighting]
  default:  [format.duration_s, format.aspect_ratio, format.fps]
```

`user` = você disse · `screenplay` = está escrito no seu trecho de roteiro ·
`inferred` = deduzido do que você disse · `default` = padrão do kit que você nunca mencionou.

## Estrutura de arquivos

```
video-spec-kit/
├── AGENTS.md  CLAUDE.md  GEMINI.md     # entradas dos agentes (todas apontam para AGENTS.md)
├── .agents/skills/<skill>/SKILL.md     # as 10 skills — fonte canônica
├── .claude/{skills,commands}/  .gemini/commands/  # wrappers gerados + aliases
├── kit/
│   ├── conventions.md                  # layout, versionamento, proveniência, política de idiomas
│   ├── defaults.yaml                   # defaults + regras de inferência
│   └── vocabulary.md                   # termos controlados de câmera/estilo
├── schemas/*.schema.json               # JSON Schema (draft 2020-12)
├── templates/                          # esqueletos de todos os arquivos gerados
├── adapters/
│   ├── wan/  adapter.md  prompt-template.md
│   ├── ltx/  adapter.md  prompt-template.md
│   └── _template/
├── presets/{styles,cameras,lighting}/*.yaml
├── projects/                           # SEU trabalho fica aqui
├── examples/
│   ├── tokyo-rain/                     # ideia → v001 → review → v002
│   ├── screenplay-rooftop/             # roteiro → um shot
│   └── screenplay-kitchen/             # roteiro (PT-BR) → três shots
├── docs/                               # filosofia, fluxo, compilador, roteiro, agentes, extensão, comfyui
└── tools/                              # opcionais: validate.py, sync_agent_wrappers.py
```

Como fica uma cena no seu projeto:

```
projects/<projeto>/
  project.yaml
  characters/<id>.yaml
  screenplay/excerpt-001/      # só quando você parte de um roteiro
    source-screenplay.md       # o trecho original, sem alterações
    screenplay-analysis.yaml   # beats, diálogos, sons, info não visual, divisão em shots
  scenes/scene-001/
    history.md                 # uma linha por versão: mudança → resultado → veredito
    v001/
      scene-spec.yaml          # fonte da verdade
      storyboard.md            # beats ao longo do tempo
      shot-spec.yaml           # resolvida + checada contra conflitos (IR do compilador)
      prompts/wan.txt  wan.negative.txt  ltx.txt  ltx.negative.txt
      generation-config.yaml   # modelo, seed, tamanho, frames, steps, CFG, sampler…
      comfyui-notes.md         # opcional
      review.md                # depois que você gera
    v002/ … + iteration.md     # o que mudou e por quê
```

Cada pasta de versão é autocontida e fica congelada depois do review, então
todo resultado continua reproduzível. Regras: [kit/conventions.md](kit/conventions.md) (em inglês).

## Agentes suportados

| Agente | Onde encontra as skills | Como chamar |
|--------|-------------------------|-------------|
| Codex | `.agents/skills/` (nativo) | `$video …` |
| Claude Code | `.claude/skills/` (wrappers gerados) | `/video …` |
| Gemini CLI | `.agents/skills/` + `.gemini/commands/` | `/video …` |
| OpenCode | `.agents/skills/` (nativo) | "use a skill video: …" |
| Qualquer outro | `AGENTS.md` | "Leia `.agents/skills/video/SKILL.md` e siga: …" |

As skills seguem o formato aberto Agent Skills (`SKILL.md` + frontmatter com
`name`/`description`). Os wrappers são gerados por script, então cada skill
existe em um único lugar. Mais detalhes, inclusive dicas para modelos locais:
[docs/agent-support.md](docs/agent-support.md) (em inglês).

## Modelos suportados

| Adapter | Modelos | Estilo do prompt | Negative prompt | Observações |
|---------|---------|------------------|-----------------|-------------|
| [`wan`](adapters/wan/adapter.md) | Wan 2.1, Wan 2.2 (T2V, I2V, TI2V-5B, FLF2V) | Shot → sujeito → ação → cenário → câmera → luz → estilo; 80–150 palavras | Sim (lista oficial, adaptada) | 16 fps / 81 frames (4n+1) nos modelos 14B |
| [`ltx`](adapters/ltx/adapter.md) | LTX-Video 0.9.x, 13B; LTX-2 | Ação primeiro, cronológico, literal; 100–180 palavras | Sim, com CFG > 1 | 24 fps, frames 8n+1, tamanhos ÷ 32 |

Os dois são modelos de pesos abertos que você pode rodar localmente (por
exemplo, no ComfyUI). A spec não depende de modelo; adicionar um modelo
significa adicionar uma pasta de adapter. Uso com ComfyUI:
[docs/comfyui.md](docs/comfyui.md) (em inglês).

> As configurações dos adapters (steps, CFG, shift…) são pontos de partida
> documentados a partir da documentação pública dos modelos. O seu workflow
> pode ser diferente — o kit registra o que você realmente usou.

## Criar um adapter

```bash
cp -r adapters/_template adapters/<id-do-modelo>
```

Preencha o perfil no frontmatter (orçamento de palavras, ordem dos slots,
negative prompt, regra de frames, tamanhos por proporção, defaults do sampler)
e as seções de orientação (câmera, movimento, imagens de referência,
consistência temporal, diálogo e som, duração, limitações). Depois rode
`$video-prompt <id-do-modelo>`.
Guia completo: [docs/extending.md](docs/extending.md#create-a-prompt-adapter) (em inglês).

## Criar um preset

```yaml
# presets/lighting/blue-hour.yaml
spec_version: 1
id: blue-hour
kind: lighting
description: Deep blue twilight after sunset; city lights just turning on.
values:
  lighting:
    type: residual skylight plus early street lights
    contrast: medium
    color_temperature: mixed
```

Use numa cena com `presets: { lighting: blue-hour }`; qualquer campo definido
explicitamente na cena sobrescreve o preset.
Guia completo: [docs/extending.md](docs/extending.md#create-a-preset) (em inglês).

## Idiomas

- Você pode escrever ideias e roteiros em **qualquer idioma**.
- O agente faz as perguntas e os relatórios **no seu idioma**.
- As specs são normalizadas para **inglês** internamente, para ficarem
  comparáveis entre projetos e colaboradores.
- Os prompts saem em **inglês**, a não ser que o adapter do modelo indique
  outro idioma porque o modelo se beneficia dele.
- Nunca são traduzidos: a sua ideia original, o trecho de roteiro, nomes
  próprios, falas e textos que precisam aparecer dentro da imagem.

Regra completa: `kit/conventions.md` §7.

## Contribuindo

Adapters para mais modelos, presets, traduções da documentação e relatos de
"o que realmente funcionou" são as contribuições mais valiosas.
Veja [CONTRIBUTING.md](CONTRIBUTING.md) (em inglês).

## Roadmap

Planejado — e de propósito **fora** da V1:

- [ ] Integração automática com ComfyUI (enviar uma versão para um ComfyUI em execução)
- [ ] Importar/exportar workflows do ComfyUI a partir de/para `generation-config.yaml`
- [ ] Avaliação multimodal automática dos clipes gerados
- [ ] Comparação de frames entre versões
- [ ] Integração direta com modelos de vídeo locais
- [ ] Uma CLI própria (`vsk new`, `vsk compile`, `vsk diff`)
- [ ] Instalador de pacote (adicionar o kit a um repositório existente)
- [ ] Marketplace / registro de adapters
- [ ] Presets da comunidade
- [ ] Editor de timeline / história entre cenas
- [ ] Geração multi-shot em um único clipe

## Como este projeto foi feito

Este projeto foi construído **principalmente com IA**. A arquitetura, as
skills, os schemas, os adapters, os exemplos e a documentação foram gerados
por um agente de código com IA (Claude, no Claude Code), a partir de
especificações detalhadas escritas pelo mantenedor, que conduziu o design,
definiu os requisitos e revisou o resultado. Os arquivos do kit foram checados
com o validador incluído, mas as configurações de Wan/LTX não foram testadas em
gerações reais — trate-as como pontos de partida documentados — e os reviews
dos exemplos são fictícios. Correções de quem roda esses modelos são
especialmente bem-vindas.

## Licença

[Apache License 2.0](LICENSE). Escolhida em vez da MIT porque é igualmente
permissiva (uso comercial, modificação, redistribuição) e acrescenta uma
concessão explícita de patentes e termos claros para contribuições — útil para
um projeto que espera receber adapters e presets de muitas pessoas.
