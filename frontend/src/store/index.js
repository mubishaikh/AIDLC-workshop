import { configureStore } from '@reduxjs/toolkit'
import authReducer from './slices/authSlice'
import ideaReducer from './slices/ideaSlice'
import uiReducer from './slices/uiSlice'

const store = configureStore({
  reducer: {
    auth: authReducer,
    ideas: ideaReducer,
    ui: uiReducer,
  },
})

export default store
