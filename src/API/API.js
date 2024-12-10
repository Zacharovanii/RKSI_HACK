import axios from "axios"

export default class ZnaniumApi {
	static api = axios.create({
    baseURL: 'http://localhost:8000', 
    withCredentials: true,
  });

	static async regin(userData) {
		const response = await this.api.post("/auth/register", userData)
		return response
	}

	static async login(email, password) {
		const params = {
			grant_type: "password",
			username: email,
			password: password
		}

		const response = await this.api.post("/auth/jwt/login", params,{
			headers: {
				"Content-Type": "application/x-www-form-urlencoded",
			}})
		return response
	}

	static async logout() {
		const response = await this.api.post("/auth/jwt/logout")
		return response
	}

	static async getUserProfileData() {
		const response = await this.api.get("/my-profile", {
			headers: {
				Accept: "application/json"
			}
		})
		return response
	}

	static async getLectures() {
		const response = await this.api.get("/lecture")
		return response
	}

}