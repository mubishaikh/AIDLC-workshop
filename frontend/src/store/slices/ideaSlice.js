import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  ideas: [],
  myIdeas: [],
  currentIdea: null,
  campaigns: [],
  loading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
    page: 1,
  },
}

const ideaSlice = createSlice({
  name: 'ideas',
  initialState,
  reducers: {
    fetchIdeasStart: (state) => {
      state.loading = true
      state.error = null
    },
    fetchIdeasSuccess: (state, action) => {
      state.loading = false
      state.ideas = action.payload.results
      state.pagination = {
        count: action.payload.count,
        next: action.payload.next,
        previous: action.payload.previous,
        page: action.payload.page || 1,
      }
    },
    fetchIdeasFailure: (state, action) => {
      state.loading = false
      state.error = action.payload
    },
    fetchMyIdeasStart: (state) => {
      state.loading = true
      state.error = null
    },
    fetchMyIdeasSuccess: (state, action) => {
      state.loading = false
      state.myIdeas = action.payload
    },
    fetchMyIdeasFailure: (state, action) => {
      state.loading = false
      state.error = action.payload
    },
    fetchIdeaStart: (state) => {
      state.loading = true
      state.error = null
    },
    fetchIdeaSuccess: (state, action) => {
      state.loading = false
      state.currentIdea = action.payload
    },
    fetchIdeaFailure: (state, action) => {
      state.loading = false
      state.error = action.payload
    },
    createIdeaStart: (state) => {
      state.loading = true
      state.error = null
    },
    createIdeaSuccess: (state, action) => {
      state.loading = false
      state.ideas.unshift(action.payload)
    },
    createIdeaFailure: (state, action) => {
      state.loading = false
      state.error = action.payload
    },
    fetchCampaignsStart: (state) => {
      state.loading = true
      state.error = null
    },
    fetchCampaignsSuccess: (state, action) => {
      state.loading = false
      state.campaigns = action.payload
    },
    fetchCampaignsFailure: (state, action) => {
      state.loading = false
      state.error = action.payload
    },
  },
})

export const {
  fetchIdeasStart,
  fetchIdeasSuccess,
  fetchIdeasFailure,
  fetchMyIdeasStart,
  fetchMyIdeasSuccess,
  fetchMyIdeasFailure,
  fetchIdeaStart,
  fetchIdeaSuccess,
  fetchIdeaFailure,
  createIdeaStart,
  createIdeaSuccess,
  createIdeaFailure,
  fetchCampaignsStart,
  fetchCampaignsSuccess,
  fetchCampaignsFailure,
} = ideaSlice.actions

export default ideaSlice.reducer
