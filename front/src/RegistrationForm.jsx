import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // Remember to import Link from react-router-dom
import { GoogleLogin } from 'react-google-login';


function RegisterForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleGoogleSuccess = async (response) => {
    const tokenBlob = new Blob([JSON.stringify({ token: response.tokenId }, null, 2)], { type: 'application/json' });
    const options = {
      method: 'POST',
      body: tokenBlob,
      cache: 'default',
      headers: {
        'Content-Type': 'application/json',
      },
    };

    try {
      const res = await fetch('http://localhost:5000/auth/google', options);
      const data = await res.json();
      // Assuming your backend sends back a success message upon successful registration
      if (data.message === 'User registered successfully') {
        navigate('/dashboard'); // Or wherever you want to redirect the user
      } else {
        console.error('Registration with Google failed:', data);
        // Optionally set an error message in your state and display it
      }
    } catch (error) {
      console.error('Error during Google auth:', error);
      // Handle error (e.g., show notification to the user)
    }
  };

  const handleGoogleFailure = (response) => {
    console.log('Google failure response:', response);
    // Handle failure (you might want to notify the user that Google login failed)
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      alert("Passwords don't match.");
      return;
    }
    
    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      const data = await response.json();
      if (response.ok) {
        console.log('Registration Success:', data);
        setSuccessMessage('Registration successful! Redirecting to login...');
        setTimeout(() => navigate('/login'), 3000);

      } else {
        alert('Registration Failed: ' + (data.error || 'Unknown Error'));
      }
    } catch (error) {
      console.error('Registration Request Failed:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div>
      {successMessage && (
        <div className="fixed top-1/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-green-100 border border-green-400 text-green-700 px-2 py-2 rounded max-w-xs text-center text-sm" role="alert">
          <span className="block sm:inline">{successMessage}</span>
        </div>
      )}  
      <form onSubmit={handleSubmit} className="space-y-6 bg-white p-8 rounded-lg shadow-lg max-w-md mx-auto mt-12">
      <h2 className="text-center text-2xl font-extrabold text-gray-900">Create your account</h2>
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
        <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">Confirm Password</label>
        <input
          type="password"
          name="confirmPassword"
          id="confirmPassword"
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm transition duration-300 ease-in-out"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>
      <div>
        <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 ease-in-out">
          Register
        </button>
      </div>
      <div className="text-center">
        <p className="text-sm">
          Already have an account?{' '}
          <Link to="/login" className="text-indigo-600 hover:text-indigo-500 transition duration-300 ease-in-out">
            Sign in
          </Link>
        </p>
      </div>
      </form>
      <div className="text-center mt-4">
        <GoogleLogin
          clientId="133030240054-rirtghd7el0m92gocug6imbkcrvdf658.apps.googleusercontent.com" // Replace with your actual client ID
          buttonText="Register with Google"
          onSuccess={handleGoogleSuccess}
          onFailure={handleGoogleFailure}
          cookiePolicy={'single_host_origin'}
        />
      </div>
    </div>

  );
}

export default RegisterForm;
