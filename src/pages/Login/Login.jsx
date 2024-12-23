import React, { useState } from "react";
import { useAuth } from "../../hooks/authContext";
import { Link, useNavigate } from "react-router-dom";
import ZnaniumApi from "../../API/API";
import "./Login.css";

function Login() {
	const { login } = useAuth()
	const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    phone: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Login data:", formData);
    // Api

		const response = await ZnaniumApi.login(formData.email, formData.password)
		console.log(response);
		
		login()
		navigate("/")
  };

  return (
    <div className="login-container">
      <h1>Login</h1>
      <form className="login-form" onSubmit={handleSubmit}>
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Password:
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </label>
				
        <button type="submit">Login</button>
      </form>
			<p>
        Don’t have an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}

export default Login;
