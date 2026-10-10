"""Extension point for GAN / learned enhancement.

To add a model: subclass JewelryEnhancer, load your PyTorch/TensorFlow weights
in __init__, implement enhance(), and register it in tryon_service.ENHANCER.
The app works without any of that."""
from abc import ABC, abstractmethod
import numpy as np


class JewelryEnhancer(ABC):
    @abstractmethod
    def enhance(self, image: np.ndarray, jewelry: np.ndarray, mask: np.ndarray | None) -> np.ndarray:
        """Return the improved composite image (same shape as `image`)."""


class BasicEnhancer(JewelryEnhancer):
    """Default: leaves the composite unchanged (no learned model)."""
    def enhance(self, image, jewelry, mask):
        return image
