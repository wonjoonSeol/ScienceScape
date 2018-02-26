import os
import itertools
import networkx
from networkx.readwrite import json_graph
import json
import codecs
import matplotlib.pyplot as plt

CONFIG = {}

def add_edge_weight(graph, node1, node2):
    if graph.has_edge(node1, node2):
        graph[node1][node2]['weight'] += 1
    else:
        graph.add_edge(node1, node2, weight = 1)

def export(graph, span, export_ref_format, parsed_data_folder):
    if export_ref_format == "gexf":
        print("Writing .gexf export")
        networkx.write_gexf(graph, os.path.join(parsed_data_folder, span, "%s.gexf" %span), encoding = "UTF-8")
    elif export_ref_format == "edgelist":
        print("Writing .csv export")
        networkx.write_weighted_edgelist(graph, os.path.join(parsed_data_folder, span, "%s.csv"%span), delimiter = "\t")
    elif export_ref_format == "pajek":
        print("Writing .pajek export")
        networkx.write_pajek(graph, os.path.join(parsed_data_folder, span, "%s.net" %span), encoding = 'UTF-8')
    elif export_ref_format == "json":
        print("Writing .json export")
        data = json_graph.node_link_data(graph)
        json.dump(data, open(os.path.join(parsed_data_folder, span, "%s.json" %span), "w"), encoding = 'UTF-8')
    else:
        print("No export compatible with the specified export format!")

def group_by_article(references_by_articles_filtered, span, references_occs, export_ref_format, parsed_data_folder):
    print("Processing edges for references...")
    graph = networkx.Graph()
    for article, art_refs in itertools.groupby(references_by_articles_filtered, key = lambda e:e[0]):
        # One link between the references cited by the same article
        for r1, r2 in itertools.combinations((r for a,r in art_refs), 2):
            graph.add_node(r1, type = "references", occurence_count = references_occs[r1])
            graph.add_node(r2, type = "references", occurence_count = references_occs[r2])
            add_edge_weight(graph, r1, r2)
    print("Remove edges with weight < %s" %CONFIG["spans"][span]["references"]["weight"])
    graph.remove_edges_from((r1, r2) for (r1, r2, d) in graph.edges(data = True) if d['weight'] < CONFIG["spans"][span]["references"]["weight"])
    print("Remove nodes with degree = 0")
    graph.remove_nodes_from(r for (r,d) in graph.degree() if d < 1)
    networkx.set_node_attributes(graph, 'type', "reference")

    # Write export file
    export(graph, span, export_ref_format, parsed_data_folder)

# -- Main script --

def run():
        for span in sorted(CONFIG["spans"]):
            print("\n#%s" %span)

            with codecs.open(os.path.join(CONFIG["parsed_data"], span, "references.dat"), "r", encoding = "UTF-8") as file:
            # .dat files have one trailing blank line
                data_lines = file.read().split("\n")[:-1]

            references_by_articles = [(l.split("\t")[0], ",".join(l.split("\t")[1:])) for l in data_lines]

            print("%s ref occurences in articles" %len(references_by_articles))
            references_by_articles.sort(key = lambda e:e[1])
            del(data_lines)

            # Filter the references which only occur in one article
            references_article_grouped = [(reference,list(ref_arts)) for reference, ref_arts in itertools.groupby(references_by_articles, key = lambda e:e[1])]
            global references_occs
            references_occs = dict([(reference, len(list(ref_arts))) for reference, ref_arts in references_article_grouped if len(ref_arts) >= CONFIG["spans"][span]["references"]["occ"]])

            print("filtering references")

            def filter_references_by_article(references_article_grouped, occurences_config_item):
                return [t for _ in (ref_arts for ref, ref_arts in references_article_grouped if len(ref_arts) >= occurences_config_item) for t in _]

            references_by_articles_filtered = filter_references_by_article(references_article_grouped, CONFIG["spans"][span]["references"]["occ"])

            # Group by articles and create a ref network
            print("Sorting references")
            references_by_articles_filtered.sort(key = lambda e:e[0])  # Sort References

            # Group by Article and Export
            group_by_article(references_by_articles_filtered, span, references_occs, CONFIG["export_ref_format"], CONFIG["parsed_data"])
