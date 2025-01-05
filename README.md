# CoRS
Concepts in Robotics Software ontology. Manually curated, raw definitions by Grok 2.

# How to use
* create new project in https://webprotege.stanford.edu/, import `CoRS.owl`
* programmatically for example:
```
from rdflib import Graph, URIRef, Literal, OWL
from rdflib.namespace import RDFS, RDF

g = Graph()
g.parse("CoRS.owl", format="xml")
```
