import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container, Box } from '@mui/material';
import QuestionList from './components/QuestionList.jsx';
import QuestionLogList from './components/QuestionLogList.jsx';

function App() {
  return (
    <Router>
      <Box>
        <AppBar position="fixed">
          <Toolbar>
            <Typography variant="h6" sx={{ flexGrow: 1 }}>
              InterviewQ
            </Typography>
            <Button color="inherit" component={Link} to="/">Questions</Button>
          </Toolbar>
        </AppBar>
        <Container sx={{ mt: { xs: 7, sm: 8 } }}>
          <Routes>
            <Route path="/" element={<QuestionList />} />
            <Route path="/logs/:questionId" element={<QuestionLogList />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
}

export default App;
