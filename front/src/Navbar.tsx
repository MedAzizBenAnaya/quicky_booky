import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import BookIcon from '../svgs/book.svg';

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between p-5">
      <div className="flex items-center text-lg font-sans-serif navbar-brand">
        <img src={BookIcon} alt="Book Icon" className="h-6 w-6 mr-2"/>
                <Link to="/">Quicky Booky</Link>

      </div>

      <div className="flex space-x-4">
        {/* Replace <a> tags with <Link> for internal navigation */}
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/login" className="nav-link">Login</Link>
        {/* External link remains unchanged */}
        <a href="https://30be44-dc.myshopify.com" className="nav-link">Store</a>
        <Link to="/contact" className="nav-link">Contact</Link>
      </div>
    </nav>
  );
};

export default Navbar;
