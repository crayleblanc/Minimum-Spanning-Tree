import numpy as np
import math
from functools import reduce


# this class uses a weighted undirected adjacency-matrix to represent the graph
class adjacencyGraph:
    def __init__(self, graphMatrix):
        connectedNodes = []
        listEdges = []
        choiceList = []

        # this is the matrix of the edge costs from the destination row to the source column
        self.graphMatrix = graphMatrix

        # these are the columns that represent which nodes are connected to the current tree, used to check
        # which edges are available to choose from in the matrix
        self.connectedNodes = connectedNodes

        # listEdges is the row index of the minimum item, the minimum item column index, and its edge cost
        self.listEdges = listEdges

        # choiceList is the number of alternative choices per row of the matrix
        self.choiceList = choiceList

        # this is a copy of the matrix used to check for alternative MST's
        self.graphCopy = np.copy(graphMatrix)

    # this method returns the number of edges needed to create the minimum spanning tree
    def getMinimumNumberOfEdges(self):
        # the number of edges (ie number of columns in the array minus 1)
        return np.shape(self.graphMatrix)[1] - 1

    # sets the value of the minimum number to 0, so that it won't be visited again
    def visitRow(self, minRowIndex, minColIndex):
        # set the row to all zeros, so the row doesn't act as a destination again(no cycles)
        self.graphMatrix[minRowIndex] = np.zeros(np.shape(self.graphMatrix)[1], dtype=int)

        # the graph is symmetric, so set the corresponding value on the diagonal to zero as well
        self.graphMatrix[minColIndex, minRowIndex] = 0

    # this method finds the minimum in the adjacency graph
    def getFirstMin(self):
        # set the min to a default value of inf, guaranteed to find a smaller edge in the rows
        absoluteMin = math.inf
        minColumnIndex = 0
        minRowIndex = 0

        # iterate through each row, and find the minimum of the current row
        for rowIndex, currentRow in enumerate(self.graphMatrix):
            for columnIndex, currentEdge in enumerate(currentRow):
                if 0 < currentEdge < absoluteMin:
                    absoluteMin = currentEdge
                    minColumnIndex = columnIndex
                    minRowIndex = rowIndex

        # change the column of the minimum value to 0s, to indicate that it's been visited
        self.visitRow(minRowIndex, minColumnIndex)

        # add the minRowIndex and minColumnIndex to the nodes available to choose the next minimum from
        # the first edge is special because it adds two nodes to the tree, while each subsequent
        # edge added, only adds one new edge to the tree
        self.connectedNodes.append(minRowIndex)
        self.connectedNodes.append(minColumnIndex)

        # add the source node, the destination node, and the cost to get there to the list of edges
        self.listEdges.append((minRowIndex + 1, minColumnIndex + 1, absoluteMin))

    # this method looks for the minimum value down the given column indexes of the matrix
    def getMinPerColumn(self, columnIndexList):
        columnMin = math.inf
        minRowIndex = 0
        minColumnIndex = 0

        for columnIndex in columnIndexList:
            for rowIndex, currentRow in enumerate(self.graphMatrix):
                if 0 < self.graphMatrix[rowIndex, columnIndex] < columnMin:
                    columnMin = self.graphMatrix[rowIndex, columnIndex]
                    minRowIndex = rowIndex
                    minColumnIndex = columnIndex
        self.visitRow(minRowIndex, minColumnIndex)
        self.connectedNodes.append(minRowIndex)
        self.listEdges.append((minRowIndex + 1, minColumnIndex + 1, columnMin))
        return columnMin

    def findAlternativeChoices(self, rowIndex, colIndex, edgeCost):
        numberOfChoices = 1
        alternativeChoices = dict()

        for currentRowIndex, currentItem in enumerate(self.graphCopy[:, rowIndex]):
            if currentItem == edgeCost:
                # adds the value of the tuple of the sourceNode, destinationNode, and edgeCost to the altChoices dict
                valueCheck = alternativeChoices.get((rowIndex + 1, colIndex + 1, edgeCost))
                if valueCheck is None:
                    alternativeChoices[(rowIndex + 1, colIndex + 1, edgeCost)] = [
                        "An alternative edge is Node {} to Node {} : cost={}".format(currentRowIndex + 1,
                                                                                     rowIndex + 1, edgeCost)]
                else:
                    alternativeChoices[(rowIndex + 1, colIndex + 1, edgeCost)].append(
                        "An alternative edge is Node {} to Node {} : cost={}".format(currentRowIndex + 1,
                                                                                     rowIndex + 1, edgeCost))

                # sets the value to zero, so it doesn't get counted again
                self.graphCopy[currentRowIndex, rowIndex] = 0

                # increments the number of choices to indicate a match
                numberOfChoices += 1
        self.choiceList.append(numberOfChoices)
        return alternativeChoices

    def getMinSpanTree(self):
        minCost = 0
        self.getFirstMin()
        for edgeNumber in range(self.getMinimumNumberOfEdges()):
            self.getMinPerColumn(self.connectedNodes)
            sourceNode, destinationNode, edgeCost = self.listEdges[edgeNumber]

            # sets the values to zero in the graphCopy, for searching for alternatives, later
            self.graphCopy[sourceNode - 1, destinationNode - 1] = 0
            self.graphCopy[destinationNode - 1, sourceNode - 1] = 0

            minCost += edgeCost
            print("Node {} ==> Node {} : cost={}".format(sourceNode, destinationNode, edgeCost))

        print("\nMinimum Cost is {}".format(minCost))

        for _ in range(self.getMinimumNumberOfEdges()):
            sourceNode, destinationNode, edgeCost = self.listEdges.pop(0)
            altChoices = self.findAlternativeChoices(sourceNode - 1, destinationNode - 1, edgeCost)
        # this multiplies each choice in the list to give the total number of possible choices
        print("There are {} total Minimum Spanning Trees.".format(reduce(lambda x, y: x * y, self.choiceList)))

        for currentKey in altChoices.keys():
            print("\nThe chosen edge was: Node {} to Node {} : cost={}".format(*currentKey))
            while len(altChoices[currentKey]) != 0:
                currentValue = altChoices[currentKey].pop(0)
                print(currentValue)


prob1Graph = np.array([[0, 1, 5, 7, 9, 0],
                       [1, 0, 6, 4, 3, 0],
                       [5, 6, 0, 5, 0, 10],
                       [7, 4, 5, 0, 8, 3],
                       [9, 3, 0, 8, 0, 0],
                       [0, 0, 10, 3, 0, 0]])

prob2Graph = np.array([[0, 5, 0, 6, 0, 0, 0, 0, 0, 0],
                       [5, 0, 5, 0, 5, 0, 0, 0, 0, 0],
                       [0, 5, 0, 0, 0, 6, 0, 0, 0, 0],
                       [6, 0, 0, 0, 5, 0, 6, 0, 0, 0],
                       [0, 5, 0, 5, 0, 5, 0, 5, 0, 0],
                       [0, 0, 6, 0, 5, 0, 0, 0, 6, 0],
                       [0, 0, 0, 6, 0, 0, 0, 5, 0, 6],
                       [0, 0, 0, 0, 5, 0, 5, 0, 5, 6],
                       [0, 0, 0, 0, 0, 6, 0, 5, 0, 6],
                       [0, 0, 0, 0, 0, 0, 6, 6, 6, 0]])

problem1 = adjacencyGraph(graphMatrix=prob1Graph)
problem1.getMinSpanTree()
print("\n============================\n")

problem2 = adjacencyGraph(graphMatrix=prob2Graph)
problem2.getMinSpanTree()
