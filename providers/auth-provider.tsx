"use client";

import { createContext, useContext, useState, useEffect } from "react";

interface AuthContextType {
  isAuthenticated: boolean;
  user: {
    name: string;
    email: string;
    profileImage: string;
  } | null;
  login: (userData: {
    name: string;
    email: string;
    profileImage: string;
  }) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<{
    name: string;
    email: string;
    profileImage: string;
  } | null>(null);

  // Carregar estado de autenticação do localStorage
  useEffect(() => {
    const savedAuth = localStorage.getItem("auth");
    if (savedAuth) {
      const authData = JSON.parse(savedAuth);
      setIsAuthenticated(authData.isAuthenticated);
      setUser(authData.user);
    }
  }, []);

  const login = (userData: {
    name: string;
    email: string;
    profileImage: string;
  }) => {
    setIsAuthenticated(true);
    setUser(userData);
    localStorage.setItem(
      "auth",
      JSON.stringify({
        isAuthenticated: true,
        user: userData,
      })
    );
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUser(null);
    localStorage.removeItem("auth");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
