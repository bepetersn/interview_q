import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container, Box } from '@mui/material';
import QuestionList from './QuestionList.jsx';
import { QuestionLogList } from '../features/question-logs/index.js';
import { LoginPage, RegisterPage } from '../features/auth/index.js';
import api from '../../api.js';
import '../../App.css';
import '../../login.css';


function App() {
    const [user, setUser] = React.useState(null);

    // Keep user state in sync on login/logout
    const handleLogin = (userObj) => {
        console.log("handleLogin. Setting user:", userObj);
        setUser(userObj);
    };

    // Fetch user identity from API and update state
    const resetUserIdentity = async () => {
        try {
            console.log("Resetting user identity...");
            const res = await api.get('/accounts/identity/');
            console.log("API response:", res);
            if (res.data && res.data.authenticated) {
                console.log("resetUserIdentity. User identity fetched successfully:", res.data);
                setUser(res.data);
                return;
            }
        } catch (err) {
            console.error("Failed to fetch user identity:", err);
        }
        setUser(null);
    };

    // Logout handler
    const handleLogout = async () => {
        try {
            await api.post('/accounts/logout/');
        } catch (err) {
            // Optionally show error feedback
            console.error('Logout failed:', err);
        }
        setUser(null);
        window.location.href = '/'; // Redirect to login
    };

    // On every page load, re-sync user state from backend
    React.useEffect(() => {
        console.log("App useEffect. Checking user state...");
        resetUserIdentity();
    }, []);

    if (!user) {
        return (
            <Router>
                <Routes>
                    <Route path="/register" element={<RegisterPage onRegister={() => window.location.href = '/'} />} />
                    <Route path="*" element={<LoginPage onLogin={handleLogin} />} />
                </Routes>
            </Router>
        );
    }

    return (
        <Router>
            <Box>
                <AppBar position="fixed">
                    <Toolbar>
                        <Typography variant="h6" sx={{ flexGrow: 1 }}>
                            InterviewQ
                        </Typography>
                        <Button color="inherit" component={Link} to="/">Questions</Button>
                        <Button color="inherit" onClick={handleLogout}>Logout</Button>
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
