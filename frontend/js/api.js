const API_BASE_URL = 'http://127.0.0.1:5000';

export async function fetchsummary() {
    try {
        const resp = await fetch(`${API_BASE_URL}/api/v1/summary`);
        if (!resp.ok) {
            throw new Error(`Error: ${resp.status}`);
        }
        return await resp.json();
    } catch (error) {
        console.error('Failed to fetch summary:', error);
        return null;
    }
}

export async function fetchTransactions() {
    try {
        const resp = await fetch(`${API_BASE_URL}/api/v1/transactions`);
        if (!resp.ok) {
            throw new Error(`Error: ${resp.status}`);
        }
        return await resp.json();
    } catch (error) {
        console.error('Failed to fetch transactions:', error);
        return null;
    }
}

