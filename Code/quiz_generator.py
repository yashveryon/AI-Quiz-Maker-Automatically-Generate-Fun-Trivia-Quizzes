from app.models.schemas import QuestionResponse
import requests
import json

def generate_questions(topic: str, difficulty: str) -> list[QuestionResponse]:
    print(f"🧠 Generating 10 questions for topic: {topic}, difficulty: {difficulty}")
    questions = []

    for i in range(10):
        print(f"🔄 Generating question {i+1}")
        system_prompt = (
            "You are a quiz generator. Create one multiple-choice question "
            f"about '{topic}' with difficulty '{difficulty}'. Respond ONLY in this JSON format:\n\n"
            "{\n"
            '  "question": "Your question text here?",\n'
            '  "options": ["A", "B", "C", "D"],\n'
            '  "correct_option": "One of A/B/C/D (as text)"\n'
            "}\n\n"
            "Use simple words. Do NOT include any explanation."
        )

        payload = {
            "model": "mistral",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a question about {topic} at {difficulty} difficulty level."}
            ],
            "temperature": 0.7,
            "max_tokens": 512
        }

        try:
            response = requests.post(
                "http://localhost:11434/v1/chat/completions",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            response.raise_for_status()
            raw = response.json()
            content = raw["choices"][0]["message"]["content"]
            print("📄 Raw model output:\n", content)

            data = json.loads(content) if content.strip().startswith("{") else {}
            question = QuestionResponse(
                question=data.get("question", "Failed"),
                options=data.get("options", []),
                correct_option=data.get("correct_option", "")
            )
            questions.append(question)

        except Exception as e:
            print(f"❌ Error for question {i+1}:", str(e))
            questions.append(QuestionResponse(
                question="Failed to generate.",
                options=[],
                correct_option=""
            ))

    return questions
