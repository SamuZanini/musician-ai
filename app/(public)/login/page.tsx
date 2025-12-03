"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Eye, EyeOff } from "lucide-react";
import appData from "../../../app-data.json";

export default function Login() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [rememberMe, setRememberMe] = useState(false);

  // Carregar email salvo se "Remember me" estava marcado
  useEffect(() => {
    const savedEmail = localStorage.getItem("rememberEmail");
    if (savedEmail) {
      setEmail(savedEmail);
      setRememberMe(true);
    }
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    // Simular validação (em produção, seria uma chamada à API)
    setTimeout(() => {
      const users = (appData as any).users || [];
      const user = users.find((u: any) => u.email === email);

      if (user) {
        // Salvar usuário no localStorage
        const userData = {
          id: user.id,
          name: user.name,
          email: user.email,
          avatarUrl: user.avatarUrl,
          favoriteInstrumentId: user.favoriteInstrumentId,
          subscriptionPlan: user.subscriptionPlan,
        };

        localStorage.setItem("user", JSON.stringify(userData));

        if (rememberMe) {
          localStorage.setItem("rememberEmail", email);
        } else {
          localStorage.removeItem("rememberEmail");
        }

        // Redirecionar para a página de prática
        router.push("/practice");
      } else {
        setError("Email ou senha inválidos");
        setIsLoading(false);
      }
    }, 1500);
  };

  return (
    <div className="min-h-screen w-full relative bg-black overflow-hidden">
      {/* Fundo com instrumentos musicais em neon */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Guitarra Elétrica (Roxa) - Topo Centro */}
        <div className="absolute top-20 left-1/2 -translate-x-1/2 opacity-60">
          <svg
            className="w-48 h-48"
            viewBox="0 0 200 200"
            fill="none"
            style={{ filter: "drop-shadow(0 0 10px rgba(168, 85, 247, 0.8))" }}
          >
            <path
              d="M100 20 L120 40 L120 80 L140 100 L140 140 L120 160 L100 180 L80 160 L60 140 L60 100 L80 80 L80 40 Z"
              stroke="#a855f7"
              strokeWidth="3"
              fill="none"
            />
            <rect x="90" y="60" width="20" height="40" stroke="#a855f7" strokeWidth="2" fill="none" />
            <line x1="100" y1="20" x2="100" y2="180" stroke="#a855f7" strokeWidth="2" />
          </svg>
        </div>

        {/* Acordeão (Verde) - Esquerda */}
        <div className="absolute left-10 top-1/3 opacity-50">
          <svg
            className="w-64 h-96"
            viewBox="0 0 150 250"
            fill="none"
            style={{ filter: "drop-shadow(0 0 8px rgba(34, 197, 94, 0.8))" }}
          >
            <rect x="20" y="30" width="110" height="190" rx="10" stroke="#22c55e" strokeWidth="3" fill="none" />
            <line x1="30" y1="50" x2="120" y2="50" stroke="#22c55e" strokeWidth="2" />
            <line x1="30" y1="80" x2="120" y2="80" stroke="#22c55e" strokeWidth="2" />
            <line x1="30" y1="110" x2="120" y2="110" stroke="#22c55e" strokeWidth="2" />
            <line x1="30" y1="140" x2="120" y2="140" stroke="#22c55e" strokeWidth="2" />
            <line x1="30" y1="170" x2="120" y2="170" stroke="#22c55e" strokeWidth="2" />
            <line x1="30" y1="200" x2="120" y2="200" stroke="#22c55e" strokeWidth="2" />
            <circle cx="75" cy="35" r="8" stroke="#22c55e" strokeWidth="2" fill="none" />
          </svg>
        </div>

        {/* Saxofone (Amarelo) - Direita Superior */}
        <div className="absolute right-32 top-40 opacity-50">
          <svg
            className="w-56 h-80"
            viewBox="0 0 200 300"
            fill="none"
            style={{ filter: "drop-shadow(0 0 8px rgba(234, 179, 8, 0.8))" }}
          >
            <path
              d="M50 20 Q60 40 70 60 Q80 100 90 140 Q100 180 110 220 Q120 250 130 280"
              stroke="#eab308"
              strokeWidth="4"
              fill="none"
            />
            <ellipse cx="110" cy="220" rx="30" ry="50" stroke="#eab308" strokeWidth="3" fill="none" />
            <circle cx="70" cy="60" r="8" stroke="#eab308" strokeWidth="2" fill="none" />
            <circle cx="90" cy="140" r="8" stroke="#eab308" strokeWidth="2" fill="none" />
            <line x1="50" y1="20" x2="60" y2="10" stroke="#eab308" strokeWidth="3" />
          </svg>
        </div>

        {/* Trompete (Amarelo) - Direita Meio */}
        <div className="absolute right-24 top-1/2 opacity-50">
          <svg
            className="w-48 h-64"
            viewBox="0 0 200 250"
            fill="none"
            style={{ filter: "drop-shadow(0 0 8px rgba(234, 179, 8, 0.8))" }}
          >
            <path
              d="M100 20 Q120 40 140 60 Q160 80 170 100 Q180 120 180 140 Q170 160 150 180 Q130 200 100 220"
              stroke="#eab308"
              strokeWidth="4"
              fill="none"
            />
            <circle cx="100" cy="20" r="15" stroke="#eab308" strokeWidth="3" fill="none" />
            <line x1="150" y1="180" x2="160" y2="200" stroke="#eab308" strokeWidth="3" />
          </svg>
        </div>

        {/* Violino (Vermelho) - Inferior Esquerda */}
        <div className="absolute bottom-32 left-20 opacity-50">
          <svg
            className="w-40 h-64"
            viewBox="0 0 150 250"
            fill="none"
            style={{ filter: "drop-shadow(0 0 8px rgba(239, 68, 68, 0.8))" }}
          >
            <ellipse cx="75" cy="50" rx="30" ry="40" stroke="#ef4444" strokeWidth="3" fill="none" />
            <rect x="70" y="90" width="10" height="120" rx="5" stroke="#ef4444" strokeWidth="3" fill="none" />
            <path
              d="M45 50 Q30 60 20 80 Q15 100 20 120 Q25 140 35 150"
              stroke="#ef4444"
              strokeWidth="3"
              fill="none"
            />
            <path
              d="M105 50 Q120 60 130 80 Q135 100 130 120 Q125 140 115 150"
              stroke="#ef4444"
              strokeWidth="3"
              fill="none"
            />
            <line x1="75" y1="50" x2="75" y2="90" stroke="#ef4444" strokeWidth="2" />
          </svg>
        </div>

        {/* Flauta (Verde) - Inferior Centro */}
        <div className="absolute bottom-24 left-1/2 -translate-x-1/2 opacity-50">
          <svg
            className="w-32 h-48"
            viewBox="0 0 100 200"
            fill="none"
            style={{ filter: "drop-shadow(0 0 8px rgba(34, 197, 94, 0.8))" }}
          >
            <line x1="50" y1="20" x2="50" y2="180" stroke="#22c55e" strokeWidth="4" />
            <circle cx="50" cy="50" r="6" stroke="#22c55e" strokeWidth="2" fill="none" />
            <circle cx="50" cy="80" r="6" stroke="#22c55e" strokeWidth="2" fill="none" />
            <circle cx="50" cy="110" r="6" stroke="#22c55e" strokeWidth="2" fill="none" />
            <circle cx="50" cy="140" r="6" stroke="#22c55e" strokeWidth="2" fill="none" />
            <circle cx="50" cy="170" r="6" stroke="#22c55e" strokeWidth="2" fill="none" />
          </svg>
        </div>

        {/* Tambor (Branco) - Inferior Direita */}
        <div className="absolute bottom-20 right-16 opacity-40">
          <svg
            className="w-48 h-48"
            viewBox="0 0 200 200"
            fill="none"
            style={{ filter: "drop-shadow(0 0 8px rgba(255, 255, 255, 0.8))" }}
          >
            <ellipse cx="100" cy="100" rx="60" ry="40" stroke="#ffffff" strokeWidth="3" fill="none" />
            <ellipse cx="100" cy="80" rx="60" ry="5" stroke="#ffffff" strokeWidth="2" fill="none" />
            <ellipse cx="100" cy="120" rx="60" ry="5" stroke="#ffffff" strokeWidth="2" fill="none" />
            <line x1="40" y1="80" x2="40" y2="120" stroke="#ffffff" strokeWidth="2" />
            <line x1="160" y1="80" x2="160" y2="120" stroke="#ffffff" strokeWidth="2" />
          </svg>
        </div>
      </div>

      {/* Conteúdo principal */}
      <div className="relative z-10 min-h-screen flex items-center justify-center px-4 py-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-16 max-w-7xl w-full items-center">
          {/* Lado esquerdo - Formulário */}
          <div className="flex flex-col justify-center z-20">
            <div className="bg-white rounded-2xl shadow-2xl p-8 lg:p-10 w-full max-w-md mx-auto">
              {/* Título */}
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Sign In</h2>
              <p className="text-gray-600 mb-8">Entre na sua conta para continuar</p>

              {/* Formulário */}
              <form onSubmit={handleLogin} className="space-y-5">
                {/* Email */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-800">Email</label>
                  <Input
                    type="email"
                    placeholder="Value"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-white border-gray-300 text-gray-900 placeholder-gray-400 h-12 rounded-lg text-base"
                    required
                  />
                </div>

                {/* Senha */}
                <div className="space-y-2">
                  <label className="block text-sm font-medium text-gray-800">Password</label>
                  <div className="relative">
                    <Input
                      type={showPassword ? "text" : "password"}
                      placeholder="Value"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="bg-white border-gray-300 text-gray-900 placeholder-gray-400 h-12 rounded-lg text-base pr-12"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                  </div>
                </div>

                {/* Erro */}
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                {/* Remember me e Forgot password */}
                <div className="flex items-center justify-between text-sm">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="w-4 h-4 rounded border-gray-300 text-gray-900 cursor-pointer"
                    />
                    <span className="text-gray-700">Remember me</span>
                  </label>
                  <a
                    href="/forgot-password"
                    className="text-gray-600 hover:text-gray-800 font-medium"
                  >
                    Forgot password?
                  </a>
                </div>

                {/* Botão Sign In */}
                <Button
                  type="submit"
                  disabled={isLoading}
                  className="w-full h-12 bg-gray-800 hover:bg-gray-900 text-white font-semibold text-base rounded-lg transition-all duration-300 disabled:opacity-50"
                >
                  {isLoading ? (
                    <div className="flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                      Entrando...
                    </div>
                  ) : (
                    "Sign In"
                  )}
                </Button>

                {/* Botão Create Account */}
                <Button
                  type="button"
                  onClick={() => router.push("/signup")}
                  className="w-full h-12 bg-gray-800 hover:bg-gray-900 text-white font-semibold text-base rounded-lg transition-all duration-300"
                >
                  Create Account
                </Button>
              </form>
            </div>
          </div>

          {/* Lado direito - Clave de Fá Metálica */}
          <div className="hidden lg:flex items-center justify-center h-full">
            <div className="relative w-full h-[600px] flex items-center justify-center">
              {/* Efeito de brilho metálico */}
              <div
                className="absolute inset-0 bg-gradient-to-br from-amber-600 via-amber-700 to-amber-800 rounded-full blur-3xl opacity-30"
                style={{ width: "500px", height: "500px" }}
              />

              {/* Clave de Fá SVG com efeito metálico */}
              <svg
                className="relative z-10 w-full h-full max-w-[400px] max-h-[600px]"
                viewBox="0 0 200 600"
                fill="none"
                style={{
                  filter: "drop-shadow(0 0 30px rgba(217, 119, 6, 0.5))",
                }}
              >
                <defs>
                  <linearGradient id="metallicGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#d97706" stopOpacity="1" />
                    <stop offset="30%" stopColor="#f59e0b" stopOpacity="1" />
                    <stop offset="50%" stopColor="#d97706" stopOpacity="1" />
                    <stop offset="70%" stopColor="#92400e" stopOpacity="1" />
                    <stop offset="100%" stopColor="#78350f" stopOpacity="1" />
                  </linearGradient>
                  <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                    <feMerge>
                      <feMergeNode in="coloredBlur" />
                      <feMergeNode in="SourceGraphic" />
                    </feMerge>
                  </filter>
                </defs>

                {/* Clave de Fá principal */}
                <path
                  d="M100 50 
                      Q90 80 85 120 
                      Q80 160 90 200 
                      Q100 240 110 280 
                      Q120 320 115 360 
                      Q110 400 100 440 
                      Q90 480 95 520 
                      Q100 550 110 550 
                      Q120 550 125 520 
                      Q130 490 135 450 
                      Q140 410 145 370 
                      Q150 330 155 290 
                      Q160 250 165 210 
                      Q170 170 175 130 
                      Q180 90 170 60 
                      Q160 30 140 20 
                      Q120 10 100 50 Z"
                  fill="url(#metallicGradient)"
                  stroke="#92400e"
                  strokeWidth="2"
                  filter="url(#glow)"
                />

                {/* Detalhes internos da clave */}
                <ellipse
                  cx="100"
                  cy="200"
                  rx="25"
                  ry="35"
                  fill="none"
                  stroke="#78350f"
                  strokeWidth="1.5"
                  opacity="0.6"
                />
                <ellipse
                  cx="100"
                  cy="350"
                  rx="20"
                  ry="30"
                  fill="none"
                  stroke="#78350f"
                  strokeWidth="1.5"
                  opacity="0.6"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
