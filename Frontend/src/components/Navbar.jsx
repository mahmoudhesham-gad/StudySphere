import { Link } from 'react-router-dom';
import { FaBars, FaTimes } from 'react-icons/fa';
import { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import  LogoutButton  from './LogoutButton';


const Navbar = () => {
  const { user } = useContext(AuthContext);
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => setIsOpen(!isOpen);
  const handleLogout = () => {
    // Handle logout logic here
    setIsOpen(false);
  };
  

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center">
            <span className="text-2xl font-bold text-blue-600">StudySphere</span>
          </Link>

          {/* Mobile menu button */}
          <button
            className="md:hidden text-gray-600 hover:text-gray-900"
            onClick={toggleMenu}
          >
            {isOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <Link to="/" className="text-gray-600 hover:text-blue-600">Home</Link>
            <Link to="/courses" className="text-gray-600 hover:text-blue-600">Courses</Link>
            <Link to="/study-groups" className="text-gray-600 hover:text-blue-600">Study Groups</Link>
            <Link to="/resources" className="text-gray-600 hover:text-blue-600">Resources</Link>
            <div className="ml-4 flex space-x-2"> {/* Added flex and space-x-2 */}
              {!user ? (
                <>
                  <Link to="/login" className="px-4 py-2 text-center text-blue-600 border border-blue-600 rounded hover:bg-blue-600 hover:text-white">
                    Login
                  </Link>
                  <Link to="/register" className="px-4 py-2 text-center bg-blue-600 text-white rounded hover:bg-blue-700">
                    Sign Up
                  </Link>
                </>
              ) : (
                <LogoutButton />
              )}
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <div className="md:hidden py-4">
            <div className="flex flex-col space-y-4">
              <Link to="/" className="text-gray-600 hover:text-blue-600">Home</Link>
              <Link to="/courses" className="text-gray-600 hover:text-blue-600">Courses</Link>
              <Link to="/study-groups" className="text-gray-600 hover:text-blue-600">Study Groups</Link>
              <Link to="/resources" className="text-gray-600 hover:text-blue-600">Resources</Link>
              {/* Mobile Navigation buttons */}
              <div className="space-y-2">
              {!user ? (
                <>
                  <Link to="/login" className="block px-4 py-2 text-center text-blue-600 border border-blue-600 rounded hover:bg-blue-600 hover:text-white">
                    Login
                  </Link>
                  <Link to="/register" className="block px-4 py-2 text-center bg-blue-600 text-white rounded hover:bg-blue-700">
                    Sign Up
                  </Link>
                </>
              ) : (
                <LogoutButton />
              )}
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
