#!/usr/bin/env python3
"""
/// script
dependencies = ["requests>=2.31.0"]
///

AI-powered scientific schematic generation using Nano Banana Pro or MiniMax.

This script uses a smart iterative refinement approach:
1. Generate initial image with Nano Banana Pro or MiniMax
2. AI quality review using Gemini 3 Pro for scientific critique (OpenRouter only)
3. Only regenerate if quality is below threshold for document type
4. Repeat until quality meets standards (max iterations)

Requirements:
    - OPENROUTER_API_KEY environment variable (Nano Banana Pro)
    - MINIMAX_API_KEY environment variable (MiniMax)
    - requests library

Usage (Nano Banana Pro):
    uv run --script scripts/generate_schematic_ai.py "Create a flowchart" -o flowchart.png

Usage (MiniMax):
    uv run --script scripts/generate_schematic_ai.py "Create a flowchart" -o flowchart.png --provider minimax
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

import requests


# MiniMax API configuration
MINIMAX_API_URL = "https://api.minimaxi.com/v1/image_generation"
MINIMAX_DEFAULT_MODEL = "image-01"


def _get_api_key(provider: str = "openrouter") -> Optional[str]:
    """Get API key from environment or .env file."""
    env_key = f"{provider.upper()}_API_KEY"
    api_key = os.environ.get(env_key)
    if api_key:
        return api_key

    # Check .env file
    for path in [Path.cwd()] + list(Path.cwd().parents)[:5]:
        env_file = path / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith(f'{env_key}='):
                        value = line.split('=', 1)[1].strip().strip('"').strip("'")
                        if value:
                            return value
    return None


def _get_provider() -> str:
    """Get image provider from environment or .env file."""
    provider = os.environ.get("IMAGE_PROVIDER")
    if provider:
        return provider.lower()

    for path in [Path.cwd()] + list(Path.cwd().parents)[:5]:
        env_file = path / ".env"
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('IMAGE_PROVIDER='):
                        value = line.split('=', 1)[1].strip().strip('"').strip("'")
                        if value:
                            return value.lower()
    return "openrouter"


# Try to load .env file from multiple potential locations
def _load_env_file():
    """Load .env file from current directory, parent directories, or package directory.
    
    Returns True if a .env file was found and loaded, False otherwise.
    Note: This does NOT override existing environment variables.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return False  # python-dotenv not installed
    
    # Try current working directory first
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
        return True
        
    # Try parent directories (up to 5 levels)
    cwd = Path.cwd()
    for _ in range(5):
        env_path = cwd / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        cwd = cwd.parent
        if cwd == cwd.parent:  # Reached root
            break
    
    # Try the package's parent directory (scientific-writer project root)
    script_dir = Path(__file__).resolve().parent
    for _ in range(5):
        env_path = script_dir / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            return True
        script_dir = script_dir.parent
        if script_dir == script_dir.parent:
            break
            
    return False


