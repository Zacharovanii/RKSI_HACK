import React from 'react';
import UserProfile from '../UserProfile/UserProfile';
import './ContentArea.css';
import LectureList from '../LecturesList';

function ContentArea({ selectedMenu }) {
  const renderContent = () => {
    switch (selectedMenu) {
      case 'Личный кабинет':
        return <UserProfile /> ;
      case 'Занятия':
        return <LectureList/>;
      case 'Преподаватели':
        return <div>Контент для Преподавателей</div>;
      case 'Вакансии':
        return <div>Контент для Вакансий</div>;
      case 'Об Организации':
        return <div>Контент для Об Организации</div>;
      case 'Настройки':
        return <div>Контент для Настроек</div>;
      default:
        return <div>Выберите опцию из меню</div>;
    }
  };

  return (
    <div className="content">
      {renderContent()}
    </div>
  );
}

export default ContentArea;
