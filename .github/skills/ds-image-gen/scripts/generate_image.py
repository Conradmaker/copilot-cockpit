#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "certifi",
#     "openai",
# ]
# ///
"""
Generate or edit images via OpenAI-compatible providers using openai-python.
"""

import argparse
import base64
import json
import mimetypes
import os
import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import certifi
from openai import OpenAI


# Configuration
MAX_INPUT_IMAGES = 3
MIME_TO_EXT = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/webp": ".webp",
}
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_MODEL = "google/gemini-3-pro-image-preview"
DEFAULT_OPENROUTER_API_KEY_ENV = "OPENROUTER_API_KEY"
DEFAULT_NANO_GPT_BASE_URL = "https://nano-gpt.com/api/v1/images/generations"
DEFAULT_NANO_GPT_MODEL = "z-image-turbo"
DEFAULT_NANO_GPT_API_KEY_ENV = "NANO_GPT_API_KEY"
DEFAULT_CONFIG_ENV = "IMAGE_PROVIDER_CONFIG"
DEFAULT_CONFIG_FILENAME = "config.local.json"


def looks_like_api_key(value) -> bool:
    return isinstance(value, str) and value.startswith("sk-")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate or edit images via OpenAI-compatible providers."
    )
    parser.add_argument("--prompt", required=True, help="Prompt describing the desired image.")
    parser.add_argument("--filename", required=True, help="Output filename (relative to CWD).")
    parser.add_argument(
        "--config",
        default=None,
        help="Optional JSON config file path. If omitted, config.local.json next to the skill will be auto-loaded when present.",
    )
    parser.add_argument(
        "--provider",
        choices=["openrouter", "custom", "nano-gpt"],
        default=None,
        help="Provider preset. 'openrouter' uses built-in defaults, 'custom' requires --base-url and --model, 'nano-gpt' uses the nano-gpt image API.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="API base URL (required when --provider custom).",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model ID (defaults to OpenRouter Nano Banana model when --provider openrouter).",
    )
    parser.add_argument(
        "--api-key-env",
        default=None,
        help="Environment variable name containing the API key.",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Raw API key value. Overrides --api-key-env.",
    )
    parser.add_argument(
        "--resolution",
        type=str.upper,
        choices=["1K", "2K", "4K"],
        default=None,
        help="Output resolution: 1K, 2K, or 4K.",
    )
    parser.add_argument(
        "--size",
        default=None,
        help="Raw output size string for provider-specific image APIs, for example 512x512.",
    )
    parser.add_argument(
        "--input-image",
        action="append",
        default=[],
        help=f"Optional input image path (repeatable, max {MAX_INPUT_IMAGES}).",
    )
    parser.add_argument(
        "--mask-image",
        default=None,
        help="Optional mask image path for providers that support masked edits.",
    )
    parser.add_argument(
        "--disable-image-config",
        action="store_true",
        help="Disable OpenRouter-specific image_config payload.",
    )
    parser.add_argument(
        "--response-format",
        default=None,
        help="Provider-specific response format, for example url or b64_json.",
    )
    parser.add_argument(
        "--n-images",
        type=int,
        default=None,
        help="Provider-specific image count. For nano-gpt this maps to nImages.",
    )
    parser.add_argument(
        "--show-explicit-content",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Provider-specific explicit content flag. Use --show-explicit-content or --no-show-explicit-content.",
    )
    parser.add_argument(
        "--user",
        default=None,
        help="Optional provider-specific user identifier.",
    )
    parser.add_argument(
        "--strength",
        type=float,
        default=None,
        help="Optional provider-specific image edit strength.",
    )
    parser.add_argument(
        "--guidance-scale",
        type=float,
        default=None,
        help="Optional provider-specific guidance scale.",
    )
    parser.add_argument(
        "--num-inference-steps",
        type=int,
        default=None,
        help="Optional provider-specific number of inference steps.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional provider-specific random seed.",
    )
    parser.add_argument(
        "--kontext-max-mode",
        action="store_true",
        help="Enable provider-specific kontext_max_mode when supported.",
    )
    return parser.parse_args()


def load_config(config_path_arg: str | None) -> dict:
    config_path = config_path_arg or os.environ.get(DEFAULT_CONFIG_ENV)
    if not config_path:
        default_path = Path(__file__).parent.parent / DEFAULT_CONFIG_FILENAME
        if not default_path.exists():
            return {}
        config_path = str(default_path)

    path = Path(config_path).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    if not path.exists():
        raise SystemExit(f"Config file not found: {path}")

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"Failed to parse config file '{path}': {e}")

    if not isinstance(config, dict):
        raise SystemExit(f"Config file '{path}' must contain a JSON object.")
    return config


