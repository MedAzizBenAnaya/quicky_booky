import React from 'react';
import placeholderImageUrl from '../public/place_holder.jpg'

import BookIcon1 from '../svgs/book-sparkles-svgrepo-com.svg';
import BookIcon2 from '../svgs/book-section-svgrepo-com.svg';
import BookIcon3 from '../svgs/book-user-svgrepo-com.svg';

const FeatureSection = () => {
  return (
    <div className="bg-gray-100 py-12 px-8">
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
        <div>
          <p className="text-sm uppercase text-gray-500 font-semibold mb-3">Revolutionary</p>
          <h2 className="text-3xl font-extrabold mb-4">Unleash the Power of AI Book Generation</h2>
          <p className="text-sm mb-6">Highlight the AI technology behind Quicky Booky and its ability to generate high-quality e-books on any topic.</p>
          <ul className="text-sm pl-6 mb-6">
            <li className="flex items-center mb-2">
              <img src={BookIcon1} alt="Generate Books" className="w-5 h-5 mr-2" />
              Generate E-books on Any Topic Imaginable
            </li>
            <li className="flex items-center mb-2">
              <img src={BookIcon2} alt="High-Quality Content" className="w-5 h-5 mr-2" />
              High-Quality Content at Your Fingertips
            </li>
            <li className="flex items-center mb-2">
              <img src={BookIcon3} alt="Create E-books" className="w-5 h-5 mr-2" />
              Effortlessly Create Professional E-books
            </li>
          </ul>
          <div className="flex gap-4">
            <button className="bg-black text-white text-sm py-2 px-4 rounded hover:bg-gray-800 transition duration-300">Learn More</button>
            <button className="bg-transparent text-sm py-2 px-4 rounded border border-black hover:bg-black hover:text-white transition duration-300">Sign Up</button>
          </div>
        </div>
        <div className="flex justify-center">
          <img src={placeholderImageUrl} alt="Placeholder" className="w-full max-w-md object-cover rounded-lg shadow-md" />
        </div>
      </div>
    </div>
  );
};

export default FeatureSection;
