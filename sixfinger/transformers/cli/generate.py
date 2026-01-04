#!/usr/bin/env python3
"""
CLI tool for text generation with SpeedLM

Usage:
    sixfinger-generate --model model.npz --prompt "Hello"
    echo "Once upon a time" | sixfinger-generate --model model.npz
"""

import argparse
import sys
from pathlib import Path

try:
    from ..models.speedlm import SpeedLM
    from ..utils.logger import ProgressLogger
except ImportError:
    print("Error: transformers module not installed")
    print("Install with: pip install sixfinger[transformers]")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate text with SpeedLM model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic generation
  sixfinger-generate --model wiki.npz --prompt "The future of AI"
  
  # Creative writing
  sixfinger-generate --model model.npz --prompt "Story:" \\
      --length 500 --temperature 1.2
  
  # Focused/deterministic
  sixfinger-generate --model model.npz --prompt "Definition:" \\
      --temperature 0.3
  
  # With top-p sampling
  sixfinger-generate --model model.npz --prompt "Code:" \\
      --top-p 0.9
  
  # From stdin
  echo "Translate to French:" | sixfinger-generate --model model.npz
        """
    )
    
    parser.add_argument(
        '--model',
        type=str,
        required=True,
        help='Model checkpoint path (.npz file)'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        default=None,
        help='Generation prompt (or read from stdin)'
    )
    
    parser.add_argument(
        '--length',
        type=int,
        default=200,
        help='Number of tokens to generate (default: 200)'
    )
    
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.8,
        help='Sampling temperature 0.0-2.0 (default: 0.8)'
    )
    
    parser.add_argument(
        '--top-k',
        type=int,
        default=0,
        help='Top-k sampling (0=disabled, default: 0)'
    )
    
    parser.add_argument(
        '--top-p',
        type=float,
        default=1.0,
        help='Nucleus sampling 0.0-1.0 (default: 1.0=disabled)'
    )
    
    parser.add_argument(
        '--num-samples',
        type=int,
        default=1,
        help='Number of samples to generate (default: 1)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Save output to file'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only output generated text'
    )
    
    parser.add_argument(
        '--show-prompt',
        action='store_true',
        help='Include prompt in output'
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    
    logger = ProgressLogger(enabled=not args.quiet)
    
    # Check model
    model_path = Path(args.model)
    if not model_path.exists():
        logger.error(f"Model not found: {model_path}")
        sys.exit(1)
    
    # Get prompt
    if args.prompt is None:
        # Read from stdin
        if not args.quiet:
            logger.info("Reading prompt from stdin...")
        prompt = sys.stdin.read().strip()
    else:
        prompt = args.prompt
    
    if not prompt:
        logger.error("Empty prompt")
        sys.exit(1)
    
    # Load model
    if not args.quiet:
        logger.section("Loading Model")
        logger.info(f"Model: {model_path}")
    
    model = SpeedLM.from_pretrained(model_path, verbose=not args.quiet)
    
    # Generation config
    gen_config = {
        'length': args.length,
        'temperature': args.temperature,
        'top_k': args.top_k,
        'top_p': args.top_p,
    }
    
    if not args.quiet:
        logger.section("Generation Config")
        logger.table({
            'Prompt': prompt[:50] + ('...' if len(prompt) > 50 else ''),
            'Length': args.length,
            'Temperature': args.temperature,
            'Top-k': args.top_k if args.top_k > 0 else 'disabled',
            'Top-p': args.top_p if args.top_p < 1.0 else 'disabled',
            'Samples': args.num_samples,
        })
    
    # Generate
    outputs = []
    
    for i in range(args.num_samples):
        if not args.quiet and args.num_samples > 1:
            logger.info(f"\nGenerating sample {i+1}/{args.num_samples}...")
        
        output = model.generate(
            prompt.encode('utf-8'),
            **gen_config,
            verbose=False
        )
        
        output_text = output.decode('utf-8', errors='ignore')
        outputs.append(output_text)
        
        # Print output
        if args.num_samples > 1 and not args.quiet:
            print(f"\n{'='*60}")
            print(f"Sample {i+1}:")
            print('='*60)
        
        if args.show_prompt:
            print(output_text)
        else:
            # Remove prompt from output
            print(output_text[len(prompt):])
        
        if args.num_samples > 1 and not args.quiet:
            print('='*60)
    
    # Save to file
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, text in enumerate(outputs):
                if args.num_samples > 1:
                    f.write(f"=== Sample {i+1} ===\n")
                f.write(text)
                if i < len(outputs) - 1:
                    f.write('\n\n')
        
        if not args.quiet:
            logger.success(f"Saved to {output_path}")


if __name__ == '__main__':
    main()