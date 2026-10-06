# Video Spec Kit

🇺🇸 [Read in English](README.md)

Video Spec Kit é um assistente conversacional para criação de prompts de
vídeo com IA. Descreva sua cena, refine conversando e gere um prompt
pronto para modelos de vídeo como Wan e LTX.

```
$video

> Quero um homem dirigindo numa estrada.

> Como ele é e onde está a câmera?

> 23 anos, machucado. Câmera fixa dentro do carro.

> Quero que seja cinematográfico, 35mm.

> Gera.

<PROMPT FINAL>
```

> O Video Spec Kit **não** gera vídeo. É um conjunto de skills em Markdown
> que rodam dentro do agente de código que você já usa (Claude Code, Codex,
> Gemini CLI, OpenCode...). Sem backend, sem API, nada pago obrigatório.

Já tem um roteiro? Cole um trecho em vez de uma ideia — `$video-screenplay`
lê o trecho e entra na mesma conversa.

---

## Sumário

- [Por quê](#por-quê)
- [Filosofia](#filosofia)
- [Instalação](#instalação)
- [Início rápido](#início-rápido)
- [A partir de um roteiro](#a-partir-de-um-roteiro)
- [Skills](#skills)
- [Como a memória funciona](#como-a-memória-funciona)
- [Estrutura de arquivos](#estrutura-de-arquivos)
- [Agentes suportados](#agentes-suportados)
- [Modelos suportados](#modelos-suportados)
- [Criar um adapter](#criar-um-adapter)
- [Idiomas](#idiomas)
- [Limitações](#limitações)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## Por quê

Escrever prompt para um modelo de vídeo costuma significar escrever um
parágrafo gigante de uma vez, torcer pra cobrir tudo, e reescrever tudo de
novo quando não cobre. Conversar em vez disso — algumas perguntas, algumas
correções, depois "gera" — é mais parecido com como você de fato orientaria
um diretor de fotografia.

## Filosofia

1. Conversa antes do prompt.
2. Pergunte só o que importa.
3. Lembre do que o usuário já disse.
4. Deixe o usuário refinar naturalmente.
5. O estado estruturado fica nos bastidores.
6. O resultado final é o prompt.
7. Nunca obrigue o usuário a agir como programador.
8. Mantenha a ferramenta simples.

## Instalação

Você precisa de:

- **git**, e
- **um agente de código** capaz de ler e escrever arquivos numa pasta —
  Claude Code, Codex, Gemini CLI, OpenCode, ou qualquer outro que leia
  Agent Skills.

```bash
git clone https://github.com/<sua-org>/video-spec-kit.git
cd video-spec-kit
```

Só isso. Sem pacotes, sem build, sem validador de schema para instalar.

## Início rápido

1. Abra o agente **na pasta do repositório**:

   ```bash
   claude        # ou: codex · gemini · opencode
   ```

2. Descreva sua cena:

   | Agente | Digite |
   |--------|--------|
   | Claude Code, Gemini CLI | `/video Um homem dirigindo numa estrada rural ao entardecer.` |
   | Codex, OpenCode | `$video Um homem dirigindo numa estrada rural ao entardecer.` |
   | Qualquer outro agente | `Leia .agents/skills/video/SKILL.md e siga: um homem dirigindo…` |

   Escreva em qualquer idioma — o agente faz as perguntas no seu idioma.

3. Responda a uma ou duas perguntas realmente necessárias. Ele guarda tudo
   que você disser.

4. Continue a conversa: adicione detalhes, corrija algo ("troca a camiseta
   para cinza") ou peça ajuda criativa ("deixa mais tenso").

5. Diga "gera" / "gera para Wan" quando estiver pronto. Você recebe um
   prompt finalizado, pronto para colar na sua ferramenta de vídeo.

## A partir de um roteiro

```
$video-screenplay

INT. COZINHA - NOITE

Maria entra lentamente na cozinha.
A luz da geladeira aberta ilumina seu rosto.
Ela percebe um copo quebrado no chão.
```

A skill lê a slugline, os personagens e a ação visível, grava na mesma
memória que o `video` usa, e só pergunta o que o roteiro realmente não
responde (geralmente câmera e visual). A partir daí é a mesma conversa —
corrija, adicione, depois "gera".

Também disponível como `$video_from_screenwright` e `$video-from-screenplay`.
Exemplo: [`examples/screenplay/`](examples/screenplay/).

## Skills

| Skill | Para quê |
|-------|----------|
| `video` | Entrada principal: ideia → conversa → prompt. |
| `video-screenplay` | Trecho de roteiro → mesma conversa. Aliases: `video_from_screenwright`, `video-from-screenplay`. |
| `video-reset` | Limpa a cena atual e começa uma nova. |

Como o loop funciona por dentro: [docs/how-it-works.md](docs/how-it-works.md) (em inglês).

## Como a memória funciona

Tudo que você disser sobre a cena fica em `.video/session.yaml` — sujeito,
ação, ambiente, câmera, luz, estilo. Você nunca precisa abrir esse arquivo;
não é algo para editar, é só a memória do agente sobre a conversa. Uma
correção sempre substitui o valor antigo, nada é perguntado duas vezes, e
`$video-reset` limpa tudo para uma cena nova.

```yaml
scene:
  subject: { type: man, age: 23, condition: [bruised], clothing: { top: dark grey t-shirt } }
  action: { primary: driving a car }
  environment: { location: rural highway, weather: hot sunny day }
  camera: { position: inside car, framing: medium shot, movement: static }
  style: { realism: photorealistic, look: cinematic }
```

Exemplo completo de conversa e o prompt que ela gerou:
[`examples/conversation/`](examples/conversation/).

## Estrutura de arquivos

```
video-spec-kit/
├── README.md  README.pt-BR.md
├── AGENTS.md  CLAUDE.md  GEMINI.md     # entradas dos agentes (todas apontam para AGENTS.md)
├── .agents/skills/<skill>/SKILL.md     # as 3 skills — fonte canônica
├── .claude/{skills,commands}/  .gemini/commands/  # wrappers gerados + aliases
├── adapters/
│   ├── wan/adapter.md
│   ├── ltx/adapter.md
│   └── _template/adapter.md
├── templates/
│   └── session.yaml                    # o vocabulário de campos que .video/session.yaml usa
├── examples/
│   ├── conversation/                   # ideia → conversa → prompt
│   └── screenplay/                     # roteiro → conversa → prompt
├── docs/
│   └── how-it-works.md                 # (em inglês)
├── projects/                           # opcional: suas próprias anotações, se quiser
└── tools/
    └── sync_agent_wrappers.py          # regenera os wrappers gerados acima
```

Em tempo de execução, o único estado que o kit escreve é
`.video/session.yaml` (fora do controle de versão — veja `.gitignore`), na
pasta de onde você roda o agente.

## Agentes suportados

| Agente | Onde encontra as skills | Como chamar |
|--------|-------------------------|-------------|
| Claude Code | `.claude/skills/` (wrappers gerados) | `/video …` |
| Gemini CLI | `.agents/skills/` + `.gemini/commands/` | `/video …` |
| Codex, OpenCode | `.agents/skills/` (nativo) | `$video …` |
| Qualquer outro | `AGENTS.md` | "Leia `.agents/skills/video/SKILL.md` e siga: …" |

As skills seguem o formato aberto Agent Skills (`SKILL.md` + frontmatter com
`name`/`description`). Os wrappers são gerados, então cada skill existe em
um único lugar.

## Modelos suportados

| Adapter | Modelos | Observações |
|---------|---------|-------------|
| [`wan`](adapters/wan/adapter.md) | Wan 2.1 / 2.2 (T2V, I2V) | 80–150 palavras, negative prompt, 16 fps / 81 frames |
| [`ltx`](adapters/ltx/adapter.md) | LTX-Video 0.9.x / 13B, LTX-2 | 100–180 palavras, negative prompt (CFG > 1), 24 fps |

Os dois são modelos de pesos abertos que você pode rodar localmente (ex.:
ComfyUI). Adicionar um modelo significa adicionar uma pasta de adapter — o
kit continua agnóstico em relação ao modelo.

## Criar um adapter

```bash
cp -r adapters/_template adapters/<id-do-modelo>
```

Preencha a orientação em linguagem simples (formato, negative prompt,
câmera/movimento, diálogo e som, duração, limitações, idioma). Sem
frontmatter, sem perfil de compilador para manter — a skill lê o arquivo
diretamente.

## Idiomas

- Descreva sua cena em **qualquer idioma**; o agente pergunta e responde
  nesse idioma.
- A memória interna é normalizada para inglês para o agente raciocinar de
  forma consistente — você nunca vê isso.
- O prompt final sai por padrão em **inglês** (os modelos de vídeo são mais
  bem documentados nele); peça outro idioma ("gera em português") e você o
  recebe.
- Nunca são traduzidos: nomes próprios, diálogos e textos que precisam
  aparecer dentro da imagem.

## Limitações

- Sem versionamento, controle de seed ou registro de reprodutibilidade —
  se você precisar disso para suas próprias anotações, mantenha por conta própria.
- A orientação dos adapters foi escrita a partir da documentação pública
  dos modelos, não verificada contra gerações reais. Correções de quem
  realmente roda esses modelos são bem-vindas.
- Uma cena por vez. Um trecho de roteiro que precisa de vários shots é
  tratado um de cada vez, não em lote.

## Contribuindo

Adapters para mais modelos e relatos de "o que realmente funcionou" são as
contribuições mais valiosas. Veja [CONTRIBUTING.md](CONTRIBUTING.md) (em inglês).

## Licença

[Apache License 2.0](LICENSE).
