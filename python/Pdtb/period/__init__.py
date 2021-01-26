import periodictable.core

# Delayed loading of the period information
def _load_discoverer():
    """
    The name of the period to which the element belongs.
    """
    from . import core
    core.init(periodictable.core.default_table())

periodictable.core.delayed_load(['period'], _load_discoverer)
