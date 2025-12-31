import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  isAuthenticated: !!localStorage.getItem('access_token'),
  user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
  loading: false,
  error: null,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart: (state) => {
      state.loading = true
      state.error = null
    },
    loginSuccess: (state, action) => {
      state.loading = false
      state.isAuthenticated = true
      state.user = action.payload.user
      localStorage.setItem('access_token', action.payload.access_token)
      localStorage.setItem('refresh_token', action.payload.refresh_token)
      localStorage.setItem('user', JSON.stringify(action.payload.user))
    },
    loginFailure: (state, action) => {
      state.loading = false
      state.error = action.payload
    },
    logout: (state) => {
      state.isAuthenticated = false
      state.user = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },
    registerStart: (state) => {
      state.loading = true
      state.error = null
    },
    registerSuccess: (state) => {
      state.loading = false
    },
    registerFailure: (state, action) => {
      state.loading = false
      state.error = action.payload
    },
  },
})

export const {
  loginStart,
  loginSuccess,
  loginFailure,
  logout,
  registerStart,
  registerSuccess,
  registerFailure,
} = authSlice.actions

export default authSlice.reducer
