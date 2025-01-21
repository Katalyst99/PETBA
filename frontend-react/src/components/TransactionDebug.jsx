import React, { useState } from 'react';

const TransactionDebug = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const testTransaction = {
    type: 'expense',
    amount: 50.00,
    description: 'Test transaction',
    category: 'Food & Dining',
    date: new Date().toISOString().split('T')[0]
  };

  const handleTest = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/transactions/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(testTransaction)
      });
      
      const data = await response.json();
      setResult({
        status: response.status,
        data: data,
        sentData: testTransaction,
        headers: Object.fromEntries(response.headers)
      });
    } catch (error) {
      setResult({
        error: error.message,
        sentData: testTransaction
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold mb-4">Transaction Debug Tool</h2>
      <div className="space-y-4">
        <div>
          <h3 className="font-bold mb-2">Test Transaction Data:</h3>
          <pre className="bg-gray-100 p-4 rounded overflow-auto">
            {JSON.stringify(testTransaction, null, 2)}
          </pre>
        </div>
        
        <button
          onClick={handleTest}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-blue-300"
        >
          {loading ? 'Testing...' : 'Test Transaction'}
        </button>

        {result && (
          <div>
            <h3 className="font-bold mb-2">Result:</h3>
            <pre className="bg-gray-100 p-4 rounded overflow-auto text-sm">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default TransactionDebug;
