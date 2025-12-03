"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import NavbarFinal from "@/components/navbar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { Calendar, Clock, Zap, Target } from "lucide-react";
import appData from "../../../app-data.json";

interface SessionRecord {
  id: string;
  userId: string;
  instrumentId: string;
  startTime: string;
  startDate: string;
  startHour: string;
  endTime?: string;
  endHour?: string;
  durationMinutes?: number;
  accuracy?: number;
  starsEarned?: number;
}

interface Instrument {
  id: string;
  name: string;
  imageUrl?: string;
}

export default function PracticeHistory() {
  const router = useRouter();
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [sessions, setSessions] = useState<SessionRecord[]>([]);
  const [instrumentMap, setInstrumentMap] = useState<Record<string, Instrument>>({});

  useEffect(() => {
    setMounted(true);

    // Buscar usuário logado
    const localUser = localStorage.getItem("user");
    if (!localUser) {
      router.push("/login");
      return;
    }

    try {
      const userObj = JSON.parse(localUser);
      const userId = userObj?.id || userObj?.userId;

      if (!userId) {
        router.push("/login");
        return;
      }

      // Buscar histórico de sessões
      const historyKey = `sessionHistory_${userId}`;
      const existingHistory = localStorage.getItem(historyKey);

      if (existingHistory) {
        try {
          const parsedSessions = JSON.parse(existingHistory);
          // Ordenar por data decrescente (mais recentes primeiro)
          const sortedSessions = parsedSessions.sort((a: SessionRecord, b: SessionRecord) => {
            return new Date(b.startTime).getTime() - new Date(a.startTime).getTime();
          });
          setSessions(sortedSessions);
        } catch (e) {
          console.warn("Erro ao parsear histórico:", e);
        }
      }

      // Criar mapa de instrumentos para fácil acesso
      const instruments = (appData as any).instruments || [];
      const instMap: Record<string, Instrument> = {};
      instruments.forEach((inst: Instrument) => {
        instMap[inst.id] = inst;
      });
      setInstrumentMap(instMap);
    } catch (e) {
      console.error("Erro ao buscar histórico:", e);
      router.push("/login");
    }
  }, []);

  const getInstrumentName = (instrumentId: string): string => {
    return instrumentMap[instrumentId]?.name || instrumentId;
  };

  const handleDeleteSession = (sessionId: string) => {
    const localUser = localStorage.getItem("user");
    if (!localUser) return;

    try {
      const userObj = JSON.parse(localUser);
      const userId = userObj?.id || userObj?.userId;

      const historyKey = `sessionHistory_${userId}`;
      const updatedSessions = sessions.filter((s) => s.id !== sessionId);
      localStorage.setItem(historyKey, JSON.stringify(updatedSessions));
      setSessions(updatedSessions);
    } catch (e) {
      console.error("Erro ao deletar sessão:", e);
    }
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full relative bg-black overflow-y-auto overflow-x-hidden">
      <NavbarFinal />

      <div
        className={`fixed inset-0 transition-all duration-300 ${
          open || openMobile ? "backdrop-blur-md bg-black/30 pointer-events-auto" : "pointer-events-none"
        }`}
        style={{ zIndex: 5 }}
      />

      <div className="relative z-10 pt-20 px-6 pb-20">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-12">
            <div>
              <h1 className="text-5xl font-bold text-white mb-2">Histórico de Prática</h1>
              <p className="text-gray-400">
                {sessions.length > 0
                  ? `Você tem ${sessions.length} sessão${sessions.length !== 1 ? "s" : ""} registrada${sessions.length !== 1 ? "s" : ""}`
                  : "Nenhuma sessão registrada ainda"}
              </p>
            </div>
            <Button
              variant="outline"
              className="border-gray-600 text-gray-300 hover:bg-gray-800"
              onClick={() => router.back()}
            >
              Voltar
            </Button>
          </div>

          {/* Lista de Sessões */}
          {sessions.length > 0 ? (
            <div className="grid gap-4">
              {sessions.map((session) => (
                <Card
                  key={session.id}
                  className="bg-gray-900/60 border-gray-700 p-6 hover:bg-gray-900/80 transition-colors"
                >
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-4 items-center">
                    {/* Data e Hora */}
                    <div className="flex items-start gap-3">
                      <Calendar className="w-5 h-5 text-yellow-400 mt-1 flex-shrink-0" />
                      <div>
                        <p className="text-gray-400 text-sm">Data</p>
                        <p className="text-white font-semibold">{session.startDate}</p>
                        <p className="text-gray-500 text-xs">{session.startHour}</p>
                      </div>
                    </div>

                    {/* Instrumento */}
                    <div className="flex items-start gap-3">
                      <Target className="w-5 h-5 text-blue-400 mt-1 flex-shrink-0" />
                      <div>
                        <p className="text-gray-400 text-sm">Instrumento</p>
                        <p className="text-white font-semibold">{getInstrumentName(session.instrumentId)}</p>
                      </div>
                    </div>

                    {/* Duração */}
                    <div className="flex items-start gap-3">
                      <Clock className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                      <div>
                        <p className="text-gray-400 text-sm">Duração</p>
                        <p className="text-white font-semibold">
                          {session.durationMinutes !== undefined
                            ? `${session.durationMinutes} min`
                            : "Em andamento"}
                        </p>
                      </div>
                    </div>

                    {/* Precisão */}
                    {session.accuracy !== undefined && (
                      <div className="flex items-start gap-3">
                        <Target className="w-5 h-5 text-purple-400 mt-1 flex-shrink-0" />
                        <div>
                          <p className="text-gray-400 text-sm">Precisão</p>
                          <p className={`font-semibold ${
                            session.accuracy >= 80
                              ? "text-green-400"
                              : session.accuracy >= 60
                              ? "text-yellow-400"
                              : "text-red-400"
                          }`}>
                            {session.accuracy.toFixed(1)}%
                          </p>
                        </div>
                      </div>
                    )}

                    {/* Estrelas */}
                    {session.starsEarned !== undefined && (
                      <div className="flex items-start gap-3">
                        <Zap className="w-5 h-5 text-yellow-400 mt-1 flex-shrink-0" />
                        <div>
                          <p className="text-gray-400 text-sm">Estrelas</p>
                          <p className="text-white font-semibold">{session.starsEarned} ⭐</p>
                        </div>
                      </div>
                    )}

                    {/* Ação */}
                    <div className="flex justify-end">
                      <Button
                        onClick={() => handleDeleteSession(session.id)}
                        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 text-sm"
                      >
                        Deletar
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            <Card className="bg-gray-900/60 border-gray-700 p-12 text-center">
              <p className="text-gray-400 text-lg">Nenhuma sessão de prática registrada ainda.</p>
              <p className="text-gray-500 mt-2">Comece a praticar para ver o seu histórico aqui!</p>
              <Button
                onClick={() => router.push("/practice-session")}
                className="mt-6 bg-yellow-400 hover:bg-yellow-500 text-black font-bold px-8 py-6 text-lg"
              >
                Iniciar Sessão de Prática
              </Button>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
