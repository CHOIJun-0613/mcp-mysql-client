from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from . import database, nlp

app = FastAPI(
    title="FastMCP Server",
    description="자연어 쿼리를 처리하는 MCP(Model Context Protocol) 서버",
    version="1.0.1",
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    natural_query: str
    sql_query: str
    status: str
    data: list | str | None

@app.on_event("startup")
async def startup_event():
    print("FastMCP 서버가 시작되었습니다.")
    conn = database.get_db_connection()
    if conn:
        print("데이터베이스 연결이 확인되었습니다.")
        conn.close()
    else:
        print("경고: 데이터베이스 연결 실패. .env 파일을 확인하세요.")

@app.post("/query", response_model=QueryResponse, summary="자연어 쿼리 처리")
async def handle_mcp_query(request: QueryRequest):
    natural_query = request.query
    db_schema = database.get_db_schema()
    if "실패" in db_schema or "오류" in db_schema:
        raise HTTPException(status_code=500, detail=db_schema)

    sql_query = nlp.convert_natural_language_to_sql(natural_query, db_schema)
    print(f"Generated SQL Query: {sql_query}")
    if "오류" in sql_query or "설정되지 않았습니다" in sql_query:
        raise HTTPException(status_code=500, detail=sql_query)

    status, data = database.execute_query(sql_query)
    if "오류" in status:
        raise HTTPException(status_code=400, detail=status)

    return QueryResponse(
        natural_query=natural_query, sql_query=sql_query, status=status, data=data
    )

if __name__ == "__main__":
    import uvicorn
    # This allows running the app directly for development.
    # Make sure to run from the project root after activating the venv:
    # python -m server.app.main
    # The --reload flag automatically restarts the server on code changes.
    uvicorn.run("server.app.main:app", host="0.0.0.0", port=8000, reload=True)