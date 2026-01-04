#!/usr/bin/env python3
"""
CLI tool for training SpeedLM models

Usage:
    sixfinger-train --data mydata.txt --output model.npz
    sixfinger-train --data mydata.txt --config config.json
"""

import argparse
import sys
from pathlib import Path
import json

try:
    from ..models.speedlm import SpeedLM
    from ..utils.logger import ProgressLogger
except ImportError:
    print("Error: transformers module not installed")
    print("Install with: pip install sixfinger[transformers]")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Train SpeedLM language model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic training
  sixfinger-train --data wiki.txt --output wiki_model.npz
  
  # Custom parameters
  sixfinger-train --data data.txt --output model.npz \\
      --buckets 1000000 --features 2048 --epochs 3
  
  # From config file
  sixfinger-train --data data.txt --config config.json
  
  # Resume training
  sixfinger-train --data data.txt --resume model.npz
        """
    )
    
    # Required
    parser.add_argument(
        '--data',
        type=str,
        required=True,
        help='Training data file path'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='speedlm_model.npz',
        help='Output model path (default: speedlm_model.npz)'
    )
    
    # Model architecture
    parser.add_argument(
        '--buckets',
        type=int,
        default=500_000,
        help='Number of hash buckets (default: 500000)'
    )
    
    parser.add_argument(
        '--features',
        type=int,
        default=1024,
        help='Hidden dimension size (default: 1024)'
    )
    
    parser.add_argument(
        '--context',
        type=str,
        default='1,2,3,4,5,8,12',
        help='Context sizes (comma-separated, default: 1,2,3,4,5,8,12)'
    )
    
    parser.add_argument(
        '--vocab',
        type=int,
        default=256,
        help='Vocabulary size (default: 256 for byte-level)'
    )
    
    # Training
    parser.add_argument(
        '--epochs',
        type=int,
        default=1,
        help='Number of training epochs (default: 1)'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=100_000,
        help='Chunk size for streaming (default: 100000)'
    )
    
    parser.add_argument(
        '--lr',
        type=float,
        default=0.01,
        help='Learning rate (default: 0.01)'
    )
    
    # Config
    parser.add_argument(
        '--config',
        type=str,
        help='Load parameters from JSON config file'
    )
    
    parser.add_argument(
        '--resume',
        type=str,
        help='Resume training from checkpoint'
    )
    
    # Options
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Disable progress output'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Generate test output after training'
    )
    
    parser.add_argument(
        '--test-prompt',
        type=str,
        default='The',
        help='Test generation prompt (default: "The")'
    )
    
    parser.add_argument(
        '--test-length',
        type=int,
        default=200,
        help='Test generation length (default: 200)'
    )
    
    return parser.parse_args()


def load_config_file(path: str) -> dict:
    """Load config from JSON"""
    with open(path, 'r') as f:
        return json.load(f)


def main():
    args = parse_args()
    
    logger = ProgressLogger(enabled=not args.quiet)
    
    # Load config from file if provided
    config = {}
    if args.config:
        logger.info(f"Loading config from {args.config}")
        config = load_config_file(args.config)
    
    # Override with command-line args
    model_config = {
        'n_buckets': config.get('n_buckets', args.buckets),
        'n_features': config.get('n_features', args.features),
        'context_sizes': config.get('context_sizes', [int(x) for x in args.context.split(',')]),
        'vocab': config.get('vocab', args.vocab),
        'lr': config.get('lr', args.lr),
        'verbose': not args.quiet,
    }
    
    training_config = {
        'chunk_size': config.get('chunk_size', args.chunk_size),
        'num_epochs': config.get('epochs', args.epochs),
    }
    
    # Check data file
    data_path = Path(args.data)
    if not data_path.exists():
        logger.error(f"Data file not found: {data_path}")
        sys.exit(1)
    
    # Header
    logger.header("SixFinger SpeedLM Training")
    
    # Create or load model
    if args.resume:
        logger.info(f"Resuming from checkpoint: {args.resume}")
        model = SpeedLM.from_pretrained(args.resume, verbose=not args.quiet)
    else:
        logger.section("Model Configuration")
        logger.table(model_config)
        model = SpeedLM(**model_config)
    
    # Training config
    logger.section("Training Configuration")
    logger.table({
        'Data file': str(data_path),
        'File size': f"{data_path.stat().st_size / 1024 / 1024:.2f} MB",
        'Epochs': training_config['num_epochs'],
        'Chunk size': f"{training_config['chunk_size'] / 1024:.1f} KB",
        'Output': args.output,
    })
    
    # Train
    try:
        stats = model.train_file(str(data_path), **training_config)
        
        # Save
        logger.section("Saving Model")
        model.save(args.output)
        
        # Summary
        logger.section("Training Summary")
        logger.table({
            'Total tokens': f"{stats['tokens']:,}",
            'Final loss': f"{stats['loss']:.4f}",
            'Training time': f"{stats['time'] / 60:.1f} minutes",
            'Speed': f"{stats['speed_kb_s']:.1f} KB/s",
            'Model size': f"{Path(args.output).stat().st_size / 1024 / 1024:.1f} MB",
        })
        
        # Test generation
        if args.test:
            logger.section("Test Generation")
            prompt = args.test_prompt.encode('utf-8')
            logger.info(f"Prompt: {args.test_prompt}")
            
            output = model.generate(prompt, length=args.test_length, temperature=0.8)
            
            print("\n" + "─" * 60)
            print(output.decode('utf-8', errors='ignore'))
            print("─" * 60 + "\n")
        
        logger.success("Training complete!")
        
    except KeyboardInterrupt:
        logger.warning("\nTraining interrupted by user")
        logger.info("Saving checkpoint...")
        model.save(args.output + '.interrupted')
        sys.exit(1)
    except Exception as e:
        logger.error(f"Training failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()