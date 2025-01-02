export async function populateSummary() {
    const summary = await fetchSummary();
    if (summary) {
        const summaryContainer = document.getElementById('summary');
        summaryContainer.innerHTML = `
            <h2>Summary</h2>
            <p><strong>Total Income:</strong> $${summary.total_income.toFixed(2)}</p>
            <p><strong>Total Expenses:</strong> $${summary.total_expenses.toFixed(2)}</p>
            <p><strong>Net Savings:</strong> $${summary.net_savings.toFixed(2)}</p>
        `;
    }
}

export async function populateTransactions() {
    const transactions = await fetchTransactions();
    if (transactions) {
        const transactionsContainer = document.getElementById('transactions');
        transactionsContainer.innerHTML = `
            <h2>Transactions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Category</th>
                        <th>Amount</th>
                    </tr>
                </thead>
                <tbody>
                    ${transactions.map(tx => `
                        <tr>
                            <td>${tx.date}</td>
                            <td>${tx.category}</td>
                            <td>$${tx.amount.toFixed(2)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }
}

