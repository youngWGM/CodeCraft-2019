#!/usr/bin/env python
#-*-coding:utf-8-*-

# 最小生成树的搜索代码改成了原来的遍历搜索
# djs算法的函数还保留着
# heap模块可以不用了

import heap
import datetime

inf = float('inf')

def main():
    start_time = datetime.datetime.now()
    car = read_data('F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-exam-1\\car.txt')
    cross = read_data('F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-exam-1\\cross.txt')
    road = read_data('F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-exam-1\\road.txt')
    answer_path = 'F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-exam-1\\answer.txt'
    Matrix, Nodes = GenerateMatrix(cross, road)

    # print(len(Matrix), len(Nodes))
    # print(Matrix, Nodes)
    # if Connectivity(Matrix) == 1:
    #     print('This Graph is Connectivity.')
    # else:
    #     print('This Graph isn\'t Connectivity')
    Mst, root = prim(Matrix, Nodes)
    # print(Mst, root)
    Mst = insert_roadlabel(Mst, road)
    # print(Mst)
    # print(Mst)
    # print(root)
    # Array = MiniTreeArray(Mst, cross)
    #print(Array)
    add_cross(Nodes)
    add_road(Mst)
    # vlist = init(Nodes)
    # print(str(g))

    all_path = []
    for each_list in car:
        a = find_shortest_path(g, each_list[1], each_list[2])
        # print(a)
        single_road = []
        for i in range(0, len(a) - 1):
            edge = g.getEdge(a[i], a[i + 1])
            Road = edge.getRoadlabel()
            single_road.append(Road)
        single_road.insert(0, each_list[0])
        if each_list[3] == 16:
            single_road.insert(1, each_list[4])
        elif each_list[3] == 14:
            single_road.insert(1, each_list[4] + 80)
        elif each_list[3] == 12:
            single_road.insert(1, each_list[4] + 175)
        elif each_list[3] == 10:
            single_road.insert(1, each_list[4] + 300)
        elif each_list[3] == 8:
            single_road.insert(1, each_list[4] + 450)
        elif each_list[3] == 6:
            single_road.insert(1, each_list[4] + 600)
        else:
            single_road.insert(1, each_list[4]*2 + 900)
        all_path.append(single_road)
    # print(all_path)


    # dijkstra算法测试模块
    # all_shortestpath = []  # 这个是由路口编号构成的路径
    # all_path = []
    # for each_list in car:
    #     shortestPath, Len = get_shortest_path(each_list[1], each_list[2], vlist)
    #     shortestPath = shortestPath[::-1]
    #     single_road = []
    #     for i in range(0, len(shortestPath) - 1):
    #         edge = g.getEdge(shortestPath[i], shortestPath[i + 1])
    #         Road = edge.getRoadlabel()
    #         single_road.append(Road)
    #     single_road.insert(0, each_list[0])
    #     if each_list[3] == 8:
    #         single_road.insert(1, each_list[4])
    #     elif each_list[3] == 6:
    #         single_road.insert(1, each_list[4] + 10)
    #     elif each_list[3] == 4:
    #         single_road.insert(1, each_list[4] + 30)
    #     else:
    #         single_road.insert(1, each_list[4] + 50)
    #     all_path.append(single_road)


    write_txt(all_path, answer_path)  # 生成txt文件
    end_time = datetime.datetime.now()
    print("Runtime:", (end_time - start_time))

class AbstractCollection(object):
    """An abstract collection implementation."""

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._size = 0
        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    # Accessor methods
    def isEmpty(self):
        """Returns True if len(self) == 0, or False otherwise."""
        return len(self) == 0

    def __len__(self):
        """Returns the number of items in self."""
        return self._size

    def __str__(self):
        """Returns the string representation of self."""
        return "[" + ", ".join(map(str, self)) + "]"

    def __add__(self, other):
        """Returns a new bag containing the contents
        of self and other."""
        result = type(self)(self)
        for item in other:
            result.add(item)
        return result

    def __eq__(self, other):
        """Returns True if self equals other,
        or False otherwise."""
        if self is other: return True
        if type(self) != type(other) or \
                len(self) != len(other):
            return False
        otherIter = iter(other)
        for item in self:
            if item != next(otherIter):
                return False
        return True


