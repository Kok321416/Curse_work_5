// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';
let authToken = localStorage.getItem('authToken');
let currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');
let currentPage = 1;
let currentFilter = 'all';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    if (authToken && currentUser) {
        showDashboard();
        loadUserHabits();
        updateStats();
    } else {
        showWelcome();
    }
});

// Utility functions
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts-container');
    const alertId = 'alert-' + Date.now();
    
    const alertHTML = `
        <div id="${alertId}" class="alert alert-${type} alert-custom alert-dismissible fade show" role="alert">
            <i class="fas fa-${getAlertIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertsContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-circle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function hideAllSections() {
    const sections = ['login-form', 'register-form', 'profile-form', 'dashboard', 'add-habit-form', 'my-habits', 'public-habits'];
    sections.forEach(section => {
        document.getElementById(section).classList.add('hidden');
    });
}

function showWelcome() {
    hideAllSections();
    hideLoading();
    document.getElementById('auth-section').classList.remove('hidden');
    document.getElementById('user-section').classList.add('hidden');
}

function showDashboard() {
    hideAllSections();
    hideLoading();
    document.getElementById('dashboard').classList.remove('hidden');
    document.getElementById('my-habits').classList.remove('hidden');
    document.getElementById('auth-section').classList.add('hidden');
    document.getElementById('user-section').classList.remove('hidden');
    document.getElementById('user-email').textContent = currentUser?.email || '';
}

// API functions
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    if (authToken) {
        config.headers['Authorization'] = `Token ${authToken}`;
    }
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || data.error || 'Произошла ошибка');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Authentication
function showLogin() {
    hideAllSections();
    document.getElementById('login-form').classList.remove('hidden');
}

function showRegister() {
    hideAllSections();
    document.getElementById('register-form').classList.remove('hidden');
}

async function login(event) {
    event.preventDefault();
    showLoading();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const data = await apiRequest('/users/login/', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        
        authToken = data.token;
        currentUser = data.user;
        
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        showAlert('Успешная авторизация!', 'success');
        showDashboard();
        loadUserHabits();
        updateStats();
        
    } catch (error) {
        showAlert(error.message, 'danger');
        hideLoading();
    }
}

async function register(event) {
    event.preventDefault();
    showLoading();
    
    const formData = {
        email: document.getElementById('register-email').value,
        username: document.getElementById('register-username').value,
        first_name: document.getElementById('register-first-name').value,
        last_name: document.getElementById('register-last-name').value,
        password: document.getElementById('register-password').value,
        password_confirm: document.getElementById('register-password-confirm').value
    };
    
    try {
        const data = await apiRequest('/users/register/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        authToken = data.token;
        currentUser = data.user;
        
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        showAlert('Регистрация прошла успешно!', 'success');
        showDashboard();
        loadUserHabits();
        updateStats();
        
    } catch (error) {
        showAlert(error.message, 'danger');
        hideLoading();
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    
    showAlert('Вы вышли из системы', 'info');
    showWelcome();
}

// Profile
function showProfile() {
    hideAllSections();
    document.getElementById('profile-form').classList.remove('hidden');
    
    // Fill form with current user data
    document.getElementById('profile-first-name').value = currentUser.first_name || '';
    document.getElementById('profile-last-name').value = currentUser.last_name || '';
    document.getElementById('profile-telegram-chat-id').value = currentUser.telegram_chat_id || '';
}

async function updateProfile(event) {
    event.preventDefault();
    showLoading();
    
    const formData = {
        first_name: document.getElementById('profile-first-name').value,
        last_name: document.getElementById('profile-last-name').value,
        telegram_chat_id: document.getElementById('profile-telegram-chat-id').value
    };
    
    try {
        const data = await apiRequest('/users/profile/', {
            method: 'PATCH',
            body: JSON.stringify(formData)
        });
        
        currentUser = { ...currentUser, ...data };
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        
        showAlert('Профиль обновлен!', 'success');
        showDashboard();
        
    } catch (error) {
        showAlert(error.message, 'danger');
        hideLoading();
    }
}

// Habits
function showMyHabits() {
    document.getElementById('my-habits').classList.remove('hidden');
    document.getElementById('public-habits').classList.add('hidden');
    document.getElementById('add-habit-form').classList.add('hidden');
    
    // Update nav
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    event.target.classList.add('active');
    
    loadUserHabits();
}

function showPublicHabits() {
    document.getElementById('my-habits').classList.add('hidden');
    document.getElementById('public-habits').classList.remove('hidden');
    document.getElementById('add-habit-form').classList.add('hidden');
    
    // Update nav
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    event.target.classList.add('active');
    
    loadPublicHabits();
}

function showAddHabit() {
    document.getElementById('my-habits').classList.add('hidden');
    document.getElementById('public-habits').classList.add('hidden');
    document.getElementById('add-habit-form').classList.remove('hidden');
    
    // Update nav
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    event.target.classList.add('active');
    
    loadPleasantHabits();
}

async function loadUserHabits(page = 1) {
    showLoading();
    
    try {
        const data = await apiRequest(`/habits/?page=${page}`);
        renderHabits(data.results, 'habits-list');
        renderPagination(data, 'habits-pagination', loadUserHabits);
        hideLoading();
    } catch (error) {
        showAlert(error.message, 'danger');
        hideLoading();
    }
}

async function loadPublicHabits(page = 1) {
    showLoading();
    
    try {
        const data = await apiRequest(`/public-habits/?page=${page}`);
        renderPublicHabits(data.results, 'public-habits-list');
        renderPagination(data, 'public-habits-pagination', loadPublicHabits);
        hideLoading();
    } catch (error) {
        showAlert(error.message, 'danger');
        hideLoading();
    }
}

async function loadPleasantHabits() {
    try {
        const data = await apiRequest('/habits/pleasant_habits/');
        const select = document.getElementById('habit-related');
        select.innerHTML = '<option value="">Выберите приятную привычку</option>';
        
        data.forEach(habit => {
            select.innerHTML += `<option value="${habit.id}">${habit.action}</option>`;
        });
    } catch (error) {
        console.error('Error loading pleasant habits:', error);
    }
}

function renderHabits(habits, containerId) {
    const container = document.getElementById(containerId);
    
    if (habits.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="fas fa-seedling fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Пока нет привычек</h5>
                <p class="text-muted">Создайте свою первую привычку!</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = habits.map(habit => `
        <div class="col-md-6 col-lg-4">
            <div class="card habit-card ${habit.is_pleasant ? 'habit-pleasant' : 'habit-useful'}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="card-title mb-0">${habit.action}</h6>
                        ${habit.is_public ? '<span class="public-badge">Публичная</span>' : ''}
                    </div>
                    
                    <div class="mb-2">
                        <small class="text-muted">
                            <i class="fas fa-map-marker-alt me-1"></i>${habit.place}
                        </small>
                    </div>
                    
                    <div class="mb-2">
                        <span class="time-badge">
                            <i class="fas fa-clock me-1"></i>${habit.time}
                        </span>
                        <span class="badge bg-secondary ms-2">
                            ${habit.execution_time} сек
                        </span>
                    </div>
                    
                    <div class="mb-2">
                        <small class="text-muted">
                            Периодичность: каждые ${habit.periodicity} ${getDaysWord(habit.periodicity)}
                        </small>
                    </div>
                    
                    ${habit.reward ? `
                        <div class="mb-2">
                            <small class="text-success">
                                <i class="fas fa-gift me-1"></i>Вознаграждение: ${habit.reward}
                            </small>
                        </div>
                    ` : ''}
                    
                    ${habit.related_habit ? `
                        <div class="mb-2">
                            <small class="text-info">
                                <i class="fas fa-link me-1"></i>Связанная привычка
                            </small>
                        </div>
                    ` : ''}
                    
                    <div class="d-flex justify-content-between align-items-center mt-3">
                        <div>
                            ${habit.is_pleasant ? 
                                '<span class="badge bg-success">Приятная</span>' : 
                                '<span class="badge bg-primary">Полезная</span>'
                            }
                        </div>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-primary" onclick="editHabit(${habit.id})">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-outline-danger" onclick="deleteHabit(${habit.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function renderPublicHabits(habits, containerId) {
    const container = document.getElementById(containerId);
    
    if (habits.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="fas fa-globe fa-3x text-muted mb-3"></i>
                <h5 class="text-muted">Нет публичных привычек</h5>
            </div>
        `;
        return;
    }
    
    container.innerHTML = habits.map(habit => `
        <div class="col-md-6 col-lg-4">
            <div class="card habit-card">
                <div class="card-body">
                    <h6 class="card-title">${habit.action}</h6>
                    
                    <div class="mb-2">
                        <small class="text-muted">
                            <i class="fas fa-user me-1"></i>Автор: ${habit.user}
                        </small>
                    </div>
                    
                    <div class="mb-2">
                        <small class="text-muted">
                            <i class="fas fa-map-marker-alt me-1"></i>${habit.place}
                        </small>
                    </div>
                    
                    <div class="mb-2">
                        <span class="time-badge">
                            <i class="fas fa-clock me-1"></i>${habit.time}
                        </span>
                        <span class="badge bg-secondary ms-2">
                            ${habit.execution_time} сек
                        </span>
                    </div>
                    
                    <div class="mb-2">
                        <small class="text-muted">
                            Периодичность: каждые ${habit.periodicity} ${getDaysWord(habit.periodicity)}
                        </small>
                    </div>
                    
                    <div class="text-end">
                        <button class="btn btn-outline-success btn-sm" onclick="copyHabit(${JSON.stringify(habit).replace(/"/g, '&quot;')})">
                            <i class="fas fa-copy me-1"></i>Скопировать
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function renderPagination(data, containerId, loadFunction) {
    const container = document.getElementById(containerId);
    
    if (!data.next && !data.previous) {
        container.innerHTML = '';
        return;
    }
    
    const currentPage = data.next ? 
        parseInt(new URL(data.next).searchParams.get('page')) - 1 : 
        parseInt(new URL(data.previous).searchParams.get('page')) + 1;
    
    let paginationHTML = '<nav><ul class="pagination">';
    
    if (data.previous) {
        paginationHTML += `
            <li class="page-item">
                <button class="page-link" onclick="${loadFunction.name}(${currentPage - 1})">Предыдущая</button>
            </li>
        `;
    }
    
    paginationHTML += `
        <li class="page-item active">
            <span class="page-link">${currentPage}</span>
        </li>
    `;
    
    if (data.next) {
        paginationHTML += `
            <li class="page-item">
                <button class="page-link" onclick="${loadFunction.name}(${currentPage + 1})">Следующая</button>
            </li>
        `;
    }
    
    paginationHTML += '</ul></nav>';
    container.innerHTML = paginationHTML;
}

