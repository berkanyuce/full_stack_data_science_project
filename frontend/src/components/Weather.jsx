import React, { useState, useEffect } from "react";

const Weather = () => {
  const [image, setImage] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/analysis/weather");
        if (!response.ok) {
          throw new Error("Error fetching weather analysis");
        }
        const data = await response.json();
        setImage(data.image);
      } catch (error) {
        console.error("Error fetching weather analysis:", error);
      }
    };

    fetchImage();
  }, []);

  return (
    <div className="p-4">
        <h1 className="text-3xl font-bold mb-4">Weather Analysis</h1>
        {image && <img src={`data:image/png;base64,${image}`} alt="Weather Analysis" className="w-full h-auto rounded-lg shadow-md" />}
    </div>
  );
};

export default Weather;