class LinkedEdge(object):

    # An edge has a source vertex, a destination vertex,
    # a weight, and a mark attribute.

    def __init__(self, fromVertex, toVertex, weight=None):
        self._vertex1 = fromVertex
        self._vertex2 = toVertex
        self._weight = weight
        self._mark = False

    def clearMark(self):
        """Clears the mark on the edge."""
        self._mark = False

    def __eq__(self, other):
        """Two edges are equal if they connect
        the same vertices."""
        # 判断两个路径是否相同
        if self is other: return True
        if type(self) != type(other):
            return False
        return self._vertex1 == other._vertex1 and \
               self._vertex2 == other._vertex2

    def getOtherVertex(self, thisVertex):
        """Returns the vertex opposite thisVertex."""
        # 给出一个顶点，返回对应的另一个顶点
        if thisVertex == None or thisVertex == self._vertex2:
            return self._vertex1
        else:
            return self._vertex2

    def getToVertex(self):
        """Returns the edge's destination vertex."""
        return self._vertex2

    def getRoadlabel(self):
        """返回道路标号"""
        return self._weight[0]

    def getRoadlength(self):
        """返回道路长度"""
        return self._weight[1]

    # def getRoadspeed(self):
    #     """返回道路限速"""
    #     return self._weight[2]
    #
    # def getRoadchannel(self):
    #     """返回车道数"""
    #     return self._weight[3]

    def isMarked(self):
        """Returns True if the edge is marked
        or False otherwise."""
        return self._mark

    def setMark(self):
        """Sets the mark on the edge."""
        self._mark = True

    def setWeight(self, weight):
        """Sets the weight on the edge to weight."""
        self._weight = weight

    def __str__(self):
        """Returns the string representation of the edge."""
        return str(self._vertex1) + ">" + \
               str(self._vertex2) + ":" + \
               str(self._weight)


class LinkedVertex(object):

    # A vertex has a label, a list of incident edges,
    # and a mark attribute.

    def __init__(self, label):
        self._label = label
        self._edgeList = list()
        self._mark = False

    def getLabel(self):
        """Returns the label of the vertex."""
        # 返回顶点对应的标签
        return self._label

    def isMarked(self):
        """Returns True if the vertex is marked
        or False otherwise."""
        return self._mark

    def setLabel(self, label, g):
        """Sets the vertex's label to label."""
        g._vertices.pop(self._label, None)
        g._vertices[label] = self
        self._label = label

    def setMark(self):
        """Sets the mark on the vertex."""
        self._mark = True

    def __str__(self):
        """Returns the string representation of the vertex."""
        return str(self._label)

    def __eq__(self, other):
        """Two vertices are equal if they have
        the same labels."""
        if self is other: return True
        if type(self) != type(other): return False
        return self.getLabel() == other.getLabel()

    # Methods used by LinkedGraph
    # 连接图的使用方法

    def addEdgeTo(self, toVertex, weight):
        """Connects the vertices with an edge."""
        edge = LinkedEdge(self, toVertex, weight)
        self._edgeList.append(edge)

    def getEdgeTo(self, toVertex):
        """Returns the connecting edge if it exists, or
        None otherwise."""
        edge = LinkedEdge(self, toVertex)
        try:
            return self._edgeList[self._edgeList.index(edge)]
        except:
            return None

    def incidentEdges(self):
        """Returns the incident edges of this vertex."""
        return iter(self._edgeList)

    def neighboringVertices(self):
        """Returns the neighboring vertices of this vertex."""
        # 返回邻居节点
        vertices = list()
        for edge in self._edgeList:
            vertices.append(edge.getOtherVertex(self))
        return iter(vertices)

    def removeEdgeTo(self, toVertex):
        """Returns True if the edge exists and is removed,
        or False otherwise."""
        edge = LinkedEdge(self, toVertex)
        if edge in self._edgeList:
            self._edgeList.remove(edge)
            return True
        else:
            return False


