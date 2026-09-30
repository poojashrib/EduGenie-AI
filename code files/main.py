import os
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. Load environment variables (.env) before importing modules
load_dotenv()

# Import all module functions
from qna import answer_question_with_gemini
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations

# 2. Initialize FastAPI app
app = FastAPI(title="EduGenie AI Learning Assistant")

# 3. Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# 4. Define Pydantic request models for JSON POST bodies
class SummarizeRequest(BaseModel):
    text: str

class QuizRequest(BaseModel):
    text: str

class ExplainRequest(BaseModel):
    topic: str


# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

# Root Route - Render Index HTML
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


# 1. Q&A Endpoint (GET)
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# 2. Explanation Endpoints (Supports both GET and POST)
@app.get("/explain")
async def explain_get(topic: str = Query(...)):
    explanation = explain_topic(topic)
    return {"explanation": explanation}

@app.post("/explain/")
async def explain_post(request: ExplainRequest):
    explanation = explain_topic(request.topic)
    return {"explanation": explanation}


# 3. Summary Endpoints (Supports both /summarize and /summarize/)
@app.post("/summarize")
@app.post("/summarize/")
async def summarize(request: SummarizeRequest):
    summary = summarize_text(request.text)
    return {"summary": summary}


# 4. Quiz Endpoint (POST)
@app.post("/quiz")
async def quiz(request: QuizRequest):
    quiz_data = generate_quiz(request.text)
    # Return wrapped dict so JavaScript can access data.quiz safely
    return {"quiz": quiz_data}


# 5. Learning Path / Recommendations Endpoints (Supports both routes)
@app.get("/learning-path")
async def learning_path(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"recommendation": recommendation}

@app.get("/learn/recommendations")
async def learn_recommendations(topic: str = Query(...)):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)