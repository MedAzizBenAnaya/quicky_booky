import React from 'react';

const PricingSection = () => {
  const price = 3; // Price per book generation

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-8 flex justify-center items-center">
      <div className="text-center">
        <p className="text-sm uppercase text-gray-500 font-semibold">Simplified</p>
        <h2 className="text-4xl font-extrabold my-4">Pricing Plans</h2>
        <p className="mb-8">Choose the plan that suits your needs.</p>
        <div className="inline-block">
          <div className="border rounded-lg px-6 py-8 shadow-lg max-w-sm mx-auto">
            <h3 className="text-lg font-semibold border-b pb-4">Basic Plan</h3>
            <div className="my-6">
              <p className="text-5xl font-bold">€{price}<span className="text-3xl">/book</span></p>
            </div>
            <ul className="text-left mb-8">
              <li className="flex items-center mb-2">
                {/* ... */}
                High quality book generation
              </li>
              {/* ... Repeat for other features */}
            </ul>
            <button className="bg-black text-white w-full py-2 rounded hover:bg-gray-800 transition duration-300">
              Get started
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingSection;
