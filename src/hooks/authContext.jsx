import React, { createContext, useState, useEffect, useContext } from 'react';

// Контекст авторизации
const AuthContext = createContext();

// Провайдер для контекста
export function AuthProvider({ children }) {
  const [isAuth, setIsAuth] = useState(() => {
    const savedAuth = localStorage.getItem('isAuth');
    return savedAuth === 'true';
  });

  useEffect(() => {
    localStorage.setItem('isAuth', isAuth);
  }, [isAuth]);

  const login = () => setIsAuth(true);
  const logout = () => setIsAuth(false);

  return (
    <AuthContext.Provider value={{ isAuth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
