import spacy
import networkx as nx
nlp = spacy.load("en_core_web_sm")

text = u'Convulsions that occur after DTaP are caused by a fever.'
entity1 = 'Convulsions'.lower()
entity2 = 'fever'
doc = nlp(text)

print('sentence:',format(doc))
# Load spacy's dependency tree into a networkx graph
edges = []
for token in doc:
    for child in token.children:
        edges.append(('{0}'.format(token.lower_),
                      '{0}'.format(child.lower_)))
graph = nx.Graph(edges)
# Get the length and path
print('shortest path lenth: ',nx.shortest_path_length(graph, source=entity1, target=entity2))
print('shortest path: ',nx.shortest_path(graph, source=entity1, target=entity2))
