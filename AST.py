import json
from Model import ASTNode
from diffOperate import DiffOperate

class AST(object):
    def constructTreeByJSON(self, subASTTree):
        '''
        通过JSON构建树型结构的AST
        递归
        '''
        children = []
        if subASTTree["children"] != []:
            for i in subASTTree["children"]:
                children.append(self.constructTreeByJSON(i))
        subASTTree["id"] = self.id
        self.id = self.id + 1
        # print(subASTTree)
        ASTNodeObj = ASTNode(subASTTree, children)
        self.ASTNodeList.append(ASTNodeObj)
        return ASTNodeObj

    def addNodeParent(self,subTree,parent):
        '''
        递归的给所有节点添加父节点的引用
        '''
        subTree.parent = parent
        for i in subTree.children:
            self.addNodeParent(i, subTree)


    def __init__(self,ASTJSON):
        # with open(code, 'r') as f:
        #     self.CODE = f.read()
        self.ASTNodeList = []


        AST = json.loads(ASTJSON)
        self.id = 0
        # print(AST["root"])
        self.constructTreeByJSON(AST["root"])
        self.addNodeParent(self.ASTNodeList[-1], None)
        # print(self.ASTNodeList[9].id)


    def astToJson(self, i=-1):
        '''
        将AST转换回json格式
        '''
        def astToDict(node):
            tempDict = {"type":str(node.type), "typeLabel":node.typeLabel, "pos":str(node.pos), "length": str(node.length)}
            if node.label != None:
                tempDict["label"]=node.label
            childrenList = []
            # print(node.children)
            for j in node.children:
                # print("fuck")
                childrenList.append(astToDict(j))
            tempDict["children"] = childrenList
            return tempDict


        return json.dumps(astToDict(self.ASTNodeList[i]))

    def getNodeByID(self, nodeID) -> ASTNode:
        return self.ASTNodeList[nodeID]

    def getHeadNode(self):
        return self.ASTNodeList[-1]

    def insertNode(self, parentID, index, node):
        parentNode = self.getNodeByID(parentID)
        parentNode.children.insert(index, node)
        node.parent = parentNode


if __name__ == "__main__":
    astBefore = AST("ASTbefore.json")
    astAfter = AST("ASTafter.json")
    diff = DiffOperate("diffscript.txt")
    changedNodeID = set() #子节点变化的Node的ID，before树中
    changedNodeID = changedNodeID | set(diff.getDeleteBeforeIDs())
    tempSet = set()
    for i in diff.getInsertedIDs():
        if diff.getMatchedBeforeID(i) != -1:
            tempSet.add(diff.getMatchedBeforeID(i))
    changedNodeID = changedNodeID | tempSet
    changedNodeID = changedNodeID | {astBefore.ASTNodeList[i].parent.id for i in diff.getMovedBeforeIDs()}
    tempSet = set()
    for i in diff.getMovedAfterIDs():
        if diff.getMatchedBeforeID(i) != -1:
            tempSet.add(diff.getMatchedBeforeID(i))
    changedNodeID = changedNodeID | tempSet
    changedNodeID = list(changedNodeID)
    def getCommonParent(changedNodeID):
        while (len(changedNodeID) > 0):
            a = astBefore.ASTNodeList[changedNodeID.pop()]
            b = astBefore.ASTNodeList[changedNodeID.pop()]
            c = a
            print(changedNodeID)
            while(b != None):
                a = c
                while(a != None):
                    print(a.id, b.id)
                    if a is b:
                        changedNodeID.append(a.id)
                        return getCommonParent(changedNodeID)
                    b = b.parent
                a = a.parent
                print(a)
        else:
            return changedNodeID
    commonParentID = getCommonParent(changedNodeID)
    print(commonParentID)
    print(astBefore.astToJson(commonParentID))