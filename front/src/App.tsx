import React from 'react';
import './index.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom'; // Import necessary components

import EbookForm from './EbookForm';
import Navbar from './Navbar'
import HeroSection from './HeroSection';
import About from './About'; // Adjust the path based on your file structure
import LoginPage from './loginForm';
import RegisterForm from './RegistrationForm';
import Dashboard from './Dashboard';
import ContactForm from './ContactForm'



function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={
            <>
              <HeroSection />
              <div className="container mx-auto px-4">
              </div>
              <Dashboard/>
              <About />
            </>
          } />
          {/* Define the route for the LoginPage */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/contact" element={<ContactForm />} />
          {/* <Route path="/stripe" element={<Stripe />} /> */}





        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
