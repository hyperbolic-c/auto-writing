#!/usr/bin/env python3
"""
/// script
dependencies = ["requests>=2.31.0"]
///

Generate and edit images using various image generation APIs.

Supports:
- OpenRouter: OpenRouter API with various image generation models
- MiniMax: MiniMax API (https://api.minimaxi.com)

Configuration (via .env or environment variables):
- IMAGE_PROVIDER: "openrouter" or "minimax" (default: openrouter)
- IMAGE_MODEL_OPENROUTER: OpenRouter model ID (default: google/gemini-3-pro-image-preview)
- IMAGE_MODEL_MINIMAX: MiniMax model ID (default: image-01)
- OPENROUTER_API_KEY / MINIMAX_API_KEY: API keys
- OPENROUTER_BASE_URL: Custom base URL for OpenRouter
"""

import sys
import json
import base64
import argparse
import os
from pathlib import Path
from typing import Optional

DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_OPENROUTER_API_PATH = "/chat/completions"
MINIMAX_API_URL = "https://api.minimaxi.com/v1/image_generation"

# Default models
DEFAULT_OPENROUTER_MODEL = "google/gemini-3-pro-image-preview"
DEFAULT_MINIMAX_MODEL = "image-01"
DEFAULT_PROVIDER = "openrouter"


def check_env_file(key: str) -> Optional[str]:
    """Check if .env file exists and contains the specified key."""
    current_dir = Path.cwd()
    for parent in [current_dir] + list(current_dir.parents):
        env_file = parent / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith(f'{key}='):
                        value = line.split('=', 1)[1].strip().strip('"').strip("'")
                        if value:
                            return value
    return None


def get_api_key(provider: str = "openrouter") -> Optional[str]:
    """Get API key from environment or .env file."""
    env_key = f"{provider.upper()}_API_KEY"
    # Check environment variable first
    api_key = os.environ.get(env_key)
    if api_key:
        return api_key
    # Fall back to .env file
    return check_env_file(env_key)


def get_base_url() -> str:
    """Get base URL from environment or .env file."""
    base_url = os.environ.get("OPENROUTER_BASE_URL")
    if base_url:
        return base_url.rstrip('/')
    env_base_url = check_env_file("OPENROUTER_BASE_URL")
    if env_base_url:
        return env_base_url.rstrip('/')
    return DEFAULT_OPENROUTER_BASE_URL


def get_provider() -> str:
    """Get image provider from environment or .env file."""
    # Check environment variable first
    provider = os.environ.get("IMAGE_PROVIDER")
    if provider:
        return provider.lower()
    # Fall back to .env file
    env_provider = check_env_file("IMAGE_PROVIDER")
    if env_provider:
        return env_provider.lower()
    return DEFAULT_PROVIDER


def get_model(provider: str) -> str:
    """Get default model for the specified provider."""
    if provider == "minimax":
        model = os.environ.get("IMAGE_MODEL_MINIMAX")
        if model:
            return model
        env_model = check_env_file("IMAGE_MODEL_MINIMAX")
        if env_model:
            return env_model
        return DEFAULT_MINIMAX_MODEL
    else:
        model = os.environ.get("IMAGE_MODEL_OPENROUTER")
        if model:
            return model
        env_model = check_env_file("IMAGE_MODEL_OPENROUTER")
        if env_model:
            return env_model
        return DEFAULT_OPENROUTER_MODEL


def save_base64_image(base64_data: str, output_path: str) -> None:
    """Save base64 encoded image to file."""
    if ',' in base64_data:
        base64_data = base64_data.split(',', 1)[1]
    image_data = base64.b64decode(base64_data)
    with open(output_path, 'wb') as f:
        f.write(image_data)


def generate_image_openrouter(
    prompt: str,
    model: str,
    output_path: str,
    api_key: str,
    base_url: str,
    input_image: Optional[str] = None
) -> dict:
    """Generate/edit images using OpenRouter API."""
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library not found. Install with: pip install requests")
        sys.exit(1)

    api_url = f"{base_url.rstrip('/')}{DEFAULT_OPENROUTER_API_PATH}"
    print(f"Using OpenRouter API URL: {api_url}")

    is_editing = input_image is not None

    if is_editing:
        print(f"Editing image with model: {model}")
        # Load input image as base64
        image_path = Path(input_image)
        if not image_path.exists():
            print(f"Error: Image file not found: {input_image}")
            sys.exit(1)

        mime_types = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}
        mime_type = mime_types.get(image_path.suffix.lower(), 'image/png')

        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        image_data_url = f"data:{mime_type};base64,{image_data}"

        message_content = [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": image_data_url}}
        ]
    else:
        print(f"Generating image with model: {model}")
        message_content = prompt

    response = requests.post(
        url=api_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": message_content}],
            "modalities": ["image", "text"]
        }
    )

    if response.status_code != 200:
        print(f"API Error ({response.status_code}): {response.text}")
        sys.exit(1)

    result = response.json()

    if result.get("choices"):
        message = result["choices"][0]["message"]
        images = []

        if message.get("images"):
            images = message["images"]
        elif message.get("content"):
            content = message["content"]
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "image":
                        images.append(part)

        if images:
            image = images[0]
            if "image_url" in image:
                save_base64_image(image["image_url"]["url"], output_path)
            elif "url" in image:
                save_base64_image(image["url"], output_path)
            print(f"Image saved to: {output_path}")
        else:
            print("No image found in response")

    return result


