import periodictable.core
# Delayed loading of the element discoverer information
def _load_discoverer():
    """
    The name of the person or group who discovered the element.
    """
    from . import core
    core.init(periodictable.core.default_table())
#periodictable.core.delayed_load(['shells'], _load,
#isotope=True, element=False)


periodictable.core.delayed_load(['group'], _load_discoverer)


#import periodictable.core
## Delayed loading of the element discoverer information
#def _load():
#    """
#    The name of the person or group who discovered the element.
#    """
#    from . import core
#    core.init(periodictable.core.default_table())
##periodictable.core.delayed_load(['shells'], _load,
##isotope=True, element=False)


#periodictable.core.delayed_load(['discoverer'], _load)
