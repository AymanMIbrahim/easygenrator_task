from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routes import generate,generate_reports_api





app = FastAPI(
    title="Easygenerator Task",
    description="AI Tool that generates balanced reviews",
    version="1.0.0",
    contact={
        "name":"Ayman M. Ibrahim",
        "email":"ayman.m.ibrahim.1994@gmail.com",
    }
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_app():
    pass

@app.on_event("shutdown")
async def shutdown_app():
    pass

app.include_router(generate.router, prefix="/generate", tags=["generate review"])
app.include_router(generate_reports_api.router, prefix="/generate_report", tags=["generate report for the generated reviews"])



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)