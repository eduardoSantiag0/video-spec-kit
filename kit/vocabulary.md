# Controlled Vocabulary

Enumerated fields in the specs use these exact values (they are also the `enum`
lists in `schemas/`). Each term has a definition and a neutral natural-language
phrase. Adapters may rephrase the neutral phrase for their model.

Free-text fields (`lens`, `movement_detail`, `lighting.type`, ...) are not
restricted, but prefer these terms when one fits.

## camera.shot_size

| Value              | Definition                                      | Neutral phrase                 |
|--------------------|-------------------------------------------------|--------------------------------|
| `extreme-wide`     | Subject tiny; environment dominates             | extreme wide shot              |
| `wide`             | Full body plus a lot of environment             | wide shot                      |
| `medium-wide`      | Body from knees up                              | medium wide shot               |
| `medium`           | Body from waist up                              | medium shot                    |
| `medium-close-up`  | Chest and head                                  | medium close-up                |
| `close-up`         | Face fills most of the frame                    | close-up                       |
| `extreme-close-up` | A detail (eyes, hands, object)                  | extreme close-up               |

## camera.angle

| Value               | Definition                                | Neutral phrase                   |
|---------------------|-------------------------------------------|----------------------------------|
| `eye-level`         | Camera at subject eye height              | eye-level angle                  |
| `low`               | Camera below, looking up                  | low angle looking up             |
| `high`              | Camera above, looking down                | high angle looking down          |
| `overhead`          | Directly above (top-down)                 | top-down overhead view           |
| `ground-level`      | Camera near the ground                    | ground-level camera              |
| `dutch`             | Camera rolled/tilted on its axis          | dutch angle, tilted horizon      |
| `over-the-shoulder` | Behind one subject, framing another       | over-the-shoulder shot           |
| `pov`               | Through the subject's eyes                | first-person point of view       |

## camera.movement

One primary movement per shot. Use `movement_detail` for direction, target,
and distance in plain words.

| Value            | Definition                                            | Neutral phrase                              |
|------------------|-------------------------------------------------------|---------------------------------------------|
| `static`         | Camera does not move (locked off)                     | static camera, locked-off shot              |
| `pan`            | Rotates left/right on a fixed point                   | the camera pans                             |
| `tilt`           | Rotates up/down on a fixed point                      | the camera tilts                            |
| `dolly-in`       | Physically moves toward the subject                   | the camera slowly pushes in                 |
| `dolly-out`      | Physically moves away from the subject                | the camera slowly pulls back                |
| `truck`          | Moves sideways, parallel to the scene                 | the camera trucks sideways                  |
| `tracking-follow`| Follows the subject from behind                       | the camera follows from behind              |
| `tracking-lead`  | Moves backward in front of an approaching subject     | the camera leads in front, moving backward  |
| `tracking-side`  | Moves alongside the subject at matching speed         | the camera tracks alongside                 |
| `orbit`          | Circles around the subject                            | the camera orbits around                    |
| `crane-up`       | Rises vertically                                      | the camera rises upward                     |
| `crane-down`     | Descends vertically                                   | the camera descends                         |
| `zoom-in`        | Lens zoom toward subject (no camera travel)           | slow zoom in                                |
| `zoom-out`       | Lens zoom away from subject                           | slow zoom out                               |
| `handheld`       | Operator-held, small organic shake; may also follow   | handheld camera with subtle natural shake   |
| `drone`          | Aerial flying camera                                  | aerial drone shot flying                    |

`handheld` describes the camera *feel*. If the handheld camera also travels,
describe the travel in `movement_detail` ("handheld, following from behind").

## camera.movement_speed

`very-slow`, `slow`, `moderate`, `fast`.

## camera.depth_of_field

| Value      | Neutral phrase                                         |
|------------|--------------------------------------------------------|
| `shallow`  | shallow depth of field, background softly blurred      |
| `moderate` | moderate depth of field                                 |
| `deep`     | deep focus, foreground and background sharp             |

## motion.pace

`calm`, `moderate`, `energetic`. Describes how much changes per second in the
whole frame (subject + background + camera).

## lighting.contrast

`low`, `medium`, `high`.

## lighting.color_temperature

`warm`, `neutral`, `cool`, `mixed` (e.g. warm practicals against cool ambient).

## style.realism

| Value                | Meaning                                      |
|----------------------|----------------------------------------------|
| `photorealistic`     | Looks like camera footage                    |
| `stylized-realistic` | Real-world forms, heavy grade or stylization |
| `3d-animation`       | CG animated film look                        |
| `2d-animation`       | Hand-drawn / cel animation                   |
| `anime`              | Japanese animation look                      |

## format.input_mode

| Value              | Meaning                                                      |
|--------------------|--------------------------------------------------------------|
| `text-to-video`    | Prompt only                                                  |
| `image-to-video`   | A start image conditions the first frame                     |
| `first-last-frame` | Start and end images condition first and last frames         |

## references.images[].role

`first_frame`, `last_frame`, `character`, `style`, `environment`.
