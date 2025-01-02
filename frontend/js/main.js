import { register, login, fetchSummary, fetchTransactions, setBudget } from './api.js';
import { populateSummary, populateTransactions } from './ui.js';

document.addEventListener('DOMContentLoaded', () => {
    populateSummary();
    populateTransactions();
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const resp = await register(email, password);
    alert(resp.message || resp.error);
});

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const resp = await login(email, password);
    if (resp.access_token) {
        alert('Login successful!');
        loadSummary();
    } else {
        alert(resp.error);
    }
});

document.getElementById('budgetForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const month = document.getElementById('budgetMonth').value;
    const limitAmount = document.getElementById('budgetAmount').value;
    const resp = await setBudget(month, limitAmount);
    alert(resp.message || resp.error);
});

async function loadSummary() {
    const month = 'January';
    const summary = await fetchSummary(month);
    if (summary) {
        console.log('Summary:', summary);
    }
}
