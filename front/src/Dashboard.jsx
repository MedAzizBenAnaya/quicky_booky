import React, {useEffect, useState} from 'react';
// import {useNavigate} from 'react-router-dom';
import EbookForm from './EbookForm';
import placeholderImageUrl from '../public/place_holder.jpg'


function Dashboard() {
  // const navigate = useNavigate();
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
    <div className="min-h-screen bg-gray-100 py-12 px-8">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div className="bg-white p-8 rounded-lg shadow-lg flex flex-col justify-between h-full">
            <EbookForm formData={formData} setFormData={setFormData} onGenerateSuccess={handleGenerateSuccess} />
          </div>
          <div className="bg-white p-8 rounded-lg shadow-md flex flex-col justify-between h-full">
            <div className="flex-1">
              {coverUrl ? (
                <img src={coverUrl} alt="Ebook Cover" className="w-full object-contain rounded mt-4" style={{ height: '30rem' }} />
              ) : (
                <img src={placeholderImageUrl} alt="Placeholder" className="w-full object-contain rounded mt-4" style={{ height: '22rem' }} />
              )}

            </div>
            <div>
                {!isPreviewGenerated && (
                <p className="text-sm text-gray-500 self-center mt-4">Please generate a preview to see your book cover.</p>
              )}
            </div>
            <button
              disabled={!isPreviewGenerated}
              onClick={handlePayment}
              className={`mt-4 py-2 px-6 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-black hover:bg-gray-800 transition duration-300 ease-in-out ${isPreviewGenerated ? '' : 'cursor-not-allowed opacity-50'}`}
            >
              Generate & Purchase your Book
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  
}

export default Dashboard;