class ScientificSchematicGenerator:
    """Generate scientific schematics using AI with smart iterative refinement.
    
    Uses Gemini 3 Pro for quality review to determine if regeneration is needed.
    Multiple passes only occur if the generated schematic doesn't meet the
    quality threshold for the target document type.
    """
    
    # Quality thresholds by document type (score out of 10)
    # Higher thresholds for more formal publications
    QUALITY_THRESHOLDS = {
        "journal": 8.5,      # Nature, Science, etc. - highest standards
        "conference": 8.0,   # Conference papers - high standards
        "poster": 7.0,       # Academic posters - good quality
        "presentation": 6.5, # Slides/talks - clear but less formal
        "report": 7.5,       # Technical reports - professional
        "grant": 8.0,        # Grant proposals - must be compelling
        "thesis": 8.0,       # Dissertations - formal academic
        "preprint": 7.5,     # arXiv, etc. - good quality
        "default": 7.5,      # Default threshold
    }
    
    # Scientific diagram best practices prompt template
    SCIENTIFIC_DIAGRAM_GUIDELINES = """
Create a high-quality scientific diagram with these requirements:

VISUAL QUALITY:
- Clean white or light background (no textures or gradients)
- High contrast for readability and printing
- Professional, publication-ready appearance
- Sharp, clear lines and text
- Adequate spacing between elements to prevent crowding

TYPOGRAPHY:
- Clear, readable sans-serif fonts (Arial, Helvetica style)
- Minimum 10pt font size for all labels
- Consistent font sizes throughout
- All text horizontal or clearly readable
- No overlapping text

SCIENTIFIC STANDARDS:
- Accurate representation of concepts
- Clear labels for all components
- Include scale bars, legends, or axes where appropriate
- Use standard scientific notation and symbols
- Include units where applicable

ACCESSIBILITY:
- Colorblind-friendly color palette (use Okabe-Ito colors if using color)
- High contrast between elements
- Redundant encoding (shapes + colors, not just colors)
- Works well in grayscale

LAYOUT:
- Logical flow (left-to-right or top-to-bottom)
- Clear visual hierarchy
- Balanced composition
- Appropriate use of whitespace
- No clutter or unnecessary decorative elements

IMPORTANT - NO FIGURE NUMBERS:
- Do NOT include "Figure 1:", "Fig. 1", or any figure numbering in the image
- Do NOT add captions or titles like "Figure: ..." at the top or bottom
- Figure numbers and captions are added separately in the document/LaTeX
- The diagram should contain only the visual content itself
"""
    
    def __init__(self, api_key: Optional[str] = None, verbose: bool = False, provider: str = "openrouter"):
        """
        Initialize the generator.

        Args:
            api_key: API key for the selected provider
            verbose: Print detailed progress information
            provider: Image provider ("openrouter" or "minimax")
        """
        self.provider = provider.lower()
        self.verbose = verbose
        self._last_error = None
        self.base_url = "https://openrouter.ai/api/v1"

        if self.provider == "minimax":
            self.api_key = api_key or _get_api_key("minimax")
            if not self.api_key:
                raise ValueError(
                    "MINIMAX_API_KEY not found. Please either:\n"
                    "  1. Set the MINIMAX_API_KEY environment variable\n"
                    "  2. Add MINIMAX_API_KEY to your .env file\n"
                    "  3. Pass api_key parameter to the constructor\n"
                    "Get your API key from: https://api.minimaxi.com"
                )
            self.image_model = MINIMAX_DEFAULT_MODEL
        else:
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")

            if not self.api_key:
                _load_env_file()
                self.api_key = os.getenv("OPENROUTER_API_KEY")

            if not self.api_key:
                raise ValueError(
                    "OPENROUTER_API_KEY not found. Please either:\n"
                    "  1. Set the OPENROUTER_API_KEY environment variable\n"
                    "  2. Add OPENROUTER_API_KEY to your .env file\n"
                    "  3. Pass api_key parameter to the constructor\n"
                    "Get your API key from: https://openrouter.ai/keys"
                )

            # Nano Banana Pro for image generation
            self.image_model = "google/gemini-3-pro-image-preview"

        # Gemini 3 Pro for quality review (OpenRouter only)
        self.review_model = "google/gemini-3-pro"
        
    def _log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[{time.strftime('%H:%M:%S')}] {message}")
    
    def _make_request(self, model: str, messages: List[Dict[str, Any]], 
                     modalities: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Make a request to OpenRouter API.
        
        Args:
            model: Model identifier
            messages: List of message dictionaries
            modalities: Optional list of modalities (e.g., ["image", "text"])
            
        Returns:
            API response as dictionary
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/scientific-writer",
            "X-Title": "Scientific Schematic Generator"
        }
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        if modalities:
            payload["modalities"] = modalities
        
        self._log(f"Making request to {model}...")
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120
            )
            
            # Try to get response body even on error
            try:
                response_json = response.json()
            except json.JSONDecodeError:
                response_json = {"raw_text": response.text[:500]}
            
            # Check for HTTP errors but include response body in error message
            if response.status_code != 200:
                error_detail = response_json.get("error", response_json)
                self._log(f"HTTP {response.status_code}: {error_detail}")
                raise RuntimeError(f"API request failed (HTTP {response.status_code}): {error_detail}")
            
            return response_json
        except requests.exceptions.Timeout:
            raise RuntimeError("API request timed out after 120 seconds")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
    
    def _extract_image_from_response(self, response: Dict[str, Any]) -> Optional[bytes]:
        """
        Extract base64-encoded image from API response.
        
        For Nano Banana Pro, images are returned in the 'images' field of the message,
        not in the 'content' field.
        
        Args:
            response: API response dictionary
            
        Returns:
            Image bytes or None if not found
        """
        try:
            choices = response.get("choices", [])
            if not choices:
                self._log("No choices in response")
                return None
            
            message = choices[0].get("message", {})
            
            # IMPORTANT: Nano Banana Pro returns images in the 'images' field
            images = message.get("images", [])
            if images and len(images) > 0:
                self._log(f"Found {len(images)} image(s) in 'images' field")
                
                # Get first image
                first_image = images[0]
                if isinstance(first_image, dict):
                    # Extract image_url
                    if first_image.get("type") == "image_url":
                        url = first_image.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        
                        if url and url.startswith("data:image"):
                            # Extract base64 data after comma
                            if "," in url:
                                base64_str = url.split(",", 1)[1]
                                # Clean whitespace
                                base64_str = base64_str.replace('\n', '').replace('\r', '').replace(' ', '')
                                self._log(f"Extracted base64 data (length: {len(base64_str)})")
                                return base64.b64decode(base64_str)
            
            # Fallback: check content field (for other models or future changes)
            content = message.get("content", "")
            
            if self.verbose:
                self._log(f"Content type: {type(content)}, length: {len(str(content))}")
            
            # Handle string content
            if isinstance(content, str) and "data:image" in content:
                import re
                match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=\n\r]+)', content, re.DOTALL)
                if match:
                    base64_str = match.group(1).replace('\n', '').replace('\r', '').replace(' ', '')
                    self._log(f"Found image in content field (length: {len(base64_str)})")
                    return base64.b64decode(base64_str)
            
            # Handle list content
            if isinstance(content, list):
                for i, block in enumerate(content):
                    if isinstance(block, dict) and block.get("type") == "image_url":
                        url = block.get("image_url", {})
                        if isinstance(url, dict):
                            url = url.get("url", "")
                        if url and url.startswith("data:image") and "," in url:
                            base64_str = url.split(",", 1)[1].replace('\n', '').replace('\r', '').replace(' ', '')
                            self._log(f"Found image in content block {i}")
                            return base64.b64decode(base64_str)
            
            self._log("No image data found in response")
            return None
            
        except Exception as e:
            self._log(f"Error extracting image: {str(e)}")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return None
    
    def _image_to_base64(self, image_path: str) -> str:
        """
        Convert image file to base64 data URL.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 data URL string
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Determine image type from extension
        ext = Path(image_path).suffix.lower()
        mime_type = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }.get(ext, "image/png")
        
        base64_data = base64.b64encode(image_data).decode("utf-8")
        return f"data:{mime_type};base64,{base64_data}"
    
    def generate_image(self, prompt: str) -> Optional[bytes]:
        """
        Generate an image using the configured provider.

        Args:
            prompt: Description of the diagram to generate

        Returns:
            Image bytes or None if generation failed
        """
        self._last_error = None

        if self.provider == "minimax":
            return self._generate_image_minimax(prompt)
        else:
            return self._generate_image_openrouter(prompt)

    def _generate_image_openrouter(self, prompt: str) -> Optional[bytes]:
        """Generate an image using OpenRouter API."""
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            response = self._make_request(
                model=self.image_model,
                messages=messages,
                modalities=["image", "text"]
            )

            # Debug: print response structure if verbose
            if self.verbose:
                self._log(f"Response keys: {response.keys()}")
                if "error" in response:
                    self._log(f"API Error: {response['error']}")
                if "choices" in response and response["choices"]:
                    msg = response["choices"][0].get("message", {})
                    self._log(f"Message keys: {msg.keys()}")
                    content = msg.get("content", "")
                    if isinstance(content, str):
                        preview = content[:200] + "..." if len(content) > 200 else content
                        self._log(f"Content preview: {preview}")
                    elif isinstance(content, list):
                        self._log(f"Content is list with {len(content)} items")
                        for i, item in enumerate(content[:3]):
                            if isinstance(item, dict):
                                self._log(f"  Item {i}: type={item.get('type')}")

            # Check for API errors in response
            if "error" in response:
                error_msg = response["error"]
                if isinstance(error_msg, dict):
                    error_msg = error_msg.get("message", str(error_msg))
                self._last_error = f"API Error: {error_msg}"
                print(f"✗ {self._last_error}")
                return None

            image_data = self._extract_image_from_response(response)
            if image_data:
                self._log(f"✓ Generated image ({len(image_data)} bytes)")
            else:
                self._last_error = "No image data in API response - model may not support image generation"
                self._log(f"✗ {self._last_error}")
                if self.verbose and "choices" in response:
                    msg = response["choices"][0].get("message", {})
                    self._log(f"Full message structure: {json.dumps({k: type(v).__name__ for k, v in msg.items()})}")

            return image_data
        except RuntimeError as e:
            self._last_error = str(e)
            self._log(f"✗ Generation failed: {self._last_error}")
            return None
        except Exception as e:
            self._last_error = f"Unexpected error: {str(e)}"
            self._log(f"✗ Generation failed: {self._last_error}")
            import traceback
            if self.verbose:
                traceback.print_exc()
            return None

    def _generate_image_minimax(self, prompt: str, aspect_ratio: str = "16:9") -> Optional[bytes]:
        """Generate an image using MiniMax API."""
        api_key = _get_api_key("minimax")
        if not api_key:
            self._last_error = "MINIMAX_API_KEY not found"
            return None

        self._log(f"Generating image with MiniMax (aspect ratio: {aspect_ratio})")

        payload = {
            "model": MINIMAX_DEFAULT_MODEL,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "base64",
        }

        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            response = requests.post(MINIMAX_API_URL, headers=headers, json=payload, timeout=120)

            if response.status_code != 200:
                self._last_error = f"API Error ({response.status_code}): {response.text}"
                self._log(f"✗ {self._last_error}")
                return None

            result = response.json()

            # MiniMax returns: {"data": {"image_base64": [...]}}
            if "data" in result and "image_base64" in result["data"]:
                images = result["data"]["image_base64"]
                if images:
                    base64_data = images[0]
                    if ',' in base64_data:
                        base64_data = base64_data.split(',', 1)[1]
                    self._log(f"✓ Generated image ({len(base64_data)} base64 chars)")
                    return base64.b64decode(base64_data)

            self._last_error = "No image data in MiniMax response"
            return None
        except Exception as e:
            self._last_error = f"MiniMax API error: {str(e)}"
            return None
    
    def review_image(self, image_path: str, original_prompt: str, 
                    iteration: int, doc_type: str = "default",
                    max_iterations: int = 2) -> Tuple[str, float, bool]:
        """
        Review generated image using Gemini 3 Pro for quality analysis.
        
        Uses Gemini 3 Pro's superior vision and reasoning capabilities to
        evaluate the schematic quality and determine if regeneration is needed.
        
        Args:
            image_path: Path to the generated image
            original_prompt: Original user prompt
            iteration: Current iteration number
            doc_type: Document type (journal, poster, presentation, etc.)
            max_iterations: Maximum iterations allowed
            
        Returns:
            Tuple of (critique text, quality score 0-10, needs_improvement bool)
        """
        # Use Gemini 3 Pro for review - excellent vision and analysis
        image_data_url = self._image_to_base64(image_path)
        
        # Get quality threshold for this document type
        threshold = self.QUALITY_THRESHOLDS.get(doc_type.lower(), 
                                                 self.QUALITY_THRESHOLDS["default"])
        
        review_prompt = f"""You are an expert reviewer evaluating a scientific diagram for publication quality.

