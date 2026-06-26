from utils.database import Graph, sessionLocal
from utils.graph import sdg
from utils.graph_snap import saveDb

def save_func():
    db = sessionLocal()
    try:
        saveDb(db, sdg, Graph)
    finally:
        db.close()
