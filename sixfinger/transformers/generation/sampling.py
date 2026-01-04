"""
Token sampling strategies for text generation
"""

import numpy as np
from typing import Optional


def greedy_sample(logits: np.ndarray) -> int:
    """
    Greedy sampling - always pick highest probability
    
    Args:
        logits: Logit scores [vocab_size]
        
    Returns:
        Token index with highest score
    """
    return int(np.argmax(logits))


def top_k_top_p_filtering(
    logits: np.ndarray,
    top_k: int = 0,
    top_p: float = 1.0,
    min_tokens_to_keep: int = 1
) -> np.ndarray:
    """
    Filter logits using top-k and/or nucleus (top-p) filtering
    
    Args:
        logits: Logit scores [vocab_size]
        top_k: Keep only top k tokens (0 = disabled)
        top_p: Keep smallest set of tokens with cumsum >= top_p (1.0 = disabled)
        min_tokens_to_keep: Minimum number of tokens to keep
        
    Returns:
        Filtered logits
    """
    
    logits = logits.copy()
    
    # Top-k filtering
    if top_k > 0:
        top_k = max(top_k, min_tokens_to_keep)
        # Get indices of top-k
        indices_to_remove = logits < np.partition(logits, -top_k)[-top_k]
        logits[indices_to_remove] = -float('inf')
    
    # Top-p (nucleus) filtering
    if top_p < 1.0:
        sorted_indices = np.argsort(logits)[::-1]
        sorted_logits = logits[sorted_indices]
        
        # Convert to probabilities
        sorted_probs = softmax(sorted_logits)
        
        # Cumulative probabilities
        cumulative_probs = np.cumsum(sorted_probs)
        
        # Remove tokens with cumulative probability above threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        
        # Keep at least min_tokens_to_keep
        sorted_indices_to_remove[:min_tokens_to_keep] = False
        
        # Scatter sorted tensors to original indexing
        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = -float('inf')
    
    return logits


def softmax(x: np.ndarray) -> np.ndarray:
    """Numerically stable softmax"""
    e_x = np.exp(x - np.max(x))
    return e_x / (e_x.sum() + 1e-10)


def sample_token(
    logits: np.ndarray,
    temperature: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    return_probs: bool = False
) -> int:
    """
    Sample next token from logits with various strategies
    
    Args:
        logits: Logit scores [vocab_size]
        temperature: Sampling temperature (higher = more random)
            - 0.0: greedy (deterministic)
            - 0.7: focused, coherent
            - 1.0: balanced
            - 1.5+: creative, diverse
        top_k: Top-k filtering (0 = disabled)
        top_p: Nucleus sampling (1.0 = disabled)
        return_probs: Also return probability distribution
        
    Returns:
        Sampled token index (and optionally probabilities)
        
    Example:
        >>> logits = model.forward(context)
        >>> next_token = sample_token(logits, temperature=0.8, top_p=0.9)
    """
    
    # Handle greedy case
    if temperature == 0.0:
        token = greedy_sample(logits)
        if return_probs:
            probs = np.zeros_like(logits)
            probs[token] = 1.0
            return token, probs
        return token
    
    # Apply temperature
    logits = logits / temperature
    
    # Apply top-k and top-p filtering
    filtered_logits = top_k_top_p_filtering(logits, top_k=top_k, top_p=top_p)
    
    # Convert to probabilities
    probs = softmax(filtered_logits)
    
    # Handle case where all probabilities are filtered out
    if np.all(np.isinf(filtered_logits)):
        # Fall back to greedy
        token = greedy_sample(logits)
        if return_probs:
            probs = np.zeros_like(logits)
            probs[token] = 1.0
            return token, probs
        return token
    
    # Sample from distribution
    token = np.random.choice(len(probs), p=probs)
    
    if return_probs:
        return int(token), probs
    return int(token)


def beam_search(
    model,
    initial_context: bytes,
    max_length: int,
    beam_width: int = 5,
    length_penalty: float = 1.0
) -> list:
    """
    Beam search decoding (for future implementation)
    
    Args:
        model: Language model with forward() method
        initial_context: Starting bytes
        max_length: Maximum generation length
        beam_width: Number of beams to maintain
        length_penalty: Length normalization factor
        
    Returns:
        List of (sequence, score) tuples
    """
    raise NotImplementedError(
        "Beam search is not yet implemented. "
        "Use sample_token() with temperature=0 for greedy decoding."
    )