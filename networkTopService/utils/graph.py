import networkx as nx 
from datetime import datetime
sdg = nx.DiGraph()
def create_graph(SPAN_CACHE, span, service_name):
    parent = SPAN_CACHE.get(span.parent_span_id.hex())
    if not parent:
        return
    source = parent["service"]
    target=service_name
    if source == target:
        return
    dur = (span.end_time_unix_nano - span.start_time_unix_nano)/1000000
    sdg.add_node(source)
    sdg.add_node(target)
    if sdg.has_edge(source,target):
        edge= sdg[source][target]
        edge["count"] +=1 
        edge["latency_sum"] += dur
        edge["last_seen"] = datetime.utcnow()
        if span.status.code != 0:
            edge["error_count"] += 1 
    else:
        sdg.add_edge(source, target, count=1, latency_sum=dur, last_seen=datetime.utcnow(), error_count=0)

def graph_data():
    edges=[]
    for source, target, attrs in sdg.edges(data=True):
        count = attrs["count"]
        avg_latency = attrs["latency_sum"]/count if count>0 else 0
        error_rate=attrs["error_count"]/count if count>0 else 0
        edges.append({"source": source, "target": target, "count": count, "avg_latency": avg_latency, "error_rate": error_rate, "last_seen": attrs["last_seen"]})
    return {"nodes": list(sdg.nodes()), "edges": edges}

def bl_radius(service_name: str):
    if service_name not in sdg:
        return []
    return list(nx.descendants(sdg, service_name))

def critic_score(service_name:str):
    if service_name not in sdg:
        return {"service_name": service_name, "criticality": 0}
    ds = list(nx.descendants(sdg, service_name))
    inbound = sdg.in_degree(service_name)
    outbound = sdg.out_degree(service_name)
    score = (ds*3)+inbound+outbound
    return {"service_name": service_name, "downstream": ds, "inbound": inbound, "outbound": outbound, "criticality": score}

