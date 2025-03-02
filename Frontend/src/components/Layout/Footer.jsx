import React from 'react';
import { Link } from 'react-router-dom';
import { FaFacebook, FaTwitter, FaInstagram, FaLinkedin } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-8 mt-auto">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">StudySphere</h3>
            <p className="text-gray-300">
              Empowering students to achieve their academic goals through collaborative learning.
            </p>
          </div>
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-300 hover:text-white">Home</Link></li>
              <li><Link to="/about" className="text-gray-300 hover:text-white">About</Link></li>
              <li><Link to="/contact" className="text-gray-300 hover:text-white">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-lg font-semibold mb-4">Follow Us</h4>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-300 hover:text-white"><FaFacebook size={24} /></a>
              <a href="#" className="text-gray-300 hover:text-white"><FaTwitter size={24} /></a>
              <a href="#" className="text-gray-300 hover:text-white"><FaInstagram size={24} /></a>
              <a href="#" className="text-gray-300 hover:text-white"><FaLinkedin size={24} /></a>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center">
          <p className="text-gray-300">© {new Date().getFullYear()} StudySphere. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
