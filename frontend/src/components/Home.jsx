import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Profile from "./Profile";
import Weather from "./Weather";
import Image from "./Image";

const Home = () => (
  <div>
    <Router>
      <div className="p-4 space-x-4">
        <Link to="/profile" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Profile
        </Link>
        <Link to="/api/analysis/weather" className="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded">
          Analysis
        </Link>
        <Link to="/api/analysis/image" className="bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded">
          Image processing
        </Link>
      </div>
      <Routes>
        <Route path="/profile" element={<Profile />} />
        <Route path="/api/analysis/weather" element={<Weather />} />
        <Route path="/api/analysis/image" element={<Image />} />
      </Routes>
    </Router>
  </div>
);

export default Home;
