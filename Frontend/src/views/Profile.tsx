import React, { useState, useEffect } from 'react';
import { authService } from '../api/authService';

export const Profile = () => {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await authService.getCurrentUser();
        setProfile(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load profile');
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) return <div className="p-4">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;
  if (!profile) return <div className="p-4">No profile data found</div>;

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <div className="flex items-center space-x-4">
          {profile.profile_picture && (
            <img 
              src={profile.profile_picture} 
              alt="Profile" 
              className="w-16 h-16 rounded-full"
            />
          )}
          <div>
            <h1 className="text-xl font-bold">{profile.user.username}</h1>
            <p className="text-gray-600 dark:text-gray-300">{profile.user.email}</p>
          </div>
        </div>
        
        {profile.bio && (
          <div className="mt-4">
            <h2 className="text-lg font-semibold">Bio</h2>
            <p className="text-gray-600 dark:text-gray-300">{profile.bio}</p>
          </div>
        )}

        {profile.Affiliation && (
          <div className="mt-4">
            <h2 className="text-lg font-semibold">Affiliation</h2>
            <p className="text-gray-600 dark:text-gray-300">{profile.Affiliation}</p>
          </div>
        )}
      </div>
    </div>
  );
};
