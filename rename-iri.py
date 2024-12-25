from rdflib import Graph, URIRef, Literal, OWL
from rdflib.namespace import RDFS, RDF

def get_label(graph, uri):
    list1 = list(graph.objects(uri, RDFS.label, None))
    list2 = list(graph.objects(uri, RDFS.label, Literal(None, lang='en')))
    labels = list(set(list1) | set(list2))
    print(labels)
    if labels:
        # Assuming labels are strings; if they could be something else, you might need to convert
        return labels[0].value if isinstance(labels[0], Literal) else str(labels[0])
    else:
        #print(uri)
        # If no label, use the local name part of the URI
        return uri.split('#')[-1] if '#' in str(uri) else uri.split('/')[-1]

g = Graph()
g.parse("CoRS.owl", format="xml")

# Define the new base IRI
new_base = "urn:CoRS#"

m = {}
for s, p, o in list(g.triples((None, None, None))):  # Convert to list to avoid modifying while iterating
    if isinstance(s, URIRef) and "webprotege.stanford.edu" in str(s):
        
        # Get the label for the entity
        if m.get(s) is None:
            label = get_label(g, s)
            label = label.replace(" ", "_")
            new_iri = URIRef(f"{new_base}{label}")
        else:
            new_iri = m.get(s)

        # Construct the new IRI
        m[s] = new_iri
        #print("{} | {}".format(s, new_iri))

        # Replace the old IRI with the new one
        g.remove((s, p, o))
        g.add((new_iri, p, o))

        # Specifically handle owl:Class declarations
        #if p == RDF.type and o == OWL.Class:
        #    g.remove((s, p, o))
        #    g.add((new_iri, p, o))

for s, p, o in list(g.triples((None, None, None))):  # Convert to list to avoid modifying while iterating
    if isinstance(s, URIRef) and "webprotege.stanford.edu" in str(o):
        # Replace the old IRI with the new one
        g.remove((s, p, o))
        g.add((s, p, m[o]))


# Serialize the modified graph to a new file
g.serialize(destination="CoRS-new.owl", format="xml")
