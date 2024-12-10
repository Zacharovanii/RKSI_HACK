import React, { useState } from "react";
import { useAuth } from "../../hooks/authContext";
import { Link, useNavigate } from "react-router-dom";
import ZnaniumAPI from "../../API/API";
import "./Reg.css";


function Reg() {
	const { login } = useAuth()
	const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role_id: "teacher",
		phone_number: "",
  });

	const mapRoleToId = (role) => {
		switch (role) {
			case "student":
				return 1;
			case "teacher":
				return 2;
			case "employer":
				return 3;
			case "admin":
				return 4;
			default:
				return 0;
		}
	}

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
		const userData = {
			...formData,
			role_id: mapRoleToId(formData.role_id),
			is_active: true,
    	is_superuser: false,
    	is_verified: false,
		};
		console.log(userData);
		try {
			const response = await ZnaniumAPI.regin(userData)
			console.log(response);
			API.login(userData.email, userData.password)
		}
		catch (error){ 
			console.log(error);
			
		}
		
		login()
		navigate("/")
  };

  return (
    <div className="registration-container">
      <h1>Register</h1>
      <form className="registration-form" onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </label>

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

				<label>
          Phone:
          <input
            type="tel"
            name="phone_number"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Role:
          <select
            name="role_id"
            value={formData.role_id}
            onChange={handleChange}
          >
            <option value="teacher">Teacher</option>
            <option value="student">Student</option>
            <option value="employer">Employer</option>
          </select>
        </label>

        <button type="submit">Register</button>
      </form>
			<p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </div>
  );
};

export default Reg;
