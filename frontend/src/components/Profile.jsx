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
        <div>
        <h2>Profil Sayfası</h2>
        {email ? (
            <div>
            <p>E-posta: {email}</p>
            {/* Diğer kullanıcı bilgileri burada görüntülenebilir */}
            </div>
        ) : (
            <p>{errorMessage || "Kullanıcı bilgileri yükleniyor..."}</p>
        )}
        </div>
    );
};

export default Profile;
