"use client";

import React, { useState, useEffect, useRef } from "react";
import NavbarFinal from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { Ripple } from "@/components/ui/ripple";
import { useMicrophone } from "@/hooks/useMicrophone";
import { useAudioProcessor } from "@/hooks/useAudioProcessor";
import { useMLIntegration } from "@/hooks/useMLIntegration";
import { tuneAudio } from "@/lib/api/mlService";

interface TuningData {
  note?: string;
  frequency?: number;
  targetFrequency?: number;
  accuracy?: number;
  centsDiff?: number;
  tuningDirection?: string;
  isInTune?: boolean;
}

export default function Tuning() {
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [tuningData, setTuningData] = useState<TuningData>({
    note: undefined,
    frequency: undefined,
    targetFrequency: undefined,
    accuracy: undefined,
    centsDiff: undefined,
    tuningDirection: undefined,
    isInTune: undefined,
  });
  const [mlEnabled, setMlEnabled] = useState(true);
  const [mlError, setMlError] = useState<string | null>(null);
  const lastFrequencyRef = useRef<number | null>(null);
  const mlProcessingRef = useRef(false);

  const { isRecording, error, startRecording, stopRecording, analyser } = useMicrophone();

  // Integração com ML
  const { processFrequency, isProcessing: isMLProcessing } = useMLIntegration({
    enabled: mlEnabled,
    onTuning: (data) => {
      if (data) {
        // TuningResponse tem 'note', TunerResponse tem 'current_note'
        const note = "current_note" in data ? data.current_note : data.note;
        const targetFreq = "target_frequency" in data ? data.target_frequency : data.frequency;
        
        setTuningData((prev) => ({
          ...prev,
          note: note || prev.note,
          frequency: data.frequency || prev.frequency,
          targetFrequency: targetFreq || prev.targetFrequency,
          accuracy: Math.round((data.confidence || 0) * 100),
          centsDiff: data.cents_diff ?? prev.centsDiff,
          tuningDirection: data.tuning_direction || prev.tuningDirection,
          isInTune: data.is_in_tune ?? prev.isInTune,
        }));
        setMlError(null);
      }
    },
    onError: (err) => {
      setMlError(err.message);
      console.error("Erro no ML:", err);
    },
  });

  // Processar áudio do microfone
  useAudioProcessor({
    analyser,
    isRecording,
    onAudioData: async (data) => {
      // Atualizar dados locais imediatamente
      setTuningData((prev) => ({
        ...prev,
        note: data.note,
        frequency: data.frequency,
        accuracy: Math.round(data.confidence * 100),
      }));

      // Enviar para ML se habilitado e frequência mudou significativamente
      if (mlEnabled && data.frequency && !mlProcessingRef.current) {
        const frequencyChanged = 
          lastFrequencyRef.current === null || 
          Math.abs(data.frequency - lastFrequencyRef.current) > 1.0; // Mais de 1 Hz de diferença

        if (frequencyChanged && data.confidence > 0.3) {
          lastFrequencyRef.current = data.frequency;
          mlProcessingRef.current = true;

          try {
            await processFrequency(data.frequency, 50);
          } catch (err) {
            console.error("Erro ao processar frequência no ML:", err);
          } finally {
            mlProcessingRef.current = false;
          }
        }
      }
    },
    interval: 200, // Processar a cada 200ms
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const toggleListening = async () => {
    if (isRecording) {
      stopRecording();
    } else {
      await startRecording();
    }
  };

  const getStatusColor = () => {
    if (tuningData.isInTune) return "#22c55e"; // verde
    if (tuningData.tuningDirection?.includes("alto")) return "#dc2626"; // vermelho
    if (tuningData.tuningDirection?.includes("baixo")) return "#3b82f6"; // azul
    return "#6b7280"; // cinza
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full relative bg-black overflow-y-auto overflow-x-hidden">
      <NavbarFinal />

      <div className={`fixed inset-0 transition-all duration-300 ${
        open || openMobile ? "backdrop-blur-md bg-black/30 pointer-events-auto" : "pointer-events-none"
      }`} style={{ zIndex: 5 }} />

      <div className="relative z-10 pt-20 px-6 pb-20 flex items-center justify-center min-h-screen">
        <div className="flex flex-col w-full items-center justify-center gap-12">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-white mb-2">Afinador</h1>
            <p className="text-gray-400">Toque uma nota no seu instrumento</p>
          </div>

          {/* Círculos concêntricos */}
          <div className="relative w-full h-140 flex items-center justify-center">
            <div
              onClick={toggleListening}
              className="relative w-full h-full flex items-center justify-center cursor-pointer"
            >
              <Ripple />

              <button
                className={`relative z-10 w-48 h-48 rounded-full font-bold text-2xl transition-all flex items-center justify-center ${
                  isRecording
                    ? "bg-gradient-to-br from-gray-400 to-gray-500 text-black"
                    : "bg-gray-300 text-gray-700 hover:bg-gray-400"
                }`}
              >
                {isRecording ? (
                  <div className="animate-pulse">Listening</div>
                ) : (
                  "Clique para iniciar"
                )}
              </button>
            </div>
          </div>

          {error && (
            <div className="w-full max-w-md bg-red-900/60 rounded-lg p-4 border border-red-700">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          {mlError && (
            <div className="w-full max-w-md bg-yellow-900/60 rounded-lg p-4 border border-yellow-700">
              <p className="text-yellow-400 text-sm">
                Aviso ML: {mlError}. Usando detecção local.
              </p>
            </div>
          )}

          <div className="w-full max-w-md bg-gray-900/60 rounded-lg p-8 border border-gray-700 space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-400">Nota:</span>
              <span className="text-2xl font-bold text-white">{tuningData.note || "---"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Frequência:</span>
              <span className="text-lg text-white">
                {tuningData.frequency !== undefined ? `${tuningData.frequency.toFixed(2)} Hz` : "---"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Alvo:</span>
              <span className="text-lg text-white">
                {tuningData.targetFrequency !== undefined ? `${tuningData.targetFrequency.toFixed(2)} Hz` : "---"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Diferença:</span>
              <span className={`text-lg font-semibold ${
                tuningData.centsDiff !== undefined
                  ? (tuningData.isInTune ? "text-green-400" : "text-yellow-400")
                  : "text-gray-500"
              }`}>
                {tuningData.centsDiff !== undefined ? `${tuningData.centsDiff.toFixed(1)} cents` : "---"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Status:</span>
              <span className={`text-lg font-semibold ${
                tuningData.tuningDirection
                  ? (tuningData.isInTune 
                      ? "text-green-400" 
                      : tuningData.tuningDirection.includes("alto")
                      ? "text-red-400"
                      : "text-blue-400")
                  : "text-gray-500"
              }`}>
                {tuningData.tuningDirection || "---"}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Precisão:</span>
              <span className="text-lg text-white">
                {tuningData.accuracy !== undefined ? `${tuningData.accuracy}%` : "---"}
              </span>
            </div>
            <div className="flex justify-between items-center pt-2 border-t border-gray-700">
              <span className="text-gray-400 text-sm">ML Service:</span>
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${
                  isMLProcessing ? "bg-yellow-400 animate-pulse" : mlEnabled ? "bg-green-400" : "bg-gray-500"
                }`}></span>
                <span className="text-sm text-gray-300">
                  {isMLProcessing ? "Processando..." : mlEnabled ? "Ativo" : "Desativado"}
                </span>
              </div>
            </div>
          </div>

          <Button variant="outline" className="border-gray-600" onClick={() => window.history.back()}>Voltar</Button>
        </div>
      </div>
    </div>
  );
}