def get_config_value(config: dict, *keys: str):
    for key in keys:
        value = config.get(key)
        if value is not None:
            return value
    return None


def resolve_runtime_config(args, config: dict) -> dict[str, str | bool]:
    provider = args.provider or get_config_value(config, "provider") or "openrouter"

    if provider == "openrouter":
        base_url = args.base_url or get_config_value(config, "baseUrl", "base_url") or DEFAULT_OPENROUTER_BASE_URL
        model = args.model or get_config_value(config, "model") or DEFAULT_OPENROUTER_MODEL
        api_key_env = args.api_key_env or get_config_value(config, "apiKeyEnv", "api_key_env") or DEFAULT_OPENROUTER_API_KEY_ENV
        use_image_config = not args.disable_image_config
        request_mode = "chat-completions"
    elif provider == "custom":
        base_url = args.base_url or get_config_value(config, "baseUrl", "base_url")
        model = args.model or get_config_value(config, "model")
        api_key_env = args.api_key_env or get_config_value(config, "apiKeyEnv", "api_key_env") or "API_KEY"
        if not base_url:
            raise SystemExit("--base-url is required when --provider custom is used.")
        if not model:
            raise SystemExit("--model is required when --provider custom is used.")
        use_image_config = False
        request_mode = "chat-completions"
    else:
        base_url = args.base_url or get_config_value(config, "baseUrl", "base_url") or DEFAULT_NANO_GPT_BASE_URL
        model = args.model or get_config_value(config, "model") or DEFAULT_NANO_GPT_MODEL
        api_key_env = args.api_key_env or get_config_value(config, "apiKeyEnv", "api_key_env") or DEFAULT_NANO_GPT_API_KEY_ENV
        use_image_config = False
        request_mode = "rest-images"

    configured_api_key = args.api_key or get_config_value(config, "apiKey", "api_key")
    if not configured_api_key and looks_like_api_key(api_key_env):
        configured_api_key = api_key_env
        api_key_env = None

    api_key = configured_api_key
    if not api_key and api_key_env:
        api_key = os.environ.get(str(api_key_env))

    if not api_key:
        if api_key_env:
            raise SystemExit(
                f"API key is not set. Provide --api-key or set environment variable '{api_key_env}'."
            )
        raise SystemExit(
            "API key is not set. Provide --api-key or add a local-only apiKey field in config.local.json."
        )

    return {
        "provider": provider,
        "base_url": base_url,
        "model": model,
        "api_key": api_key,
        "use_image_config": use_image_config,
        "request_mode": request_mode,
    }


def map_resolution_to_size(resolution: str, separator: str = "x") -> str:
    return {
        "1K": f"1024{separator}1024",
        "2K": f"2048{separator}2048",
        "4K": f"4096{separator}4096",
    }[resolution]


def normalize_dimension_string(value: str, separator: str) -> str:
    return value.replace("X", separator).replace("x", separator).replace("*", separator)


def encode_image_to_data_url(path: Path) -> str:
    if not path.exists():
        raise SystemExit(f"Input image not found: {path}")
    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "image/png"
    data = path.read_bytes()
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def build_message_content(prompt: str, input_images: list[str]) -> list[dict]:
    content: list[dict] = [{"type": "text", "text": prompt}]
    for image_path in input_images:
        data_url = encode_image_to_data_url(Path(image_path))
        content.append({"type": "image_url", "image_url": {"url": data_url}})
    return content


def parse_data_url(data_url: str) -> tuple[str, bytes]:
    if not data_url.startswith("data:") or ";base64," not in data_url:
        raise SystemExit("Image URL is not a base64 data URL.")
    header, encoded = data_url.split(",", 1)
    mime = header[5:].split(";", 1)[0]
    try:
        raw = base64.b64decode(encoded)
    except Exception as e:
        raise SystemExit(f"Failed to decode base64 image payload: {e}")
    return mime, raw


