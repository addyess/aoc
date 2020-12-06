import itertools


class GroupParsed:
    @classmethod
    def parsed(cls, ins):
        """
        Parses lines of text into groups separated by empty lines

        :param Iterable[str] ins: iterable of strings
        :return: generator of objects
        """
        stream = iter(ins)
        group = True
        while group:
            group = list(itertools.takewhile(lambda _: _, stream))
            if group:
                yield cls(group)

