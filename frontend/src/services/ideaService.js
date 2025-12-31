import api from './api'

const ideaService = {
  // Get all ideas
  getIdeas: (params = {}) => {
    return api.get('/ideas/', { params })
  },

  // Get user's ideas
  getMyIdeas: (params = {}) => {
    return api.get('/ideas/my/', { params })
  },

  // Get idea by ID
  getIdeaById: (id) => {
    return api.get(`/ideas/${id}/`)
  },

  // Create idea
  createIdea: (data) => {
    return api.post('/ideas/', data)
  },

  // Update idea
  updateIdea: (id, data) => {
    return api.put(`/ideas/${id}/`, data)
  },

  // Delete idea
  deleteIdea: (id) => {
    return api.delete(`/ideas/${id}/`)
  },

  // Submit idea
  submitIdea: (id) => {
    return api.post(`/ideas/${id}/submit/`, {})
  },

  // Add contributor
  addContributor: (ideaId, userId) => {
    return api.post(`/ideas/${ideaId}/add_contributor/`, {
      user_id: userId,
    })
  },

  // Get contributors
  getContributors: (ideaId) => {
    return api.get(`/ideas/${ideaId}/contributors/`)
  },

  // Get documents
  getDocuments: (ideaId) => {
    return api.get(`/ideas/${ideaId}/documents/`)
  },

  // Get campaigns
  getCampaigns: (params = {}) => {
    return api.get('/campaigns/', { params })
  },

  // Get campaign by ID
  getCampaignById: (id) => {
    return api.get(`/campaigns/${id}/`)
  },
}

export default ideaService
