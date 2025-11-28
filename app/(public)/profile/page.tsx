"use client";

import React, { useState, useEffect } from "react";
import NavbarFinal from "@/components/navbar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { Input } from "@/components/ui/input";
import { Mail, Lock, Settings } from "lucide-react";
import appData from "../../../app-data.json";

interface UserProfile {
  id?: string;
  name: string;
  email: string;
  avatar: string;
  favoriteInstrument: string;
  subscriptionPlan: string;
  subscriptionStatus: string;
}

interface EditState {
  editingEmail: boolean;
  editingPassword: boolean;
  newEmail?: string;
  currentPassword?: string;
  newPassword?: string;
}

export default function Profile() {
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [userProfile, setUserProfile] = useState<UserProfile>({
    name: "---",
    email: "---",
    avatar: "",
    favoriteInstrument: "---",
    subscriptionPlan: "---",
    subscriptionStatus: "---",
  });

  const [editState, setEditState] = useState<EditState>({
    editingEmail: false,
    editingPassword: false,
  });

  useEffect(() => {
    setMounted(true);
    
    // Buscar dados do localStorage e JSON
    const loadProfileData = () => {
      // Buscar dados do localStorage
      const localUser = localStorage.getItem("user");
      let favoriteInstrumentId: string | null = null;
      
      if (localUser) {
        try {
          const userObj = JSON.parse(localUser);
          favoriteInstrumentId = userObj?.favoriteInstrumentId || null;
        } catch (e) {
          // ignore parse errors
        }
      }

      // Buscar informações do instrumento no JSON
      const instruments = (appData as any).instruments || [];
      let instrumentName = "---";
      
      if (favoriteInstrumentId) {
        const instrument = instruments.find((inst: any) => inst.id === favoriteInstrumentId);
        if (instrument) {
          instrumentName = instrument.name || "---";
        }
      }

      // Buscar dados do usuário do localStorage primeiro
      let userData = {
        name: "---",
        email: "---",
        avatar: "",
        subscriptionPlan: "---",
        subscriptionStatus: "---",
      };

      if (localUser) {
        try {
          const userObj = JSON.parse(localUser);
          const userId = userObj?.id || userObj?.userId;
          
          if (userId) {
            // Buscar dados do usuário do JSON
            const users = (appData as any).users || [];
            const foundUser = users.find((u: any) => u.id === userId);
            
            if (foundUser) {
              // Buscar plano de assinatura
              const subscriptions = (appData as any).subscriptions || [];
              const userSubscription = subscriptions.find((sub: any) => sub.userId === foundUser.id);
              const pricingPlans = (appData as any).pricingPlans || [];
              let planName = "---";
              
              if (userSubscription) {
                const plan = pricingPlans.find((p: any) => p.id === userSubscription.planType);
                if (plan) {
                  planName = plan.name || "---";
                }
              }

              userData = {
                name: foundUser.name || "---",
                email: foundUser.email || "---",
                avatar: foundUser.avatarUrl || "",
                subscriptionPlan: planName,
                subscriptionStatus: userSubscription?.status || "---",
              };
            }
          }
        } catch (e) {
          console.error("Erro ao processar dados do usuário:", e);
        }
      }

      setUserProfile({
        ...userData,
        favoriteInstrument: instrumentName,
      });
    };

    loadProfileData();
  }, []);

  const handleEmailEdit = () => {
    setEditState({ ...editState, editingEmail: !editState.editingEmail });
  };

  const handlePasswordEdit = () => {
    setEditState({ ...editState, editingPassword: !editState.editingPassword });
  };

  const handleConfirmEmail = () => {
    if (editState.newEmail) {
      setUserProfile({ ...userProfile, email: editState.newEmail });
      setEditState({ ...editState, editingEmail: false, newEmail: "" });
    }
  };

  const handleConfirmPassword = () => {
    // Validação e chamada à API
    setEditState({ ...editState, editingPassword: false, currentPassword: "", newPassword: "" });
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full relative bg-black">
      <NavbarFinal />

      <div className={`fixed inset-0 transition-all duration-300 ${
        open || openMobile ? "backdrop-blur-md bg-black/30 pointer-events-auto" : "pointer-events-none"
      }`} style={{ zIndex: 5 }} />

      <div className="relative z-10 min-h-screen overflow-y-auto overflow-x-hidden pt-20 px-6 pb-20">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-white mb-12">Meu Perfil</h1>

          {/* Profile Header */}
          <Card className="bg-gray-900/60 border-gray-700 p-8 mb-8">
            <div className="flex items-start gap-8">
              <img
                src={userProfile.avatar}
                alt={userProfile.name}
                className="w-32 h-32 rounded-full object-cover border-2 border-yellow-400"
              />

              <div className="flex-1">
                <h2 className="text-4xl font-bold text-white mb-4">{userProfile.name}</h2>

                <div className="space-y-3 mb-6">
                  <div>
                    <p className="text-gray-400 text-sm">Email</p>
                    <p className="text-white text-lg">{userProfile.email}</p>
                  </div>

                  <div>
                    <p className="text-gray-400 text-sm">Instrumento Favorito</p>
                    <p className="text-white text-lg">{userProfile.favoriteInstrument}</p>
                  </div>

                  <div>
                    <p className="text-gray-400 text-sm">Plano de Assinatura</p>
                    <p className="text-yellow-400 text-lg font-bold">{userProfile.subscriptionPlan}</p>
                  </div>
                </div>

                <Button className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold">
                  Estender Assinatura
                </Button>
              </div>
            </div>
          </Card>

          {/* Settings */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <Settings className="w-6 h-6" /> Configurações
            </h3>

            {/* Email Edit */}
            <Card className="bg-gray-900/60 border-gray-700 p-6">
              <div className="flex items-center gap-4">
                <Mail className="w-6 h-6 text-gray-400" />
                <div className="flex-1">
                  <p className="text-gray-400 mb-2">Email Atual</p>
                  <p className="text-white font-semibold">{userProfile.email}</p>
                </div>
                <Button
                  variant="outline"
                  className="border-gray-600 text-gray-300"
                  onClick={handleEmailEdit}
                >
                  {editState.editingEmail ? "Cancelar" : "Editar"}
                </Button>
              </div>

              {editState.editingEmail && (
                <div className="mt-6 space-y-4 border-t border-gray-700 pt-6">
                  <div>
                    <label className="text-gray-400 text-sm">Email Atual</label>
                    <Input
                      type="email"
                      value={userProfile.email}
                      disabled
                      className="bg-gray-800/50 border-gray-600 text-gray-400"
                    />
                  </div>
                  <div>
                    <label className="text-gray-400 text-sm">Novo Email</label>
                    <Input
                      type="email"
                      placeholder="Novo email"
                      value={editState.newEmail || ""}
                      onChange={(e) => setEditState({ ...editState, newEmail: e.target.value })}
                      className="bg-gray-800/50 border-gray-600"
                    />
                  </div>
                  <div className="flex gap-3">
                    <Button
                      className="flex-1 bg-gray-700 hover:bg-gray-600 text-white"
                      onClick={() => setEditState({ ...editState, editingEmail: false })}
                    >
                      Cancelar
                    </Button>
                    <Button
                      className="flex-1 bg-yellow-400 hover:bg-yellow-500 text-black font-bold"
                      onClick={handleConfirmEmail}
                    >
                      Confirmar
                    </Button>
                  </div>
                </div>
              )}
            </Card>

            {/* Password Edit */}
            <Card className="bg-gray-900/60 border-gray-700 p-6">
              <div className="flex items-center gap-4">
                <Lock className="w-6 h-6 text-gray-400" />
                <div className="flex-1">
                  <p className="text-gray-400 mb-2">Senha</p>
                  <p className="text-white font-semibold">••••••••••••••••</p>
                </div>
                <Button
                  variant="outline"
                  className="border-gray-600 text-gray-300"
                  onClick={handlePasswordEdit}
                >
                  {editState.editingPassword ? "Cancelar" : "Editar"}
                </Button>
              </div>

              {editState.editingPassword && (
                <div className="mt-6 space-y-4 border-t border-gray-700 pt-6">
                  <div>
                    <label className="text-gray-400 text-sm">Senha Atual</label>
                    <Input
                      type="password"
                      placeholder="Senha atual"
                      value={editState.currentPassword || ""}
                      onChange={(e) => setEditState({ ...editState, currentPassword: e.target.value })}
                      className="bg-gray-800/50 border-gray-600"
                    />
                  </div>
                  <div>
                    <label className="text-gray-400 text-sm">Nova Senha</label>
                    <Input
                      type="password"
                      placeholder="Nova senha"
                      value={editState.newPassword || ""}
                      onChange={(e) => setEditState({ ...editState, newPassword: e.target.value })}
                      className="bg-gray-800/50 border-gray-600"
                    />
                  </div>
                  <div className="flex gap-3">
                    <Button
                      className="flex-1 bg-gray-700 hover:bg-gray-600 text-white"
                      onClick={() => setEditState({ ...editState, editingPassword: false })}
                    >
                      Cancelar
                    </Button>
                    <Button
                      className="flex-1 bg-yellow-400 hover:bg-yellow-500 text-black font-bold"
                      onClick={handleConfirmPassword}
                    >
                      Confirmar
                    </Button>
                  </div>
                </div>
              )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
