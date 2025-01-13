import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [summary, setSummary] = useState({
    totalIncome: 0,
    totalExpenses: 0,
    balance: 0
  });

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    // Fetch user data and financial information
    fetchDashboardData(token);
  }, [navigate]);

  const fetchDashboardData = async (token) => {
    try {
      // Fetch transactions
      const transResponse = await fetch('http://localhost:5000/transactions', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (transResponse.ok) {
        const transData = await transResponse.json();
        setTransactions(transData.slice(0, 5)); // Show only latest 5 transactions
      }

      // Fetch budgets
      const budgetResponse = await fetch('http://localhost:5000/budgets', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (budgetResponse.ok) {
        const budgetData = await budgetResponse.json();
        setBudgets(budgetData);
      }

      // Fetch summary
      const summaryResponse = await fetch('http://localhost:5000/summary', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (summaryResponse.ok) {
        const summaryData = await summaryResponse.json();
        setSummary(summaryData);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex justify-between items-center py-4">
            <h1 className="text-xl font-semibold text-gray-800">PETBA Dashboard</h1>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Financial Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Total Income</h3>
            <p className="text-2xl text-green-600">${summary.totalIncome.toFixed(2)}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Total Expenses</h3>
            <p className="text-2xl text-red-600">${summary.totalExpenses.toFixed(2)}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">Current Balance</h3>
            <p className="text-2xl text-blue-600">${summary.balance.toFixed(2)}</p>
          </div>
        </div>

        {/* Recent Transactions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
          {transactions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2">Date</th>
                    <th className="text-left py-2">Description</th>
                    <th className="text-right py-2">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map((transaction, index) => (
                    <tr key={index} className="border-b">
                      <td className="py-2">{new Date(transaction.date).toLocaleDateString()}</td>
                      <td className="py-2">{transaction.description}</td>
                      <td className={`text-right py-2 ${
                        transaction.amount < 0 ? 'text-red-600' : 'text-green-600'
                      }`}>
                        ${Math.abs(transaction.amount).toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="text-gray-500">No recent transactions</p>
          )}
        </div>

        {/* Budget Overview */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Budget Overview</h2>
          {budgets.length > 0 ? (
            <div className="space-y-4">
              {budgets.map((budget, index) => (
                <div key={index} className="border-b pb-4">
                  <div className="flex justify-between mb-2">
                    <span className="font-medium">{budget.category}</span>
                    <span>{`$${budget.spent.toFixed(2)} / $${budget.limit.toFixed(2)}`}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className={`h-2.5 rounded-full ${
                        (budget.spent / budget.limit) > 0.9 ? 'bg-red-600' :
                        (budget.spent / budget.limit) > 0.7 ? 'bg-yellow-600' :
                        'bg-green-600'
                      }`}
                      style={{ width: `${Math.min((budget.spent / budget.limit) * 100, 100)}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No budgets set</p>
          )}
        </div>
      </main>
    </div>
  );
}
