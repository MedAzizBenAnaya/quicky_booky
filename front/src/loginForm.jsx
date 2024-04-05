import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate for redirection

function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loginSuccess, setLoginSuccess] = useState(false); // State for login success message
  const navigate = useNavigate(); // Initialize navigate for later redirection

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (response.ok) {
        console.log('Login Success:', data);
        setLoginSuccess(true); // Indicate login success
        setTimeout(() => {
          setLoginSuccess(false); // Reset login success message state
          navigate('/dashboard'); // Redirect or navigate to another route
        }, 3000); // Show success message for 3 seconds
      } else {
        console.error('Login Failed:', data.error);
        // Handle login failure here (e.g., showing an error message)
      }
    } catch (error) {
      console.error('Login Request Failed:', error);
      // Handle error here
    }
  };

  

  return (
    <div>
      {loginSuccess && (
        <div className="fixed top-1/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-green-100 border border-green-400 text-green-700 px-2 py-2 rounded max-w-xs text-center text-sm" role="alert">
          <span>Login successful! Redirecting...</span>
        </div>
      )}      

      <form onSubmit={handleSubmit} className="space-y-6 bg-white p-8 rounded-lg shadow-lg max-w-md mx-auto mt-12">
    <h2 className="text-center text-2xl font-extrabold text-gray-900">Sign in to your account</h2>
    <div>
      <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email address</label>
      <input
        type="email"
        name="email"
        id="email"
        required
        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-300 ease-in-out"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
    </div>
    <div>
      <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
      <input
        type="password"
        name="password"
        id="password"
        required
        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-300 ease-in-out"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
    </div>
    <div>
      <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 ease-in-out">
        Sign in
      </button>
    </div>
    <div className="text-center">
      <p className="text-sm">
        Don't have an account?{' '}
        <Link to="/register" className="text-indigo-600 hover:text-indigo-500 transition duration-300 ease-in-out">
          Register
        </Link>
      </p>
    </div>
  </form></div>

  );
}

export default LoginForm;
