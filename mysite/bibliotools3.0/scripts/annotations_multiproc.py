import os
import networkx
import itertools
from networkx.readwrite import json_graph
import json
import codecs
from multiprocessing import Process
from multiprocessing import JoinableQueue

CONFIG = {}

def log(message, span):
    if verbose:
        log_messages.put("%s: %s" %(span,message))

def add_edge_weight(graph, node1, node2, weight = 1):
    if graph.has_edge(node1, node2):
        graph[node1][node2]['weight'] += weight
    else:
        graph.add_edge(node1, node2, weight = weight)

def add_item_category(span, items_name, parsed_data_folder):
    with codecs.open(os.path.join(parsed_data_folder, span, "%s.dat" % items_name), "r", encoding = "UTF-8") as items_file:
        articles_items = [(l.split("\t")[0], l.split("\t")[-1]) for l in items_file.read().split("\n")[:-1]]
        log("imported %s" %items_name, span)
    return articles_items

def group_by_item(articles_items):
    articles_items.sort(key = lambda e:e[1])
    item_articles_grouped = [(item,list(items_arts)) for item, items_arts in itertools.groupby(articles_items, key=lambda e:e[1])]
    return item_articles_grouped

def filter_by_occurrence(item_articles_grouped, occurrence_threshold, span, items_name):
    items_occs = dict((item, len(items_arts)) for item, items_arts in item_articles_grouped if len(items_arts) >= occurrence_threshold)
    article_items = [t for _ in (items_arts for item,items_arts in item_articles_grouped if len(items_arts) >= occurrence_threshold) for t in _]
    log("filtered %s by occ>=%s" %(items_name, occurrence_threshold), span)
    return (items_occs, article_items)

def group_by_article(article_items, items_name, span):
    article_items.sort(key = lambda e:e[0])
    article_items = dict((a, list(s for _, s in a_s)) for (a, a_s) in itertools.groupby(article_items, key = lambda e:e[0]))
    log("%s grouped by articles" %items_name, span)
    return article_items

def add_reference_nodes(references_article_grouped, article_items, items_occs, graph, items_name, weight_for_items_name, network_colours_for_items_name):
    for r,r_as in references_article_grouped:
        items = [s for ss in (article_items[a] for a, _ in r_as if a in article_items) for s in ss]
        items.sort()
        items_grouped = ((s, len(list(vs))) for s, vs in itertools.groupby(items))
        items_filtered = [(s, nb) for s, nb in items_grouped if nb >= weight_for_items_name]
        del items
        del items_grouped

        if len(items_filtered) > 0:
            for s, w in items_filtered:
                graph.add_node(s, label = s, type = items_name, occurence_count = items_occs[s], r = network_colours_for_items_name["r"], graph = network_colours_for_items_name["g"], b = network_colours_for_items_name["b"])
                add_edge_weight(graph, r, s, w)
        del items_filtered

def add_annotations(span, items_name, references_article_grouped, graph, all_spans, parsed_data_folder, network_colours):
    nb_nodes_before = len(graph.nodes())

    articles_items = add_item_category(span, items_name, parsed_data_folder)
    item_articles_grouped = group_by_item(articles_items)
    del articles_items

    occurrence_filtered = filter_by_occurrence(item_articles_grouped, all_spans[span][items_name]["occ"], span, items_name)
    items_occs = occurrence_filtered[0]
    article_items = occurrence_filtered[1]
    del item_articles_grouped

    article_items = group_by_article(article_items, items_name, span)
    add_reference_nodes(references_article_grouped, article_items, items_occs, graph, items_name, all_spans[span][items_name]["weight"], network_colours[items_name])

    log("Remove nodes with degree = 0", span)
    graph.remove_nodes_from(r for (r,d) in graph.degree() if d < 1)
    nb_items_added = len(graph.nodes()) - nb_nodes_before
    log("Added %s %s nodes in network" %(nb_items_added, items_name), span)
    return nb_items_added

def print_references_article_grouped(span_info, span, references_article_grouped, graph, all_spans, parsed_data_folder, network_colours):
    log("Imported, filtered and grouped references by articles", span)
    items = ["subjects", "authors", "institutions", "article_keywords", "title_keywords", "isi_keywords", "countries"]
    for item in items:
        span_info[item + "_occ_filtered"] = add_annotations(span, item, references_article_grouped, graph, all_spans, parsed_data_folder, network_colours)

