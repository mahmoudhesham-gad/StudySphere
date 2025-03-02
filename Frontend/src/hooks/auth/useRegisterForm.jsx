import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {authService} from '../../features/auth/authService';

export function useRegisterForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const userData = {
        username: formData.name,
        email: formData.email,
        password: formData.password,
        confirm_password: formData.confirmPassword
      };
      
      const response = await authService.register(userData);
      console.log('Registration response:', response);
      navigate('/', { 
      });
    } catch (err) {
      console.error('Registration error:', err);
      if (err.response?.data?.email) {
        setError(err.response.data.email[0]);
      } else if (err.response?.data?.username) {
        setError(err.response.data.username[0]);
      } else if (err.response?.data?.password) {
        setError(err.response.data.password[0]);
      } else {
        setError(err.response?.data?.message || 'Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return { formData, error, loading, handleChange, handleSubmit };
}