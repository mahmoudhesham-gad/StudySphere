import React from 'react';
import { useProfile } from '../../features/user/useProfile';

function Profile() {
  const {
    profile,
    isEditing,
    loading,
    error,
    handleUpdate,
    handleImageUpload,
    updateProfileField,
    toggleEditing
  } = useProfile();

  if (loading) return <div className="text-center mt-8">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 pt-20">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-blue-600 px-6 py-4">
            <h3 className="text-xl font-semibold text-white text-center">
              Profile Settings
            </h3>
          </div>

          <div className="p-6">
            {error && (
              <div className="mb-4 text-sm text-red-600 bg-red-50 p-3 rounded">
                {error}
              </div>
            )}

            <div className="mb-6 text-center">
              <div className="mb-4">
                {profile.profile_picture ? (
                  <img
                    src={profile.profile_picture}
                    alt="Profile"
                    className="w-32 h-32 rounded-full mx-auto object-cover"
                  />
                ) : (
                  <div className="w-32 h-32 rounded-full bg-gray-200 mx-auto flex items-center justify-center">
                    <span className="text-4xl text-gray-500">{profile.user.username[0]}</span>
                  </div>
                )}
              </div>
              <input
                type="file"
                onChange={handleImageUpload}
                className="hidden"
                id="profile-image"
                accept="image/*"
              />
              <label
                htmlFor="profile-image"
                className={`cursor-pointer text-blue-600 hover:text-blue-500 text-sm ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={loading}
              >
                {loading ? 'Uploading...' : 'Change Profile Picture'}
              </label>
            </div>

            <form onSubmit={handleUpdate}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Username</label>
                  <input
                    type="text"
                    value={profile.user.username}
                    disabled
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Email</label>
                  <input
                    type="email"
                    value={profile.user.email}
                    disabled
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm bg-gray-50"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Bio</label>
                  <textarea
                    value={profile.bio || ''}
                    onChange={e => updateProfileField('bio', e.target.value)}
                    disabled={!isEditing}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    rows="3"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700">Affiliation</label>
                  <input
                    type="text"
                    value={profile.Affiliation || ''}
                    onChange={e => updateProfileField('Affiliation', e.target.value)}
                    disabled={!isEditing}
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>

              <div className="mt-6 flex justify-end space-x-3">
                {!isEditing ? (
                  <button
                    type="button"
                    onClick={toggleEditing}
                    className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    Edit Profile
                  </button>
                ) : (
                  <>
                    <button
                      type="button"
                      onClick={toggleEditing}
                      className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Save Changes
                    </button>
                  </>
                )}
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
