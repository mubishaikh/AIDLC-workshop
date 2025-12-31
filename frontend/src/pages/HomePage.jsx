import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Box, Typography, Button, Grid, Card, CardContent } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import ideaService from '../services/ideaService'
import {
  fetchIdeasStart,
  fetchIdeasSuccess,
  fetchIdeasFailure,
} from '../store/slices/ideaSlice'

function HomePage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { ideas, loading } = useSelector((state) => state.ideas)
  const { isAuthenticated } = useSelector((state) => state.auth)

  useEffect(() => {
    const fetchIdeas = async () => {
      dispatch(fetchIdeasStart())
      try {
        const response = await ideaService.getIdeas({ status: 'SUBMITTED' })
        dispatch(fetchIdeasSuccess(response.data))
      } catch (error) {
        dispatch(fetchIdeasFailure(error.message))
      }
    }

    fetchIdeas()
  }, [dispatch])

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Welcome to Ideation Portal
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Share your innovative ideas and collaborate with your team to drive organizational growth.
        </Typography>
        {isAuthenticated && (
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/submit')}
          >
            Submit Your Idea
          </Button>
        )}
      </Box>

      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Recent Ideas
      </Typography>

      {loading ? (
        <Typography>Loading...</Typography>
      ) : (
        <Grid container spacing={2}>
          {ideas.map((idea) => (
            <Grid item xs={12} sm={6} md={4} key={idea.id}>
              <Card
                sx={{ cursor: 'pointer' }}
                onClick={() => navigate(`/ideas/${idea.id}`)}
              >
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {idea.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {idea.description?.substring(0, 100)}...
                  </Typography>
                  <Typography variant="caption">
                    Impact: {idea.expected_impact}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  )
}

export default HomePage
