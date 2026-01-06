import requests, json

UQV_API = "http://localhost:8002/uqv"          # micro-service or GOAT internal route

def vault_query(user_id, session_id, query_text,
                clusters_found=0, max_conf=0.0,
                worker="unknown", reason="no_cluster"):
    payload = {
        "user_id": user_id,
        "session_id": session_id,
        "query_text": query_text,
        "skg_clusters_returned": clusters_found,
        "max_cluster_conf": max_conf,
        "worker_name": worker,
        "vault_reason": reason
    }
    try:
        requests.post(UQV_API + "/store", json=payload, timeout=3)
    except Exception as e:
        print(f"[UQV] vault failed: {e}")