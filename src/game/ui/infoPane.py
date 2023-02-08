import label


class infoPane:

    def __init__(self):
        self.fields = {}

    def addField(self, reference, newLabel):
        assert not reference in self.fields
        self.fields[reference] = newLabel



    def drawAllField(self):
        for f in self.fields:
            f.draw()
