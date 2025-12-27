"""
pygenetic: An Efficient Generic, User-friendly Python Genetic Algorithm API

This package provides both high-level and low-level APIs for genetic algorithms,
supporting various selection, crossover, and mutation operations.
"""

from . import ChromosomeFactory
from . import Evolution
from . import GAEngine
from . import Population
from . import SimpleGA
from . import Statistics
from . import Utils

# Optional import for ANNEvolve (requires keras/tensorflow)
try:
    from . import ANNEvolve
    _HAS_ANN = True
except ImportError:
    _HAS_ANN = False
    ANNEvolve = None

__version__ = "1.0.2"
__author__ = "Bharatraj S Telkar, Daniel Isaac, Shreyas V Patil"
__email__ = "telkarraj@gmail.com, danielbcbs2@gmail.com, pshreyasv100@gmail.com"

__all__ = [
    'ChromosomeFactory', 
    'Evolution',
    'GAEngine',
    'Population',
    'SimpleGA',
    'Statistics',
    'Utils'
]

if _HAS_ANN:
    __all__.append('ANNEvolve')