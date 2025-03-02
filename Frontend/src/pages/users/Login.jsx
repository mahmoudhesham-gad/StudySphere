// src/pages/Login.jsx
import { Link } from 'react-router-dom';
import { useLoginForm } from '../../hooks/auth/useLoginForm';

function Login() {
  const { formData, error, loading, handleChange, handleSubmit } = useLoginForm();
  

  return (
    <div className="min-h-screen bg-gray-50 pt-20">

      <div className="max-w-md mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-blue-600 px-6 py-4 border-b border-gray-200">
            <h3 className="text-xl font-semibold text-gray-900 text-center">
              Login to Your Account
            </h3>
          </div>

          <div className="px-6 py-8">
            {error && (
              <div className="mb-4 text-sm text-red-600 bg-red-50 p-3 rounded">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-20 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Don't have an account?{' '}
                <Link to="/register" className="font-medium text-blue-600 hover:text-blue-500">
                  Register here
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;