def generate_image_minimax(
    prompt: str,
    model: str,
    output_path: str,
    api_key: str,
    aspect_ratio: str = "16:9"
) -> dict:
    """Generate images using MiniMax API."""
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library not found. Install with: pip install requests")
        sys.exit(1)

    print(f"Generating image with MiniMax model: {model}")
    print(f"Aspect ratio: {aspect_ratio}")

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "base64",
    }

    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.post(MINIMAX_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"API Error ({response.status_code}): {response.text}")
        sys.exit(1)

    result = response.json()

    # MiniMax returns: {"data": {"image_base64": [...]}}
    if "data" in result and "image_base64" in result["data"]:
        images = result["data"]["image_base64"]
        for i, img_data in enumerate(images):
            out_path = output_path if len(images) == 1 else output_path.replace('.png', f'-{i}.png').replace('.jpeg', f'-{i}.jpeg')
            save_base64_image(img_data, out_path)
            print(f"Image saved to: {out_path}")
    else:
        print("No image found in response")
        print(f"Response: {json.dumps(result, indent=2)}")

    return result


def generate_image(
    prompt: str,
    model: str = "google/gemini-3-pro-image-preview",
    output_path: str = "generated_image.png",
    api_key: Optional[str] = None,
    input_image: Optional[str] = None,
    base_url: Optional[str] = None,
    provider: str = "openrouter",
    aspect_ratio: str = "16:9"
) -> dict:
    """
    Generate or edit an image using the specified provider API.

    Args:
        prompt: Text description of the image to generate
        model: Model ID (OpenRouter: google/gemini-3-pro-image-preview, MiniMax: image-01)
        output_path: Path to save the generated image
        api_key: API key (will check .env if not provided)
        input_image: Path to an input image for editing (OpenRouter only)
        base_url: Base URL for the API (OpenRouter only)
        provider: API provider ("openrouter" or "minimax")
        aspect_ratio: Image aspect ratio (MiniMax only, e.g., "16:9", "9:16", "1:1")

    Returns:
        dict: Response from the API
    """
    if provider == "minimax":
        if not api_key:
            api_key = get_api_key("minimax")
        if not api_key:
            print("Error: MINIMAX_API_KEY not found!")
            print("\nPlease create a .env file with:")
            print("MINIMAX_API_KEY=your-api-key-here")
            sys.exit(1)
        return generate_image_minimax(prompt, model, output_path, api_key, aspect_ratio)
    else:
        if not api_key:
            api_key = get_api_key("openrouter")
        if not api_key:
            print("Error: OPENROUTER_API_KEY not found!")
            print("\nPlease create a .env file with:")
            print("OPENROUTER_API_KEY=your-api-key-here")
            sys.exit(1)
        if not base_url:
            base_url = get_base_url()
        return generate_image_openrouter(prompt, model, output_path, api_key, base_url, input_image)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using OpenRouter or MiniMax API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (OpenRouter):
  python generate_image.py "A sunset over mountains"
  python generate_image.py "A cat in space" -m "black-forest-labs/flux.2-pro"
  python generate_image.py "Make it purple" --input photo.jpg -o edited.png

Examples (MiniMax):
  python generate_image.py "A beautiful landscape" --provider minimax
  python generate_image.py "Portrait photo" --provider minimax --aspect-ratio "9:16" -o portrait.png

Popular models:
  OpenRouter: google/gemini-3-pro-image-preview, black-forest-labs/flux.2-pro
  MiniMax: image-01

Configuration (.env):
  # Provider selection
  IMAGE_PROVIDER=openrouter  # or minimax

  # OpenRouter
  OPENROUTER_API_KEY=sk-or-...
  OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
  IMAGE_MODEL_OPENROUTER=google/gemini-3-pro-image-preview

  # MiniMax
  MINIMAX_API_KEY=your-minimax-key
  IMAGE_MODEL_MINIMAX=image-01
        """
    )

    parser.add_argument("prompt", type=str, help="Text description of the image to generate")

    parser.add_argument("--model", "-m", type=str,
                        help=f"Model ID (default: from IMAGE_MODEL_OPENROUTER or IMAGE_MODEL_MINIMAX env)")

    parser.add_argument("--output", "-o", type=str, default="generated_image.png",
                        help="Output file path (default: generated_image.png)")

    parser.add_argument("--input", "-i", type=str,
                        help="Input image path for editing (OpenRouter only)")

    parser.add_argument("--api-key", type=str, help="API key for the provider")

    parser.add_argument("--base-url", type=str,
                        help="Base URL for the API (OpenRouter only)")

    parser.add_argument("--provider", type=str, choices=["openrouter", "minimax"],
                        help=f"API provider (default: from IMAGE_PROVIDER env or 'openrouter')")

    parser.add_argument("--aspect-ratio", type=str, default="16:9",
                        help="Image aspect ratio for MiniMax (default: 16:9)")

    args = parser.parse_args()

    # Get default provider and model from environment
    env_provider = get_provider()
    provider = args.provider or env_provider
    env_model = get_model(provider)
    model = args.model or env_model

    generate_image(
        prompt=args.prompt,
        model=model,
        output_path=args.output,
        api_key=args.api_key,
        input_image=args.input,
        base_url=args.base_url,
        provider=provider,
        aspect_ratio=args.aspect_ratio
    )


if __name__ == "__main__":
    main()
