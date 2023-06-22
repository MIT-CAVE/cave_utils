import sys


class Arguments:
    def __init__(self):
        self.kwargs = {}
        self.flags = []
        self.other = []
        skip_next = True  # Skip the first argument, which is the file name
        for idx, i in enumerate(sys.argv):
            if skip_next:
                skip_next = False
                continue
            if i.lower().startswith("--"):
                self.kwargs[i[2:]] = sys.argv[idx + 1]
                skip_next = True
            elif i.lower().startswith("-"):
                self.flags.append(i[1:])
            else:
                self.other.append(i)

    def get_kwarg(self, key, default=None):
        return self.kwargs.get(key, default)

    def has_kwarg(self, key):
        return key in self.kwargs

    def has_flag(self, key):
        return key in self.flags
