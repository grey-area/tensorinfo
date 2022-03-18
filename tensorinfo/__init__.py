from .tensors import tensorinfo

__version__ = '0.0.1'


def param_count(module):
    return sum(p.numel() for p in module.parameters() if p.requires_grad)