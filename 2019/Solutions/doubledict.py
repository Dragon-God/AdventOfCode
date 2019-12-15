from collections import defaultdict


class DoubleDict(defaultdict):
    def __init__(self, *args, func=None, **kwargs):
        super().__init__(func, *args, **kwargs)
        self.values_dict = defaultdict(lambda: [])
        for key, value in self.items():
            self.values_dict[value] += [key]

    def __setitem__(self, key, value):
        var = self.get(key)
        if var in self.values_dict:
            self.values_dict[var].remove(key)
            if not self.values_dict[var]:
                del self.values_dict[var]
        super().__setitem__(key, value)
        self.values_dict[value] += [key]

    def index(self, value):
        return self.values_dict[value][-1]

    def indices(self, value):
        return self.values_dict[value]

    def __delitem__(self, key):
        var = self.get(key)
        self.values_dict[var].remove(key)
        if not self.values_dict[var]:
            del self.values_dict[var]
        super().__delitem__(key)


if __name__ == "__main__":
    dct = DoubleDict(((i, (i//2)**2) for i in range(10)))
    print(dct)
    print(dct.indices(9))
    del dct[7]
    print(dct)
    print(dct.values_dict)
    dct[2] = 200
    print(dct)
    print(dct.values_dict)