def read_export(export_ref_format, parsed_data_folder, span):
    graph = networkx.Graph()
    if export_ref_format == "gexf":
        if process_verbose: log("read gexf", span)
        graph = networkx.read_gexf(os.path.join(parsed_data_folder, span, "%s.gexf" %span), node_type = str)
    elif export_ref_format == "edgelist":
        if process_verbose: log("read csv export", span)
        graph = networkx.read_weighted_edgelist(os.path.join(parsed_data_folder, span, "%s.csv" %span), delimiter = "\t")
    elif export_ref_format == "pajek":
        if process_verbose: log("read pajek export", span)
        graph = networkx.read_pajek(os.path.join(parsed_data_folder, span, "%s.csv" %span))
    elif export_ref_format == "json":
        if process_verbose: log("read pajek export", span)
        data = json.load(open(os.path.join(parsed_data_folder, span, "%s.json" %span), "r"),encoding = "UTF-8")
        graph = json_graph.node_link_graph(data)
    else:
        log("no export compatible export format specified", span)
        exit(1)
    return graph

def write_export(output_directory, export_ref_annotated_format, span, graph):
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    if export_ref_annotated_format == "gexf":
        log("write gexf export", span)
        networkx.write_gexf(graph, os.path.join(output_directory,"%s_annotated.gexf" %span))
    elif export_ref_annotated_format == "edgelist":
        log("write csv export", span)
        networkx.write_weighted_edgelist(graph,os.path.join(output_directory,"%s_annotated.csv"%span),delimiter="\t")
    elif export_ref_annotated_format == "pajek":
        log("write pajek export", span)
        networkx.write_pajek(graph,os.path.join(output_directory,"%s_annotated.net"%span))
    elif export_ref_annotated_format == "graphml":
        log("write pajek export", span)
        networkx.write_graphml(graph,os.path.join(output_directory,"%s_annotated.graphml"%span))
    else:
        log("no compatible export format specified", span)

def process_span(span, span_done, all_spans, parsed_data_folder, network_colours, export_ref_format, export_ref_annotated_format, output_directory):
    # Data to be reported after processing
    span_info = {"span":span}
    log("starting", span)

    graph = read_export(export_ref_format, parsed_data_folder, span)

    network_references = graph.nodes()
    nb_network_references = len(network_references)

    log("loaded %s ref from graph" %nb_network_references, span)
    span_info["references_occ_filtered"] = nb_network_references

    with codecs.open(os.path.join(parsed_data_folder, span, "references.dat"), "r", encoding = "UTF-8") as file:
        # .dat files have one trailing blank line
        data_lines = file.read().split("\n")[:-1]

    references_by_articles = [(l.split("\t")[0], ",".join(l.split("\t")[1:])) for l in data_lines]

    references_by_articles.sort(key = lambda e:e[1])
    article_groupby_reference = [(reference, list(ref_arts)) for reference, ref_arts in itertools.groupby(references_by_articles, key = lambda e:e[1])]
    span_info["nb_reference_before_filtering"] = len(article_groupby_reference)
    references_article_grouped = [t for t in article_groupby_reference if len(t[1]) >= all_spans[span]["references"]["occ"]]
    del article_groupby_reference
    del references_by_articles

    # Make sure we have same references as network

    ref_filtered = [r for r, _ in references_article_grouped]
    if(len(ref_filtered)) != nb_network_references:
        s1 = set(ref_filtered)
        s2 = set(network_references)
        to_remove = s1 - s2
        if len(to_remove) > 0:
            log("filtering ref which are not in original network : removing %s ref" %len(to_remove), span)
            references_article_grouped = [(r, ref_arts) for r, ref_arts in references_article_grouped if r not in to_remove]
        del s1
        del s2
    del ref_filtered
    del network_references

    # Print references_article_grouped
    print_references_article_grouped(span_info, span, references_article_grouped, graph, all_spans, parsed_data_folder, network_colours)
    del references_article_grouped

    log("have now %s nodes"%len(graph.nodes()), span)

    write_export(output_directory, export_ref_annotated_format, span, graph)

    with codecs.open(os.path.join(parsed_data_folder, span, "articles.dat"), "r", encoding = "UTF-8") as articles_file:
        nb_articles = len(articles_file.read().split("\n")[:-1])

    span_info["nb_articles"] = nb_articles
    span_done.put(span_info)
    del graph

