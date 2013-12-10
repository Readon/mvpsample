"""
MiniVC - a small and simple, mvc library for python. it doesn't do much. thats a feature.
mvc, so if nothing else, we can throw the laundry that is our code into three different piles.
inspired by puremvc python by Toby de Havilland <toby.de.havilland@puremvc.org>
"""



from functools import partial

class Singleton(object):
    """singleton check. only instantiates when passed a string key"""

    def __init__(self, *args):
        print args
        assert args[-1] == 'there_can_be_only_one', 'singletons cant be instantiated directly'

class Controller(Singleton):
    """singleton. manages controller objects"""

    def __init__(self, *args):
        Singleton.__init__(self, *args)
        self.view = get_view()
        self.command_map = { }

    def handle_note(self, note):
        assert note['name'] in self.command_map, 'no such command: {0}'.format(note['name'])
        cmd = self.command_map[note['name']]
        cmd(get_facade(), note)

    def register_command(self, name, cmd): # cmd is a controller function or a controller class
        assert name not in self.command_map, 'there is already a command with name {0}: {1}'.format(name, self.command_map[name])
        self.view.register_observer(name, { 'func': self.handle_note, 'obj': self })
        self.command_map[name] = cmd

    def remove_command(self, name):
        if name in self.command_map:
            self.view.remove_observer(name, self)
            del self.command_map[name]

class Model(Singleton):
    """singleton. manages model objects"""

    def __init__(self, *args):
        Singleton.__init__(self, *args)
        self.proxy_map = { }

    def register_proxy(self, proxy):
        assert proxy.name not in self.proxy_map, 'proxy with name {0} already registered'.format(proxy.name)
        self.proxy_map[proxy.name] = proxy
        proxy.on_register()
        return proxy

    def get_proxy(self, name):
        return self.proxy_map.get(name, None)

    def remove_proxy(self, name):
        proxy = self.proxy_map.get(name, None)
        if proxy:
            del self.proxy_map[name]
            proxy.on_remove()

class View(Singleton):
    """singleton. manages view objects"""

    def __init__(self, *args):
        Singleton.__init__(self, *args)
        self.observer_map = { }
        self.mediator_map = { }

    def register_observer(self, name, observer):
        assert { 'func', 'obj' } == set(observer.keys()), "observer should be {'func':f, 'obj':o}"
        if not name in self.observer_map:
            self.observer_map[name] = []
        observers = self.observer_map[name]
        assert observer['obj'] not in [o['obj'] for o in observers], 'obj: {0} is already observing note.name: {1}'.format(observer['obj'], name)
        observers.append(observer)

    def notify_observers(self, note):
        for observer in self.observer_map.get(note['name'], []):
            observer['func'](note)

    def remove_observer(self, name, obj):
        observers = self.observer_map[name]
        for observer in observers:
            if observer['obj'] is obj:
                observers.remove(observer)
                break

    def register_mediator(self, mediator):
        assert mediator.name not in self.mediator_map, 'mediator with name "{0}" already registered.'.format(mediator.name)
        self.mediator_map[mediator.name] = mediator
        for interest in mediator.interests:
            self.register_observer(interest, { 'func': mediator.handle_note, 'obj': mediator })
        mediator.on_register()
        return mediator

    def get_mediator(self, name):
        return self.mediator_map.get(name, None)

    def remove_mediator(self, name):
        mediator = self.get_mediator(name)
        assert mediator, 'no mediator with name "{0}" to remove.'.format(name)
        for interest in mediator.interests:
            self.remove_observer(interest, mediator)
        del self.mediator_map[name]
        mediator.on_remove()

class Facade(Singleton):
    """singleton. instantiates the mvc and exposes their api's"""

    def __init__(self, *args):
        Singleton.__init__(self, *args)
        self.controller = get_controller()
        self.model = get_model()
        self.view = get_view()
        self.build_api()

    def build_api(self):
        self.register_command = self.controller.register_command
        self.register_proxy = self.model.register_proxy
        self.register_mediator = self.view.register_mediator
        self.remove_command = self.controller.remove_command
        self.remove_proxy = self.model.remove_proxy
        self.remove_mediator = self.view.remove_mediator
        self.get_proxy = self.model.get_proxy
        self.get_mediator = self.view.get_mediator

    def send_note(self, name, body=None):
        self.view.notify_observers({ 'name': name, 'body': body })

def command(facade, note):
    """use this signature for a controller"""
    pass

def register_command(name):
    """decorator to register a command with the controller"""

    def register(cmd):
        get_facade().register_command(name, cmd)
        return cmd

    return register

class Proxy(object):
    """extend me for a model object"""

    name = ''

    def __init__(self):
        self.facade = get_facade()

    def on_register(self): pass

    def on_remove(self): pass

class Mediator(Proxy):
    """extend me for a view object """

    interests = [] # must be defined in subclass, not dynamically inserted

    def handle_note(self, note): pass # called whenever a note is sent who's name is listed in self.interests

singletons = { }

def singleton_factory(name, cls, *args, **kwargs):
    if not name in singletons:
        args += ('there_can_be_only_one',)
        singletons[name] = cls(*args, **kwargs)
    return singletons[name]

get_controller = partial(singleton_factory, 'controller', Controller)
get_model = partial(singleton_factory, 'model', Model)
get_view = partial(singleton_factory, 'view', View)
get_facade = partial(singleton_factory, 'facade', Facade)


