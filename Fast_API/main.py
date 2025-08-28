from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import quiz

app = FastAPI(
    title="AI Quiz Maker",
    description="Generate fun and educational quizzes using AI!",
    version="1.0.0"
)

# CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "🎉 Welcome to the AI Quiz Maker API!"}

# Register quiz routes
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])
