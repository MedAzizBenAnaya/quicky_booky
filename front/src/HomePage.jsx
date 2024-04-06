// src/HomePage.jsx
import React from 'react';

const HomePage = () => {
    return (
        <div className="min-h-screen bg-gray-100 p-8">
            <header className="flex justify-between items-center py-4">

            </header>
            <main className="flex flex-col items-center">
                <section className="mt-10 mb-6 text-center">
                    <h1 className="text-5xl font-bold mb-4">Create captivating books on any topic</h1>
                    <p className="max-w-2xl mb-6">Quickly Booky's AI-powered e-book generation tool allows you to effortlessly create high-quality books about any topic you like. With our advanced technology, you can turn your ideas into engaging content that captivates readers.</p>
                    <div className="flex justify-center gap-4">
                        <button className="bg-black text-white px-6 py-2 rounded shadow-lg hover:bg-gray-800">Get Started</button>
                        <button className="bg-transparent px-6 py-2 rounded shadow-lg border-2 border-black hover:bg-gray-800 hover:text-white hover:border-transparent">Learn More</button>
                    </div>
                </section>
                <section className="w-full grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {/* Placeholder for images or content */}
                    {[...Array(8)].map((_, i) => (
                        <div key={i} className="bg-gray-300 aspect-w-1 aspect-h-1 rounded-lg shadow-md flex justify-center items-center">
                            <span className="text-gray-500 text-4xl">+</span>
                        </div>
                    ))}
                </section>
            </main>
        </div>
    );
};

export default HomePage;
