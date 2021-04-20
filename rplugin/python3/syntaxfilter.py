from functools import reduce
import re


class SyntaxFilterFactory(object):

    def __init__(self):
        self.valueTable = {'latex': LatexFilter}

    def getSyntaxFilter(self, syntaxName):
        syntaxFilter = self.valueTable.get(syntaxName)
        return syntaxFilter()


class SyntaxFilter(object):

    def __init__(self):
        self.filters = []

    def filterReduce(f, line):
        return f(line)

    def filterLine(self, line):
        reduce(self.filterReduce(self.filters, line))

    def filterLines(self, lines):
        return list(
            map(
                lambda line: (reduce(self.filterReduce(self.filters, line))),
                lines
            )
        )


def LatexFilter(SyntaxFilter):
    def __init__(self):
        super.__init__(self)
        self.filters = [LatexFilter.commentFilter, LatexFilter.commandFilter]

    def commentFilter(line):
        if "%" in line:
            return line.split("%", 2)[0]
        else:
            return line

    def commandFilter(line):
        line = re.sub('\\\\[\w[]*]*\*?(\{[\w -_:]*\})*', ' ', line)
        return line
