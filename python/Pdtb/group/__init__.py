import periodictable.core
# Delayed loading of the element group information.
def _load_group():
    """
    The name of the group of the element.
    """
    from . import core
    core.init(periodictable.core.default_table())

periodictable.core.delayed_load(['group'], _load_group)
