# vault_generator.py
import os
import json
import zipfile
from datetime import datetime
import requests  # For API uploads

# API Keys (rotated for security)
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
WEB3_STORAGE_TOKEN = os.getenv("WEB3_STORAGE_TOKEN")
ARWEAVE_KEY = os.getenv("ARWEAVE_KEY")
ESTUARY_TOKEN = os.getenv("ESTUARY_TOKEN")

VAULT_TEMPLATE = {
    "vault_version": "1.0",
    "generated_by": "GOAT Vault Forge",
    "date": datetime.utcnow().isoformat() + "Z",
    "certsig_ready": False,
    "truemark_ready": False,
    "storage": [],
    "assets": []
}

def upload_to_ipfs(file_path, service="pinata"):
    """Upload file to IPFS service"""
    if service == "pinata":
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {"Authorization": f"Bearer {PINATA_API_KEY}"}
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, headers=headers)
            return response.json().get('IpfsHash')
    elif service == "web3storage":
        url = "https://api.web3.storage/upload"
        headers = {"Authorization": f"Bearer {WEB3_STORAGE_TOKEN}"}
        with open(file_path, 'rb') as f:
            response = requests.post(url, files={'file': f}, headers=headers)
            return response.json().get('cid')
    return None

def upload_to_arweave(file_path):
    """Upload to Arweave"""
    # Placeholder for Arweave upload
    return "arweave_tx_id_placeholder"

def upload_to_filecoin(file_path):
    """Upload to Filecoin via Estuary"""
    url = "https://api.estuary.tech/content/add"
    headers = {"Authorization": f"Bearer {ESTUARY_TOKEN}"}
    with open(file_path, 'rb') as f:
        files = {'data': f}
        response = requests.post(url, files=files, headers=headers)
        return response.json().get('cid')

def reserve_truemark_domain(project_name, wallet):
    """Reserve TrueMark .go domain"""
    # Placeholder for TrueMark API
    return f"{project_name}.go"

def create_vault(project_name, tier="basic", deliverables_path=".", auto_upload=False):
    root = f"{project_name}_GOAT_VAULT"
    os.makedirs(root, exist_ok=True)
    os.makedirs(f"{root}/metadata", exist_ok=True)
    os.makedirs(f"{root}/originals", exist_ok=True)
    os.makedirs(f"{root}/deliverables", exist_ok=True)
    os.makedirs(f"{root}/hashes", exist_ok=True)
    os.makedirs(f"{root}/proofs", exist_ok=True)

    # Base manifest
    manifest = VAULT_TEMPLATE.copy()
    manifest["project"] = project_name
    manifest["tier"] = tier

    storage_cids = {}

    if tier in ["pro", "immortal", "dynasty"]:
        manifest["storage"].append("arweave")
        manifest["certsig_ready"] = True
        if auto_upload:
            storage_cids["arweave"] = upload_to_arweave(root)
    if tier in ["immortal", "dynasty"]:
        manifest["storage"].append("filecoin")
        if auto_upload:
            storage_cids["filecoin"] = upload_to_filecoin(root)
    if tier == "dynasty":
        manifest["truemark_ready"] = True
        manifest["storage"].append("truemark_gdis")
        # Auto-reserve domain
        manifest["truemark_domain"] = reserve_truemark_domain(project_name, "{{wallet}}")

    # Always include IPFS for basic+
    manifest["storage"].append("ipfs")
    if auto_upload:
        storage_cids["ipfs"] = upload_to_ipfs(root, "pinata")

    # CertSig metadata
    certsig_meta = {
        "name": f"{project_name} — Official Legacy Vault",
        "description": f"Immutable GOAT-created masterclass/audiobook/coaching empire permanently stored across Web3",
        "external_url": f"https://truemark.gg/{project_name.lower()}",
        "attributes": [
            {"trait_type": "Creator Tool", "value": "GOAT"},
            {"trait_type": "Vault Tier", "value": tier.capitalize()},
            {"trait_type": "Storage Layers", "value": len(manifest["storage"])}
        ]
    }
    with open(f"{root}/metadata/certsig_metadata.json", "w") as f:
        json.dump(certsig_meta, f, indent=2)

    # TrueMark GDIS record
    if tier == "dynasty":
        gdis = {
            "owner": "{{wallet}}",
            "identity": project_name.lower(),
            "vault_cid": storage_cids.get("ipfs", "{{ipfs_cid}}"),
            "linked_assets": "all",
            "domain": manifest["truemark_domain"]
        }
        with open(f"{root}/metadata/truemark_gdis_record.json", "w") as f:
            json.dump(gdis, f, indent=2)

    # Copy deliverables
    import shutil
    if os.path.exists(deliverables_path):
        shutil.copytree(deliverables_path, f"{root}/deliverables", dirs_exist_ok=True)

    # Write hashes
    for service, cid in storage_cids.items():
        with open(f"{root}/hashes/{service}_cid.txt", "w") as f:
            f.write(cid or "pending")

    # Finalize
    with open(f"{root}/asset_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    # Flags
    if manifest["certsig_ready"]:
        open(f"{root}/proofs/certsig_ready.flag", "w").write("MINT NOW")
    if manifest["truemark_ready"]:
        open(f"{root}/proofs/truemark_link.flag", "w").write("LINK DOMAIN")

    # Zip it
    zip_name = f"{root}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
        for folder_name, subs, files in os.walk(root):
            for file in files:
                z.write(os.path.join(folder_name, file),
                        os.path.relpath(os.path.join(folder_name, file), os.path.join(root, '..')))

    return zip_name