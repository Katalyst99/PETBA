import React, { useState } from 'react';

export function TransactionForm({ onTransactionAdded }) {
  const [formData, setFormData] = useState({
    description: '',
    amount: '',
    category: '',
    date: new Date().toISOString().split('T')[0],
    type: 'expense' // or 'income'
  });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const categories = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Bills & Utilities',
    'Entertainment',
    'Health',
    'Income',
    'Other'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      const token = localStorage.getItem('token');
      const amount = formData.type === 'expense' 
        ? -Math.abs(parseFloat(formData.amount)) 
        : Math.abs(parseFloat(formData.amount));

      const response = await fetch('http://localhost:5000/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          ...formData,
          amount
        })
      });

      const data = await response.json();

      if (response.ok) {
        setFormData({
          description: '',
          amount: '',
          category: '',
          date: new Date().toISOString().split('T')[0],
          type: 'expense'
        });
        onTransactionAdded(data);
      } else {
        setError(data.message || 'Failed to add transaction');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Add New Transaction</h2>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="flex space-x-4">
          <div className="flex-1">
            <label className="block text-gray-700 mb-2" htmlFor="type">
              Type
            </label>
            <select
              id="type"
              className="w-full p-2 border rounded"
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              required
            >
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
          </div>
          
          <div className="flex-1">
            <label className="block text-gray-700 mb-2" htmlFor="amount">
              Amount
            </label>
            <input
              type="number"
              id="amount"
              step="0.01"
              min="0"
              className="w-full p-2 border rounded"
              value={formData.amount}
              onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-gray-700 mb-2" htmlFor="description">
            Description
          </label>
          <input
            type="text"
            id="description"
            className="w-full p-2 border rounded"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            required
          />
        </div>

        <div className="flex space-x-4">
          <div className="flex-1">
            <label className="block text-gray-700 mb-2" htmlFor="category">
              Category
            </label>
            <select
              id="category"
              className="w-full p-2 border rounded"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              required
            >
              <option value="">Select a category</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
          
          <div className="flex-1">
            <label className="block text-gray-700 mb-2" htmlFor="date">
              Date
            </label>
            <input
              type="date"
              id="date"
              className="w-full p-2 border rounded"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              required
            />
          </div>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Adding...' : 'Add Transaction'}
        </button>
      </form>
    </div>
  );
}
