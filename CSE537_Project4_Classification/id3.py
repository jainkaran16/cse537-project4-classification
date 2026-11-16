# id3.py
# -------
# ID3 Decision Tree implementation

import util
import math


class _TreeNode:
    """A compact binary decision-tree node used internally by ID3."""

    def __init__(self, prediction, feature=None, zero=None, one=None):
        self.prediction = prediction
        self.feature = feature
        self.zero = zero
        self.one = one

    @property
    def isLeaf(self):
        return self.feature is None

class ID3Classifier:
    """
    ID3 Decision Tree classifier.
    """

    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "id3"
        self.tree = None
        self.pruning = False

        self.features = []

    def setPruning(self, pruning):
        self.pruning = pruning

    def train(self, trainingData, trainingLabels,
              validationData, validationLabels):
        """
        Train the ID3 decision tree using information gain.
        Apply pruning if enabled.
        """
        self.features = list(set(feature for datum in trainingData
                                 for feature in datum.keys()))
        examples = list(range(len(trainingData)))
        default = self.legalLabels[0] if self.legalLabels else None
        self.tree = self._buildTree(trainingData, trainingLabels, examples,
                                    tuple(self.features), default)
        if self.pruning and validationData:
            validationExamples = list(range(len(validationData)))
            self._prune(self.tree, validationData, validationLabels,
                        validationExamples)

    def classify(self, testData):
        """
        Return the predicted labels for the test data.
        """
        return [self._classifyOne(datum, self.tree) for datum in testData]

    # You may add additional helper methods here.

    @staticmethod
    def _entropy(labelCounts):
        total = float(sum(labelCounts.values()))
        if not total:
            return 0.0
        return -sum((count / total) * math.log(count / total, 2)
                    for count in labelCounts.values() if count)

    def _majority(self, labels, examples, default):
        if not examples:
            return default
        counts = {label: 0 for label in self.legalLabels}
        for index in examples:
            counts[labels[index]] += 1
        # legalLabels supplies a deterministic tie break.
        return max(self.legalLabels, key=lambda label: counts[label])

    def _buildTree(self, data, labels, examples, features, default):
        majority = self._majority(labels, examples, default)
        if not examples:
            return _TreeNode(majority)
        first = labels[examples[0]]
        if all(labels[index] == first for index in examples):
            return _TreeNode(first)
        if not features:
            return _TreeNode(majority)

        parentCounts = {}
        for index in examples:
            parentCounts[labels[index]] = parentCounts.get(labels[index], 0) + 1
        parentEntropy = self._entropy(parentCounts)
        bestFeature = None
        bestGain = -1.0
        bestPartitions = None
        for feature in features:
            partitions = ([], [])
            counts = ({}, {})
            for index in examples:
                value = 1 if data[index][feature] == 1 else 0
                partitions[value].append(index)
                label = labels[index]
                counts[value][label] = counts[value].get(label, 0) + 1
            weighted = sum((len(partitions[value]) / float(len(examples))) *
                           self._entropy(counts[value]) for value in (0, 1))
            gain = parentEntropy - weighted
            if gain > bestGain + 1e-12:
                bestFeature = feature
                bestGain = gain
                bestPartitions = partitions

        # ID3 must still permit a zero-gain split: parity/XOR data can have no
        # informative root feature while becoming perfectly separable below it.
        if bestFeature is None:
            return _TreeNode(majority)
        remaining = tuple(feature for feature in features
                          if feature != bestFeature)
        zero = self._buildTree(data, labels, bestPartitions[0], remaining,
                               majority)
        one = self._buildTree(data, labels, bestPartitions[1], remaining,
                              majority)
        return _TreeNode(majority, bestFeature, zero, one)

    def _classifyOne(self, datum, node):
        while not node.isLeaf:
            node = node.one if datum[node.feature] == 1 else node.zero
        return node.prediction

    def _prune(self, node, data, labels, examples):
        """Post-prune when a majority leaf is no worse on held-out data."""
        if node.isLeaf or not examples:
            return
        zeroExamples = [i for i in examples if data[i][node.feature] != 1]
        oneExamples = [i for i in examples if data[i][node.feature] == 1]
        self._prune(node.zero, data, labels, zeroExamples)
        self._prune(node.one, data, labels, oneExamples)
        subtreeCorrect = sum(self._classifyOne(data[i], node) == labels[i]
                             for i in examples)
        leafCorrect = sum(node.prediction == labels[i] for i in examples)
        if leafCorrect >= subtreeCorrect:
            node.feature = None
            node.zero = None
            node.one = None
