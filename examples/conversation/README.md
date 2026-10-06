# Example: idea → conversation → prompt

A complete `$video` run, start to finish, with the state it accumulates and
the final prompt it produces.

```
User: $video Quero uma cena de um homem dirigindo em uma estrada rural.

Agent: Como é esse homem? E a câmera está dentro ou fora do carro?

User: Ele tem 23 anos, está machucado e assustado. O carro está andando.
      A câmera está fixa dentro do carro, plano médio, altura dos olhos.

Agent: Entendido. Você quer um visual mais realista ou estilizado?

User: O dia está quente e ensolarado e quero um visual cinematográfico e
      realista, tipo 35mm.

Agent: Anotado — homem de 23 anos, machucado e assustado, dirigindo numa
       estrada rural num dia quente e ensolarado; câmera fixa dentro do
       carro em plano médio na altura dos olhos; visual fotorrealista e
       cinematográfico, grão sutil de 35mm. Quer mudar algo ou já gero o
       prompt?

User: Troca a camiseta dele para cinza escuro.

Agent: Pronto — camiseta cinza escuro.

User: Gera para Wan.

Agent: <final prompt below>
```

## Accumulated state (`.video/session.yaml`) before generating

```yaml
scene:
  subject:
    type: man
    age: 23
    appearance:
      hair: short messy dark brown
    condition: [bruised, startled]
    clothing:
      top: plain dark grey t-shirt
    emotion: [anxious]
  action:
    primary: driving a car
  environment:
    interior_exterior: interior
    location: rural highway
    weather: hot sunny day
    background: [soybean fields]
  camera:
    position: inside car
    framing: medium shot
    angle: eye level
    movement: static
  lighting:
    source: daylight
    direction: front and above
    temperature: warm
  style:
    realism: photorealistic
    look: cinematic
    film_grain: subtle 35mm
meta:
  language: pt-BR
  last_model: wan
```

## Final prompt (`$video gera para Wan`)

> Medium shot at eye level, static camera locked inside a moving car. A
> 23-year-old man with short, messy dark brown hair, bruised and startled,
> wearing a plain dark grey t-shirt, drives steadily along a rural highway
> on a hot, sunny day, soybean fields passing in the background. The camera
> remains completely still, framing him from the passenger seat. Warm
> daylight falls on his face from the front and above, even and natural.
> Photorealistic, cinematic look with subtle 35mm film grain.

Negative prompt (Wan quality list, trimmed for a static shot):

> blurry details, subtitles, text, watermark, painting, still image,
> overall gray, worst quality, low quality, jpeg compression artifacts,
> ugly, extra fingers, poorly drawn hands, poorly drawn face, deformed,
> disfigured, malformed limbs, fused fingers
