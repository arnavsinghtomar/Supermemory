from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.main_graph import app as workflow_app  

class QueryRequest(BaseModel):
    query: str

api = FastAPI(title="LangGraph API", version="1.0")

@api.post("/run")
def run_query(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    try:
        result = workflow_app.invoke({"query": request.query})
        return {"success": True, "result": result["generation"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @api.post("/save")
# def save_query(request: QueryRequest):
#     if not request.query.strip():
#         raise HTTPException(status_code=400, detail="Query cannot be empty")
#     try:
#         save_to_memory(request.query)
#         return {"success": True}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run("main:api", host="127.0.0.1", port=8000, reload=True)
