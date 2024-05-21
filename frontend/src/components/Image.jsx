import React, { useState } from 'react';

const ImageUpload = () => {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) return;

    const formData = new FormData();
    formData.append('image', image);

    try {
      const response = await fetch('http://localhost:8000/api/analysis/image', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data.class); // Save only the class result
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };

  return (
    <div className="p-4">
        <form onSubmit={handleSubmit} className="space-y-4">
            <input
            type="file"
            onChange={handleImageChange}
            className="block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
            Upload Image
            </button>
        </form>
        {result && (
            <div className="mt-4">
            <h3 className="text-xl font-semibold">Prediction Result: {result}</h3>
            </div>
        )}
        </div>

  );
};

export default ImageUpload;
