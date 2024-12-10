import React from 'react'
import { useAuth } from '../hooks/authContext'

function Test() {
	const { logout } = useAuth()
	return (
		<div
		style={{
			width: "100vw",
			height: "100vh",
		}}
		>
			<h1>
			Test
			</h1>
			<button onClick={() => {
				logout()
			}} >Logout</button>
			</div>
	)
}

export default Test