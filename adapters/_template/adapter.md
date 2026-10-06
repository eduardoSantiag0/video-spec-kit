# <Model> adapter

Copy this folder to `adapters/<your-model-id>/` and fill in each section
below as plain guidance the `video` skill can follow when composing a
prompt from the accumulated scene facts. No frontmatter, no compiler
profile — just tell the agent how this model likes to be prompted.

## Shape

What order the information should come in, roughly how long the prompt
should be (a word range), and whether it's one paragraph, a tag list, or
structured sections.

## Negative prompt

Whether this model uses one, and what belongs in it (a short quality list is
typical). Say when it stops mattering (e.g. at CFG = 1 on distilled checkpoints).

## Camera & motion

How this model likes camera movement and motion described — any verbs or
phrasing it responds well or badly to.

## Dialogue and sound

Whether this model can generate audio. If not, say so plainly: dialogue and
sound effects must never appear as words in the prompt, only as visible
action/reaction.

## Duration and limitations

Any hard constraints (frame-count rule, fps, size divisibility) and known
weak spots (hands, text, fast motion, exact counts...).

## Language

Which languages this model is well-documented for, and whether the kit's
default (compile in the user's language, or English if unspecified) needs a
caveat here.
