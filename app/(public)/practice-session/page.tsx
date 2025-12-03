"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { useRouter } from "next/navigation";
import NavbarFinal from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { Ripple } from "@/components/ui/ripple";
import { Play, Pause, Square } from "lucide-react";
import { useMicrophone } from "@/hooks/useMicrophone";
import { useAudioProcessor } from "@/hooks/useAudioProcessor";
import { useMLIntegration } from "@/hooks/useMLIntegration";


// Notas serão obtidas do ML Service ou armazenamento

// Componente Ripple customizado com cor
const ColoredRipple = React.memo(function ColoredRipple({
  color,
  className,
  mainCircleSize = 210,
  mainCircleOpacity = 0.24,
  numCircles = 8,
}: {
  color: string;
  className?: string;
  mainCircleSize?: number;
  mainCircleOpacity?: number;
  numCircles?: number;
}) {
  return (
    <div
      className={`pointer-events-none absolute inset-0 [mask-image:linear-gradient(to_bottom,white,transparent)] select-none ${className || ""}`}
    >
      {Array.from({ length: numCircles }, (_, i) => {
        const size = mainCircleSize + i * 70;
        const opacity = mainCircleOpacity - i * 0.03;
        const animationDelay = `${i * 0.06}s`;

        return (
          <div
            key={i}
            className="animate-ripple absolute rounded-full border shadow-xl"
            style={{
              "--i": i,
              width: `${size}px`,
              height: `${size}px`,
              opacity,
              animationDelay,
              borderStyle: "solid",
              borderWidth: "1px",
              borderColor: color,
              top: "50%",
              left: "50%",
              transform: "translate(-50%, -50%) scale(1)",
            } as React.CSSProperties}
          />
        );
      })}
    </div>
  );
});

ColoredRipple.displayName = "ColoredRipple";

