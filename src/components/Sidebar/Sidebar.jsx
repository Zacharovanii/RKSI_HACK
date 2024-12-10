import React, { useState } from 'react';
import './Sidebar.css';

function Sidebar({ onSelectMenu }) {
  const [activeMenu, setActiveMenu] = useState('Личный кабинет');

  const handleClick = (menuItem) => {
    setActiveMenu(menuItem);
    onSelectMenu(menuItem);
  };

  return (
    <div className="sidebar">
      <h2>Навигация</h2>
      <ul className="menu">
        {['Личный кабинет', 'Занятия', 'Преподаватели', 'Вакансии', 'Об Организации', 'Настройки'].map((item) => (
          <li
            key={item}
            className={`menuItem ${activeMenu === item ? 'active' : ''}`}
            onClick={() => handleClick(item)}
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Sidebar;
