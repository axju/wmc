"""Load all entry poins"""
from pkg_resources import iter_entry_points
from wmc.utils import BasicCommand


def get_basic_call():
    """get all functions from the basic class"""
    for name in dir(BasicCommand):
        if not name.startswith('_') and callable(getattr(BasicCommand, name)):
            yield name


def find_entry_points():
    """Find all register entry points."""
    entrys = [enp.name for enp in iter_entry_points(group='wmc.register_cls')]
    for name in get_basic_call():
        entrys += [enp.name for enp in iter_entry_points(group='wmc.register_{}'.format(name))]
    return entrys


def load_entry_points():
    """Load the classes and create new for only functions entry points"""
    command = {}
    for enp in iter_entry_points(group='wmc.register_cls'):
        cls = enp.load()
        command[enp.name] = cls
        command[enp.name].__name__ = enp.name

    for name in get_basic_call():
        for enp in iter_entry_points(group='wmc.register_{}'.format(name)):
            func = enp.load()
            if enp.name in command:
                setattr(command[enp.name], name, func)
            else:
                command[enp.name] = type(enp.name, (BasicCommand, ), {name: func, '__name__': enp.name})
    return command
