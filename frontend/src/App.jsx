import React, { useContext, useEffect, useState } from "react";

import Register from "./components/Register";
import Login from "./components/Login";
import Header from "./components/Header";
import Home from "./components/Home";
import { UserContext } from "./context/UserContext";

const App = () => {
  const [message, setMessage] = useState("");
  const [token] = useContext(UserContext);

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("http://localhost:8000/api", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("something messed up");
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);

  return (
    <>
      <Header title={message} />
      <div className="flex flex-col md:flex-row">
        <div className="flex-1"></div>
        <div className="flex-1 md:flex-2/3 p-5">
          {!token ? (
            <div className="flex flex-col md:flex-row">
              <Register />
              <Login />
            </div>
          ) : (
            <Home />
          )}
        </div>
        <div className="flex-1"></div>
      </div>

    </>
  );
};

export default App;