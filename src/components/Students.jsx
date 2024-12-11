import React, {useState, useEffect } from 'react'
import ZnaniumApi from '../API/API'

function Students() {
	const [stud, setStud] = useState([])

	useEffect(() => {
		async function getStud() {
				const response = await ZnaniumApi.getStudents()
				return response
		}
		getStud.then((studs) => {
			console.log(studs);
			
			setStud(studs.data)
		})
	}, [])


	return (
		<div>Students</div>
	)
}

export default Students