# Example: screenplay excerpt → conversation → prompt

A complete `$video-screenplay` run.

```
User: $video-screenplay
      INT. COZINHA - NOITE
      Maria entra lentamente na cozinha.
      A luz da geladeira aberta ilumina seu rosto.
      Ela percebe um copo quebrado no chão.

Agent: Entendi — cozinha, de noite, Maria encontra um copo quebrado no chão.
       Só faltam duas coisas que fariam bastante diferença: como a câmera
       está posicionada, e que aparência visual você quer?

User: Quero que a cozinha seja velha e pequena. A câmera começa atrás dela.
      Visual realista, meio sombrio.

Agent: Anotado.

User: Gera o prompt.

Agent: <final prompt below>
```

## What was extracted from the screenplay

| Element | Value | Source |
|---|---|---|
| Location | kitchen, old and small | screenplay + user |
| Time | night | screenplay |
| Character | Maria, on screen | screenplay |
| Action (in order) | enters slowly → fridge light on her face → notices broken glass | screenplay |
| Camera | starts behind her | user |
| Look | realistic, slightly dark | user |

## Final prompt

> A woman enters slowly into a small, old kitchen at night, seen from
> behind as she steps forward. The open refrigerator's light washes over
> her face, pale and cool against the dark room. She looks down and notices
> a broken glass scattered on the floor, pausing mid-step. The camera starts
> behind her and holds steady as she moves deeper into the room. Lighting is
> low-key, mostly the cold glow from the fridge against the dim kitchen,
> realistic and slightly somber in tone.

Dialogue and sound: this excerpt has none in this beat — if a later line had
a "João?" call or a noise, it would be kept verbatim for continuity but
never turned into words or sound effects in the prompt (see
`.agents/skills/video-screenplay/SKILL.md` → Rules).
