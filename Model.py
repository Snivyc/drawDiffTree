class ASTNode(object):
    def __init__(self, temp, children):
        self.type = int(temp["type"])
        self.label = temp.get("label")
        self.typeLabel = temp["typeLabel"]
        self.pos = int(temp["pos"])
        self.length = int(temp["length"])
        self.children = children
        self.beforeID = temp["id"]
        self.afterID = None
        self.parent = None
        self.operation = None
