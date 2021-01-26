import periodictable.core
# Delayed loading of the element discoverer information
def _load_group_color():
    """
    The name of the group color of the element.
    """
    from . import core
    core.init(periodictable.core.default_table())

periodictable.core.delayed_load(['group_color'], _load_group_color)
