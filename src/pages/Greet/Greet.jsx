import React from "react";
import { Link } from "react-router-dom";
import "./Greet.css";

function Greet() {
  return (
    <div className="home-container">
      <h1>Знаниум</h1>
      <p>Добро пожаловать! Выберите действие:</p>
      <div className="home-buttons">
        <Link to="/register">
          <button className="home-button">Регистрация</button>
        </Link>
        <Link to="/login">
          <button className="home-button">Логин</button>
        </Link>
      </div>
    </div>
  );
}

export default Greet;
