"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import NavbarFinal from "@/components/navbar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { Clock, TrendingUp, Medal, Star } from "lucide-react";
import appData from "../../../app-data.json";

interface StatCard {
  icon: React.ReactNode;
  label: string;
  value: number | string;
}

interface PracticeData {
  practiceTime?: number;
  dayStreak?: number;
  division?: number;
  stars?: number;
  favoriteInstrument: string;
  instrumentImage: string;
}

export default function PracticeArea() {
  const router = useRouter();
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [practiceData, setPracticeData] = useState<PracticeData>({
    practiceTime: undefined,
    dayStreak: undefined,
    division: undefined,
    stars: undefined,
    favoriteInstrument: "---",
    instrumentImage: "",
  });

  useEffect(() => {
    setMounted(true);
    
    // Buscar dados do localStorage e JSON
    const loadPracticeData = () => {
      // Buscar instrumento favorito do localStorage
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
      let instrumentImage = "";
      
      if (favoriteInstrumentId) {
        const instrument = instruments.find((inst: any) => inst.id === favoriteInstrumentId);
        if (instrument) {
          instrumentName = instrument.name || "---";
          instrumentImage = instrument.imageUrl || "";
        }
      }

      // Buscar estatísticas do usuário do JSON baseado no userId do localStorage
      const userStatistics = (appData as any).userStatistics || [];
      let stats = {
        practiceTime: undefined as number | undefined,
        dayStreak: undefined as number | undefined,
        division: undefined as number | undefined,
        stars: undefined as number | undefined,
      };

      if (localUser) {
        try {
          const userObj = JSON.parse(localUser);
          const userId = userObj?.id || userObj?.userId;
          
          console.log("🔍 [PRACTICE] Buscando estatísticas para userId:", userId);
          
          if (userId) {
            // Primeiro tenta buscar do localStorage (estatísticas atualizadas)
            const localStats = localStorage.getItem(`userStats_${userId}`);
            if (localStats) {
              try {
                const parsedStats = JSON.parse(localStats);
                console.log("✅ [PRACTICE] Estatísticas encontradas no localStorage:", parsedStats);
                stats = {
                  practiceTime: parsedStats.totalPracticeTime,
                  dayStreak: parsedStats.currentStreak,
                  division: parsedStats.totalSessions,
                  stars: parsedStats.totalStars,
                };
              } catch (e) {
                console.warn("⚠️ [PRACTICE] Erro ao parsear estatísticas do localStorage:", e);
              }
            }
            
            // Se não encontrou no localStorage, busca no JSON
            if (stats.practiceTime === undefined) {
              const userStats = userStatistics.find((stat: any) => stat.userId === userId);
              if (userStats) {
                console.log("✅ [PRACTICE] Estatísticas encontradas no JSON:", userStats);
                stats = {
                  practiceTime: userStats.totalPracticeTime,
                  dayStreak: userStats.currentStreak,
                  division: userStats.totalSessions,
                  stars: userStats.totalStars,
                };
              } else {
                console.warn("⚠️ [PRACTICE] Nenhuma estatística encontrada para userId:", userId);
              }
            }
          } else {
            console.warn("⚠️ [PRACTICE] userId não encontrado no objeto do usuário");
          }
        } catch (e) {
          console.error("❌ [PRACTICE] Erro ao processar estatísticas do usuário:", e);
        }
      } else {
        console.warn("⚠️ [PRACTICE] Nenhum usuário encontrado no localStorage");
      }

      setPracticeData({
        practiceTime: stats.practiceTime,
        dayStreak: stats.dayStreak,
        division: stats.division,
        stars: stats.stars,
        favoriteInstrument: instrumentName,
        instrumentImage: instrumentImage,
      });
    };

    loadPracticeData();
  }, []);

  const statCards: StatCard[] = [
    {
      icon: <Clock className="w-8 h-8" />,
      label: "Practice time",
      value: practiceData.practiceTime,
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      label: "Day Streak",
      value: practiceData.dayStreak,
    },
    {
      icon: <Medal className="w-8 h-8" />,
      label: "Division",
      value: practiceData.division,
    },
    {
      icon: <Star className="w-8 h-8" />,
      label: "Stars",
      value: practiceData.stars,
    },
  ];

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full relative bg-black overflow-y-auto overflow-x-hidden">
      <NavbarFinal />

      <div className={`fixed inset-0 transition-all duration-300 ${
        open || openMobile ? "backdrop-blur-md bg-black/30 pointer-events-auto" : "pointer-events-none"
      }`} style={{ zIndex: 5 }} />

      <div className="relative z-10 pt-20 px-6 pb-20">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-5xl font-bold text-white mb-12">Área de Prática</h1>

          <div className="grid grid-cols-2 gap-6 mb-12">
            {statCards.map((stat, idx) => (
              <Card key={idx} className="bg-gray-900/60 border-gray-700 p-6 hover:bg-gray-900/80 transition-colors">
                <div className="flex flex-col items-center gap-3">
                  <div className="text-gray-400">{stat.icon}</div>
                  <span className="text-3xl font-bold text-white">
                    {stat.value !== undefined ? stat.value : "---"}
                  </span>
                  <span className="text-gray-400 text-sm">{stat.label}</span>
                </div>
              </Card>
            ))}
          </div>

          {/* Instrumento favorito */}
          <Card className="bg-gray-900/60 border-gray-700 p-8">
            <div className="grid grid-cols-2 gap-8">
              <div>
                <h2 className="text-2xl font-bold text-white mb-6">Instrument Favorito</h2>
                {practiceData.instrumentImage ? (
                  <img
                    src={practiceData.instrumentImage}
                    alt={practiceData.favoriteInstrument}
                    className="w-full h-auto rounded-lg"
                  />
                ) : (
                  <div className="w-full h-64 bg-gray-800/50 rounded-lg flex items-center justify-center">
                    <span className="text-gray-500 text-lg">---</span>
                  </div>
                )}
              </div>

              <div className="flex flex-col justify-center">
                <div className="bg-gray-800/50 rounded-lg p-6 mb-6">
                  <p className="text-gray-400 mb-2">Instrumento:</p>
                  <p className="text-3xl font-bold text-white">{practiceData.favoriteInstrument}</p>
                </div>

                <div className="space-y-4">
                  <Button 
                    onClick={() => router.push("/practice-session")}
                    className="w-full bg-yellow-400 hover:bg-yellow-500 text-black font-bold py-6 text-lg"
                  >
                    Começar Sessão de Prática
                  </Button>
                  <Button variant="outline" className="w-full border-gray-600 text-gray-300 hover:bg-gray-800 py-6">
                    Ver Histórico
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
