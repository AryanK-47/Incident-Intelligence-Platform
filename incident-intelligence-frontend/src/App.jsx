import React from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Incidents from './pages/Incidents';
import IncidentDetail from './pages/IncidentDetail';
import { isAuthenticated } from './api/auth';

function Protected({ children }) { const location = useLocation(); return isAuthenticated() ? children : <Navigate to="/login" replace state={{ from: location.pathname }} />; }
export default function App() {
 return <Routes><Route path="/login" element={isAuthenticated()?<Navigate to="/" replace/>:<Login/>}/><Route path="/" element={<Protected><AppLayout/></Protected>}><Route index element={<Dashboard/>}/><Route path="incidents" element={<Incidents/>}/><Route path="incidents/:id" element={<IncidentDetail/>}/></Route><Route path="*" element={<Navigate to="/" replace/>}/></Routes>;
}
