"""
Sixfinger Transformers
======================

CPU-optimized language models for on-device training and inference.

Key Features:
  - 10-40x faster than traditional transformers on CPU
  - No GPU required - runs on phones (PyDroid3, Termux)
  - Memory efficient: ternary weights (-1, 0, +1)
  - Streaming training: no batch loading needed

Models:
  - SpeedLM: Hash-based ternary model (recommended)

Example:
  >>> from sixfinger.transformers import SpeedLM
  >>> 
  >>> # Train
  >>> model = SpeedLM(n_buckets=500_000, n_features=1024)
  >>> model.train_file('mydata.txt')
  >>> model.save('my_model.npz')
  >>> 
  >>> # Generate
  >>> model.load('my_model.npz')
  >>> output = model.generate(b'Hello world', length=200)
  >>> print(output.decode('utf-8'))

Installation:
  pip install sixfinger[transformers]
"""

__version__ = "2.0.0"

# Check dependencies
try:
    import numpy as np
except ImportError:
    raise ImportError(
        "Sixfinger transformers requires numpy. "
        "Install with: pip install sixfinger[transformers]"
    )

# Import models
from .models.speedlm import SpeedLM
from .utils.logger import ProgressLogger
from .generation.sampling import sample_token, greedy_sample

__all__ = [
    'SpeedLM',
    'ProgressLogger',
    'sample_token',
    'greedy_sample',
]