def logger(filename,log_messages):
    while True:
        m = log_messages.get()
        with open(filename, "a") as logfile:
            logfile.write(m + "\n")
            logfile.flush()
        log_messages.task_done()

def csv_writing(s, reports_directory, all_spans):
    span = s["span"]
    csv_export = []
    line = [s["span"]]
    line.append(s["nb_articles"])
    nb_reference_before_filtering = s["nb_reference_before_filtering"]
    line.append(nb_reference_before_filtering)
    line.append("%s | %s" %(all_spans[span]["references"]["occ"], all_spans[span]["references"]["weight"]))
    nb_ref_filtered = s["references_occ_filtered"]
    line.append(nb_ref_filtered)
    for items in ["subjects","authors","institutions","article_keywords","title_keywords","isi_keywords","countries"]:
        f = "%s | %s"%(all_spans[span][items]["occ"], all_spans[span][items]["weight"])
        nb = s["%s_occ_filtered" %items]
        line += [f,nb]
    csv_export.append(",".join(str(_) for _ in line))
    write_to_csv(csv_export, reports_directory)

def prepare_csv(reports_directory):
    line = ["span","nb articles","nb ref","f_ref occ|weight","nb_ref_filtered"]
    for items in ["subjects","authors","institutions","article_keywords","title_keywords","isi_keywords","countries"]:
            line += ["f %s"%items,"nb %s"%items]
    csv_export = []
    csv_export.append(",".join(line))
    write_to_csv(csv_export, reports_directory)

def write_to_csv(lines, reports_directory):
    with open(os.path.join(reports_directory, "filtering_report.csv"), "a") as csvfile:
        csvfile.write("\n" + "\n".join(lines))
        csvfile.flush()

# -- Main Script --
def run():
    global verbose
    verbose = CONFIG["process_verbose"] or CONFIG["report_verbose"]
    global process_verbose
    process_verbose = CONFIG["process_verbose"]
    span_done = JoinableQueue()

    global log_messages
    log_messages = JoinableQueue()

    spans_to_process = sorted(CONFIG["spans"],reverse=True)

    # Create the logger process
    log_filename = "annotated_network_processing.log"
    if os.path.exists(log_filename):
        os.remove(log_filename)
    loggerP = Process(target = logger, args = (log_filename, log_messages))
    loggerP.daemon = True
    loggerP.start()

    # Create the first process on spans
    span_procs = {}
    for _ in range(min(CONFIG["nb_processes"], len(spans_to_process))):
        span = spans_to_process.pop()
        p = Process(target = process_span, args = (span,span_done, CONFIG["spans"], CONFIG["parsed_data"], CONFIG["network_colours"], CONFIG["export_ref_format"], CONFIG["export_ref_annotated_format"], CONFIG["output_directory"]))
        p.daemon = True
        p.start()
        span_procs[span] = p

    if CONFIG["report_csv"]:
        prepare_csv(CONFIG["reports_directory"])

    while len(spans_to_process) > 0 or len(span_procs) > 0:
        s = span_done.get()
        span = s["span"]
        span_procs[s["span"]].join()
        log_messages.put("%s done" %s['span'])
        del span_procs[s["span"]]

        # Create a new process if needed
        print("still %s spans to process" %len(spans_to_process))
        if len(spans_to_process) > 0:
            next_span = spans_to_process.pop()
            span_procs[next_span] = Process(target = process_span, args = (next_span, span_done, CONFIG["spans"], CONFIG["parsed_data"], CONFIG["network_colours"], CONFIG["export_ref_format"], CONFIG["export_ref_annotated_format"], CONFIG["output_directory"]))
            span_procs[next_span].daemon = True
            span_procs[next_span].start()
            print("new process on %s" %next_span)

        if CONFIG["report_csv"]:
            csv_writing(s, CONFIG["reports_directory"], CONFIG["spans"])
            span_done.task_done()

    span_done.join()
    log_messages.join()
    loggerP.terminate()
