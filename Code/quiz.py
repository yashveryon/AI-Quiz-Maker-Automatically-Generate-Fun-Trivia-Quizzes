from fastapi import APIRouter, HTTPException
from uuid import uuid4
from typing import Dict, List

from app.services.quiz_generator import generate_questions
from app.models.schemas import (
    QuestionRequest,
    QuestionResponse,
    StartQuizRequest,
    SubmitAnswerRequest,
    QuestionHistory
)

router = APIRouter()

# In-memory quiz session storage
quiz_sessions: Dict[str, Dict] = {}

DIFFICULTY_ORDER = ["easy", "medium", "hard"]

def adjust_difficulty(current: str, correct: bool) -> str:
    idx = DIFFICULTY_ORDER.index(current)
    if correct and idx < len(DIFFICULTY_ORDER) - 1:
        return DIFFICULTY_ORDER[idx + 1]
    elif not correct and idx > 0:
        return DIFFICULTY_ORDER[idx - 1]
    return current

@router.post("/generate", response_model=List[QuestionResponse])
def generate_quiz(quiz_req: QuestionRequest):
    print(f"📩 Generating 10 questions for topic: {quiz_req.topic}, difficulty: {quiz_req.difficulty}")
    return generate_questions(quiz_req.topic, quiz_req.difficulty)

@router.post("/start")
def start_quiz(req: StartQuizRequest):
    topic = req.topic
    session_id = str(uuid4())
    difficulty = "medium"
    questions = generate_questions(topic, difficulty)

    history = []
    for idx, q in enumerate(questions):
        print(f"🔢 Q{idx + 1}: {q.question}")
        history.append(QuestionHistory(
            question=q.question,
            options=q.options,
            correct_option=q.correct_option,
            user_answer=None,
            result=None,
            difficulty=difficulty
        ).dict())

    quiz_sessions[session_id] = {
        "topic": topic,
        "difficulty": difficulty,
        "score": 0,
        "current_qn": 1,
        "history": history
    }

    return {
        "session_id": session_id,
        "question_num": 1,
        "difficulty": difficulty,
        "question": questions[0]
    }

@router.post("/answer")
def submit_answer(req: SubmitAnswerRequest):
    session = quiz_sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Invalid session ID")

    idx = session["current_qn"] - 1
    current = session["history"][idx]

    correct = (
        req.user_answer.strip().lower() ==
        current["correct_option"].strip().lower()
    )

    current["user_answer"] = req.user_answer
    current["result"] = correct

    session["difficulty"] = adjust_difficulty(session["difficulty"], correct)
    if correct:
        session["score"] += 1

    session["current_qn"] += 1

    if session["current_qn"] > 10:
        return {
            "completed": True,
            "final_score": session["score"],
            "history": session["history"]
        }

    next_q = session["history"][session["current_qn"] - 1]
    print(f"🔢 Q{session['current_qn']}: {next_q['question']}")

    return {
        "completed": False,
        "question_num": session["current_qn"],
        "difficulty": session["difficulty"],
        "question": QuestionResponse(
            question=next_q["question"],
            options=next_q["options"],
            correct_option=next_q["correct_option"]
        ),
        "result": "correct" if correct else "incorrect"
    }

