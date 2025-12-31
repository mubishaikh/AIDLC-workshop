import { Box, Container, Typography } from '@mui/material'

function Footer() {
  return (
    <Box
      sx={{
        bgcolor: 'background.paper',
        py: 4,
        borderTop: '1px solid',
        borderColor: 'divider',
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          © 2024 Ideation Portal. All rights reserved.
        </Typography>
      </Container>
    </Box>
  )
}

export default Footer
