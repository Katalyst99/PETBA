import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { TransactionForm } from './TransactionForm';
import TransactionDebug from './TransactionDebug';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';

const API_BASE_URL = 'http://localhost:5000';

export function Dashboard() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [showTransactionForm, setShowTransactionForm] = useState(false);
  const [chartData, setChartData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [summary, setSummary] = useState({
    totalIncome: 0,
    totalExpenses: 0,
    balance: 0
  });
  const [error, setError] = useState(null); // New state for errors

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }
    fetchDashboardData(token);
  }, [navigate]);

  const fetchDashboardData = async (token) => {
    setError(null);
    try {
      const headers = {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      };

      // Fetch transactions
      const transResponse = await fetch(`${API_BASE_URL}/transactions/list`, {
        headers,
        credentials: 'include'
      });

      if (transResponse.status === 401) {
        // Token expired or invalid
        localStorage.removeItem('token');
        navigate('/login');
        return;
      }

      if (!transResponse.ok) {
        const errorData = await transResponse.json();
        throw new Error(errorData.error || transResponse.statusText);
      }

      const transData = await transResponse.json();
      setTransactions(transData);

      // Fetch budgets with correct URL
      const budgetResponse = await fetch(`${API_BASE_URL}/budgets/list`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!budgetResponse.ok) {
        throw new Error(`Failed to fetch budgets: ${budgetResponse.statusText}`);
      }
      const budgetData = await budgetResponse.json();
      setBudgets(budgetData);

      // Fetch summary with correct URL
      const summaryResponse = await fetch(`${API_BASE_URL}/summary`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!summaryResponse.ok) {
        throw new Error(`Failed to fetch summary: ${summaryResponse.statusText}`);
      }
      const summaryData = await summaryResponse.json();
      setSummary(summaryData);

      // Process chart data
      processChartData(transData);
    } catch (err) {
      console.error('Dashboard data fetch error:', err);
      setError(err.message);
    }
  };

  const handleTransactionAdded = async (newTransaction) => {
    const token = localStorage.getItem('token');
    if (token) {
      await fetchDashboardData(token); // Refresh all data after new transaction
    }
  };

  const processChartData = (transactions) => {
    const categoryTotals = transactions.reduce((acc, trans) => {
      const category = trans.category || 'Uncategorized';
      acc[category] = (acc[category] || 0) + Math.abs(trans.amount);
      return acc;
    }, {});

    const pieData = Object.entries(categoryTotals).map(([name, value]) => ({
      name,
      value
    }));

    setCategoryData(pieData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

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
        {error && ( // Display error message if there's an error
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded">
            <p>{error}</p>
          </div>
        )}

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

        {/* Add Transaction Button */}
	<div className="mb-8">
  	  <button
            onClick={() => setShowTransactionForm(!showTransactionForm)}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
    	    {showTransactionForm ? 'Hide Form' : 'Add Transaction'}
  	  </button>
	</div>

        {/* Debug Tool - Remove in production */}
        <div className="mb-8">
          <TransactionDebug />
        </div>

	{/* Transaction Form */}
        {showTransactionForm && (
          <div className="mb-8">
            <TransactionForm onTransactionAdded={handleTransactionAdded} />
          </div>
        )}

	{/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Spending by Category */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Spending by Category</h2>
            {categoryData.length > 0 ? (
              <PieChart width={400} height={300}>
                <Pie
                  data={categoryData}
                  cx={200}
                  cy={150}
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            ) : (
              <p className="text-gray-500">No data available</p>
            )}
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
                        <td
                          className={`text-right py-2 ${
                            transaction.amount < 0 ? 'text-red-600' : 'text-green-600'
                          }`}
                        >
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
                            budget.spent / budget.limit > 0.9
                              ? 'bg-red-600'
                              : budget.spent / budget.limit > 0.7
                              ? 'bg-yellow-600'
                              : 'bg-green-600'
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
          </div>
      </main>
    </div>
  );
}
