---
name: ds-image-gen
description: "Generate or edit images via OpenAI-compatible providers. Use when Painter or a direct image workflow needs prompt-only image generation, image edits, or multi-image compositing. Defaults to OpenRouter + Gemini 3 Pro Image and supports switching provider base URL and model via CLI options or using the nano-gpt image API preset. Triggers on: image generation, prompt-only image, image edit, visual asset backend, Painter backend, 이미지 생성, 이미지 수정, 비주얼 에셋 생성."
disable-model-invocation: false
user-invocable: false
metadata:
  emoji: 🍌
  requires:
    bins:
      - uv
    env:
      - OPENROUTER_API_KEY
      - NANO_GPT_API_KEY
  primaryEnv: OPENROUTER_API_KEY
---

# DS Image Gen

## Overview

Generate or edit images with OpenAI-compatible providers.

Painter uses this skill as the image execution backend. This skill is responsible for provider configuration and file output, not for reading `design.md` or deciding visual tone.

- Default profile: OpenRouter + `google/gemini-3-pro-image-preview`
- Custom profile: any OpenAI-compatible endpoint via `--provider custom --base-url ... --model ...`
- Dedicated preset: nano-gpt image API via `--provider nano-gpt`

Supports prompt-only generation, single-image edits, and multi-image composition.

## Settings management

Recommended split:

- API key: environment variable only
- Stable defaults like provider, model, resolution, image count: `config.local.json`
- One-off overrides: CLI flags

Compatibility note:

- Preferred: keep secrets in env vars.
- Local-only fallback: ignored `config.local.json` may use `apiKey`, and legacy local setups with a raw key in `apiKeyEnv` are also supported.

Priority order:

1. CLI arguments
2. `--config <path>`
3. `IMAGE_PROVIDER_CONFIG` env var
4. `config.local.json` in this skill folder
5. Built-in defaults

Do not commit real API keys into JSON config files. Keep secrets in env vars like `OPENROUTER_API_KEY` or `NANO_GPT_API_KEY`.

Example local config for the payload shape below:

```json
{
  "provider": "nano-gpt",
  "baseUrl": "https://nano-gpt.com/api/v1/images/generations",
  "apiKeyEnv": "NANO_GPT_API_KEY",
  "model": "z-image-turbo",
  "showExplicitContent": true,
  "nImages": 1,
  "resolution": "1024*1024"
}
```

You can copy [config.example.json](config.example.json) to `config.local.json` and adjust only the non-secret fields.

### Prompt-only generation

```
uv run {baseDir}/scripts/generate_image.py \
  --prompt "A cinematic sunset over snow-capped mountains" \
  --filename sunset.png
```

### Edit a single image

```
uv run {baseDir}/scripts/generate_image.py \
  --prompt "Replace the sky with a dramatic aurora" \
  --input-image input.jpg \
  --filename aurora.png
```

### Compose multiple images

```
uv run {baseDir}/scripts/generate_image.py \
  --prompt "Combine the subjects into a single studio portrait" \
  --input-image face1.jpg \
  --input-image face2.jpg \
  --filename composite.png
```

### Switch provider and model

```
export MY_PROVIDER_API_KEY="<your-key>"

uv run {baseDir}/scripts/generate_image.py \
  --provider custom \
  --base-url "https://your-provider.example.com/v1" \
  --api-key-env MY_PROVIDER_API_KEY \
  --model "your/image-model" \
  --prompt "Create a vibrant product hero image" \
  --filename custom-provider.png
```

### Use the nano-gpt preset

Note: the correct endpoint is `https://nano-gpt.com/api/v1/images/generations`. Do not use `https://https://...`.

```
export NANO_GPT_API_KEY="<your-key>"

uv run {baseDir}/scripts/generate_image.py \
  --provider nano-gpt \
  --model "nano-banana" \
  --size "512x512" \
  --response-format url \
  --user "example-user-123" \
  --prompt "A serene mountain landscape at sunset" \
  --filename nano-gpt-output.png
```

If you keep defaults in `config.local.json`, the command can stay short:

```
export NANO_GPT_API_KEY="<your-key>"

uv run {baseDir}/scripts/generate_image.py \
  --config {baseDir}/config.local.json \
  --prompt "아무 이미지" \
  --filename output.png
```

You can also pass edit inputs:

```
uv run {baseDir}/scripts/generate_image.py \
  --provider nano-gpt \
  --model "nano-banana" \
  --input-image input.jpg \
  --mask-image mask.png \
  --strength 0.8 \
  --guidance-scale 7.5 \
  --num-inference-steps 30 \
  --seed 42 \
  --prompt "Replace the background with a misty forest" \
  --filename edited.png
```

## Resolution

- Use `--resolution` with `1K`, `2K`, or `4K`.
- Default is `1K` if not specified.
- Resolution is applied via OpenRouter `image_config`. For `--provider custom`, this payload is disabled by default.
- For `--provider nano-gpt`, you can override with `--size` like `512x512`.
- For `--provider nano-gpt`, `config.local.json` can hold `model`, `showExplicitContent`, `nImages`, and `resolution` like `1024*1024`.

## System prompt customization

The skill reads an optional system prompt from `assets/SYSTEM_TEMPLATE`. This allows you to customize the image generation behavior without modifying code.

## Behavior and constraints

- Accept up to 3 input images via repeated `--input-image`.
- `--filename` accepts relative paths (saves to current directory) or absolute paths.
- If multiple images are returned, append `-1`, `-2`, etc. to the filename.
- For `--provider custom`, `--base-url` and `--model` are required.
- For `--provider nano-gpt`, the script calls a direct image generation endpoint and supports `--size`, `--response-format`, `--user`, `--mask-image`, `--strength`, `--guidance-scale`, `--num-inference-steps`, `--seed`, and `--kontext-max-mode`.
- For `--provider nano-gpt`, the script also maps `--n-images` to `nImages` and `--show-explicit-content` to `showExplicitContent`.
- Print `MEDIA: <path>` for each saved image. Do not read images back into the response.

## Troubleshooting

If the script exits non-zero, check stderr against these common blockers:

| Symptom | Resolution |
| --- | --- |
| `OPENROUTER_API_KEY is not set` | Ask the user to set it. PowerShell: `$env:OPENROUTER_API_KEY = "sk-or-..."` / bash: `export OPENROUTER_API_KEY="sk-or-..."` |
| `NANO_GPT_API_KEY` missing | Set it before running `--provider nano-gpt`, or pass `--api-key` directly. |
| `API key is not set. Provide --api-key or set environment variable ...` | Either pass `--api-key` directly or set the env var selected by `--api-key-env` (default: `OPENROUTER_API_KEY` for openrouter, `API_KEY` for custom). |
| `--base-url is required when --provider custom is used` | Provide a valid provider endpoint URL with `--base-url`. |
| `--model is required when --provider custom is used` | Provide a model ID with `--model`. |
| nano-gpt URL contains `https://https://` | Remove the duplicated protocol. Use `https://nano-gpt.com/api/v1/images/generations`. |
| `uv: command not found` or not recognized | macOS/Linux: <code>curl -LsSf https://astral.sh/uv/install.sh &#124; sh</code>. Windows: <code>powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 &#124; iex"</code>. Then restart the terminal. |
| `AuthenticationError` / HTTP 401 | Key is invalid or has no credits. Verify at <https://openrouter.ai/settings/keys>. |

For transient errors (HTTP 429, network timeouts), retry once after 30 seconds. Do not retry the same error more than twice — surface the issue to the user instead.