class LinkedDirectedGraph(AbstractCollection):

    # A graph has a count of vertices, a count of edges,
    # and a dictionary of label/vertex pairs.

    def __init__(self, sourceCollection=None):
        self._edgeCount = 0
        self._vertices = {}
        AbstractCollection.__init__(self, sourceCollection)

    # Methods for clearing, marks, sizes, string rep

    def sizeEdges(self):
        """Returns the number of edges."""
        return self._edgeCount

    def sizeVertices(self):
        """Returns the number of vertices."""
        return len(self)

    # def __str__(self):
    #     """Returns the string representation of the graph."""
    #     result = str(self.sizeVertices()) + " Vertices: "
    #     for vertex in self._vertices:
    #         result += " " + str(vertex)
    #     result += "\n";
    #     result += str(self.sizeEdges()) + " Edges: "
    #     for edge in self.edges():
    #         result += " " + str(edge)
    #     return result

    def add(self, label):
        """For compatibility with other collections."""
        self.addVertex(label)

    # Vertex related methods

    def addVertex(self, label):
        """Adds a vertex with the given label to the graph."""
        if self.containsVertex(label):
            raise Exception("The vertex is existing")
        self._vertices[label] = LinkedVertex(label)
        self._size += 1

    def containsVertex(self, label):
        return label in self._vertices

    def getVertex(self, label):
        return self._vertices[label]

    # Methods related to edges

    def addEdge(self, fromLabel, toLabel, weight):
        """Connects the vertices with an edge with the given weight."""
        if self.containsEdge(fromLabel, toLabel):
            raise Exception("The edge is existing")
        fromVertex = self.getVertex(fromLabel)
        toVertex = self.getVertex(toLabel)
        fromVertex.addEdgeTo(toVertex, weight)
        self._edgeCount += 1

    def containsEdge(self, fromLabel, toLabel):
        """Returns True if an edge connects the vertices,
        or False otherwise."""
        return self.getEdge(fromLabel, toLabel) != None

    def getEdge(self, fromLabel, toLabel):
        """Returns the edge connecting the two vertices, or None if
        no edge exists."""
        fromVertex = self.getVertex(fromLabel)
        toVertex = self.getVertex(toLabel)
        return fromVertex.getEdgeTo(toVertex)

    # Iterators

    def __iter__(self):
        """Supports iteration over a view of self (the vertices)."""
        return self.vertices()

    def edges(self):
        """Supports iteration over the edges in the graph."""
        result = list()
        for vertex in self.vertices():
            result += list(vertex.incidentEdges())
        return iter(result)

    def vertices(self):
        """Supports iteration over the vertices in the graph."""
        return iter(self._vertices.values())

    def incidentEdges(self, label):
        """Supports iteration over the incident edges of the
        given verrtex."""
        return self.getVertex(label).incidentEdges()

    def neighboringVertices(self, label):
        """Supports iteration over the neighboring vertices of the
        given verrtex."""
        return self.getVertex(label).neighboringVertices()


def read_data(path):
    data_list = []
    with open(path, "r") as f:
        for line in f.readlines():
            data_list.append(line.replace('(', '').replace(')', '').strip('\n').split(','))
        del(data_list[0])
        for each_list in data_list:
            for i in range(0, len(each_list)):
                each_list[i] = int(each_list[i])
    return data_list

def insert_roadlabel(Mst, road):
    for i in range(len(Mst)):
        Mst.append([Mst[i][1], Mst[i][0], Mst[i][2]])
    for each_list in Mst:
        for each_load in road:
            if each_list[0] == each_load[4] and each_list[1] == each_load[5]:
                each_list.append(each_load[0])
            elif each_list[0] == each_load[5] and each_list[1] == each_load[4]:
                each_list.append(each_load[0])
            else:
                continue
    return Mst


# Generate the Cross matrix
def GenerateMatrix(cross, road):
    Matrix = []
    for i in range(0, len(cross)):
        Matrix.append([])
        for j in range(0, len(cross)):
            Matrix[i].append(inf)
    for i in range(len(road)):
        if road[i][6] == 1:
            Matrix[suoyin(road[i][4], cross)][suoyin(road[i][5], cross)] = road[i][1] / (road[i][3]*5) + (8 - road[i][2] / 2)
            Matrix[suoyin(road[i][5], cross)][suoyin(road[i][4], cross)] = road[i][1] / (road[i][3]*5) + (8 - road[i][2] / 2)
    Nodes = []
    for i in range(0, len(cross)):
        Nodes.append(cross[i][0])
    return Matrix, Nodes

def suoyin(crossID, cross):
    for each_list in cross:
        if crossID in each_list:
            cross_suoyin = cross.index(each_list)
            return cross_suoyin


# This fucntion is used to judge array 2-dimision weather is Conectivity
# if the array is Conectivity Return 1 else return 0
# def Connectivity(Matrix):
#     for i in range(len(Matrix)):
#         temp = 0
#         for j in range(len(Matrix[i])):
#             if Matrix[i][j] == 0:
#                 temp = 0
#             else:
#                 temp = 1
#         if temp == 0:
#             break
#     return temp


# Using Prim Algorithm Compute Mining Spining Tree
def prim(primgraph, chararray):
    Mst = []
    charlist = []
    charlist.append(chararray[0])
    mid = []      # mid[i]表示生成树集合中与点i最近的点的编号
    lowcost = []      # lowcost[i]表示生成树集合中与点i最近的点构成的边最小权值 ，-1表示i已经在生成树集合中
    lowcost.append(-1)
    mid.append(0)
    n = len(chararray)
    for i in range(1, n):   # 初始化mid数组和lowcost数组
        lowcost.append(primgraph[0][i])
        mid.append(0)
    sum = 0
    for _ in range(1, n):   # 插入n-1个结点
        minid = 0
        min = inf
        for j in range(1, n):    # 寻找每次插入生成树的权值最小的结点
            if lowcost[j] != -1 and lowcost[j] < min:
                minid = j
                min = lowcost[j]
        charlist.append(chararray[minid])
        temp = ([chararray[mid[minid]], chararray[minid], lowcost[minid]])
        Mst.append(temp)
        # print(chararray[mid[minid]],'——',chararray[minid],'权值：',str(lowcost[minid]))
        sum += min
        lowcost[minid] = -1
        for j in range(1, n):    # 更新插入结点后lowcost数组和mid数组值
            if lowcost[j] != -1 and lowcost[j] > primgraph[minid][j]:
                lowcost[j] = primgraph[minid][j]
                mid[j] = minid
    # print("sum="+str(sum))
    # print("插入结点顺序："+str(charlist))
    root = Mst[0][0]
    return Mst, root


