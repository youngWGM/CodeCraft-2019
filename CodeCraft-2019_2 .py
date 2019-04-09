#!/usr/bin/env python
# -*-coding:utf-8-*

# 测试版2.0日志:
#   ***实现dijkstra算法
#   ***移植heapq模块到本地
#   ***将输出路口标号改为道路标号
#   ***道路的weight中依次为[道路编号，道路长度，限速，车道数]
#   ***完善程序输出，生成"answer.txt"文件
#   ***整理程序结构，增加主程序，与题目要求贴合
#   ***备份用

import heap
import datetime
import time
import logging
import sys

# logging.basicConfig(level=logging.DEBUG,
#                     filename='../logs/CodeCraft-2019.log',
#                     format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filemode='a')


def main():
    # if len(sys.argv) != 5:
    #     logging.info('please input args: car_path, road_path, cross_path, answerPath')
    #     exit(1)
    #
    # car_path = sys.argv[1]
    # road_path = sys.argv[2]
    # cross_path = sys.argv[3]
    # answer_path = sys.argv[4]
    #
    # logging.info("car_path is %s" % (car_path))
    # logging.info("road_path is %s" % (road_path))
    # logging.info("cross_path is %s" % (cross_path))
    # logging.info("answer_path is %s" % (answer_path))

    start_time = datetime.datetime.now()
    car = read_data('F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-training-1\\car.txt')
    cross = read_data('F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-training-1\\cross.txt')
    road = read_data('F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-training-1\\road.txt')

    add_cross(cross)
    add_road(road)
    vlist = init(cross)
    # print(str(g))

    # dijkstra算法测试模块
    all_shortestpath = []   # 这个是由路口编号构成的路径
    all_len = []
    all_path = []  # 这个是道路编号构成的路径
    count = 0
    for each_list in car:
        shortestPath, Len = get_shortest_path(each_list[1], each_list[2], vlist)
        shortestPath = shortestPath[::-1]
        all_shortestpath.append(shortestPath)
        single_road = []
        for i in range(0, len(shortestPath)-1):
            edge = g.getEdge(shortestPath[i], shortestPath[i+1])
            Road = edge.getRoadlabel()
            single_road.append(Road)
        single_road.insert(0, each_list[0])   # 在每个路径前面加上车子编号
        if count >= each_list[4]:
            single_road.insert(1, count + each_list[2])
        else:
            single_road.insert(1, each_list[4])
        if car.index(each_list) % 25 == 0:
            count += 1
        # single_road.insert(1, each_list[4])    # 将每辆车的出发时间初始化为计划出发时间
        #count += 1
        all_path.append(single_road)
        # all_len.append(Len)
        # print(i)
        # print('{}->{}的最短路径是：{}，最短路径长度为：{}'.format(each_list[1], each_list[2], shortestPath[::-1], len))
        # i = i+1
    # print("所有最短路径(道路)：")
    # print(all_path)
    # print("所有最短路径(路口)：")
    # print(all_shortestpath)
    # print("所有路径长度")
    # print(all_len)

    write_txt(all_path, 'F:\\pycharm my project\\SDK\\SDK_python\\CodeCraft-2019\\1-map-training-1\\answer.txt')  # 生成txt文件
    end_time = datetime.datetime.now()
    print("Runtime:", (end_time - start_time))


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

    def getRoadlabel(self):
        """返回道路标号"""
        return self._weight[0]

    def getRoadlength(self):
        """返回道路长度"""
        return self._weight[1]

    def getRoadspeed(self):
        """返回道路限速"""
        return self._weight[2]

    def getRoadchannel(self):
        """返回车道数"""
        return self._weight[3]

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
    return data_list

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


g = LinkedDirectedGraph()


# 加入所有顶点
def add_cross(cross):
    for each_list in cross:
        g.addVertex(each_list[0])


# 加入边和权重
def add_road(road):
    for each_list in road:
        g.addEdge(each_list[4], each_list[5], [each_list[0], each_list[1], each_list[2], each_list[3]])
        if each_list[6] == 1:
            g.addEdge(each_list[5], each_list[4], [each_list[0], each_list[1], each_list[2], each_list[3]])


# 标记所有的顶点为可用
# for vertex in g.vertices():
#     vertex.setMark()

# 打印出所有的邻居节点
# v = g.getVertex(22)
# for neighbor in g.neighboringVertices(v.getLabel()):
#     print(neighbor)


# dijkstra算法寻找最短路径
# 初始化参数
def init(cross):
    vlist = [False]
    for each_list in cross:
        vlist.append(each_list[0])
    return vlist


# 最短路径函数
def get_shortest_path(start, end, vlist):
    # distances使用字典的方式保存每一个顶点到start点的距离
    distances = {}

    # 从start到某点的最优路径的前一个结点
    # eg:start->B->D->E,则previous[E]=D,previous[D]=B,等等
    previous = {}

    # 用来保存图中所有顶点的到start点的距离的优先队列
    # 这个距离不一定是最短距离
    nodes = []

    for vertex in vlist:
        if vertex == start:
            distances[vertex] = 0   # 将start点的距离初始化为0
            heap.heappush(nodes, [0, vertex])
            # nodes.append([0,vertex])
        elif vertex in g.neighboringVertices(start):
            distances[vertex] = length(start, vertex)   # 把与star点相连的结点距离start点的距离初始化为对应的道路长度
            heap.heappush(nodes, [length(start, vertex), vertex])
            # nodes.append([length(start, vertex), vertex])
            previous[vertex] = start
        else:
            distances[vertex] = 9999    # 把与start点不直接连接的结点距离start的距离初始化为9999
            heap.heappush(nodes, [9999, vertex])
            # nodes.append([9999, vertex])
            previous[vertex] = None
    shortest_path = [1]
    lenPath = 0
    while nodes:
        smallest = heap.heappop(nodes)[1]   # 取出队列中最小距离的结点
        # smallest = nodes.pop()[1]
        if smallest == end:
            shortest_path = []
            lenPath = distances[smallest]
            temp = smallest
            #print('previous[temp]:',temp)
            while (temp != start) :
                shortest_path.append(temp)
                temp = previous[temp]
            shortest_path.append(temp)  # 将start点也加入到shortest_path中
        if distances[smallest] == 9999:
            # 所有点不可达
            break
        # 遍历与smallest相连的结点，更新其与结点的距离、前继节点
        for neighbor in g.neighboringVertices(smallest):
            dis = distances[smallest] + length(smallest, neighbor.getLabel())
            if dis < distances[neighbor.getLabel()]:
                distances[neighbor.getLabel()] = dis
                previous[neighbor.getLabel()] = smallest    # 更新与smallest相连的结点的前继节点
                for node in nodes:
                    if node[1] == neighbor.getLabel():
                        node[0] = dis   # 更新与smallest相连的结点到start的距离
                        break
                heap.heapify(nodes)
    return shortest_path, lenPath


# 计算a路口到b路口路径的长度
def length(a, b):
    edge = g.getEdge(a, b)
    length = int(edge.getRoadlength()) / (int(edge.getRoadchannel())*3) + (5 - int(edge.getRoadspeed())/2)
    return length


# 将path写入到txt文件中
def write_txt(input_list, txt_path):
    file = open(txt_path, 'w')
    for i in range(len(input_list)):
        s = str(input_list[i]).replace('[', '(').replace(']', ')') + '\n'
        file.write(s)
    file.close()
    print("保存txt文件成功")


if __name__ == "__main__":
    main()
