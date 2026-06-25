import networkx as nx 
sdg = nx.DiGraph()
def create_graph(SPAN_CACHE, span, service_name):
    parent = SPAN_CACHE.get(span.parent_span_id.hex())
    if parent:
        source = parent["service"]
        target= service_name
        dur= (span.end_time_unix_nano - span.start_time_unix_nano)/1000000
        if source==target:
            return
        if sdg.has_edge(source, target):
            sdg[source][target]["count"] +=1
            sdg[source][target]["latency"] += dur
        else:
            sdg.add_edge(source, target, count=1, latency=dur)
    else:
        return
        
