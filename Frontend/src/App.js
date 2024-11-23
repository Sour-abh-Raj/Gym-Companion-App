import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Container, 
  Grid, 
  Paper, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel, 
  Button, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  CircularProgress,
  useMediaQuery,
  useTheme
} from '@mui/material'
import { FitnessCenter, Videocam } from '@mui/icons-material'

export default function ExerciseCounterApp() {
  const [exercise, setExercise] = useState('')
  const [videoSource, setVideoSource] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const [count, setCount] = useState(0)
  const [exerciseHistory, setExerciseHistory] = useState([])
  const [loading, setLoading] = useState(false)

  const theme = useTheme()
  const isMediumScreen = useMediaQuery(theme.breakpoints.up('md'))

  const userId = 'sample_user_id' // Replace this with actual user ID logic

  useEffect(() => {
    // Fetch exercise history from the backend
    axios.get(`http://localhost:5000/exercise/history/${userId}`)
      .then(response => {
        setExerciseHistory(response.data)
      })
      .catch(error => {
        console.error("Error fetching exercise history:", error)
      })
  }, [userId])

  const handleExerciseChange = (event) => {
    setExercise(event.target.value)
  }

  const handleVideoSourceChange = (event) => {
    setVideoSource(event.target.value)
  }

  const toggleStreaming = () => {
    setIsStreaming(!isStreaming)
    // Trigger backend to start/stop exercise counting
    if (!isStreaming) {
      startExerciseCounting()
    } else {
      stopExerciseCounting()
    }
  }

  const startExerciseCounting = () => {
    setLoading(true)
    axios.post(`http://localhost:5000/exercise/start-exercise`, { userId, exercise })
      .then(response => {
        setCount(response.data.initialCount)
        setLoading(false)
      })
      .catch(error => {
        console.error("Error starting exercise counting:", error)
        setLoading(false)
      })
  }

  const stopExerciseCounting = () => {
    setLoading(true)
    axios.post(`http://localhost:5000/exercise/stop-exercise`, { userId })
      .then(response => {
        setLoading(false)
      })
      .catch(error => {
        console.error("Error stopping exercise counting:", error)
        setLoading(false)
      })
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <AppBar position="static">
        <Toolbar>
          <FitnessCenter sx={{ mr: 2 }} />
          <Typography variant="h6">Exercise Counter App</Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: { xs: 2, sm: 3, md: 4 } }}>
        <Grid container spacing={{ xs: 2, sm: 3 }}>
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: { xs: 2, sm: 3 } }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel id="exercise-select-label">Exercise</InputLabel>
                    <Select
                      labelId="exercise-select-label"
                      value={exercise}
                      label="Exercise"
                      onChange={handleExerciseChange}
                    >
                      <MenuItem value="bicep-curls">Bicep Curls</MenuItem>
                      <MenuItem value="pull-ups">Pull-ups</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth>
                    <InputLabel id="video-source-select-label">Video Source</InputLabel>
                    <Select
                      labelId="video-source-select-label"
                      value={videoSource}
                      label="Video Source"
                      onChange={handleVideoSourceChange}
                    >
                      <MenuItem value="webcam">Webcam</MenuItem>
                      <MenuItem value="upload">Upload Video</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
              <div className="aspect-video bg-gray-200 flex items-center justify-center my-4">
                {isStreaming ? (
                  <video className="w-full h-full object-cover" />
                ) : (
                  <Videocam sx={{ fontSize: 64, color: 'text.secondary' }} />
                )}
              </div>
              <Button 
                variant="contained" 
                color={isStreaming ? "secondary" : "primary"}
                onClick={toggleStreaming}
                fullWidth
              >
                {isStreaming ? 'Stop' : 'Start'} Exercise
              </Button>
              {loading && (
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '1rem' }}>
                  <CircularProgress />
                </div>
              )}
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: { xs: 2, sm: 3 }, mb: { xs: 2, sm: 3 } }}>
              <Typography variant="h4" align="center" gutterBottom>Count</Typography>
              <Typography variant="h2" align="center">{count}</Typography>
            </Paper>
            <Paper sx={{ p: { xs: 2, sm: 3 } }}>
              <Typography variant="h6" gutterBottom>Exercise History</Typography>
              <TableContainer>
                <Table size={isMediumScreen ? "medium" : "small"}>
                  <TableHead>
                    <TableRow>
                      <TableCell>Date</TableCell>
                      <TableCell>Exercise</TableCell>
                      <TableCell align="right">Count</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {exerciseHistory.map((row, index) => (
                      <TableRow key={index}>
                        <TableCell>{new Date(row.timestamp).toLocaleDateString()}</TableCell>
                        <TableCell>{row.exercise_type}</TableCell>
                        <TableCell align="right">{row.count}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </div>
  )
}
