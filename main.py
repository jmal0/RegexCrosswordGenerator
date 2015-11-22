from RegexCrossword import RegexCrossword

if __name__ == '__main__':
    xSize = 2
    ySize = 2
    columnRules = ["[^SPEAK]+", "EP|IP|EF"]
    rowRules = ["HE|LL|O+", "[PLEASE]+"]
    puzzle = RegexCrossword(xSize, ySize, columnRules, rowRules)
    print puzzle