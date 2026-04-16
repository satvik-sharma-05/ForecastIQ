import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Datasets from './pages/Datasets';
import Forecast from './pages/Forecast';
import History from './pages/History';
import Insights from './pages/Insights';
import Compare from './pages/Compare';
import Layout from './components/Layout';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const ProtectedRoute = ({ children }) => {
    return token ? children : <Navigate to="/login" />;
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login setToken={setToken} />} />
        <Route path="/signup" element={<Signup setToken={setToken} />} />

        <Route path="/app" element={
          <ProtectedRoute>
            <Layout setToken={setToken} />
          </ProtectedRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="datasets" element={<Datasets />} />
          <Route path="forecast" element={<Forecast />} />
          <Route path="history" element={<History />} />
          <Route path="insights" element={<Insights />} />
          <Route path="compare" element={<Compare />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
