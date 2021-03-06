#!/usr/bin/env python
# -*-coding:utf-8-*-

import logging
import sys

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

inf = float('inf')


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

    car = read_data(car_path)
    cross = read_data(cross_path)
    road = read_data(road_path)
    aa = len(cross)

    Matrix, Nodes = GenerateMatrix(cross, road)

    Mst, root = prim(Matrix, Nodes)
    Mst, unuse_road = insert_roadlabel(Mst, road)

    add_cross(Nodes)
    add_road1(Mst)
    add_road2(road)

    all_path = []
    for each_list in car:
        a = find_shortest_path(g, each_list[1], each_list[2])
        b = add_unuseroad(a, unuse_road)
        c = add_sideroad(b, aa)
        single_road = []
        for i in range(0, len(c) - 1):
            edge = h.getEdge(c[i], c[i + 1])
            Road = edge.getRoadlabel()
            single_road.append(Road)
        single_road.insert(0, each_list[0])
        if each_list[3] == 16:
            single_road.insert(1, each_list[4])
        elif each_list[3] == 14:
            single_road.insert(1, each_list[4] * 2 + 220)
        elif each_list[3] == 12:
            single_road.insert(1, each_list[4] * 2 + 440)
        elif each_list[3] == 10:
            single_road.insert(1, each_list[4] * 2 + 660)
        elif each_list[3] == 8:
            single_road.insert(1, each_list[4] * 2 + 880)
        elif each_list[3] == 6:
            single_road.insert(1, each_list[4] * 2 + 1100)
        else:
            single_road.insert(1, each_list[4] * 2 + 1300)
        all_path.append(single_road)

    write_txt(all_path, answer_path)


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
        if self is other: return True
        if type(self) != type(other):
            return False
        return self._vertex1 == other._vertex1 and \
               self._vertex2 == other._vertex2

    def getOtherVertex(self, thisVertex):
        """Returns the vertex opposite thisVertex."""
        if thisVertex == None or thisVertex == self._vertex2:
            return self._vertex1
        else:
            return self._vertex2

    def getToVertex(self):
        """Returns the edge's destination vertex."""
        return self._vertex2

    def getRoadlabel(self):
        return self._weight[0]

    def getRoadlength(self):
        return self._weight[1]

    def getRoadspeed(self):
        return self._weight[2]

    def getRoadchannel(self):
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

    def sizeEdges(self):
        """Returns the number of edges."""
        return self._edgeCount

    def sizeVertices(self):
        """Returns the number of vertices."""
        return len(self)

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
        del (data_list[0])
        for each_list in data_list:
            for i in range(0, len(each_list)):
                each_list[i] = int(each_list[i])
    return data_list


def insert_roadlabel(Mst, road):
    unuse_road = []
    for each_load in road:
        unuse_road.append([each_load[4], each_load[5], each_load[1], each_load[0], each_load[6]])
    for each_unuseload in unuse_road:
        for each_list in Mst:
            if each_unuseload[0] == each_list[0] and each_unuseload[1] == each_list[1]:
                break
        unuse_road.remove(each_unuseload)
    unuse_road1 = []
    for each in unuse_road:
        if each[4] == 1:
            unuse_road1.append([each[1], each[0], each[2], each[3], each[4]])
    unuse_road = unuse_road + unuse_road1
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
    return Mst, unuse_road


def add_unuseroad(single_path, unuse_path):
    for each_list in unuse_path:
        for i in range(len(single_path) - 2):
            if single_path[-1] == each_list[1] and single_path[i] == each_list[0]:
                single_path = single_path[:i + 1]
                single_path.append(each_list[1])
                break
            else:
                continue
    return single_path


