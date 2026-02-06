#!/usr/bin/env python3
/// script
dependencies = ["requests>=2.31.0", "python-dotenv>=1.0.0"]
///

"""
Scientific schematic generation using Nano Banana Pro or MiniMax.

Generate any scientific diagram by describing it in natural language.
Supports two providers:
- Nano Banana Pro (default): Smart iterative refinement with Gemini 3 Pro quality review
- MiniMax: Fast single-shot generation

Configuration:
  API keys can be set via environment variables or .env file in the project root.

Usage (Nano Banana Pro):
    python generate_schematic.py "CONSORT flowchart" -o flowchart.png --provider openrouter

Usage (MiniMax):
    python generate_schematic.py "CONSORT flowchart" -o flowchart.png --provider minimax
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Try to load .env file from current directory or project root
def _load_env_file():
    """Load .env file from current directory or parent directories."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return False

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
        if cwd == cwd.parent:
            break

    return False


def main():
    """Command-line interface."""
    # Load .env file first
    _load_env_file()

    parser = argparse.ArgumentParser(
        description="Generate scientific schematics using Nano Banana Pro or MiniMax",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Providers:
  openrouter  Nano Banana Pro with iterative refinement (default)
  minimax     MiniMax fast single-shot generation

Document Types (quality thresholds, openrouter only):
  journal      8.5/10  - Nature, Science, peer-reviewed journals
  conference   8.0/10  - Conference papers
  thesis       8.0/10  - Dissertations, theses
  grant        8.0/10  - Grant proposals
  preprint     7.5/10  - arXiv, bioRxiv, etc.
  report       7.5/10  - Technical reports
  poster       7.0/10  - Academic posters
  presentation 6.5/10  - Slides, talks
  default      7.5/10  - General purpose

Examples (Nano Banana Pro - default):
  python generate_schematic.py "CONSORT flow" -o flowchart.png --doc-type journal
  python generate_schematic.py "Neural network" -o nn.png --doc-type presentation

Examples (MiniMax):
  python generate_schematic.py "CONSORT flow" -o flowchart.png --provider minimax
  python generate_schematic.py "Circuit diagram" -o circuit.png --provider minimax --aspect-ratio 16:9

Environment (openrouter):
  OPENROUTER_API_KEY    Required for Nano Banana Pro

Environment (minimax):
  MINIMAX_API_KEY       Required for MiniMax
  IMAGE_PROVIDER        "openrouter" or "minimax" (default: openrouter)
        """
    )

    parser.add_argument("prompt",
                       help="Description of the diagram to generate")
    parser.add_argument("-o", "--output", required=True,
                       help="Output file path")
    parser.add_argument("--provider", choices=["openrouter", "minimax"],
                       help="Image provider (default: openrouter, or set IMAGE_PROVIDER env)")
    parser.add_argument("--doc-type", default="default",
                       choices=["journal", "conference", "poster", "presentation",
                               "report", "grant", "thesis", "preprint", "default"],
                       help="Document type for quality threshold (default: default)")
    parser.add_argument("--iterations", type=int, default=2,
                       help="Maximum refinement iterations (default: 2, max: 2, openrouter only)")
    parser.add_argument("--aspect-ratio", default="16:9",
                       help="Aspect ratio for MiniMax (default: 16:9)")
    parser.add_argument("--api-key",
                       help="API key for the provider (or use provider-specific env var)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")

    args = parser.parse_args()

    # Get provider from args or environment
    provider = args.provider or os.getenv("IMAGE_PROVIDER", "openrouter")

    # Check for API key based on provider
    if provider == "minimax":
        api_key = args.api_key or os.getenv("MINIMAX_API_KEY")
        if not api_key:
            print("Error: MINIMAX_API_KEY environment variable not set")
            print("\nFor MiniMax generation, you need a MiniMax API key.")
            print("Get one at: https://api.minimaxi.com")
            print("\nSet it with:")
            print("  export MINIMAX_API_KEY='your_api_key'")
            print("\nOr use --api-key flag")
            sys.exit(1)
    else:
        api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY environment variable not set")
            print("\nFor Nano Banana Pro generation, you need an OpenRouter API key.")
            print("Get one at: https://openrouter.ai/keys")
            print("\nSet it with:")
            print("  export OPENROUTER_API_KEY='your_api_key'")
            print("\nOr use --api-key flag")
            sys.exit(1)
    
    # Find AI generation script
    script_dir = Path(__file__).parent
    ai_script = script_dir / "generate_schematic_ai.py"
    
    if not ai_script.exists():
        print(f"Error: AI generation script not found: {ai_script}")
        sys.exit(1)
    
    # Build command
    cmd = [sys.executable, str(ai_script), args.prompt, "-o", args.output]

    if provider and provider != "openrouter":
        cmd.extend(["--provider", provider])

    if args.aspect_ratio and provider == "minimax":
        cmd.extend(["--aspect-ratio", args.aspect_ratio])

    if args.doc_type != "default":
        cmd.extend(["--doc-type", args.doc_type])

    # Enforce max 2 iterations (openrouter only, minimax ignores)
    iterations = min(args.iterations, 2)
    if iterations != 2:
        cmd.extend(["--iterations", str(iterations)])

    if api_key:
        cmd.extend(["--api-key", api_key])

    if args.verbose:
        cmd.append("-v")
    
    # Execute
    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error executing AI generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

