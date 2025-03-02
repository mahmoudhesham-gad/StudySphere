import { useState, useEffect } from 'react';
import { userService } from './userService';
import { cloudinaryConfig } from '../../../config/cloudinaryConfig';
import axios from 'axios';

export const useProfile = () => {
  const [profile, setProfile] = useState({
    user: {
      id: '',
      email: '',
      username: ''
    },
    bio: '',
    profile_picture: null,
    Affiliation: ''
  });
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchProfile = async () => {
    try {
      const response = await userService.getCurrentUser();
      setProfile(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to load profile');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await userService.updateProfile(profile);
      setIsEditing(false);
      fetchProfile();
    } catch (err) {
      setError('Failed to update profile');
    }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    setLoading(true);
    
    try {
      // Create a FormData instance for Cloudinary upload
      const uploadData = new FormData();
      uploadData.append('file', file);
      uploadData.append('upload_preset', cloudinaryConfig.uploadPreset);
      uploadData.append('cloud_name', cloudinaryConfig.cloudName);
      
      // Upload to Cloudinary
      const cloudinaryResponse = await axios.post(cloudinaryConfig.apiUrl, uploadData);
      
      if (cloudinaryResponse.data && cloudinaryResponse.data.secure_url) {
        // Update profile with the Cloudinary URL
        const profileUpdate = {
          profile_picture: cloudinaryResponse.data.secure_url
        };
        
        await userService.updateProfile(profileUpdate);
        fetchProfile();
      } else {
        throw new Error('Failed to get image URL from Cloudinary');
      }
    } catch (err) {
      console.error('Image upload error:', err);
      setError('Failed to upload image to Cloudinary');
    } finally {
      setLoading(false);
    }
  };

  const updateProfileField = (field, value) => {
    setProfile({ ...profile, [field]: value });
  };

  const toggleEditing = () => {
    setIsEditing(!isEditing);
  };

  return {
    profile,
    isEditing,
    loading,
    error,
    handleUpdate,
    handleImageUpload,
    updateProfileField,
    toggleEditing
  };
};
