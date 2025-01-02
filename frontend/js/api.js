const API_BASE_URL = 'http://127.0.0.1:5000';

export async function register(email, password) {
    try {
        const resp = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        return await resp.json();
    } catch (error) {
        console.error('Registration failed:', error);
        return null;
    }
}

export async function login(email, password) {
    try {
        const resp = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });
        const data = await resp.json();
        if (resp.ok) {
            localStorage.setItem('token', data.access_token);
        }
        return data;
    } catch (error) {
        console.error('Login failed:', error);
        return null;
    }
}

function getToken() {
    return localStorage.getItem('token');
}

export async function fetchSummary(month) {
    try {
        const resp = await fetch(`${API_BASE_URL}/summary/get?month=${month}`, {
            headers: { Authorization: `Bearer ${getToken()}` },
        });
        return await resp.json();
    } catch (error) {
        console.error('Failed to fetch summary:', error);
        return null;
    }
}

export async function fetchTransactions() {
    try {
        const resp = await fetch(`${API_BASE_URL}/transactions/get`, {
            headers: { Authorization: `Bearer ${getToken()}` },
        });
        if (!resp.ok) {
            throw new Error(`Error: ${resp.status}`);
        }
        return await resp.json();
    } catch (error) {
        console.error('Failed to fetch transactions:', error);
        return null;
    }
}

export async function setBudget(month, limitAmount) {
    try {
        const resp = await fetch(`${API_BASE_URL}/budgets/set`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${getToken()}`,
            },
            body: JSON.stringify({ month, limit_amount: limitAmount }),
        });
        return await resp.json();
    } catch (error) {
        console.error('Failed to set budget:', error);
        return null;
    }
}

export async function addTransaction(amount, category, type) {
    try {
        const resp = await fetch(`${API_BASE_URL}/transactions/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${getToken()}`,
            },
            body: JSON.stringify({ amount, category, type }),
        });
        return await resp.json();
    } catch (error) {
        console.error('Failed to add transaction:', error);
        return null;
    }
}
