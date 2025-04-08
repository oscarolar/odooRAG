import json
import chromadb
from tqdm import tqdm

commits = json.load(open("commit_changes.json"))
docs = json.load(open("parsed_docs.json"))

client = chromadb.Client()
commit_collection = client.create_collection(name="odoo_migration_commits")

for idx, (hash_, message) in enumerate(tqdm(commits)):
    commit_collection.add(documents=[message], metadatas=[{"commit_hash": hash_}], ids=[f"commit-{idx}"])

client.persist()

doc_client = chromadb.Client()
doc_collection = doc_client.create_collection(name="odoo_migration_docs")

for idx, doc in enumerate(tqdm(docs)):
    doc_collection.add(documents=[doc], metadatas=[{"path": f"doc-{idx}"}], ids=[f"doc-{idx}"])

doc_client.persist()
