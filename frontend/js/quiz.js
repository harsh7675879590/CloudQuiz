// quiz.js - Execution Engine for Student Quiz View

let quizData = null;
let attemptId = null;
let currentQuestionIndex = 0;
let userAnswers = {}; // { question_id: option_id }
let timerInterval = null;

document.addEventListener('DOMContentLoaded', async () => {
    Auth.requireRole('student');
    feather.replace();
    
    const params = new URLSearchParams(window.location.search);
    const quizId = params.get('id');
    
    if (!quizId) {
        window.location.href = 'dashboard.html';
        return;
    }
    
    await initQuiz(quizId);
});

async function initQuiz(id) {
    showOverlay('Starting Quiz...');
    try {
        // 1. Start Attempt
        let res = await api.post(`/student/quizzes/${id}/start`);
        attemptId = res.data.id;
        
        // 2. Fetch Quiz Details
        res = await api.get(`/student/quizzes/${id}`);
        quizData = res.data;
        
        document.getElementById('quizTitle').textContent = quizData.title;
        
        // 3. Render Navigation
        renderNav();
        
        // 4. Start Timer
        startTimer(quizData.time_limit);
        
        // 5. Render first question
        renderQuestion(0);
        
        // 6. Bind Buttons
        document.getElementById('btnPrev').addEventListener('click', () => {
            if (currentQuestionIndex > 0) renderQuestion(currentQuestionIndex - 1);
        });
        
        document.getElementById('btnNext').addEventListener('click', () => {
            if (currentQuestionIndex < quizData.questions.length - 1) {
                renderQuestion(currentQuestionIndex + 1);
            }
        });
        
        document.getElementById('btnSubmit').addEventListener('click', () => submitQuiz());
        
        hideOverlay();
    } catch (err) {
        console.error(err);
        showOverlay('Error loading quiz. Redirecting...', true);
        setTimeout(() => window.location.href = 'dashboard.html', 2000);
    }
}

function renderNav() {
    const nav = document.getElementById('questionNav');
    nav.innerHTML = quizData.questions.map((q, idx) => `
        <div class="nav-bubble ${idx === 0 ? 'active' : ''}" 
             id="navBubble-${idx}" 
             onclick="renderQuestion(${idx})">
             ${idx + 1}
        </div>
    `).join('');
}

function renderQuestion(index) {
    if (index < 0 || index >= quizData.questions.length) return;
    
    // Update State
    currentQuestionIndex = index;
    const q = quizData.questions[index];
    
    // Update Header
    document.getElementById('quizProgress').textContent = `Question ${index + 1} of ${quizData.questions.length}`;
    document.getElementById('qNum').textContent = `Q${index + 1}`;
    document.getElementById('qText').textContent = q.text;
    
    // Update Options List
    const selectedOption = userAnswers[q.id];
    const optsHTML = q.options.map(o => `
        <div class="option-item ${selectedOption === o.id ? 'selected' : ''}" 
             onclick="selectOption(${q.id}, ${o.id})">
            <span>${o.text}</span>
            ${selectedOption === o.id ? '<i data-feather="check-circle" class="text-primary"></i>' : ''}
        </div>
    `).join('');
    
    document.getElementById('optionsList').innerHTML = optsHTML;
    feather.replace();
    
    // Update Navigation Buttons & Submit
    document.getElementById('btnPrev').disabled = (index === 0);
    
    if (index === quizData.questions.length - 1) {
        document.getElementById('btnNext').classList.add('hidden');
        document.getElementById('btnSubmit').classList.remove('hidden');
    } else {
        document.getElementById('btnNext').classList.remove('hidden');
        document.getElementById('btnSubmit').classList.add('hidden');
    }
    
    // Update Bubbles
    document.querySelectorAll('.nav-bubble').forEach((b, i) => {
        b.classList.remove('active');
        if (i === index) b.classList.add('active');
    });
}

window.selectOption = function(qId, oId) {
    userAnswers[qId] = oId;
    
    // Mark bubble as answered visually
    const idx = quizData.questions.findIndex(q => q.id === qId);
    if (idx !== -1) {
        document.getElementById(`navBubble-${idx}`).classList.add('answered');
    }
    
    // Re-render current question immediately to show selection
    renderQuestion(currentQuestionIndex);
};

function startTimer(seconds) {
    const display = document.getElementById('timeRemaining');
    
    let time = seconds;
    const updateDisplay = () => {
        const m = Math.floor(time / 60).toString().padStart(2, '0');
        const s = (time % 60).toString().padStart(2, '0');
        display.textContent = `${m}:${s}`;
        
        if (time <= 60) {
            document.getElementById('timerDisplay').classList.add('danger');
        }
    };
    
    updateDisplay();
    timerInterval = setInterval(() => {
        time--;
        updateDisplay();
        
        if (time <= 0) {
            clearInterval(timerInterval);
            submitQuiz(true); // Auto submit
        }
    }, 1000);
}

async function submitQuiz(autoSubmit = false) {
    if (!autoSubmit && !confirm("Are you sure you want to submit?")) return;
    
    clearInterval(timerInterval);
    showOverlay('Submitting Answers...');
    
    const answersArray = Object.keys(userAnswers).map(qId => ({
        question_id: parseInt(qId),
        option_id: userAnswers[qId]
    }));
    
    try {
        await api.post(`/student/attempts/${attemptId}/submit`, {
            answers: answersArray
        });
        window.location.href = 'results.html';
    } catch (err) {
        console.error(err);
        showOverlay('Failed to submit. Please try again.', true);
        setTimeout(hideOverlay, 3000);
    }
}

function showOverlay(text, isError = false) {
    const overlay = document.getElementById('overlay');
    overlay.classList.remove('hidden');
    document.getElementById('overlayText').textContent = text;
    if (isError) {
        document.getElementById('overlayText').classList.add('text-danger');
        document.querySelector('#overlay i').setAttribute('data-feather', 'alert-circle');
        feather.replace();
    }
}

function hideOverlay() {
    document.getElementById('overlay').classList.add('hidden');
}
