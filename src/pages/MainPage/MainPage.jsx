import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/Sidebar/Sidebar';
import ContentArea from '../../components/ContentArea/ContentArea';
import './MainPage.css';
import ZnaniumApi from '../../API/API';

function MainPage() {
  const [selectedMenu, setSelectedMenu] = useState('Личный кабинет');

  const handleMenuSelect = (menuItem) => {
    setSelectedMenu(menuItem);
  };

	const [roleId, setRoleId] = useState(0)
	
	useEffect(() => {
		async function getUser() {
			const response = await ZnaniumApi.getUserProfileData()
			return response.data.user
		}
		getUser().then(({role_id}) => {
      if (role_id) {
				console.log(role_id);
				
        setRoleId(role_id);
      }
    });
  }, []);


  return (
    <div className="appContainer">
      <Sidebar onSelectMenu={handleMenuSelect} roleId={roleId} />
      <ContentArea selectedMenu={selectedMenu} roleId={roleId} />
    </div>
  );
}

export default MainPage;
