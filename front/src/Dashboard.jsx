import React, {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import EbookForm from './EbookForm';
import placeholderImageUrl from '../public/place_holder.jpg'


function Dashboard() {
  const navigate = useNavigate();
  const [coverUrl, setCoverUrl] = useState('');
  const [isPreviewGenerated, setIsPreviewGenerated] = useState(false);


  // Added formData and setFormData states to Dashboard
  const [formData, setFormData] = useState({
    title: '',
    topic: '',
    gender: '',
    age: '',
    additionalInfo: '',
  });


  const handleGenerateSuccess = () => {
    fetchCover();
    setIsPreviewGenerated(true);
  };

  useEffect(() => {
    const savedState = sessionStorage.getItem('dashboardState');
    if (savedState) {
      const { formData, coverUrl, isPreviewGenerated } = JSON.parse(savedState);

      setFormData(formData);
      setCoverUrl(coverUrl);
      setIsPreviewGenerated(isPreviewGenerated);

      const coverImageData = sessionStorage.getItem('coverImageData');

      if (coverImageData) {
        setCoverUrl(coverImageData);
        sessionStorage.removeItem('coverImageData'); // Clear the stored image data
      }
      sessionStorage.removeItem('dashboardState'); // Clear saved state

      const sessionId = sessionStorage.getItem('paymentSessionId');
      if (sessionId) {
        checkBookReadyAndDownload(sessionId);
      }else {console.error('Session ID not found');}


    }
  }, []);



  const handlePayment = async () => {
    
    try {
      const response = await fetch('http://localhost:5000/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({    metadata: { ...formData },
        }),
      });

  
      if (!response.ok) {
        throw new Error('Failed to initiate checkout session');
      }

  
      const session = await response.json();

      const sessionId =  session.id


      sessionStorage.setItem('paymentSessionId', sessionId );
      console.log('Saved session ID:', sessionId);
      
      sessionStorage.setItem('dashboardState', JSON.stringify({
        formData,
        coverUrl,
        isPreviewGenerated
        }));

      window.location = session.url;
    } catch (error) {
      console.error('Payment initiation failed:', error);
      alert('Payment initiation failed. Please try again.');
    }
  };

  const checkBookReadyAndDownload = async (sessionId) => {
    console.log('Retrieved session ID:', sessionId); // Debugging
    const checkUrl = `http://localhost:5000/check_book_ready/${sessionId}`;

    const intervalId = setInterval(async () => {
      try {
        const response = await fetch(checkUrl);
        if (!response.ok) throw new Error('Failed to check book readiness');

        const { ready, bookId } = await response.json();
        if (ready) {
          clearInterval(intervalId);
          downloadBook(bookId); // Trigger the download
          sessionStorage.removeItem('paymentSessionId'); // Cleanup
        }
      } catch (error) {
        console.error('Error checking book readiness:', error);
        clearInterval(intervalId);
      }
    }, 20000); // Poll every 20 seconds
  };

const downloadBook = (bookId) => {
  window.location.href = `http://localhost:5000/download_book/${bookId}`; // Redirect to trigger the download.
};

  const fetchCover = async () => {
    try {
      const response = await fetch('http://localhost:5000/preview_cover', {
        method: 'POST',
        headers: {
          'Content-type': 'application/json'
        },
        body:JSON.stringify(formData),
      });
      if (!response.ok){
        throw new Error('Network response was not ok');

      }

      const blob = await response.blob();
      const reader = new FileReader();
      reader.readAsDataURL(blob);


      reader.onloadend = () => {
        const base64data = reader.result;
      
      // Store the base64 image data
        sessionStorage.setItem('coverImageData', base64data);
      
        setCoverUrl(URL.createObjectURL(blob));
    };


    } catch (error) {
      console.error('Failed to fetch eBook cover:', error);
    }
  };



  return (
    <div className="max-w-5xl mx-auto mt-12 px-4">
      <div className="grid grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-lg shadow-lg flex flex-col justify-between">
          <EbookForm formData={formData} setFormData={setFormData} onGenerateSuccess={handleGenerateSuccess} />
        </div>
        <div className="bg-white p-8 rounded-lg shadow-lg flex flex-col justify-between space-y-4">
          {coverUrl ? (
            <img src={coverUrl} alt="Ebook Cover" className="w-full h-auto mb-4 rounded" />
          ) : (
            // Show placeholder image if coverUrl is not set
            <img src={placeholderImageUrl} alt="Placeholder" className="w-full h-auto mb-4 rounded" />
          )}
          
          {/* Conditionally rendered hint about generating a preview */}
          {!isPreviewGenerated && (
            <p className="text-sm text-gray-500 self-center mt-auto"> Please generate a preview to see your book</p>
          )}
          
          {/* Purchase button, always at the bottom due to justify-between in the parent flex container */}
          <button 
            disabled={!isPreviewGenerated}
            onClick={handlePayment}
            className={`self-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white transition duration-300 ease-in-out ${isPreviewGenerated ? 'bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500' : 'bg-gray-400 hover:bg-gray-500 cursor-not-allowed'}`}
          >
            Generate & Purchase your Book
          </button>
        </div>
      </div>

    </div>
  );
  
}

export default Dashboard;
