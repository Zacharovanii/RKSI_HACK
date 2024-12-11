import React, { useEffect, useState } from 'react'
import ZnaniumApi from '../API/API'


const User = ({ user }) => (
  <div className="user-card">
    <h3>{user.name}</h3>
    <p><strong>Email:</strong> {user.email}</p>
    <p><strong>Phone Number:</strong> {user.phone_number}</p>
  </div>
);

function Teachers() {
	const [teachers, setTeachers] = useState([])

	useEffect(() => {
		async function getTeachers() {
			const response = await ZnaniumApi.getTeachers()
			return response.data
		}
		getTeachers().then(t => {
			console.log(t.users);
			
			setTeachers(t.users)
		})
	}, [])

	return (
		<>
		{teachers.map((el) => ( 
			<User user={el}/>
		))}
		</>
	)
}

export default Teachers