export default function PracticeSession() {
  const router = useRouter();
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentNote, setCurrentNote] = useState<string>("");
  const [practiceNotes, setPracticeNotes] = useState<string[]>([]);
  const [noteIndex, setNoteIndex] = useState(0);
  const [feedback, setFeedback] = useState<"correct" | "incorrect" | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [countdown, setCountdown] = useState(10);
  const [detectedNote, setDetectedNote] = useState<string>("");
  const [sessionTime, setSessionTime] = useState(0); // Tempo em segundos
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const feedbackTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const countdownRef = useRef<NodeJS.Timeout | null>(null);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const sessionStartTimeRef = useRef<number | null>(null);

  const { isRecording, error, startRecording, stopRecording, analyser } = useMicrophone();
  const [mlEnabled, setMlEnabled] = useState(true);
  const [mlNote, setMlNote] = useState<string | undefined>(undefined);
  const [mlAccuracy, setMlAccuracy] = useState<number | undefined>(undefined);
  const [mlFeedback, setMlFeedback] = useState<string | undefined>(undefined);
  const [mlIsCorrect, setMlIsCorrect] = useState<boolean | undefined>(undefined);
  const lastFrequencyRef = useRef<number | null>(null);
  const mlProcessingRef = useRef(false);

  // Integração com ML - usando Practice Service
  const { checkPracticeWithFrequency, isProcessing: isMLProcessing, lastPracticeCheck } = useMLIntegration({
    enabled: mlEnabled && isPlaying,
    onPracticeCheck: (data) => {
      console.log("🎯 [PRACTICE SESSION] onPracticeCheck chamado com dados:", data);
      if (data) {
        console.log("📊 [PRACTICE SESSION] Atualizando métricas:", {
          detected_note: data.detected_note,
          accuracy_score: data.accuracy_score,
          feedback_message: data.feedback_message,
          is_correct: data.is_correct,
        });
        setMlNote(data.detected_note || undefined);
        setMlAccuracy(data.accuracy_score !== undefined ? data.accuracy_score : undefined);
        setMlFeedback(data.feedback_message || undefined);
        setMlIsCorrect(data.is_correct !== undefined ? data.is_correct : undefined);
        
        // Usar feedback do ML para validar acerto/erro
        if (data.is_correct && data.confidence > 0.3) {
          handleMLFeedback(true);
        } else if (!data.is_correct && data.confidence > 0.3) {
          handleMLFeedback(false);
        }
      } else {
        console.warn("⚠️ [PRACTICE SESSION] onPracticeCheck recebeu dados null/undefined");
      }
    },
    onError: (err) => {
      console.error("❌ [PRACTICE SESSION] Erro no ML durante prática:", err);
    },
  });

  // Função para normalizar nota (remover oitava)
  const normalizeNote = useCallback((note: string) => {
    return note.replace(/\d+$/, "");
  }, []);

  // Processar áudio do microfone e comparar com a nota atual
  useAudioProcessor({
    analyser,
    isRecording: isRecording && isPlaying,
    onAudioData: useCallback(async (data: { note: string; confidence: number; frequency: number }) => {
      if (!isPlaying) return;
      
      setDetectedNote(data.note);
      
      // Comparar nota detectada localmente com a nota atual (ignorar oitava para comparação)
      const currentNoteBase = normalizeNote(currentNote);
      const detectedNoteBase = normalizeNote(data.note);
      
      if (data.confidence > 0.3) {
        if (currentNoteBase === detectedNoteBase) {
          handleMLFeedback(true);
        } else if (detectedNoteBase !== "" && currentNoteBase !== "") {
          // Só mostrar erro se detectou uma nota diferente com confiança suficiente
          handleMLFeedback(false);
        }
      }

      // Enviar frequência para ML Practice Service se habilitado
      if (mlEnabled && data.frequency && !mlProcessingRef.current && currentNote) {
        const frequencyChanged = 
          lastFrequencyRef.current === null || 
          Math.abs(data.frequency - lastFrequencyRef.current) > 2.0; // Mais de 2 Hz de diferença

        if (frequencyChanged && data.confidence > 0.3) {
          lastFrequencyRef.current = data.frequency;
          mlProcessingRef.current = true;

          try {
            // Usar Practice Service para validação completa
            await checkPracticeWithFrequency(data.frequency, currentNote, 50);
          } catch (err) {
            console.error("Erro ao validar prática no ML:", err);
          } finally {
            mlProcessingRef.current = false;
          }
        }
      }
    }, [isPlaying, currentNote, normalizeNote, mlEnabled, checkPracticeWithFrequency]),
    interval: 500, // Processar a cada 500ms
  });

  // Buscar notas do ML Service ou usar padrão
  useEffect(() => {
    setMounted(true);
    
    const loadPracticeNotes = async () => {
      try {
        // Tentar buscar notas do ML Service
        const mlServiceUrl = process.env.NEXT_PUBLIC_ML_SERVICE_URL || "http://localhost:8001";
        const response = await fetch(`${mlServiceUrl}/notes`);
        
        if (response.ok) {
          const data = await response.json();
          // Pegar algumas notas comuns para prática (oitavas 3-5)
          const allNotes = Object.keys(data.notes || {});
          const commonNotes = allNotes.filter((note: string) => {
            const octaveMatch = note.match(/\d+$/);
            if (!octaveMatch) return false;
            const octave = parseInt(octaveMatch[0]);
            return octave >= 3 && octave <= 5;
          }).slice(0, 20); // Limitar a 20 notas
          
          if (commonNotes.length > 0) {
            setPracticeNotes(commonNotes);
            setCurrentNote(commonNotes[0]);
            return;
          }
        }
      } catch (err) {
        console.warn("Não foi possível carregar notas do ML Service:", err);
      }
      
      // Se não conseguir carregar, usar array vazio (mostrará "---")
      setPracticeNotes([]);
      setCurrentNote("");
    };
    
    loadPracticeNotes();
  }, []);

  useEffect(() => {
    if (isPlaying) {
      // Iniciar timer da sessão
      if (sessionStartTimeRef.current === null) {
        sessionStartTimeRef.current = Date.now();
      }
      
      timerRef.current = setInterval(() => {
        if (sessionStartTimeRef.current !== null) {
          const elapsedSeconds = Math.floor((Date.now() - sessionStartTimeRef.current) / 1000);
          setSessionTime(elapsedSeconds);
        }
      }, 1000);

      // Contador regressivo
      setCountdown(10);
      countdownRef.current = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            return 10;
          }
          return prev - 1;
        });
      }, 1000);

      // Mudar nota a cada 10 segundos
      if (practiceNotes.length > 0) {
        intervalRef.current = setInterval(() => {
          setNoteIndex((prev) => {
            const nextIndex = (prev + 1) % practiceNotes.length;
            setCurrentNote(practiceNotes[nextIndex]);
            return nextIndex;
          });
          // Resetar feedback quando mudar a nota
          setFeedback(null);
          setShowFeedback(false);
          setCountdown(10);
        }, 10000);
      }
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
        countdownRef.current = null;
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
      setCountdown(10);
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [isPlaying, practiceNotes]);

  // Função para simular feedback do ML (será substituída pela conexão real)
  const handleMLFeedback = useCallback((isCorrect: boolean) => {
    setFeedback(isCorrect ? "correct" : "incorrect");
    setShowFeedback(true);

    // Esconder feedback após 2 segundos
    if (feedbackTimeoutRef.current) {
      clearTimeout(feedbackTimeoutRef.current);
    }
    feedbackTimeoutRef.current = setTimeout(() => {
      setShowFeedback(false);
      setFeedback(null);
    }, 2000);
  }, []);


  const togglePlay = async () => {
    if (!isPlaying) {
      // Iniciar gravação e sessão
      await startRecording();
      setIsPlaying(true);
      
      // Registrar o início da sessão no histórico
      recordSessionStart();
    } else {
      // Pausar gravação e sessão
      stopRecording();
      setIsPlaying(false);
    }
  };

  // Função para registrar o início de uma sessão
  const recordSessionStart = useCallback(() => {
    try {
      const localUser = localStorage.getItem("user");
      if (!localUser) {
        console.warn("⚠️ [PRACTICE SESSION] Nenhum usuário encontrado para registrar sessão");
        return;
      }

      const userObj = JSON.parse(localUser);
      const userId = userObj?.id || userObj?.userId;
      
      if (!userId) {
        console.warn("⚠️ [PRACTICE SESSION] userId não encontrado");
        return;
      }

      // Buscar instrumento favorito
      const favoriteInstrumentId = userObj?.favoriteInstrumentId || "unknown";
      
      // Criar registro de sessão
      const sessionRecord = {
        id: `session-${userId}-${Date.now()}`,
        userId: userId,
        instrumentId: favoriteInstrumentId,
        startTime: new Date().toISOString(),
        startDate: new Date().toLocaleDateString("pt-BR"),
        startHour: new Date().toLocaleTimeString("pt-BR"),
      };

      // Buscar histórico existente
      const historyKey = `sessionHistory_${userId}`;
      const existingHistory = localStorage.getItem(historyKey);
      
      let sessions = [];
      if (existingHistory) {
        try {
          sessions = JSON.parse(existingHistory);
        } catch (e) {
          console.warn("⚠️ [PRACTICE SESSION] Erro ao parsear histórico existente:", e);
        }
      }

      // Adicionar nova sessão ao histórico
      sessions.push(sessionRecord);
      
      // Salvar no localStorage
      localStorage.setItem(historyKey, JSON.stringify(sessions));
      console.log("✅ [PRACTICE SESSION] Sessão registrada:", sessionRecord);
    } catch (e) {
      console.error("❌ [PRACTICE SESSION] Erro ao registrar sessão:", e);
    }
  }, []);

  // Função para salvar estatísticas da sessão
  const saveSessionStats = useCallback(() => {
    try {
      const localUser = localStorage.getItem("user");
      if (!localUser) {
        console.warn("⚠️ [PRACTICE SESSION] Nenhum usuário encontrado para salvar estatísticas");
        return;
      }

      const userObj = JSON.parse(localUser);
      const userId = userObj?.id || userObj?.userId;
      
      if (!userId) {
        console.warn("⚠️ [PRACTICE SESSION] userId não encontrado");
        return;
      }

      // Buscar estatísticas existentes
      const localStatsKey = `userStats_${userId}`;
      const existingStats = localStorage.getItem(localStatsKey);
      
      let stats = {
        totalPracticeTime: 0,
        currentStreak: 0,
        totalSessions: 0,
        totalStars: 0,
      };

      if (existingStats) {
        try {
          stats = JSON.parse(existingStats);
        } catch (e) {
          console.warn("⚠️ [PRACTICE SESSION] Erro ao parsear estatísticas existentes:", e);
        }
      }

      // Adicionar tempo de prática (em minutos)
      const practiceMinutes = Math.floor(sessionTime / 60);
      stats.totalPracticeTime = (stats.totalPracticeTime || 0) + practiceMinutes;
      
      // Contar sessão
      stats.totalSessions = (stats.totalSessions || 0) + 1;
      
      // Incrementar estrelas baseado na precisão média (se houver)
      const starsEarned = mlAccuracy !== undefined && mlAccuracy > 0 ? Math.floor(mlAccuracy / 20) : 0;
      stats.totalStars = (stats.totalStars || 0) + starsEarned;

      // Salvar no localStorage
      localStorage.setItem(localStatsKey, JSON.stringify(stats));
      console.log("✅ [PRACTICE SESSION] Estatísticas salvas:", {
        totalPracticeTime: stats.totalPracticeTime,
        totalSessions: stats.totalSessions,
        totalStars: stats.totalStars,
        practiceMinutesThisSession: practiceMinutes,
      });

      // Atualizar histórico de sessões com dados finais
      const historyKey = `sessionHistory_${userId}`;
      const existingHistory = localStorage.getItem(historyKey);
      
      let sessions = [];
      if (existingHistory) {
        try {
          sessions = JSON.parse(existingHistory);
        } catch (e) {
          console.warn("⚠️ [PRACTICE SESSION] Erro ao parsear histórico:", e);
        }
      }

      // Encontrar a última sessão e atualizar com dados finais
      if (sessions.length > 0) {
        const lastSession = sessions[sessions.length - 1];
        lastSession.endTime = new Date().toISOString();
        lastSession.endHour = new Date().toLocaleTimeString("pt-BR");
        lastSession.durationMinutes = practiceMinutes;
        lastSession.accuracy = mlAccuracy || 0;
        lastSession.starsEarned = starsEarned;
        
        localStorage.setItem(historyKey, JSON.stringify(sessions));
        console.log("✅ [PRACTICE SESSION] Histórico atualizado com dados finais da sessão");
      }
    } catch (e) {
      console.error("❌ [PRACTICE SESSION] Erro ao salvar estatísticas:", e);
    }
  }, [mlAccuracy, sessionTime]);

  const stopSession = () => {
    setIsPlaying(false);
    stopRecording();
    
    // Salvar estatísticas antes de parar
    saveSessionStats();
    
    setFeedback(null);
    setShowFeedback(false);
    setCountdown(10);
    setDetectedNote("");
    setSessionTime(0);
    sessionStartTimeRef.current = null;
    // Resetar métricas ML
    setMlNote(undefined);
    setMlAccuracy(undefined);
    setMlFeedback(undefined);
    setMlIsCorrect(undefined);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (countdownRef.current) {
      clearInterval(countdownRef.current);
      countdownRef.current = null;
    }
    if (timerRef.current) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    if (feedbackTimeoutRef.current) {
      clearTimeout(feedbackTimeoutRef.current);
      feedbackTimeoutRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (countdownRef.current) {
        clearInterval(countdownRef.current);
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      if (feedbackTimeoutRef.current) {
        clearTimeout(feedbackTimeoutRef.current);
      }
    };
  }, []);

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full relative bg-black overflow-y-auto overflow-x-hidden">
      <NavbarFinal />

      <div
        className={`fixed inset-0 transition-all duration-300 ${
          open || openMobile
            ? "backdrop-blur-md bg-black/30 pointer-events-auto"
            : "pointer-events-none"
        }`}
        style={{ zIndex: 5 }}
      />

      <div className="relative z-10 pt-20 px-6 pb-20 min-h-screen">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="flex justify-between items-center mb-12">
            <div>
              <h1 className="text-5xl font-bold text-white mb-2">Sessão de Prática</h1>
              <p className="text-gray-400">Toque as notas exibidas no seu instrumento</p>
            </div>
            <Button
              variant="outline"
              className="border-gray-600 text-gray-300 hover:bg-gray-800"
              onClick={() => router.back()}
            >
              Voltar
            </Button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Lado Esquerdo - Ripples */}
            <div className="relative w-full h-[600px] flex items-center justify-center">
              {/* Ripple padrão (sempre visível) */}
              <Ripple className="z-10" />

              {/* Ripple verde (feedback correto) */}
              {showFeedback && feedback === "correct" && (
                <ColoredRipple
                  color="#22c55e"
                  className="z-20"
                  mainCircleSize={210}
                  mainCircleOpacity={0.4}
                />
              )}

              {/* Ripple vermelho (feedback incorreto) */}
              {showFeedback && feedback === "incorrect" && (
                <ColoredRipple
                  color="#dc2626"
                  className="z-20"
                  mainCircleSize={210}
                  mainCircleOpacity={0.4}
                />
              )}

              {/* Indicador de status */}
              <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-30">
                <div className="bg-gray-900/80 rounded-lg px-6 py-3 border border-gray-700">
                  <p className="text-white text-sm">
                    {isPlaying ? (
                      <span className="flex items-center gap-2">
                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                        Gravando...
                      </span>
                    ) : (
                      <span className="text-gray-400">Pausado</span>
                    )}
                  </p>
                </div>
              </div>
            </div>

            {/* Lado Direito - Display de Notas */}
            <div className="flex flex-col items-center justify-center">
              <div className="w-full max-w-md bg-gray-900/60 rounded-lg p-12 border border-gray-700">
                <div className="text-center mb-8">
                  <p className="text-gray-400 mb-4">Nota Atual</p>
                  <div className="text-8xl font-bold text-white mb-4">
                    {currentNote || "---"}
                  </div>
                  <p className="text-gray-500 text-sm">
                    {isPlaying
                      ? "Toque esta nota no seu instrumento"
                      : "Clique em 'Iniciar' para começar"}
                  </p>
                </div>

                {/* Controles */}
                <div className="flex gap-4 justify-center mt-8">
                  <Button
                    onClick={togglePlay}
                    className={`${
                      isPlaying
                        ? "bg-yellow-400 hover:bg-yellow-500 text-black"
                        : "bg-green-600 hover:bg-green-700 text-white"
                    } font-bold px-8 py-6 text-lg`}
                  >
                    {isPlaying ? (
                      <>
                        <Pause className="w-5 h-5 mr-2" />
                        Pausar
                      </>
                    ) : (
                      <>
                        <Play className="w-5 h-5 mr-2" />
                        Iniciar
                      </>
                    )}
                  </Button>
                  <Button
                    onClick={stopSession}
                    variant="outline"
                    className="border-gray-600 text-gray-300 hover:bg-gray-800 px-8 py-6 text-lg"
                  >
                    <Square className="w-5 h-5 mr-2" />
                    Parar
                  </Button>
                </div>

                {/* Informações adicionais */}
                <div className="mt-8 pt-8 border-t border-gray-700 space-y-3">
                  <div className="flex justify-between text-sm items-center">
                    <span className="text-gray-400">Tempo de Prática:</span>
                    <span className="text-white font-bold text-lg">
                      {`${Math.floor(sessionTime / 60)}:${(sessionTime % 60).toString().padStart(2, '0')}`}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm items-center">
                    <span className="text-gray-400">Próxima nota em:</span>
                    <span className="text-white font-bold text-lg">
                      {isPlaying ? `${countdown}s` : "—"}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm items-center">
                    <span className="text-gray-400">Status:</span>
                    <span
                      className={`font-semibold ${
                        showFeedback
                          ? feedback === "correct"
                            ? "text-green-400"
                            : "text-red-400"
                          : "text-gray-400"
                      }`}
                    >
                      {showFeedback
                        ? feedback === "correct"
                          ? "✓ Correto"
                          : "✗ Incorreto"
                        : "Aguardando..."}
                    </span>
                  </div>
                  {isPlaying && (
                    <>
                      <div className="flex justify-between text-sm items-center">
                        <span className="text-gray-400">Nota detectada (local):</span>
                        <span className="text-white font-semibold">{detectedNote || "---"}</span>
                      </div>
                      {mlEnabled && (
                        <>
                          <div className="flex justify-between text-sm items-center">
                            <span className="text-gray-400">Nota detectada (ML):</span>
                            <span className={`font-semibold ${
                              mlNote !== undefined 
                                ? (mlIsCorrect ? "text-green-400" : "text-red-400") 
                                : "text-gray-500"
                            }`}>
                              {mlNote !== undefined ? mlNote : "---"}
                            </span>
                          </div>
                          <div className="flex justify-between text-sm items-center">
                            <span className="text-gray-400">Precisão (ML):</span>
                            <span className={`font-semibold ${
                              mlAccuracy !== undefined && mlAccuracy > 0 
                                ? (mlAccuracy >= 80 ? "text-green-400" : mlAccuracy >= 60 ? "text-yellow-400" : "text-red-400")
                                : "text-gray-500"
                            }`}>
                              {mlAccuracy !== undefined && mlAccuracy > 0 ? `${mlAccuracy.toFixed(1)}%` : "---"}
                            </span>
                          </div>
                          {mlFeedback !== undefined && mlFeedback && (
                            <div className="mt-2 p-2 bg-gray-800/50 rounded text-xs">
                              <p className={`${
                                mlIsCorrect ? "text-green-400" : "text-yellow-400"
                              }`}>
                                {mlFeedback}
                              </p>
                            </div>
                          )}
                        </>
                      )}
                    </>
                  )}
                  {isPlaying && (
                    <div className="flex justify-between text-sm items-center pt-2 border-t border-gray-700">
                      <span className="text-gray-400 text-xs">ML Service:</span>
                      <div className="flex items-center gap-2">
                        <span className={`w-2 h-2 rounded-full ${
                          isMLProcessing ? "bg-yellow-400 animate-pulse" : mlEnabled ? "bg-green-400" : "bg-gray-500"
                        }`}></span>
                        <span className="text-xs text-gray-300">
                          {isMLProcessing ? "Processando..." : mlEnabled ? "Ativo" : "Desativado"}
                        </span>
                      </div>
                    </div>
                  )}
                  {error && (
                    <div className="mt-4 p-3 bg-red-900/60 rounded border border-red-700">
                      <p className="text-red-400 text-xs">{error}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

