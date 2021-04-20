import pynvim
from libvoikko import Voikko
import re
import sys


@pynvim.plugin
class Oiko(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.highlightSource = self.nvim.new_highlight_source()
        sff = SyntaxFilterFactory()
        self.syntaxFilter = sff.getSyntaxFilter("tex")
        self.on = False

    @pynvim.autocmd(
        'BufEnter',
        pattern='*',
        eval='expand("<afile>")',
        sync=True
    )
    def setFileType(self, filename):
        try:
            sff = SyntaxFilterFactory()
            extension = filename.split('.')[1]
            self.syntaxFilter = sff.getSyntaxFilter(extension)
            self.nvim.out_write(extension + '\n')
        except Exception:
            pass

    @pynvim.command('OikoOn')
    def oikoOn(self):
        self.on = True
        self.spell()

    @pynvim.command('OikoOff')
    def oikoOff(self):
        self.on = False
        self.spellClear()

    @pynvim.autocmd('InsertLeave')
    def autoOiko(self):
        if self.on:
            self.spell()

    @pynvim.command('OikoCheck')
    def spell(self):
        self.spellClear()
        vimbuffer = self.nvim.current.buffer
        src = self.highlightSource
        lines = self.getLines()
        misspellings = Oiko.analyzeWords(self.readWords(lines))
        highlights = Oiko.createHighLights(misspellings)
        vimbuffer.update_highlights(src, highlights)

    @pynvim.command('OikoClear')
    def spellClear(self):
        buf = self.nvim.current.buffer
        buf.clear_highlight(self.highlightSource)

    def createHighLights(misspellings):
        return list(map(
            lambda misspelling: ("OikoError",
                                 misspelling["linenumber"],
                                 misspelling['columnstart'],
                                 misspelling['columnend']),
            misspellings))

    def analyzeWords(words):
        v = Voikko(u"fi")
        v.setIgnoreDot(True)
        v.setIgnoreNonwords(True)
        errors = []
        for word in words:
            if not v.spell(word["value"]):
                word["suggestions"] = v.suggest(word["value"])
                errors.append(word)
        v.terminate()
        return errors

    def getLines(self):
        buf = self.nvim.current.buffer
        lines = []
        for line in buf:
            lines.append(line)
        return lines

    def handleSpecialCharacters(self, line):
        words = []
        lineWithNoSyntax = self.syntaxFilter.filterLine(line)
        lineWithNoPunct = Oiko.removePunctuationFrom(lineWithNoSyntax)
        for word in lineWithNoPunct.split():
            words.append(word)
        return words

    def readWords(self, lines):
        words = []
        linenumber = 0
        for line in lines:
            for word in self.handleSpecialCharacters(line):
                columnStart = Oiko.bytewiseLen(line[:line.index(word)])
                columnEnd = columnStart + Oiko.bytewiseLen(word)
                data = {'value': word, 'linenumber': linenumber,
                        'columnstart': columnStart, 'columnend': columnEnd}
                words.append(data)
            linenumber = linenumber + 1

        return words

    def bytewiseLen(string):
        sysencoding = sys.getdefaultencoding()
        return len(string.encode(sysencoding))

    def removePunctuationFrom(line):
        return re.sub('[.,:]', ' ', line)


class SyntaxFilterFactory(object):

    def __init__(self):
        self.valueTable = {'tex': LatexFilter()}

    def getSyntaxFilter(self, syntaxName):
        try:
            return self.valueTable[syntaxName]
        except KeyError:
            return SyntaxFilter()


class SyntaxFilter(object):

    def __init__(self):
        self.filters = []

    def applyFilters(self, line):
        filteredLine = line
        for f in self.filters:
            filteredLine = f(filteredLine)
        return filteredLine

    def filterLine(self, line):
        return self.applyFilters(line)


class LatexFilter(SyntaxFilter):
    def __init__(self):
        super().__init__()
        self.filters = [
            LatexFilter.commentFilter,
            LatexFilter.commandFilter,
            LatexFilter.replaceNonBreakingSpace
        ]

    def commentFilter(line):
        if "%" in line:
            return line.split("%", 2)[0]
        else:
            return line

    def replaceNonBreakingSpace(line):
        return line.replace('~', ' ')

    def commandFilter(line):
        return re.sub('\\\\[\w[]*]*\*?(\{[\w -_:]*\})*', ' ', line)
