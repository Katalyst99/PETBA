import React, { useState } from 'react';

export function PETBAApp() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  const handleLogin = async (credentials) => {
    // TODO: Implement login logic
    console.log('Login attempted with:', credentials);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {!isLoggedIn ? (
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-center mb-4">
            Welcome to PETBA
          </h1>
          <p className="text-center text-gray-600 mb-6">
            Personal Expense Tracking and Budget Application
          </p>
          {/* Login form will go here */}
          <div className="text-center">
            <button 
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
              onClick={() => setIsLoggedIn(true)}>
              Login
            </button>
          </div>
        </div>
      ) : (
        <div>
          <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
          <p>Welcome back!</p>
        </div>
      )}
    </div>
  );
}
