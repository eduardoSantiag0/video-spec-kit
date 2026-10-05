---
# Copy this folder to adapters/<your-model-id>/ and fill every field.
# See docs/extending.md → "Create a prompt adapter".
id: <model-id>
name: <Model name (publisher)>
written_against: [<model versions you actually tested>]
weights: <open / closed; license; how it runs locally>
prompt:
  form: <single paragraph | tag list | structured sections>
  language: en
  target_words: [<min>, <max>]
  max_words: <hard limit>
  section_order: [<slot>, <slot>]
negative_prompt: <true | false>
supports:
  image_to_video: <true | false>
  first_last_frame: <true | false>
  audio: <true | false>
frame_rule: "<constraint on num_frames / width / height>"
profiles:
  - id: <profile-id>
    model: <checkpoint name>
    fps: <int>
    num_frames: <int>
    sizes: { "16:9": [<w>, <h>], "9:16": [<w>, <h>] }
    steps: <int>
    cfg: <number>
    sampler: <sampler>
    scheduler: <scheduler>
    params: {}
default_profile: <profile-id>
---

# <Model> adapter

Every section below is required. Write rules an agent can apply
deterministically; cite the model's official guidance when you have it.

## Order of information
## Level of detail
## Negative prompt
## Camera
## Motion
## Reference images (image-to-video / first-last-frame)
## Temporal consistency
## Duration
## Known limitations
## Example
