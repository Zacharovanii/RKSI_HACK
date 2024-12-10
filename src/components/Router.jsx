import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "../hooks/authContext";
import React from 'react'
import Reg from "../pages/Reg/Reg"
import Login from "../pages/Login/Login"
import Greet from "../pages/Greet/Greet"
import MainPage from "../pages/MainPage/MainPage";

function Router() {
	const { isAuth } = useAuth()

	if (isAuth) {
		return (
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<MainPage/>} />
					<Route path="*" element={<Navigate to="/" replace />} />
				</Routes>
		</BrowserRouter>
		)
	}

	return (
		<BrowserRouter>
				<Routes>
					<Route path="/" element={<Greet />} />
					<Route path="/register" element={<Reg />} />
					<Route path="/login" element={<Login />} />

					<Route path="*" element={<Navigate to="/" replace />} />
				</Routes>
		</BrowserRouter>
	)
}

export default Router