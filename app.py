from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import chromadb
import requests

app = FastAPI()
commits_client = chromadb.PersistentClient(path='vectorstore/')
docs_client = chromadb.PersistentClient(path='vectorstore_docs/')

commits_collection = commits_client.get_collection(name='odoo_migration_commits')
docs_collection = docs_client.get_collection(name='odoo_migration_docs')

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="<h1>Odoo Migration Assistant</h1>")

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    q = data.get("question")
    scope = data.get("scope", "both")
    contexts = []
    if scope in ("both", "commits"):
        contexts += commits_collection.query(query_texts=[q], n_results=50)['documents'][0]
    if scope in ("both", "docs"):
        contexts += docs_collection.query(query_texts=[q], n_results=50)['documents'][0]
    prompt = "You are an expert in Odoo migration. Use the following information strictly.\n\n" + "\n\n".join(contexts) + "\n\nUser Question:\n" + q
    r = requests.post("http://localhost:11434/api/generate", json={"model":"codellama:latest","prompt":prompt})
    result = r.json()
    return JSONResponse(content={"answer": result['response']})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
