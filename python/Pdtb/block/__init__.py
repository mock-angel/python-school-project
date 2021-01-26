import periodictable.core
# Delayed loading of the element block information.

def _load_block():
    """
    The block it belongs to [s, p, d, f].
    """
    from . import core
    core.init(periodictable.core.default_table())
    
periodictable.core.delayed_load(['block'], _load_block)
