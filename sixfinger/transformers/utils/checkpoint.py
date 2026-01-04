"""
Model checkpoint utilities
"""

import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional
import json
import time


def save_checkpoint(
    path: Path,
    model_state: Dict[str, np.ndarray],
    config: Dict[str, Any],
    training_state: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Save model checkpoint
    
    Args:
        path: Save path (.npz file)
        model_state: Model weights (numpy arrays)
        config: Model configuration
        training_state: Training state (step, epoch, etc.)
        metadata: Additional metadata
    """
    
    checkpoint = {
        'version': '1.0',
        'timestamp': time.time(),
    }
    
    # Add all components
    checkpoint.update(model_state)
    checkpoint['config'] = np.array([config], dtype=object)
    
    if training_state:
        checkpoint['training_state'] = np.array([training_state], dtype=object)
    
    if metadata:
        checkpoint['metadata'] = np.array([metadata], dtype=object)
    
    # Save compressed
    np.savez_compressed(path, **checkpoint)


def load_checkpoint(path: Path) -> Dict[str, Any]:
    """
    Load model checkpoint
    
    Args:
        path: Checkpoint path
        
    Returns:
        Dictionary with 'model_state', 'config', 'training_state', 'metadata'
    """
    
    if not path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {path}")
    
    data = np.load(path, allow_pickle=True)
    
    # Extract model weights (all arrays except special keys)
    special_keys = {'config', 'training_state', 'metadata', 'version', 'timestamp'}
    model_state = {
        key: data[key]
        for key in data.files
        if key not in special_keys
    }
    
    # Extract config
    config = data['config'].item() if 'config' in data else {}
    
    # Extract training state
    training_state = None
    if 'training_state' in data and data['training_state'] is not None:
        training_state = data['training_state'].item()
    
    # Extract metadata
    metadata = None
    if 'metadata' in data and data['metadata'] is not None:
        metadata = data['metadata'].item()
    
    return {
        'model_state': model_state,
        'config': config,
        'training_state': training_state,
        'metadata': metadata,
        'version': data.get('version', 'unknown'),
        'timestamp': data.get('timestamp', 0),
    }


def save_config(path: Path, config: Dict[str, Any]):
    """Save config as JSON"""
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)


def load_config(path: Path) -> Dict[str, Any]:
    """Load config from JSON"""
    with open(path, 'r') as f:
        return json.load(f)