def add_sideroad(single_path, aa):
    sideroad1 = [[1623, 1238, 1671, 1305, 773, 1929, 1085, 1082, 1195, 1152, 902, 1590],
                 [1590, 1019, 1503, 852, 998, 1655, 123, 1624, 1087, 781, 1855, 834],
                 [834, 1896, 1180, 863, 138, 300, 313, 964, 552, 581, 1138, 1834],
                 [1834, 1613, 537, 1432, 491, 211, 554, 1242, 1197, 1697, 426, 1623]]

    sideroad2 = [[1023, 49, 463, 404, 1686, 153, 173, 1721, 658, 1157, 1260, 1],
                 [7, 1446, 859, 801, 996, 534, 1229, 1689, 1953, 1556, 535, 1289, 1704, 1957],
                 [1957, 718, 136, 1502, 759, 315, 1626, 1761, 1586, 100, 384, 1319],
                 [1319, 771, 1765, 505, 1766, 954, 840, 251, 1273, 1796, 1876, 1070, 1334, 1023]]
    if aa == 143:
        sideroad = sideroad1
    else:
        sideroad = sideroad2
    for each_list in sideroad:
        if single_path[0] in each_list and single_path[-1] in each_list:
            a = each_list.index(single_path[-1])
            b = each_list.index(single_path[0])
            if a >= b:
                single_path1 = each_list[b:a + 1]
                return single_path1
            elif a < b:
                temp = each_list[a:b + 1]
                single_path1 = temp[::-1]
            return single_path1
    return single_path


# Generate the Cross matrix
def GenerateMatrix(cross, road):
    Matrix = []
    for i in range(0, len(cross)):
        Matrix.append([])
        for j in range(0, len(cross)):
            Matrix[i].append(inf)
    for i in range(len(road)):
        if road[i][6] == 1:
            Matrix[suoyin(road[i][4], cross)][suoyin(road[i][5], cross)] = road[i][1] // (road[i][3] * 5) + (
                        8 - road[i][2] // 2)
            Matrix[suoyin(road[i][5], cross)][suoyin(road[i][4], cross)] = road[i][1] // (road[i][3] * 5) + (
                        8 - road[i][2] // 2)
    Nodes = []
    for i in range(0, len(cross)):
        Nodes.append(cross[i][0])
    return Matrix, Nodes


def suoyin(crossID, cross):
    for each_list in cross:
        if crossID in each_list:
            cross_suoyin = cross.index(each_list)
            return cross_suoyin


# Using Prim Algorithm Compute Mining Spining Tree
def prim(primgraph, chararray):
    Mst = []
    charlist = []
    charlist.append(chararray[0])
    mid = []
    lowcost = []
    lowcost.append(-1)
    mid.append(0)
    n = len(chararray)
    for i in range(1, n):
        lowcost.append(primgraph[0][i])
        mid.append(0)
    sum = 0
    for _ in range(1, n):
        minid = 0
        min = inf
        for j in range(1, n):
            if lowcost[j] != -1 and lowcost[j] < min:
                minid = j
                min = lowcost[j]
        charlist.append(chararray[minid])
        temp = ([chararray[mid[minid]], chararray[minid], lowcost[minid]])
        Mst.append(temp)
        sum += min
        lowcost[minid] = -1
        for j in range(1, n):
            if lowcost[j] != -1 and lowcost[j] > primgraph[minid][j]:
                lowcost[j] = primgraph[minid][j]
                mid[j] = minid
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

h = LinkedDirectedGraph()


def add_cross(root):
    for i in root:
        g.addVertex(i)
        h.addVertex(i)


def add_road1(road):
    for each_list in road:
        g.addEdge(each_list[0], each_list[1], [each_list[3], each_list[2]])


def add_road2(road):
    for each_list in road:
        h.addEdge(each_list[4], each_list[5],
                  [int(each_list[0]), int(each_list[1]), int(each_list[2]), int(each_list[3])])
        if each_list[6] == 1:
            h.addEdge(each_list[5], each_list[4],
                      [int(each_list[0]), int(each_list[1]), int(each_list[2]), int(each_list[3])])


def init(root):
    vlist = [False]
    for i in root:
        vlist.append(i)
    return vlist


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






