import React from "react";
import { Link } from "react-router-dom";
import "./Greet.css";

function Greet() {
  return (
		<div className="main">
			<div className="container">
    	<h1 className="name">Знаниум</h1>
    	<p className="txt1">Обрзовательная платформа</p>

    	<Link to="/register">
          <button className="in btn">Регистрация</button>
        </Link>
        <Link to="/login">
          <button className="reg btn">Логин</button>
      </Link>
    </div>
		</div>
  );
}

export default Greet;
