import React, { useEffect, useState } from 'react';
import UserProfile from '../UserProfile/UserProfile';
import './ContentArea.css';
import LectureList from '../LecturesList';
import { VacancyList } from '../Vacancies/Vacamcies';
import Teachers from '../Teachers';


function ContentArea({ selectedMenu, roleId }) {
		const renderContent = () => {
			switch (selectedMenu) {
				case 'Личный кабинет':
					return <UserProfile /> ;
				case 'Занятия':
					return <LectureList roleId={roleId} />;
				case 'Преподаватели':
					return <Teachers/>;
				case "Студенты":
					return <Students />
				case 'Вакансии':
					return <VacancyList/>;
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
