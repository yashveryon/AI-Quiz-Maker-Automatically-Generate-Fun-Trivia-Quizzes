let sessionId = null;
let currentQuestion = {};
let currentIndex = 0;

function startQuiz() {
  const topic = document.getElementById('quizTopic').value.trim(); // 🔄 Corrected ID here
  if (!topic) return alert("Please enter a topic!");

  // Reset results section
  document.getElementById('history').innerHTML = '';
  document.getElementById('score').innerText = '';

  fetch('http://localhost:8000/quiz/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic })
  })
    .then(res => res.json())
    .then(data => {
      sessionId = data.session_id;
      showQuestion(data);
    })
    .catch(err => {
      console.error("Error starting quiz:", err);
      alert("Something went wrong while starting the quiz.");
    });
}

function showQuestion(data) {
  document.getElementById('start-section').style.display = 'none';
  document.getElementById('quiz-section').style.display = 'block';
  document.getElementById('result-section').style.display = 'none';

  currentQuestion = data.question;
  currentIndex = data.question_num;

  document.getElementById('question-number').innerText = `Question ${currentIndex} (${data.difficulty})`;
  document.getElementById('question-text').innerText = currentQuestion.question;

  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';

  currentQuestion.options.forEach(option => {
    const label = document.createElement('label');
    label.innerHTML = `<input type="radio" name="option" value="${option}"/> ${option}`;
    label.style.display = 'block';
    optionsDiv.appendChild(label);
  });
}

function submitAnswer() {
  const selected = document.querySelector('input[name="option"]:checked');
  if (!selected) return alert("Please select an answer!");

  fetch('http://localhost:8000/quiz/answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      user_answer: selected.value
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.completed) {
        showFinalResult(data);
      } else {
        showQuestion(data);
      }
    })
    .catch(err => {
      console.error("Error submitting answer:", err);
      alert("Something went wrong while submitting your answer.");
    });
}

function showFinalResult(data) {
  document.getElementById('quiz-section').style.display = 'none';
  document.getElementById('result-section').style.display = 'block';

  document.getElementById('score').innerText = `You got ${data.final_score} out of 10 correct.`;

  const historyDiv = document.getElementById('history');
  historyDiv.innerHTML = '';

  data.history.forEach((q, i) => {
    const div = document.createElement('div');
    div.innerHTML = `
      <strong>Q${i + 1}:</strong> ${q.question}<br>
      Your Answer: ${q.user_answer || 'N/A'} | 
      Correct: ${q.correct_option} 
      <span style="color:${q.result ? 'green' : 'red'}">${q.result ? '✅' : '❌'}</span>
      <br><br>
    `;
    historyDiv.appendChild(div);
  });
}
