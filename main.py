from AST import AST
from diffOperate import DiffOperate
from Model import ASTNode
from copy import deepcopy,copy
import sys
sys.setrecursionlimit(1000000) #例如这里设置为一百万
dotID = 0


def main(before_json,after_json,diff_script):

    astBefore = AST(before_json)
    astAfter = AST(after_json)
    diff = DiffOperate(diff_script)

    afterASTNode = [None for i in range(len(astAfter.ASTNodeList))] # type: list[ASTNode]
    typeDeclarationLst = []
    movedNode = []
    def markMoveBefore(i:ASTNode):
        '''
        在beforetree中标记是否修改
        :param i:
        :return:
        '''
        i.operation = "Move Before"
        if i.children != []:
            for k in i.children:
                # print("fuck")
                markMoveBefore(k)

    def isNoChange(i:ASTNode):
        '''
        判断子树是否发生改变
        :param i:
        :return:
        '''
        if i.operation != None:
            return False
        else:
            for k in i.children:
                if not isNoChange(k):
                    return False
            else:
                return True


    # 标记删除和移动节点
    for i in astBefore.ASTNodeList[::-1]:
        if i.typeLabel == "TypeDeclaration":
            typeDeclarationLst.append(i)


        afterID = diff.getMatchedAfterID(i.beforeID)
        if afterID != -1:
            i.afterID = afterID
            afterASTNode[afterID] = i
        if diff.isMoveBeforeNode(i.beforeID):
            # i.operation = "Move Before"
            markMoveBefore(i)
            info = diff.getMoveInfo(i.beforeID)
            movedNode.append((i,info))
        elif diff.isDeleteNode(i.beforeID):
            i.operation = "Delete"


    # for i in afterASTNode:
    #     if i != None:
    #         print(i.afterID, end=", ")
    #     else:
    #         print("None", end=", ")


    tempLst = [("i", i[0], i[1], i[2]) for i in diff.insertList]
    k = 0
    for i in tempLst:
        k += 1
        id = i[1]
    #     print(id)
        node = astAfter.getNodeByID(id)
        node.afterID = node.beforeID
        node.beforeID = None
        # if (i[0] == "i"):
        node.operation = "Insert"
        node.children = []

        afterASTNode[i[2]].children.insert(i[3], node)
        afterASTNode[i[1]] = node
    print(k)


    def ASTcopy(node):
        '''
        deepcopy一个子树（parent没考虑）
        :param i:
        :return:
        '''
        node.parent = None
        for f in node.children:
            ASTcopy(f)

    for node,info in movedNode:
        node2 = node
        ASTcopy(node)
        node = deepcopy(node)
        def markMoveAftere(node):
            if node.operation == "Move Before":
                node.operation = "Move After"
            nC = []
            for s in node.children:
                if not s.operation == "Delete":
                    nC.append(s)
            node.children = nC
            for s in node.children:
                markMoveAftere(s)
        # print(afterASTNode[info[1]].children)
        markMoveAftere(node)
        afterASTNode[info[1]].children.insert(info[2],node)

        def deleteInsert(node):
            nC = []
            for s in node.children:
                if not s.operation == "Insert":
                    nC.append(s)
            node.children = nC
            for s in node.children:
                deleteInsert(s)
        deleteInsert(node2)
    # tempLst2 = [("M", astAfter.getNodeByID(i[1]).children[i[2]].beforeID, i[1], i[2]) for i in diff.moveList]
    # addLst = tempLst + tempLst2
    # addLst.sort(key=lambda a:a[2], reverse=True)
    # print(addLst)
    # for i in tempLst:
    #     id = i[1]
    # #     print(id)
    #     node = astAfter.getNodeByID(id)
    #     node.afterID = node.beforeID
    #     node.beforeID = None
    #     if (i[0] == "i"):
    #         node.operation = "Insert"
    #         node.children = []
    #
    #     elif (i[0] == "M"):
    #         node.operation = "Move After"
    #     else:
    #         raise RuntimeError("?")
    #     print(i[2])
    #     print(afterASTNode[i[2]].children)
    #     afterASTNode[i[2]].children.insert(i[3], node)
    #     afterASTNode[i[1]] = node
    #
    #
    # for i in
    #
    #     astBefore.insertNode(i[1], i[2], node)
    #
    #
    # tempLst = diff.moveList
    # for i in tempLst:
    #     node = astAfter.getNodeByID(i[1]).children[i[2]]
    #     node.afterID = node.beforeID
    #     node.beforeID = None
    #     node.operation = "Move After"
    #     node.children = []
    #
    #     astBefore.insertNode(i[1], i[2], node)
    #
    #

    # 剪枝未修改的节点
    # for i in typeDeclarationLst:
    #     newChildren = []
    #     for j in i.children:
    #         if isNoChange(j):
    #             pass
    #         else:
    #             newChildren.append(j)
    #     i.children = newChildren


    def drawFullDiffAST(ast):
        from graphviz import Digraph
        dot = Digraph(comment='The Round Table')

        def drawNode(node: ASTNode, parent):
            # node = ast.getNodeByID(ID)
            nodeText = None
            if node.label == None:
                nodeText = node.typeLabel
            else:
                nodeText = node.typeLabel + " : " + node.label
            # nodeText += " " + str(node.id)
            global dotID
            dotID += 1
            myID = dotID
            # dot.attr('node', color='lightgrey')
            if node.operation == "Delete":
                nodeText += " bID: " + str(node.beforeID)
                dot.attr('node', color='lightgrey')
            elif node.operation == "Move Before":
                nodeText += " bID: " + str(node.beforeID)
                nodeText += " aID: " + str(node.afterID)
                dot.attr('node', color='yellow')
            elif node.operation == "Insert":
                nodeText += " aID: " + str(node.afterID)
                dot.attr('node', color='blue')
            elif node.operation == "Move After":
                nodeText += " bID: " + str(node.beforeID)
                nodeText += " aID: " + str(node.afterID)
                dot.attr('node', color='red')
            else:
                nodeText += " bID: " + str(node.beforeID)
                nodeText += " aID: " + str(node.afterID)
                dot.attr("node", color='black')

            dot.node(str(myID), nodeText)
            if parent != -1:
                dot.edge(str(parent), str(myID))
            for i in node.children:
                drawNode(i, myID)

        drawNode(ast.getHeadNode(),-1)
        # print(dot)
        dot.render('test-output/round-table2.gv', view=True)


    drawFullDiffAST(astBefore)