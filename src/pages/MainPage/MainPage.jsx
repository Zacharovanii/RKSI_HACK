import React, { useState } from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import ContentArea from '../../components/ContentArea/ContentArea';
import './MainPage.css';

function MainPage() {
  const [selectedMenu, setSelectedMenu] = useState('Личный кабинет');

  const handleMenuSelect = (menuItem) => {
    setSelectedMenu(menuItem);
  };

  return (
    <div className="appContainer">
      <Sidebar onSelectMenu={handleMenuSelect} />
      <ContentArea selectedMenu={selectedMenu} />
    </div>
  );
}

export default MainPage;