# Generating the Array of Mining Spining Tree.
def MiniTreeArray(Mst, cross):
    Matrix = []
    for i in range(len(cross)):
        Matrix.append([])
        for j in range(len(cross)):
            Matrix[i].append(0)
    for i in range(len(Mst)):
        Matrix[Mst[i][0] - 1][Mst[i][1] - 1] = Mst[i][2]
    return Matrix


def DeleteFE(Array):
    for i in range(0, len(Array) - 1):
        Array[i] = Array[i + 1]
    Array.pop()
    return Array

g = LinkedDirectedGraph()


# 加入所有顶点
def add_cross(root):
    for i in root:
        g.addVertex(i)


# 加入边和权重
def add_road(road):
    for each_list in road:
        g.addEdge(each_list[0], each_list[1], [each_list[3], each_list[2]])


# 初始化参数
def init(root):
    vlist = [False]
    for i in root:
        vlist.append(i)
    return vlist


# def get_shortest_path(start, end, vlist):
#     # distances使用字典的方式保存每一个顶点到start点的距离
#     distances = {}
#
#     # 从start到某点的最优路径的前一个结点
#     # eg:start->B->D->E,则previous[E]=D,previous[D]=B,等等
#     previous = {}
#
#     # 用来保存图中所有顶点的到start点的距离的优先队列
#     # 这个距离不一定是最短距离
#     nodes = []
#
#     for vertex in vlist:
#         if vertex == start:
#             distances[vertex] = 0   # 将start点的距离初始化为0
#             heap.heappush(nodes, [0, vertex])
#             # nodes.append([0,vertex])
#         elif vertex in g.neighboringVertices(start):
#             distances[vertex] = length(start, vertex)   # 把与star点相连的结点距离start点的距离初始化为对应的道路长度
#             heap.heappush(nodes, [length(start, vertex), vertex])
#             # nodes.append([length(start, vertex), vertex])
#             previous[vertex] = start
#         else:
#             distances[vertex] = inf    # 把与start点不直接连接的结点距离start的距离初始化为9999
#             heap.heappush(nodes, [inf, vertex])
#             # nodes.append([9999, vertex])
#             previous[vertex] = None
#     shortest_path = [1]
#     lenPath = 0
#     while nodes:
#         smallest = heap.heappop(nodes)[1]   # 取出队列中最小距离的结点
#         # smallest = nodes.pop()[1]
#         if smallest == end:
#             shortest_path = []
#             lenPath = distances[smallest]
#             temp = smallest
#             #print('previous[temp]:',temp)
#             while (temp != start):
#                 shortest_path.append(temp)
#                 temp = previous[temp]
#             shortest_path.append(temp)  # 将start点也加入到shortest_path中
#         if distances[smallest] == inf:
#             # 所有点不可达
#             break
#         # 遍历与smallest相连的结点，更新其与结点的距离、前继节点
#         for neighbor in g.neighboringVertices(smallest):
#             dis = distances[smallest] + length(smallest, neighbor.getLabel())
#             if dis < distances[neighbor.getLabel()]:
#                 distances[neighbor.getLabel()] = dis
#                 previous[neighbor.getLabel()] = smallest    # 更新与smallest相连的结点的前继节点
#                 for node in nodes:
#                     if node[1] == neighbor.getLabel():
#                         node[0] = dis   # 更新与smallest相连的结点到start的距离
#                         break
#                 heap.heapify(nodes)
#     return shortest_path, lenPath


def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if graph.getVertex(start) not in graph.vertices():
        return None
    shortest = None
    for node in graph.neighboringVertices(start):
        node = node.getLabel()
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or length(newpath) < length(shortest):
                    shortest = newpath
        else:
            continue
    return shortest


# 计算a路口到b路口路径的长度
def length(a, b):
    edge = g.getEdge(a, b)
    length = edge.getRoadlength()
    return length

def write_txt(input_list, answer_path):
    file = open(answer_path, 'w')
    for i in range(len(input_list)):
        s = str(input_list[i]).replace('[', '(').replace(']', ')') + '\n'
        file.write(s)
    file.close()


if __name__ == "__main__":
    main()






