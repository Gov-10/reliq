from networkx.readwrite import json_graph
def saveDb(db, sdg, Graph):
    snap=json_graph.node_link_data(sdg)
    db_note=Graph(graph=snap)
    db.add(db_note)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        return str(e)
    db.refresh(db_note)

