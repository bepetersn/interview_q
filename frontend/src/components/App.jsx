import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container, Box } from '@mui/material';
import QuestionList from './QuestionList.jsx';
import QuestionLogList from './QuestionLogList.jsx';
import LoginPage from './LoginPage.jsx';
import '../App.css';
import '../login.css';


function App() {
    const [user, setUser] = React.useState(() => {
        // Restore user from localStorage only if sessionid cookie is present
        const userData = localStorage.getItem("user");
        const sessionid = document.cookie
            .split(';')
            .map(c => c.trim())
            .find(c => c.startsWith('sessionid='));
        if (userData && sessionid) {
            try {
                const user = JSON.parse(userData);
                if (user?.username) return user;
            } catch {}
        }
        return null;
    });

    // Keep user state and localStorage in sync on login/logout
    const handleLogin = (userObj) => {
        if (userObj) {
            localStorage.setItem("user", JSON.stringify(userObj));
            setUser(userObj);
        } else {
            localStorage.removeItem("user");
            setUser(null);
        }
    };

    // On every page load, re-sync user state from localStorage and sessionid
    React.useEffect(() => {
        const userData = localStorage.getItem("user");
        const sessionid = document.cookie
            .split(';')
            .map(c => c.trim())
            .find(c => c.startsWith('sessionid='));
        if (userData && sessionid) {
            try {
                const userObj = JSON.parse(userData);
                if (userObj?.username) {
                    setUser(userObj);
                    return;
                }
            } catch {}
        }
        setUser(null);
    }, []);

    if (!user) {
        return <LoginPage onLogin={handleLogin} />;
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
