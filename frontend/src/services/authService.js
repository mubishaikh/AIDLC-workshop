import api from './api'

const authService = {
  // Register user
  register: (userData) => {
    return api.post('/auth/users/register/', userData)
  },

  // Login user
  login: (username, password) => {
    return api.post('/auth/login/', {
      username,
      password,
    })
  },

  // Refresh token
  refreshToken: (refreshToken) => {
    return api.post('/auth/refresh/', {
      refresh: refreshToken,
    })
  },

  // Get current user
  getCurrentUser: () => {
    return api.get('/auth/users/me/')
  },

  // Change password
  changePassword: (oldPassword, newPassword, newPassword2) => {
    return api.post('/auth/users/change_password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password2: newPassword2,
    })
  },

  // Logout
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  },
}

export default authService
