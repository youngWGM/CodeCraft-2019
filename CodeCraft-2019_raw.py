#!/usr/bin/env python
# -*-coding:utf-8-*-

# 正式版代码，稳定
# 遍历搜索，很慢

import logging
import sys


"""
logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
"""

def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))


# 读取数据文件car.txt,cross.txt,road.txt，
# 分别存到三个列表中：car[]  cross[]  road[]
# 去除括号和逗号，每行5列
# 去除第一行说明，只保留数字

def read_data(path):
    data_list = []
    with open(path, "r") as f:
        for line in f.readlines():
            data_list.append(line.replace('(', '').replace(')', '').strip('\n').split(','))
        del(data_list[0])
        for each_list in data_list:
            for i in range(0, len(each_list)):
                each_list[i] = int(each_list[i])
            each_list.append(0)      # 在car的最后一列加上运行状态
    return data_list


car = read_data('F:/pycharm my project/SDK_python/CodeCraft-2019/1-map-training-1/car.txt')
cross = read_data('F:/pycharm my project/SDK_python/CodeCraft-2019/1-map-training-1/cross.txt')
road = read_data('F:/pycharm my project/SDK_python/CodeCraft-2019/1-map-training-1/road.txt')


num_car = len(car)
num_cross = len(cross)
num_road = len(road)


# 数据索引：
# car:        (车辆id=0，始发地=1、目的地=2、最高速度=3、计划出发时间=4)
#             (id,from,to,speed,planTime)
#             (0, 1, 2, 3, 4)

# cross:      (路口id=0,  道路id=1,  道路id=2,  道路id=3,  道路id=4)
#             (id,roadId,roadId,roadId,roadId)
#             (0, 1, 2, 3, 4)

# road:       (道路id=0，道路长度=1，最高限速=2，车道数目=3，起始点id=4，终点id=5，是否双向=6)
#             (id,length,speed,channel,from,to,isDuplex)
#             (0, 1, 2, 3, 4, 5, 6)

# process


# 构建有向图

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

    def getWeight(self):
        """Returns the edge's weight."""
        return self._weight

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

    def clearMark(self):
        """Clears the mark on the vertex."""
        self._mark = False

    def getLabel(self):
        """Returns the label of the vertex."""
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

    def clear(self):
        """Clears the graph."""
        self._size = 0
        self._edgeCount = 0
        self._vertices = {}

    def clearEdgeMarks(self):
        """Clears all the edge marks."""
        for edge in self.edges():
            edge.clearMark()

    def clearVertexMarks(self):
        """Clears all the vertex marks."""
        for vertex in self.vertices():
            vertex.clearMark()

    def sizeEdges(self):
        """Returns the number of edges."""
        return self._edgeCount

    def sizeVertices(self):
        """Returns the number of vertices."""
        return len(self)

    def __str__(self):
        """Returns the string representation of the graph."""
        result = str(self.sizeVertices()) + " Vertices: "
        for vertex in self._vertices:
            result += " " + str(vertex)
        result += "\n";
        result += str(self.sizeEdges()) + " Edges: "
        for edge in self.edges():
            result += " " + str(edge)
        return result

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

    def removeVertex(self, label):
        """Returns True if the vertex was removed, or False otherwise."""
        removedVertex = self._vertices.pop(label, None)
        if removedVertex is None:
            return False

        # Examine all other vertices to remove edges
        # directed at the removed vertex
        for vertex in self.vertices():
            if vertex.removeEdgeTo(removedVertex):
                self._edgeCount -= 1

        # Examine all edges from the removed vertex to others
        for edge in removedVertex.incidentEdges():
            self._edgeCount -= 1
        self._size -= 1
        return True

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

    def removeEdge(self, fromLabel, toLabel):
        """Returns True if the edge was removed, or False otherwise."""
        fromVertex = self.getVertex(fromLabel)
        toVertex = self.getVertex(toLabel)
        edgeRemovedFlg = fromVertex.removeEdgeTo(toVertex)
        if edgeRemovedFlg:
            self._edgeCount -= 1
        return edgeRemovedFlg

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
            each_list.append(0)
    return data_list


# 调用有向图的类
g = LinkedDirectedGraph()

# 加入所有顶点到图中
for each_list in cross:
    g.addVertex(each_list[0])

# 加入路径和权重
for each_list in road:
    g.addEdge(each_list[4], each_list[5], int(each_list[1]))
    if each_list[6] == 1:
        g.addEdge(each_list[5], each_list[4], int(each_list[1]))
print(str(g))

# 标记所有顶点
for vertex in g.vertices():
    vertex.setMark()

# 查找所有路径
"""
def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if graph.getVertex(start) not in graph.vertices():
        return None
    paths = []
    for node in graph.neighboringVertices(start):
        #if node not in node_list:
            if node not in path:
                print(node)
                node_label = node.getLabel()
                #node_list.append(node)
                newpaths = find_all_paths(graph, node_label, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
    return paths
"""


# 查找最短路径
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    #print(path)
    if start == end:
        return path
    if graph.getVertex(start) not in graph.vertices():
        return None
    shortest = None
    for node in graph.neighboringVertices(start):
        node = node.getLabel()
        #print(node)
        if node not in path:
            #print(node)
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or length(newpath) < length(shortest):
                    shortest = newpath
        else:
            continue
    return shortest


# 根据路径求总长度，每段路的路程相加
def length(path):
    length = 0
    if path == None:
        return None
    if len(path) >= 2:
        for i in range(len(path)-1):
            edge = g.getEdge(path[i], path[i+1])
            length += edge.getWeight()
    return length


# for edge in g.incidentEdges(v.getLabel()):
#     print("所有的有向边：\n", edge)


# 初始化
# 初始化调度时间
Total_Time = 0


# 当前车组内出发时间最迟的车辆
def go_time(car):
    a = []
    for each_list in car:
        a.append(each_list[4])
    return max(a)


# 当前位置


# 约束条件

# 可行驶速度
def velocity(v_car, v_load):
    return min(v_car, v_load)


# 路径生成


# to write output file
# answer = [[0 for i in range(3)] for i in range(len_car)]
# for i in range(num_car):
    # answer = []


# “answer.txt“文件中每行数据表示：每一辆车的行驶路线规划，具体格式为(车辆id，实际出发时间，行驶路线序列)格式的向量。
# 例如(1001, 1, 501, 502, 503, 516, 506, 505, 518, 508, 509, 524)
# 即为上述1001号车辆自时间点1开始出发，从道路501、502、503…行驶至道路524的行驶路线。

if __name__ == "__main__":
    # for i in range(num_car):
    #     print(car[i][0])

    # print(find_shortest_path(g, car[1][1], car[1][2]))

    # 执行搜索最短路径
    shortest_path = []
    for each_list in car:
        #print("路径：")
        #print(find_all_paths(g, each_list[1], each_list[2]))
        #print("最短路径：")
        a = find_shortest_path(g, each_list[1], each_list[2])
        print(a)
        shortest_path.append(a)
    print(shortest_path)
