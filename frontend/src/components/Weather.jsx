import React, { useState, useEffect } from "react";

const Weather = () => {
  const [correlationImage, setCorrelationImage] = useState('');
  const [regressionImage, setRegressionImage] = useState('');

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/analysis/weather");
        if (!response.ok) {
          throw new Error("Error fetching weather analysis");
        }
        const data = await response.json();
        setCorrelationImage(data.correlation_image);
        setRegressionImage(data.regression_image);
      } catch (error) {
        console.error("Error fetching weather analysis:", error);
      }
    };

    fetchImages();
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold mb-4">Weather Analysis</h1>
      {correlationImage && (
        <div>
          <h2 className="text-2xl font-semibold mb-2">Correlation Matrix</h2>
          <img
            src={`data:image/png;base64,${correlationImage}`}
            alt="Correlation Matrix"
            className="w-full h-auto rounded-lg shadow-md mb-4"
          />
        </div>
      )}
      {regressionImage && (
        <div>
          <h2 className="text-2xl font-semibold mb-2">Regression Analysis</h2>
          <img
            src={`data:image/png;base64,${regressionImage}`}
            alt="Regression Analysis"
            className="w-full h-auto rounded-lg shadow-md"
          />
        </div>
      )}
    </div>
  );
};

export default Weather;
