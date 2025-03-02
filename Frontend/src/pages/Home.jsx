// src/pages/Home.jsx
import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      <section className="py-12 md:py-20 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl mb-12">
        <div className="max-w-3xl mx-auto text-center px-4">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">Welcome to StudySphere</h1>
          <p className="text-xl text-gray-600 mb-8">A secure and intuitive platform for collaborative learning</p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/login" className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition duration-300">Login</Link>
            <Link to="/register" className="px-6 py-3 bg-white text-blue-600 font-medium rounded-lg border border-blue-600 hover:bg-blue-50 transition duration-300">Register</Link>
          </div>
        </div>
      </section>
      
      <section className="py-12 mb-12">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition duration-300">
            <div className="text-4xl mb-4 text-blue-600">🔒</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Secure Authentication</h3>
            <p className="text-gray-600">HTTP-only cookies ensure your login remains secure and protected from XSS attacks</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition duration-300">
            <div className="text-4xl mb-4 text-blue-600">📊</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Interactive Dashboard</h3>
            <p className="text-gray-600">View your stats and recent activity all in one place</p>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition duration-300">
            <div className="text-4xl mb-4 text-blue-600">👤</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Profile Management</h3>
            <p className="text-gray-600">Easily update your personal information and preferences</p>
          </div>
        </div>
      </section>
      
      <section className="py-12 bg-gray-50 rounded-xl px-4 md:px-8">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-6">About Our Platform</h2>
          <p className="text-gray-600 mb-4 leading-relaxed">
            Our application is built with React, React Router for seamless navigation, 
            and a secure authentication system. We prioritize user experience and security,
            providing you with a robust platform to manage your information.
          </p>
          <p className="text-gray-600 leading-relaxed">
            Get started today by creating an account or logging in if you're already a member.
          </p>
        </div>
      </section>
    </div>
  );
}

export default Home;