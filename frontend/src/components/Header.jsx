import React, { useContext } from "react";

import { UserContext } from "../context/UserContext";

const Header = ({ title }) => {
  const [token, setToken] = useContext(UserContext);

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <div className="text-center m-6">
      <h1 className="text-2xl font-bold mb-4">{title}</h1>
      {token && (
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
          onClick={handleLogout}
        >
          Logout
        </button>
      )}
    </div>

  );
};

export default Header;