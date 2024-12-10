import React, { useEffect, useState } from 'react';
import './UserProfile.css';
import { useAuth } from '../../hooks/authContext';
import ZnaniumApi from '../../API/API';

function UserProfile() {
  const { logout } = useAuth()
	const [userData, setUserData] = useState({
    email: '',
    name: '',
    phone_number: '',
  });

	const exit = async () => {
		logout()
		const response = await ZnaniumApi.logout()
		console.log(response);
		
	}

	useEffect(() => {
		async function getUser() {
			const response = await ZnaniumApi.getUserProfileData()
			console.log(response.data.user)
			return response.data.user
		}
		getUser().then((user) => {
      if (user) {
        setUserData({
          email: user.email,
          name: user.name,
          phone_number: user.phone_number,
        });
      }
    });
  }, []);

	return (
    <div className="user-profile">
      <div className="user-info">
        <div className="avatar"></div>
        <div className="user-details">
          <h2>{userData.name}</h2>
          <p>{userData.phone_number}</p>
          <p>{userData.email}</p>
        </div>
      </div>

      <div className="lists-container">
        <div className="list achievements">
          <h3>Достижения</h3>
          <ul>
            <li>Мастер-класс "Биолог"</li>
            <li>Курс "Логарифмы"</li>
          </ul>
        </div>

        <div className="list statistics">
          <h3>Статистика</h3>
          <ul>
            <li>Тема: "Деление клетки"</li>
          </ul>
        </div>
      </div>
			<button onClick={exit} >logout</button>
    </div>
  );
}

export default UserProfile;
