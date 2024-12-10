import React from "react";
import { AuthProvider } from "./hooks/authContext";
import Router from "./components/Router";


function App() {
	return (
		<AuthProvider>
			<Router/>
		</AuthProvider>
	);
}

export default App;
