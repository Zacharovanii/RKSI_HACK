import React from 'react';
import './UserProfile.css';

function UserProfile() {
  return (
    <div className="user-profile">
      <div className="user-info">
        <div className="avatar"></div>
        <div className="user-details">
          <h2>Иванов Иван Иванович</h2>
          <p>+7 (800) 555-35-35</p>
          <p>pochta@gmail.ru</p>
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
    </div>
  );
}

export default UserProfile;