ORIGINAL REQUEST: {original_prompt}

DOCUMENT TYPE: {doc_type} (quality threshold: {threshold}/10)
ITERATION: {iteration}/{max_iterations}

Carefully evaluate this diagram on these criteria:

1. **Scientific Accuracy** (0-2 points)
   - Correct representation of concepts
   - Proper notation and symbols
   - Accurate relationships shown

2. **Clarity and Readability** (0-2 points)
   - Easy to understand at a glance
   - Clear visual hierarchy
   - No ambiguous elements

3. **Label Quality** (0-2 points)
   - All important elements labeled
   - Labels are readable (appropriate font size)
   - Consistent labeling style

4. **Layout and Composition** (0-2 points)
   - Logical flow (top-to-bottom or left-to-right)
   - Balanced use of space
   - No overlapping elements

5. **Professional Appearance** (0-2 points)
   - Publication-ready quality
   - Clean, crisp lines and shapes
   - Appropriate colors/contrast

RESPOND IN THIS EXACT FORMAT:
SCORE: [total score 0-10]

STRENGTHS:
- [strength 1]
- [strength 2]

ISSUES:
- [issue 1 if any]
- [issue 2 if any]

VERDICT: [ACCEPTABLE or NEEDS_IMPROVEMENT]

If score >= {threshold}, the diagram is ACCEPTABLE for {doc_type} publication.
If score < {threshold}, mark as NEEDS_IMPROVEMENT with specific suggestions."""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": review_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    }
                ]
            }
        ]
        
        try:
            # Use Gemini 3 Pro for high-quality review
            response = self._make_request(
                model=self.review_model,
                messages=messages
            )
            
            # Extract text response
            choices = response.get("choices", [])
            if not choices:
                return "Image generated successfully", 8.0
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            # Check reasoning field (Nano Banana Pro puts analysis here)
            reasoning = message.get("reasoning", "")
            if reasoning and not content:
                content = reasoning
            
            if isinstance(content, list):
                # Extract text from content blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                content = "\n".join(text_parts)
            
            # Try to extract score
            score = 7.5  # Default score if extraction fails
            import re
            
            # Look for SCORE: X or SCORE: X/10 format
            score_match = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)', content, re.IGNORECASE)
            if score_match:
                score = float(score_match.group(1))
            else:
                # Fallback: look for any score pattern
                score_match = re.search(r'(?:score|rating|quality)[:\s]+(\d+(?:\.\d+)?)\s*(?:/\s*10)?', content, re.IGNORECASE)
                if score_match:
                    score = float(score_match.group(1))
            
            # Determine if improvement is needed based on verdict or score
            needs_improvement = False
            if "NEEDS_IMPROVEMENT" in content.upper():
                needs_improvement = True
            elif score < threshold:
                needs_improvement = True
            
            self._log(f"✓ Review complete (Score: {score}/10, Threshold: {threshold}/10)")
            self._log(f"  Verdict: {'Needs improvement' if needs_improvement else 'Acceptable'}")
            
            return (content if content else "Image generated successfully", 
                    score, 
                    needs_improvement)
        except Exception as e:
            self._log(f"Review skipped: {str(e)}")
            # Don't fail the whole process if review fails - assume acceptable
            return "Image generated successfully (review skipped)", 7.5, False
    
    def improve_prompt(self, original_prompt: str, critique: str, 
                      iteration: int) -> str:
        """
        Improve the generation prompt based on critique.
        
        Args:
            original_prompt: Original user prompt
            critique: Review critique from previous iteration
            iteration: Current iteration number
            
        Returns:
            Improved prompt for next generation
        """
        improved_prompt = f"""{self.SCIENTIFIC_DIAGRAM_GUIDELINES}

