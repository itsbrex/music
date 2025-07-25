"""Legacy synthesizers maintained for backwards compatibility."""

from .CanonicalSynth import CanonicalSynth
from .IteratorSynth import IteratorSynth
from .classes import Being

__all__ = [
    'Being',
    'CanonicalSynth',
    'IteratorSynth'
]
