class AppErrorBaseClass(Exception):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass


class BadRequest(AppErrorBaseClass):
    pass

