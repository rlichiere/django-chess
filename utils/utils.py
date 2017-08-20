
def access(container, path, value=None):
    paths = path.split('/')
    key = paths[0]
    paths.pop(0)
    if len(paths) == 0:
        # leaf
        if value:
            container[key] = value
            return True
        else:
            if key in container:
                return container[key]
            else:
                return False
    else:
        # path
        path = ''.join('%s/' % p for p in paths)
        path = path[:len(path) - 1]
        if value:
            # set
            if type(container) is not dict:
                container = dict()
            if key in container:
                if type(container[key]) is not dict:
                    container[key] = dict()
            else:
                container[key] = dict()
            return access(container[key], path, value)
        else:
            # get
            if type(container) is not dict:
                return False
            else:
                if key not in container:
                    return False
                else:
                    return access(container[key], path, value)
