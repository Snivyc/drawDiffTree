import re


class DiffOperate():
    def __init__(self, diffscript):
        self.updateList = []
        self.matchList = []
        self.insertList = []
        self.moveList = []
        self.deleteList = []

        # with open(file, 'r') as f:
        for line in diffscript.split("\n"):
            if line.startswith("Match"):
                # print(line)
                matchObj = re.findall(r'(?<=\()\d+(?=\))', line)
                # print(matchObj)
                matchTuple = (int(matchObj[0]), int(matchObj[1]))
                self.matchList.append(matchTuple)
            elif line.startswith("Insert"):
                matchObj = re.findall(r'(?<=\()\d+(?=\))', line)
                t = int(re.findall(r'\d+', line)[-1])
                insertTuple = (int(matchObj[0]), int(matchObj[1]),t)
                self.insertList.append(insertTuple)
            elif line.startswith("Move"):
                matchObj = re.findall(r'(?<=\()\d+(?=\))', line)
                t = int(re.findall(r'\d+', line)[-1])
                MoveTuple = (int(matchObj[0]), int(matchObj[1]),t)
                self.moveList.append(MoveTuple)
            elif line.startswith("Delete"):
                matchObj = re.findall(r'(?<=\()\d+(?=\))', line)
                self.deleteList.append(int(matchObj[0]))
            elif line.startswith("Update"):
                matchObj = re.findall(r'(?<=\()\d+(?=\))', line)
                self.updateList.append(int(matchObj[0]))
                # print("update", matchObj[0])

        # print(self.matchList)
        # print(self.insertList)
        # print(self.moveList)
        # print(self.deleteList)

    def getMatchedAfterID(self, beforeID):
        for i in self.matchList:
            if i[0] == beforeID:
                return i[1]
        else:
            return -1

    def getMatchedBeforeID(self, afterID):
        for i in self.matchList:
            if i[1] == afterID:
                return i[0]
        else:
            return -1

    def getInsertedIDs(self):
        '''
        返回After树被插入子节点的节点的ID
        '''
        tempList = []
        for i in self.insertList:
            tempList.append(i[1])
        return tempList

    def getJoinedIDs(self):
        '''
        返回加入After树的节点的ID
        '''
        tempList = []
        for i in self.insertList:
            tempList.append(i[0])
        return tempList


    def getMovedAfterIDs(self):
        '''
        返回被移动之后的节点在After树中的ID
        '''
        tempList = []
        for i in self.moveList:
            tempList.append(i[1])
        return tempList

    def getMovedBeforeIDs(self):
        '''
        返回被移动之前的节点在Before树中的ID
        '''
        tempList = []
        for i in self.moveList:
            tempList.append(i[0])
        return tempList

    def getDeleteBeforeIDs(self):
        '''
        返回被删除的节点在After树中的ID
        '''
        return self.deleteList

    def getUpdateBeforeIDs(self):
        return self.updateList

    def isJoinNode(self, id):
        '''
        判断是否是新加入的节点
        '''
        return (id in self.getJoinedIDs())

    def isDeleteNode(self, id):
        '''
        new 判断是否是将删除的节点
        '''
        return (id in self.getDeleteBeforeIDs())

    def isMoveBeforeNode(self, id):
        '''
        new 判断是否是将被移动的节点
        '''
        return (id in self.getMovedBeforeIDs())

    def getMoveInfo(self,id):
        '''
        根据移动前的id获取移动信息
        :param id:
        :return:
        '''
        for i in self.moveList:
            if id == i[0]:
                return i
        else:
            raise RuntimeError("fuck")


if __name__ == "__main__":
    d = DiffOperate("diffscript.txt")
