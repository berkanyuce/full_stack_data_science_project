import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Profile from "./Profile";
import Weather from "./Weather";

const Home = () => (
  <div>
    <p className="has-text-weight-bold has-text-danger">Home page</p>
    <Router>
        <Routes>
            <Route path="/profile" element={<Profile />} />
            <Route path="/api/analysis/weather" element={<Weather />} />
            <Route path="/image-processing" element={<h1>Image Processing Page</h1>} />
        </Routes>
        <Link to="/profile" className="button is-primary">Profile</Link>
        <Link to="/api/analysis/weather" className="button is-link">Analysis</Link>
        <Link to="/image-processing" className="button is-info">Image processing</Link>
    </Router>
  </div>
);

export default Home;
