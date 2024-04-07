import React from 'react';
import FacebookIcon from '../svgs/facebook-logo-svgrepo-com.svg';
import TwitterIcon from '../svgs/twitter-x-logo-black-round-20851.svg';
import InstagramIcon from '../svgs/instagram-logo-facebook-svgrepo-com.svg';
import LinkedInIcon from '../svgs/logo-linkedin-svgrepo-com.svg';
import YouTubeIcon from '../svgs/logo-youtube-svgrepo-com.svg';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white py-8">
      <div className="max-w-6xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-8">
        <div>
          <h2 className="font-bold text-lg mb-4">Quicky Booky</h2>
          <p className="mb-2">Address:</p>
          <p className="mb-2">Munich, Germany, DE</p>
          <p className="mb-2">Contact:</p>
          <p>+49 172 1616874</p>
          <p>info@quickybooky.com</p>
        </div>
        <div className="col-span-2 md:col-span-3 flex justify-between">
          <div>
            <h3 className="font-bold text-lg mb-4">Company</h3>
            <ul>
              <li className="mb-2">About Us</li>
              <li className="mb-2">Contact Us</li>
              <li className="mb-2">FAQs</li>
              <li className="mb-2">Support</li>
              <li>Blog</li>
            </ul>
          </div>
          <div>
            <h3 className="font-bold text-lg mb-4">Resources</h3>

          </div>
        </div>
        <div className="flex items-center justify-end md:col-span-4 space-x-4">
          {/* Social media icons */}
          <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer">
            <img src={FacebookIcon} alt="Facebook" className="w-6 h-6" />
          </a>
          <a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer">
            <img src={TwitterIcon} alt="Twitter" className="w-6 h-6" />
          </a>
          <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer">
            <img src={InstagramIcon} alt="Instagram" className="w-6 h-6" />
          </a>
          <a href="https://www.linkedin.com" target="_blank" rel="noopener noreferrer">
            <img src={LinkedInIcon} alt="LinkedIn" className="w-6 h-6" />
          </a>
          <a href="https://www.youtube.com" target="_blank" rel="noopener noreferrer">
            <img src={YouTubeIcon} alt="YouTube" className="w-6 h-6" />
          </a>
        </div>
      </div>
      <div className="text-center py-4 border-t mt-8">
        <p>© {currentYear} Quicky Booky. All rights reserved.</p>
        <div className="mt-2">
          <a href="/privacy" className="mx-2">Privacy Policy</a>|
          <a href="/terms" className="mx-2">Terms and Conditions</a>|
          <a href="/cookie" className="mx-2">Cookie Policy</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
