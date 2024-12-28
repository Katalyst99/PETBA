const API_BASE_URL = 'http://127.0.0.1:5000'; // Update this with your backend URL if different

async function summaryFetch() {
    try {
        const resp = await fetch(`${API_BASE_URL}/api/v1/summary`);
        if (!resp.ok) {
            throw new Error(`Error: ${resp.status}`);
        }
        const data = await resp.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch summary:', error);
    }
}

async function transactionsFetch() {
    try {
        const resp = await fetch(`${API_BASE_URL}/api/v1/transactions`);
        if (!resp.ok) {
            throw new Error(`Error: ${response.status}`);
        }
        const data = await resp.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch transactions:', error);
    }
}