function togglePleasantHabit() {
    const isPleasant = document.getElementById('habit-is-pleasant').checked;
    const rewardSection = document.getElementById('reward-section');
    
    if (isPleasant) {
        rewardSection.style.display = 'none';
        document.getElementById('habit-reward').value = '';
        document.getElementById('habit-related').value = '';
    } else {
        rewardSection.style.display = 'block';
    }
}

async function addHabit(event) {
    event.preventDefault();
    showLoading();
    
    const formData = {
        action: document.getElementById('habit-action').value,
        place: document.getElementById('habit-place').value,
        time: document.getElementById('habit-time').value,
        execution_time: parseInt(document.getElementById('habit-execution-time').value),
        periodicity: parseInt(document.getElementById('habit-periodicity').value),
        is_pleasant: document.getElementById('habit-is-pleasant').checked,
        is_public: document.getElementById('habit-is-public').checked,
        reward: document.getElementById('habit-reward').value || null,
        related_habit: document.getElementById('habit-related').value || null
    };
    
    try {
        await apiRequest('/habits/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        showAlert('Привычка создана!', 'success');
        
        // Reset form
        event.target.reset();
        
        // Show my habits
        showMyHabits();
        updateStats();
        
    } catch (error) {
        showAlert(error.message, 'danger');
        hideLoading();
    }
}

async function deleteHabit(habitId) {
    if (!confirm('Вы уверены, что хотите удалить эту привычку?')) {
        return;
    }
    
    try {
        await apiRequest(`/habits/${habitId}/`, {
            method: 'DELETE'
        });
        
        showAlert('Привычка удалена!', 'success');
        loadUserHabits();
        updateStats();
        
    } catch (error) {
        showAlert(error.message, 'danger');
    }
}

function copyHabit(habit) {
    // Fill the form with habit data
    document.getElementById('habit-action').value = habit.action;
    document.getElementById('habit-place').value = habit.place;
    document.getElementById('habit-time').value = habit.time;
    document.getElementById('habit-execution-time').value = habit.execution_time;
    document.getElementById('habit-periodicity').value = habit.periodicity;
    
    showAddHabit();
    showAlert('Данные привычки скопированы в форму!', 'info');
}

function filterHabits(filter) {
    currentFilter = filter;
    // Update active button
    document.querySelectorAll('.btn-group .btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // This would need to be implemented with API filtering
    loadUserHabits();
}

async function updateStats() {
    try {
        const habits = await apiRequest('/habits/');
        const allHabits = habits.results || [];
        
        const totalHabits = allHabits.length;
        const pleasantHabits = allHabits.filter(h => h.is_pleasant).length;
        const publicHabits = allHabits.filter(h => h.is_public).length;
        const avgTime = totalHabits > 0 ? 
            Math.round(allHabits.reduce((sum, h) => sum + h.execution_time, 0) / totalHabits / 60) : 0;
        
        document.getElementById('total-habits').textContent = totalHabits;
        document.getElementById('pleasant-habits').textContent = pleasantHabits;
        document.getElementById('public-habits').textContent = publicHabits;
        document.getElementById('avg-time').textContent = avgTime;
        
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Utility functions
function getDaysWord(days) {
    if (days === 1) return 'день';
    if (days >= 2 && days <= 4) return 'дня';
    return 'дней';
}

function editHabit(habitId) {
    showAlert('Функция редактирования будет добавлена в следующей версии', 'info');
}

