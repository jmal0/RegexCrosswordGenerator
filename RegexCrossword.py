
class RegexCrossword:
    def __init__(self, xSize, ySize, columnRules, rowRules):
        self.xSize = xSize
        self.ySize = ySize
        self.grid = [[" " for i in xrange(xSize)] for i in xrange(ySize)]
        
        if(xSize != len(columnRules)):
            raise ValueError("Length of columnRules must equal xSize")
        if(ySize != len(rowRules)):
            raise ValueError("Length of rowRules must equal ySize")

        self.cRules = columnRules
        self.rRules = rowRules
        
    def __str__(self):
        puzzle = ""
        puzzle += "%-10s" % ""
        for r in xrange(self.xSize):
            puzzle += "%-10s" % self.cRules[r]
        puzzle += "\n"

        for r in xrange(self.xSize):
            puzzle += "%-10s" % self.rRules[r]
            for c in xrange(self.ySize):
                puzzle += "%-10s" % self.grid[r][c]
            puzzle += "\n"
        return puzzle