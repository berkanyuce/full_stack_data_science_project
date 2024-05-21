import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "../context/UserContext";

const Profile = () => {
    const [token] = useContext(UserContext);
    const [email, setEmail] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        const getUserData = async () => {
          try {
            const requestOptions = {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
              },
            };
            const response = await fetch(`http://localhost:8000/api/users/me`, requestOptions);
    
            if (!response.ok) {
              throw new Error("Could not get the user data");
            }
            const data = await response.json();
            setEmail(data.email);
          } catch (error) {
            setErrorMessage(error.message);
          }
        };

        getUserData();
      }, [token]);

    return (
        <div className="container mx-auto p-4">
            <h2 className="text-2xl font-bold mb-4">Profil Sayfası</h2>
            {email ? (
                <div className="bg-white shadow-md rounded-lg p-6">
                <p className="text-lg">E-posta: {email}</p>
                </div>
            ) : (
                <p className="text-red-500">{errorMessage || "Loading..."}</p>
            )}
        </div>

    );
};

export default Profile;