def resolve_output_path(filename: str, image_index: int, total_count: int, mime: str) -> Path:
    output_path = Path(filename)
    suffix = output_path.suffix

    # Validate/correct suffix matches MIME type
    expected_suffix = MIME_TO_EXT.get(mime, ".png")
    if suffix and suffix.lower() != expected_suffix.lower():
        print(f"Warning: filename extension '{suffix}' doesn't match returned MIME type '{mime}'. Using '{expected_suffix}' instead.")
        suffix = expected_suffix
    elif not suffix:
        suffix = expected_suffix

    # Single image: use original stem + corrected suffix
    if total_count <= 1:
        return output_path.with_suffix(suffix)

    # Multiple images: append numbering
    return output_path.with_name(f"{output_path.stem}-{image_index + 1}{suffix}")


def extract_image_url(image: dict | object) -> str | None:
    if isinstance(image, dict):
        return image.get("image_url", {}).get("url") or image.get("url")
    return None


def load_system_prompt():
    """Load system prompt from assets/SYSTEM_TEMPLATE if it exists and is not empty."""
    script_dir = Path(__file__).parent.parent
    template_path = script_dir / "assets" / "SYSTEM_TEMPLATE"

    if template_path.exists():
        content = template_path.read_text(encoding="utf-8").strip()
        if content:
            return content
    return None


def decode_base64_payload(encoded: str, fallback_mime: str = "image/png") -> tuple[str, bytes]:
    try:
        raw = base64.b64decode(encoded)
    except Exception as e:
        raise SystemExit(f"Failed to decode base64 image payload: {e}")
    return fallback_mime, raw


def create_ssl_context() -> ssl.SSLContext:
    return ssl.create_default_context(cafile=certifi.where())


def guess_mime_from_url(url: str) -> str:
    mime, _ = mimetypes.guess_type(urlparse(url).path)
    return mime or "image/png"


def download_image_url(url: str) -> tuple[str, bytes]:
    request = Request(url, method="GET")
    try:
        with urlopen(request, context=create_ssl_context()) as response:
            raw = response.read()
            mime = response.headers.get_content_type() or guess_mime_from_url(url)
            return mime, raw
    except HTTPError as e:
        raise SystemExit(f"Failed to download generated image: HTTP {e.code} {e.reason}")
    except URLError as e:
        raise SystemExit(f"Failed to download generated image: {e.reason}")


def build_nano_gpt_payload(args, model: str, config: dict) -> dict:
    raw_resolution = args.size or get_config_value(config, "resolution", "size")
    if raw_resolution:
        resolution = normalize_dimension_string(str(raw_resolution), "*")
    else:
        preset_resolution = args.resolution or get_config_value(config, "presetResolution", "preset_resolution") or "1K"
        resolution = map_resolution_to_size(str(preset_resolution), separator="*")

    n_images = args.n_images
    if n_images is None:
        n_images = get_config_value(config, "nImages", "n_images") or 1

    payload = {
        "model": model,
        "prompt": args.prompt,
        "nImages": int(n_images),
        "resolution": resolution,
    }

    show_explicit_content = args.show_explicit_content
    if show_explicit_content is None:
        show_explicit_content = get_config_value(
            config,
            "showExplicitContent",
            "show_explicit_content",
        )
    if show_explicit_content is not None:
        payload["showExplicitContent"] = bool(show_explicit_content)

    response_format = args.response_format or get_config_value(
        config,
        "responseFormat",
        "response_format",
    )
    if response_format:
        payload["response_format"] = response_format

    user = args.user or get_config_value(config, "user")
    if user:
        payload["user"] = user

    if len(args.input_image) == 1:
        payload["imageDataUrl"] = encode_image_to_data_url(Path(args.input_image[0]))
    elif len(args.input_image) > 1:
        payload["imageDataUrls"] = [
            encode_image_to_data_url(Path(image_path)) for image_path in args.input_image
        ]

    if args.mask_image:
        payload["maskDataUrl"] = encode_image_to_data_url(Path(args.mask_image))
    strength = args.strength if args.strength is not None else get_config_value(config, "strength")
    guidance_scale = args.guidance_scale if args.guidance_scale is not None else get_config_value(config, "guidanceScale", "guidance_scale")
    num_inference_steps = args.num_inference_steps if args.num_inference_steps is not None else get_config_value(config, "numInferenceSteps", "num_inference_steps")
    seed = args.seed if args.seed is not None else get_config_value(config, "seed")
    kontext_max_mode = args.kontext_max_mode or bool(get_config_value(config, "kontextMaxMode", "kontext_max_mode") or False)

    if strength is not None:
        payload["strength"] = strength
    if guidance_scale is not None:
        payload["guidance_scale"] = guidance_scale
    if num_inference_steps is not None:
        payload["num_inference_steps"] = num_inference_steps
    if seed is not None:
        payload["seed"] = seed
    if kontext_max_mode:
        payload["kontext_max_mode"] = True

    return payload


