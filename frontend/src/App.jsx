import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/NavBar";  
import Footer from "./components/Footer";  

import Home from "./pages/Home";
import Upload from "./pages/button/Upload.jsx";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Caserecord from "./pages/Caserecord"; // ✅ Import the new page
import Profile from "./pages/Profile";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";

import "./App.css";

function App() {
  return (
    <Router>
        <AuthProvider>
      {/* Navbar visible on all pages */}
      <Navbar />

      {/* Routes */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<ProtectedRoute><Upload /></ProtectedRoute>} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/case-record" element={<ProtectedRoute><Caserecord /></ProtectedRoute>} />
        <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      </Routes>

      {/* Footer visible on all pages */}
      <Footer />
      </AuthProvider>
    </Router>
  );
}

export default App;
