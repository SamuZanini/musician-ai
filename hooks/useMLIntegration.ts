import { useState, useCallback, useRef } from "react";
import {
  detectAudio,
  tuneAudio,
  tuneInstrument,
  detectAudioAdvanced,
  checkPracticeNote,
  processPracticeSession,
  type DetectionResponse,
  type TuningResponse,
  type TunerResponse,
  type DetectionServiceResponse,
  type PracticeCheckResponse,
  type PracticeSessionResponse,
} from "@/lib/api/mlService";

type TuningResult = TuningResponse | TunerResponse;

interface UseMLIntegrationOptions {
  enabled?: boolean;
  instrument?: string;
  useAdvancedDetection?: boolean;
  onDetection?: (data: DetectionResponse | DetectionServiceResponse) => void;
  onTuning?: (data: TuningResult) => void;
  onPracticeCheck?: (data: PracticeCheckResponse | PracticeSessionResponse) => void;
  onError?: (error: Error) => void;
}

/**
 * Hook para integrar detecção de áudio do frontend com os serviços de ML
 */
export function useMLIntegration(options: UseMLIntegrationOptions = {}) {
  const {
    enabled = true,
    instrument,
    useAdvancedDetection = false,
    onDetection,
    onTuning,
    onError,
  } = options;

  const [isProcessing, setIsProcessing] = useState(false);
  const [lastDetection, setLastDetection] = useState<DetectionResponse | DetectionServiceResponse | null>(null);
  const [lastTuning, setLastTuning] = useState<TuningResult | null>(null);
  const [lastPracticeCheck, setLastPracticeCheck] = useState<PracticeCheckResponse | PracticeSessionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const processingRef = useRef(false);
  
  const {
    onPracticeCheck,
  } = options;

  /**
   * Detecta áudio usando os serviços de ML
   */
  const detectWithML = useCallback(
    async (audioData: number[], sampleRate: number = 44100) => {
      if (!enabled || processingRef.current) return null;

      try {
        setIsProcessing(true);
        processingRef.current = true;
        setError(null);

        let result: DetectionResponse | DetectionServiceResponse;

        if (useAdvancedDetection) {
          result = await detectAudioAdvanced(audioData, sampleRate, instrument);
        } else {
          result = await detectAudio(audioData, sampleRate);
        }

        setLastDetection(result);
        onDetection?.(result);

        return result;
      } catch (err: any) {
        const errorMessage = err.message || "Erro ao detectar áudio com ML";
        setError(errorMessage);
        onError?.(err);
        console.error("Erro na detecção ML:", err);
        return null;
      } finally {
        setIsProcessing(false);
        processingRef.current = false;
      }
    },
    [enabled, useAdvancedDetection, instrument, onDetection, onError]
  );

  /**
   * Obtém feedback de afinação usando frequência detectada
   */
  const tuneWithML = useCallback(
    async (frequency: number, toleranceCents: number = 50) => {
      if (!enabled || processingRef.current) return null;

      try {
        setIsProcessing(true);
        processingRef.current = true;
        setError(null);

        let result: TuningResult;

        if (instrument) {
          result = await tuneInstrument(instrument, frequency, toleranceCents);
        } else {
          result = await tuneAudio(frequency, toleranceCents);
        }

        setLastTuning(result);
        onTuning?.(result);

        return result;
      } catch (err: any) {
        const errorMessage = err.message || "Erro ao afinar com ML";
        setError(errorMessage);
        onError?.(err);
        console.error("Erro na afinação ML:", err);
        return null;
      } finally {
        setIsProcessing(false);
        processingRef.current = false;
      }
    },
    [enabled, instrument, onTuning, onError]
  );

  /**
   * Processa frequência detectada localmente e envia para ML
   */
  const processFrequency = useCallback(
    async (frequency: number, toleranceCents: number = 50) => {
      if (!enabled) return null;

      // Primeiro tenta afinar com ML
      const tuningResult = await tuneWithML(frequency, toleranceCents);
      
      return tuningResult;
    },
    [enabled, tuneWithML]
  );

  /**
   * Valida nota de prática usando frequência
   */
  const checkPracticeWithFrequency = useCallback(
    async (frequency: number, targetNote: string, toleranceCents: number = 50) => {
      if (!enabled || processingRef.current) {
        console.log("⏭️ [ML INTEGRATION] checkPracticeWithFrequency ignorado (disabled ou processing)");
        return null;
      }

      console.group("🎓 [ML INTEGRATION] checkPracticeWithFrequency");
      console.log("📋 Parâmetros:", {
        frequency: frequency.toFixed(2) + " Hz",
        targetNote,
        toleranceCents,
        instrument: instrument || "none",
      });

      try {
        setIsProcessing(true);
        processingRef.current = true;
        setError(null);

        const result = await checkPracticeNote(frequency, targetNote, toleranceCents, instrument);

        console.log("✅ Resultado da validação:", {
          detected_note: result.detected_note,
          target_note: result.target_note,
          is_correct: result.is_correct,
          accuracy_score: result.accuracy_score,
          feedback_message: result.feedback_message,
        });

        setLastPracticeCheck(result);
        onPracticeCheck?.(result);

        console.groupEnd();
        return result;
      } catch (err: any) {
        const errorMessage = err.message || "Erro ao validar prática";
        console.error("❌ [ML INTEGRATION] Erro na validação de prática:", {
          error: err,
          message: errorMessage,
        });
        setError(errorMessage);
        onError?.(err);
        console.groupEnd();
        return null;
      } finally {
        setIsProcessing(false);
        processingRef.current = false;
      }
    },
    [enabled, instrument, onPracticeCheck, onError]
  );

  /**
   * Processa sessão de prática com dados de áudio
   */
  const processPracticeWithAudio = useCallback(
    async (audioData: number[], targetNote: string, sampleRate: number = 44100, toleranceCents: number = 50) => {
      if (!enabled || processingRef.current) return null;

      try {
        setIsProcessing(true);
        processingRef.current = true;
        setError(null);

        const result = await processPracticeSession(
          audioData,
          targetNote,
          sampleRate,
          toleranceCents,
          instrument
        );

        setLastPracticeCheck(result);
        onPracticeCheck?.(result);

        return result;
      } catch (err: any) {
        const errorMessage = err.message || "Erro ao processar prática";
        setError(errorMessage);
        onError?.(err);
        console.error("Erro no processamento de prática:", err);
        return null;
      } finally {
        setIsProcessing(false);
        processingRef.current = false;
      }
    },
    [enabled, instrument, onPracticeCheck, onError]
  );

  return {
    detectWithML,
    tuneWithML,
    processFrequency,
    checkPracticeWithFrequency,
    processPracticeWithAudio,
    isProcessing,
    lastDetection,
    lastTuning,
    lastPracticeCheck,
    error,
  };
}

