class _DefaultList(list):
    def __init__(self, fx, *args):
        super().__init__(*args)
        self._fx = fx

    def _extend(self, index):
        if isinstance(index, slice):
            tot = len(self)
            start = 0 if index.start is None else index.start
            stop = tot if index.stop is None else index.stop
            step = 1 if index.step is None else index.step
            return [self[i] for i in range(start, min(stop, tot), step)]
        while len(self) <= index:
            self.append(self._fx())

    def __getitem__(self, index):
        self._extend(index)
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        self._extend(index)
        super().__setitem__(index, value)


defaultlist = _DefaultList