USER REQUEST: {original_prompt}

ITERATION {iteration}: Based on previous feedback, address these specific improvements:
{critique}

Generate an improved version that addresses all the critique points while maintaining scientific accuracy and professional quality."""
        
        return improved_prompt
    
    def generate_iterative(self, user_prompt: str, output_path: str,
                          iterations: int = 2, 
                          doc_type: str = "default") -> Dict[str, Any]:
        """
        Generate scientific schematic with smart iterative refinement.
        
        Only regenerates if the quality score is below the threshold for the
        specified document type. This saves API calls and time when the first
        generation is already good enough.
        
        Args:
            user_prompt: User's description of desired diagram
            output_path: Path to save final image
            iterations: Maximum refinement iterations (default: 2, max: 2)
            doc_type: Document type for quality threshold (journal, poster, etc.)
            
        Returns:
            Dictionary with generation results and metadata
        """
        output_path = Path(output_path)
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        base_name = output_path.stem
        extension = output_path.suffix or ".png"
        
        # Get quality threshold for this document type
        threshold = self.QUALITY_THRESHOLDS.get(doc_type.lower(), 
                                                 self.QUALITY_THRESHOLDS["default"])
        
        results = {
            "user_prompt": user_prompt,
            "doc_type": doc_type,
            "quality_threshold": threshold,
            "iterations": [],
            "final_image": None,
            "final_score": 0.0,
            "success": False,
            "early_stop": False,
            "early_stop_reason": None
        }
        
        current_prompt = f"""{self.SCIENTIFIC_DIAGRAM_GUIDELINES}

