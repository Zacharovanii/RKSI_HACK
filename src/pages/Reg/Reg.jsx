import React, { useState } from "react";
import { useAuth } from "../../hooks/authContext";
import { Link, useNavigate } from "react-router-dom";
import "./Reg.css";


function Reg() {
	const { login } = useAuth()
	const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "teacher",
		phone: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Submitted data:", formData);
    // Api

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
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Role:
          <select
            name="role"
            value={formData.role}
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