def post_json(url: str, headers: dict[str, str], payload: dict) -> dict:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request, context=create_ssl_context()) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Image API request failed: HTTP {e.code} {e.reason}\n{body}")
    except URLError as e:
        raise SystemExit(f"Image API request failed: {e.reason}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Image API returned invalid JSON: {e}")


def extract_generated_images(payload: dict) -> list[tuple[str, bytes]]:
    candidates = payload.get("data") or payload.get("images") or payload.get("results") or payload.get("output")
    if isinstance(candidates, dict):
        candidates = [candidates]
    if not isinstance(candidates, list) or not candidates:
        raise SystemExit("No images returned by the image API.")

    extracted_images = []
    for item in candidates:
        if isinstance(item, str):
            extracted_images.append(download_image_url(item))
            continue
        if not isinstance(item, dict):
            continue

        data_url = item.get("data_url")
        if data_url:
            extracted_images.append(parse_data_url(data_url))
            continue

        b64_json = item.get("b64_json") or item.get("base64")
        if b64_json:
            extracted_images.append(
                decode_base64_payload(b64_json, item.get("mime_type", "image/png"))
            )
            continue

        image_url = item.get("url") or item.get("image_url")
        if image_url:
            extracted_images.append(download_image_url(image_url))

    if not extracted_images:
        raise SystemExit("No supported image payloads were found in the image API response.")
    return extracted_images


def generate_images_via_chat_completions(args, runtime: dict[str, str | bool], config: dict) -> list[tuple[str, bytes]]:
    image_size = args.resolution or get_config_value(config, "presetResolution", "preset_resolution") or "1K"

    client = OpenAI(base_url=runtime["base_url"], api_key=runtime["api_key"])

    messages = []

    system_prompt = load_system_prompt()
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt,
        })

    messages.append({
        "role": "user",
        "content": build_message_content(args.prompt, args.input_image),
    })

    request_kwargs = {
        "model": runtime["model"],
        "messages": messages,
    }
    if runtime["use_image_config"]:
        request_kwargs["extra_body"] = {
            "modalities": ["image", "text"],
            # https://openrouter.ai/docs/guides/overview/multimodal/image-generation#image-configuration-options
            "image_config": {
                # "aspect_ratio": "16:9",
                "image_size": image_size,
            },
        }

    response = client.chat.completions.create(**request_kwargs)

    message = response.choices[0].message
    images = getattr(message, "images", None)
    if not images:
        raise SystemExit("No images returned by the API.")

    extracted_images = []
    for image in images:
        image_url = extract_image_url(image)
        if not image_url:
            raise SystemExit("Image payload missing image_url.url.")
        extracted_images.append(parse_data_url(image_url))

    return extracted_images


def generate_images_via_rest_api(args, runtime: dict[str, str | bool], config: dict) -> list[tuple[str, bytes]]:
    headers = {
        "Authorization": f"Bearer {runtime['api_key']}",
        "Content-Type": "application/json",
    }
    payload = build_nano_gpt_payload(args, str(runtime["model"]), config)
    response = post_json(str(runtime["base_url"]), headers, payload)
    return extract_generated_images(response)


def main():
    args = parse_args()
    config = load_config(args.config)
    runtime = resolve_runtime_config(args, config)

    if len(args.input_image) > MAX_INPUT_IMAGES:
        raise SystemExit(f"Too many input images: {len(args.input_image)} (max {MAX_INPUT_IMAGES}).")

    if runtime["request_mode"] == "rest-images":
        images = generate_images_via_rest_api(args, runtime, config)
    else:
        images = generate_images_via_chat_completions(args, runtime, config)

    # Create output directory once before processing images
    output_base_path = Path(args.filename)
    if output_base_path.parent and str(output_base_path.parent) != '.':
        output_base_path.parent.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for idx, image in enumerate(images):
        mime, raw = image
        output_path = resolve_output_path(args.filename, idx, len(images), mime)
        output_path.write_bytes(raw)
        saved_paths.append(output_path.resolve())

    for path in saved_paths:
        print(f"Saved image to: {path}")
        print(f"MEDIA: {path}")


if __name__ == "__main__":
    main()