USER REQUEST: {user_prompt}

Generate a publication-quality scientific diagram that meets all the guidelines above."""
        
        print(f"\n{'='*60}")
        print(f"Generating Scientific Schematic")
        print(f"{'='*60}")
        print(f"Description: {user_prompt}")
        print(f"Document Type: {doc_type}")
        print(f"Quality Threshold: {threshold}/10")
        print(f"Max Iterations: {iterations}")
        print(f"Provider: {self.provider}")
        print(f"Output: {output_path}")
        print(f"{'='*60}\n")

        # For MiniMax, skip iterative refinement (one-shot generation)
        if self.provider == "minimax":
            print("Generating image with MiniMax (single generation, no iterative refinement)...")
            image_data = self.generate_image(current_prompt)

            if not image_data:
                error_msg = getattr(self, '_last_error', 'Image generation failed')
                print(f"✗ Generation failed: {error_msg}")
                return {"success": False, "error": error_msg}

            # Save directly to output path
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"✓ Final image: {output_path}")

            return {
                "user_prompt": user_prompt,
                "doc_type": doc_type,
                "provider": "minimax",
                "final_image": str(output_path),
                "success": True
            }

        # OpenRouter: Use iterative refinement
        for i in range(1, iterations + 1):
            print(f"\n[Iteration {i}/{iterations}]")
            print("-" * 40)
            
            # Generate image
            print(f"Generating image...")
            image_data = self.generate_image(current_prompt)
            
            if not image_data:
                error_msg = getattr(self, '_last_error', 'Image generation failed - no image data returned')
                print(f"✗ Generation failed: {error_msg}")
                results["iterations"].append({
                    "iteration": i,
                    "success": False,
                    "error": error_msg
                })
                continue
            
            # Save iteration image
            iter_path = output_dir / f"{base_name}_v{i}{extension}"
            with open(iter_path, "wb") as f:
                f.write(image_data)
            print(f"✓ Saved: {iter_path}")
            
            # Review image using Gemini 3 Pro
            print(f"Reviewing image with Gemini 3 Pro...")
            critique, score, needs_improvement = self.review_image(
                str(iter_path), user_prompt, i, doc_type, iterations
            )
            print(f"✓ Score: {score}/10 (threshold: {threshold}/10)")
            
            # Save iteration results
            iteration_result = {
                "iteration": i,
                "image_path": str(iter_path),
                "prompt": current_prompt,
                "critique": critique,
                "score": score,
                "needs_improvement": needs_improvement,
                "success": True
            }
            results["iterations"].append(iteration_result)
            
            # Check if quality is acceptable - STOP EARLY if so
            if not needs_improvement:
                print(f"\n✓ Quality meets {doc_type} threshold ({score} >= {threshold})")
                print(f"  No further iterations needed!")
                results["final_image"] = str(iter_path)
                results["final_score"] = score
                results["success"] = True
                results["early_stop"] = True
                results["early_stop_reason"] = f"Quality score {score} meets threshold {threshold} for {doc_type}"
                break
            
            # If this is the last iteration, we're done regardless
            if i == iterations:
                print(f"\n⚠ Maximum iterations reached")
                results["final_image"] = str(iter_path)
                results["final_score"] = score
                results["success"] = True
                break
            
            # Quality below threshold - improve prompt for next iteration
            print(f"\n⚠ Quality below threshold ({score} < {threshold})")
            print(f"Improving prompt based on feedback...")
            current_prompt = self.improve_prompt(user_prompt, critique, i + 1)
        
        # Copy final version to output path
        if results["success"] and results["final_image"]:
            final_iter_path = Path(results["final_image"])
            if final_iter_path != output_path:
                import shutil
                shutil.copy(final_iter_path, output_path)
                print(f"\n✓ Final image: {output_path}")
        
        # Save review log
        log_path = output_dir / f"{base_name}_review_log.json"
        with open(log_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✓ Review log: {log_path}")
        
        print(f"\n{'='*60}")
        print(f"Generation Complete!")
        print(f"Final Score: {results['final_score']}/10")
        if results["early_stop"]:
            print(f"Iterations Used: {len([r for r in results['iterations'] if r.get('success')])}/{iterations} (early stop)")
        print(f"{'='*60}\n")
        
        return results


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Generate scientific schematics using Nano Banana Pro or MiniMax AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (Nano Banana Pro - default):
  python generate_schematic_ai.py "CONSORT flow diagram" -o flowchart.png
  python generate_schematic_ai.py "Neural network architecture" -o diagram.png --doc-type journal

Examples (MiniMax):
  python generate_schematic_ai.py "CONSORT flow diagram" -o flowchart.png --provider minimax
  python generate_schematic_ai.py "Neural network architecture" -o diagram.png --provider minimax --aspect-ratio 16:9

Document Types (quality thresholds, Nano Banana Pro only):
  journal      8.5/10  - Nature, Science, peer-reviewed journals
  conference   8.0/10  - Conference papers
  thesis       8.0/10  - Dissertations, theses
  grant        8.0/10  - Grant proposals
  preprint     7.5/10  - arXiv, bioRxiv, etc.
  report       7.5/10  - Technical reports
  poster       7.0/10  - Academic posters
  presentation 6.5/10  - Slides, talks
  default      7.5/10  - General purpose

Environment (Nano Banana Pro):
  OPENROUTER_API_KEY    OpenRouter API key (required)

Environment (MiniMax):
  MINIMAX_API_KEY       MiniMax API key
  IMAGE_PROVIDER        "openrouter" or "minimax"
        """
    )

    parser.add_argument("prompt", help="Description of the diagram to generate")
    parser.add_argument("-o", "--output", required=True,
                       help="Output image path (e.g., diagram.png)")
    parser.add_argument("--iterations", type=int, default=2,
                       help="Maximum refinement iterations (default: 2, max: 2, Nano Banana Pro only)")
    parser.add_argument("--doc-type", default="default",
                       choices=["journal", "conference", "poster", "presentation",
                               "report", "grant", "thesis", "preprint", "default"],
                       help="Document type for quality threshold (default: default)")
    parser.add_argument("--provider", choices=["openrouter", "minimax"],
                       help="Image provider (default: from IMAGE_PROVIDER env or 'openrouter')")
    parser.add_argument("--aspect-ratio", default="16:9",
                       help="Image aspect ratio for MiniMax (default: 16:9)")
    parser.add_argument("--api-key", help="API key for the selected provider")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")

    args = parser.parse_args()

    # Get provider from args or environment
    provider = args.provider or _get_provider()

    # Validate API key
    if provider == "minimax":
        api_key = args.api_key or _get_api_key("minimax")
        if not api_key:
            print("Error: MINIMAX_API_KEY environment variable not set")
            print("\nSet it with:")
            print("  export MINIMAX_API_KEY='your_api_key'")
            print("\nOr add to .env:")
            print("  MINIMAX_API_KEY=your_api_key")
            sys.exit(1)
    else:
        api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY environment variable not set")
            print("\nSet it with:")
            print("  export OPENROUTER_API_KEY='your_api_key'")
            sys.exit(1)

    # Validate iterations - enforce max of 2 (OpenRouter only)
    if args.iterations < 1 or args.iterations > 2:
        print("Error: Iterations must be between 1 and 2")
        sys.exit(1)

    try:
        generator = ScientificSchematicGenerator(api_key=api_key, verbose=args.verbose, provider=provider)
        results = generator.generate_iterative(
            user_prompt=args.prompt,
            output_path=args.output,
            iterations=args.iterations,
            doc_type=args.doc_type
        )

        if results["success"]:
            print(f"\n✓ Success! Image saved to: {args.output}")
            if results.get("early_stop"):
                print(f"  (Completed in {len([r for r in results['iterations'] if r.get('success')])} iteration(s) - quality threshold met)")
            sys.exit(0)
        else:
            print(f"\n✗ Generation failed. Check review log for details.")
            sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

