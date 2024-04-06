import React, { useState } from 'react';

// Adjusted EbookForm to receive formData and setFormData via props
const EbookForm = ({ formData, setFormData, onGenerateSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [progress, setProgress] = useState(0);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };

  const simulateProgress = () => {
    const incrementAmount = 0.5;
    const intervalDuration = 500;
  
    const interval = setInterval(() => {
      setProgress((prevProgress) => {
        const nextProgress = prevProgress + incrementAmount;
        if (nextProgress >= 100) {
          clearInterval(interval);
          return 100;
        }
        return nextProgress;
      });
    }, intervalDuration);
  
    return () => clearInterval(interval);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // setIsLoading(true);
    // setProgress(0);
    setMessage('');
    onGenerateSuccess(); 

    const cleanupProgress = simulateProgress();
  
    try {
      const response = await fetch('http://localhost:5000/generate_book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.setAttribute('download', 'eBook.pdf');
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
        setMessage('eBook generated and downloaded successfully.');
        setProgress(100);
      } else {
        setMessage('Failed to generate eBook. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting form data:', error);
      setMessage('An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
      cleanupProgress();
    }
  };

  
return (
  <div className="space-y-6">
    <h2 className="text-center text-3xl font-extrabold text-gray-900">Quicky Booky Generator</h2>
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-gray-800 text-sm font-medium mb-1">
          Ebook Title
        </label>
        <input
          type="text"
          name="title"
          id="title"
          value={formData.title}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-black text-gray-700 placeholder-gray-400"
          placeholder="Enter title"
          required
        />
      </div>

      <div>
        <label htmlFor="topic" className="block text-gray-800 text-sm font-medium mb-1">
          Topic
        </label>
        <input
          type="text"
          name="topic"
          id="topic"
          value={formData.topic}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-black text-gray-700 placeholder-gray-400"
          placeholder="What's it about?"
          required
        />
      </div>

      <div>
        <label htmlFor="gender" className="block text-gray-800 text-sm font-medium mb-1">
          Gender
        </label>
        <select
          name="gender"
          id="gender"
          value={formData.gender}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-black text-gray-700"
          required
        >
          <option value="">Select your gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div>
        <label htmlFor="age" className="block text-gray-800 text-sm font-medium mb-1">
          Age
        </label>
        <input
          type="number"
          name="age"
          id="age"
          value={formData.age}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-black text-gray-700 placeholder-gray-400"
          placeholder="Your age"
          required
        />
      </div>

      <div>
        <label htmlFor="additionalInfo" className="block text-gray-800 text-sm font-medium mb-1">
          Additional Info
        </label>
        <textarea
          name="additionalInfo"
          id="additionalInfo"
          value={formData.additionalInfo}
          onChange={handleChange}
          className="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-black text-gray-700 placeholder-gray-400"
          placeholder="Anything else you want to add?"
          rows="3"
        ></textarea>
      </div>

      <button
        type="submit"
        className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black transition duration-300 ease-in-out"
        disabled={isLoading}
      >
        {isLoading ? 'Generating...' : 'Generate Preview'}
      </button>
    </form>

    {isLoading && (
      <div className="mt-2">
        <p className="text-center text-gray-600">Generating your eBook preview...</p>
        <div className="w-full bg-gray-200 rounded h-2 overflow-hidden">
          <div className="bg-green-500 h-2 rounded transition-all duration-500 ease-in-out" style={{ width: `${progress}%` }}></div>
        </div>
      </div>
    )}

    {message && <p className="text-center text-gray-600 mt-2">{message}</p>}
  </div>
);

  
};

export default EbookForm;
