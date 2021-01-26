import periodictable.core
def _load_discoverer():
    from . import core
    core.init(periodictable.core.default_table())

periodictable.core.delayed_load(['series'], _load_discoverer)
