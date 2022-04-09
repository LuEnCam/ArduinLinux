
class Event():
    def __init__(self):
        self.__eventhandlerjoystick = []
    def __iadd__(self, Ehandler):
        self.__eventhandlerjoystick.append(Ehandler)
        return self
    def __isub__(self, Ehandler):
        self.__eventhandlerjoystick.remove(Ehandler)
        return self

    def __call__(self, *args, **kwargs):
        for evenhandler in self.__eventhandlerjoystick:
            evenhandler(*args, **kwargs)

ledEvent = Event()
joystickEvent = Event()

# def ledcalled(checked):
#     print("led called with", checked)
# ledEvent += ledcalled