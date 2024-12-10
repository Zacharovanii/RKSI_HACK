import axios from "axios"

export default class ZnaniumApi {
	static async regin(userData) {
		const response = await axios.post("http://127.0.0.1:8000/auth/register", userData)
		return response
	}

	static async login(email, password) {
		const params = {
			// grant_type: "password",
			username: email,
			password: password

		}
		const response = await axios.post("http://127.0.0.1:8000/auth/jwt/login", params,{
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			}})
		return response
	}

	static async logout() {
		const response = await axios.post("http://127.0.0.1:8000/auth/jwt/logout")
		return response
	}

	static async getUserProfileData() {
		const response = await axios.get("http://127.0.0.1:8000/my-profile", {
			headers: {
				Accept: "application/json"
			}
		})
		return response
	}
}