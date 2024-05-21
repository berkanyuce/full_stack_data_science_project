import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Profile from "./Profile";
import Weather from "./Weather";
import Image from "./Image";

const Home = () => (
  <div>
    <p className="has-text-weight-bold has-text-danger">Home page</p>
    <Router>
        <Routes>
            <Route path="/profile" element={<Profile />} />
            <Route path="/api/analysis/weather" element={<Weather />} />
            <Route path="/api/analysis/image" element={<Image />} />
        </Routes>
        <Link to="/profile" className="button is-primary">Profile</Link>
        <Link to="/api/analysis/weather" className="button is-link">Analysis</Link>
        <Link to="/api/analysis/image" className="button is-info">Image processing</Link>
    </Router>
  </div>
);

export default Home;
