import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Catalogue from './pages/Catalogue';
import Lab from './pages/Lab';
import Compare from './pages/Compare';
import './design/tokens.css';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Catalogue />} />
        <Route path="/lab/:algorithmId" element={<Lab />} />
        <Route path="/compare" element={<Compare />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
