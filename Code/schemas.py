from pydantic import BaseModel
from typing import List, Optional

# 🧠 Input schema for quiz generation (/generate)
class QuestionRequest(BaseModel):
    topic: str
    difficulty: str

# ✅ Output schema for a single multiple-choice question
class QuestionResponse(BaseModel):
    question: str
    options: List[str]
    correct_option: str

# 🧪 Optional: Answer checking (for standalone validation or future use)
class AnswerRequest(BaseModel):
    question: str
    selected_option: str
    correct_option: str

# 🔄 Input for starting a quiz session
class StartQuizRequest(BaseModel):
    topic: str

# 🔄 Input for submitting an answer
class SubmitAnswerRequest(BaseModel):
    session_id: str
    user_answer: str

# 🧾 Structure for saving question attempts in session history
class QuestionHistory(BaseModel):
    question: str
    options: List[str]
    correct_option: str
    user_answer: Optional[str]
    result: Optional[bool]
    difficulty: str

# 📦 Optional: if you want to return a batch of questions as an object
class QuizBatchResponse(BaseModel):
    questions: List[QuestionResponse]
