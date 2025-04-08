import os
import subprocess
import json

def clone_doc_repo():
    subprocess.run(["git", "clone", "git@github.com:odoo/documentation.git", "odoo_docs"], check=True)

def parse_rst_files():
    docs = []
    for root, _, files in os.walk("odoo_docs/content/developer"):
        for file in files:
            if file.endswith(".rst"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    docs.append(f.read())
    return docs

def main():
    clone_doc_repo()
    docs = parse_rst_files()
    with open("parsed_docs.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

if __name__ == "__main__":
    main()
