### Graph Builder (GB)

Graph Builder (GB) is the module responsible for creating and maintaining the word graph used by the system. It processes word lists obtained from one or more dictionaries and constructs a graph where each word is represented as a node, with edges connecting words that differ by exactly one letter.

This module applies filtering and normalization rules to ensure that only valid and meaningful words are included in the graph. It then generates the connections between words based on the defined similarity criteria and persists the resulting structure in a graph database.

GB is designed to support graph generation for different word lengths, enabling incremental increases in graph size and complexity. By decoupling graph construction from query processing, the system allows the graph to be rebuilt or extended without impacting API availability or ongoing computations.

Graph Builder typically runs as a batch or scheduled process and serves as the data preparation layer for the rest of the architecture.
