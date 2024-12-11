import React, { useEffect, useState } from 'react';
import './Sidebar.css';

function Sidebar({ onSelectMenu, roleId }) {
  const [activeMenu, setActiveMenu] = useState('Личный кабинет');
	// const [menu, setMenu] = useState(
	// 	['Личный кабинет', 'Занятия', 'Преподаватели', 'Вакансии', 'Об Организации', 'Настройки']
	// )

	var menu = []
	if (roleId == 2) {
		menu = ['Личный кабинет', 'Занятия', 'Студенты', 'Настройки']
	} else if (roleId == 3) {
		menu = ['Личный кабинет', 'Студенты', 'Вакансии', 'Настройки']
	} else {
		menu = 	['Личный кабинет', 'Занятия', 'Преподаватели', 'Вакансии', 'Об Организации', 'Настройки']
	}

  const handleClick = (menuItem) => {
    setActiveMenu(menuItem);
    onSelectMenu(menuItem);
  };
	useEffect(() => {
	if (roleId == 2) {
		setMenu(['Личный кабинет', 'Занятия', 'Студенты', 'Настройки'])
	} else if (roleId == 3) {
		setMenu(['Личный кабинет', 'Студенты', 'Вакансии', 'Настройки'])
	}}, [])

  return (
    <div className="sidebar">
      <h2>Навигация</h2>
      <ul className="menu">
        {menu.map((item) => (
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
