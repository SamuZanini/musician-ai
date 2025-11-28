/**
 * Cliente para os serviços de ML do Musician AI
 * Conecta o frontend com os endpoints de Machine Learning
 */

const ML_SERVICE_URL = process.env.NEXT_PUBLIC_ML_SERVICE_URL || "http://localhost:8001";
const TUNER_SERVICE_URL = process.env.NEXT_PUBLIC_TUNER_SERVICE_URL || "http://localhost:8002";
const DETECTION_SERVICE_URL = process.env.NEXT_PUBLIC_DETECTION_SERVICE_URL || "http://localhost:8003";
const PRACTICE_SERVICE_URL = process.env.NEXT_PUBLIC_PRACTICE_SERVICE_URL || "http://localhost:8004";

// Tipos para as respostas da API
export interface TuningResponse {
  note: string;
  frequency: number;
  is_in_tune: boolean;
  cents_diff: number;
  tuning_direction: string;
  confidence: number;
}

export interface DetectionResponse {
  pitch: number | null;
  note: string;
  confidence: number;
  is_detected: boolean;
}

export interface TunerResponse {
  current_note: string;
  target_note: string;
  frequency: number;
  target_frequency: number;
  cents_diff: number;
  is_in_tune: boolean;
  tuning_direction: string;
  confidence: number;
}

export interface DetectionServiceResponse {
  pitch: number | null;
  note: string;
  confidence: number;
  is_detected: boolean;
  timestamp: number;
  instrument?: string;
}

export interface PracticeCheckResponse {
  detected_note: string;
  target_note: string;
  frequency: number;
  target_frequency: number;
  is_correct: boolean;
  confidence: number;
  cents_diff: number;
  accuracy_score: number;
  feedback_message: string;
  tuning_direction: string;
  harmonics_detected?: number[] | null;
}

export interface PracticeSessionResponse {
  detected_note: string;
  target_note: string;
  pitch: number | null;
  target_frequency: number;
  is_correct: boolean;
  confidence: number;
  cents_diff: number;
  accuracy_score: number;
  feedback_message: string;
  tuning_direction: string;
  is_detected: boolean;
  harmonics_detected?: number[] | null;
}

/**
 * ML Service - Detecção básica de pitch e notas
 */

/**
 * Detecta pitch e nota a partir de dados de áudio
 */
export async function detectAudio(
  audioData: number[],
  sampleRate: number = 44100
): Promise<DetectionResponse> {
  const startTime = performance.now();
  console.group("🔍 [ML SERVICE] detectAudio");
  console.log("📤 Request:", {
    url: `${ML_SERVICE_URL}/detect`,
    method: "POST",
    audioDataLength: audioData.length,
    sampleRate,
    audioDataSample: audioData.slice(0, 10), // Primeiros 10 valores para debug
  });

  try {
    const response = await fetch(`${ML_SERVICE_URL}/detect`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        audio_data: audioData,
        sample_rate: sampleRate,
      }),
    });

    const duration = performance.now() - startTime;
    console.log("📥 Response:", {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: duration.toFixed(2) + "ms",
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Erro HTTP:", {
        status: response.status,
        statusText: response.statusText,
        body: errorText,
      });
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Data recebida:", data);
    console.groupEnd();
    return data;
  } catch (error) {
    const duration = performance.now() - startTime;
    console.error("❌ [ML SERVICE] Erro ao detectar áudio:", {
      error,
      duration: duration.toFixed(2) + "ms",
    });
    console.groupEnd();
    throw error;
  }
}

/**
 * Obtém feedback de afinação a partir de uma frequência
 */
export async function tuneAudio(
  frequency: number,
  toleranceCents: number = 50
): Promise<TuningResponse> {
  try {
    const response = await fetch(`${ML_SERVICE_URL}/tune`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        frequency: frequency,
        tolerance_cents: toleranceCents,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Erro ao afinar áudio:", error);
    throw error;
  }
}

/**
 * Verifica saúde do ML Service
 */
export async function checkMLServiceHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${ML_SERVICE_URL}/health`);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === "healthy";
  } catch (error) {
    console.error("Erro ao verificar saúde do ML Service:", error);
    return false;
  }
}

/**
 * Tuner Service - Afinação específica por instrumento
 */

/**
 * Afina para um instrumento específico
 */
export async function tuneInstrument(
  instrument: string,
  frequency: number,
  toleranceCents: number = 50
): Promise<TunerResponse> {
  const startTime = performance.now();
  console.group(`🎸 [TUNER SERVICE] tuneInstrument (${instrument})`);
  console.log("📤 Request:", {
    url: `${TUNER_SERVICE_URL}/tune/${instrument}`,
    method: "POST",
    frequency: frequency.toFixed(2) + " Hz",
    toleranceCents,
  });

  try {
    const response = await fetch(`${TUNER_SERVICE_URL}/tune/${instrument}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        frequency: frequency,
        tolerance_cents: toleranceCents,
      }),
    });

    const duration = performance.now() - startTime;
    console.log("📥 Response:", {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: duration.toFixed(2) + "ms",
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Erro HTTP:", {
        status: response.status,
        statusText: response.statusText,
        body: errorText,
      });
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Data recebida:", data);
    console.groupEnd();
    return data;
  } catch (error) {
    const duration = performance.now() - startTime;
    console.error(`❌ [TUNER SERVICE] Erro ao afinar ${instrument}:`, {
      error,
      duration: duration.toFixed(2) + "ms",
    });
    console.groupEnd();
    throw error;
  }
}

/**
 * Obtém notas de afinação de um instrumento
 */
export async function getInstrumentNotes(
  instrument: string
): Promise<{ instrument: string; notes: Record<string, number>; total_notes: number }> {
  try {
    const response = await fetch(`${TUNER_SERVICE_URL}/instruments/${instrument}/notes`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Erro ao obter notas do ${instrument}:`, error);
    throw error;
  }
}

/**
 * Obtém lista de instrumentos suportados
 */
export async function getSupportedInstruments(): Promise<string[]> {
  try {
    const response = await fetch(`${TUNER_SERVICE_URL}/instruments`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.instruments || [];
  } catch (error) {
    console.error("Erro ao obter instrumentos:", error);
    return [];
  }
}

/**
 * Detection Service - Detecção em tempo real
 */

/**
 * Detecta áudio usando o Detection Service
 */
export async function detectAudioAdvanced(
  audioData: number[],
  sampleRate: number = 44100,
  instrument?: string
): Promise<DetectionServiceResponse> {
  const startTime = performance.now();
  console.group("🔬 [DETECTION SERVICE] detectAudioAdvanced");
  console.log("📤 Request:", {
    url: `${DETECTION_SERVICE_URL}/detect`,
    method: "POST",
    audioDataLength: audioData.length,
    sampleRate,
    instrument: instrument || "none",
    audioDataSample: audioData.slice(0, 10),
  });

  try {
    const response = await fetch(`${DETECTION_SERVICE_URL}/detect`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        audio_data: audioData,
        sample_rate: sampleRate,
        instrument: instrument,
      }),
    });

    const duration = performance.now() - startTime;
    console.log("📥 Response:", {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: duration.toFixed(2) + "ms",
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Erro HTTP:", {
        status: response.status,
        statusText: response.statusText,
        body: errorText,
      });
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Data recebida:", data);
    console.groupEnd();
    return data;
  } catch (error) {
    const duration = performance.now() - startTime;
    console.error("❌ [DETECTION SERVICE] Erro ao detectar áudio (advanced):", {
      error,
      duration: duration.toFixed(2) + "ms",
    });
    console.groupEnd();
    throw error;
  }
}

/**
 * Verifica saúde do Detection Service
 */
export async function checkDetectionServiceHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${DETECTION_SERVICE_URL}/health`);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === "healthy";
  } catch (error) {
    console.error("Erro ao verificar saúde do Detection Service:", error);
    return false;
  }
}

/**
 * Practice Service - Validação de prática musical
 */

/**
 * Valida se a nota tocada corresponde à nota alvo (usando frequência)
 */
export async function checkPracticeNote(
  frequency: number,
  targetNote: string,
  toleranceCents: number = 50,
  instrument?: string
): Promise<PracticeCheckResponse> {
  const startTime = performance.now();
  console.group("🎓 [PRACTICE SERVICE] checkPracticeNote");
  console.log("📤 Request:", {
    url: `${PRACTICE_SERVICE_URL}/practice/check`,
    method: "POST",
    frequency: frequency.toFixed(2) + " Hz",
    targetNote,
    toleranceCents,
    instrument: instrument || "none",
  });

  try {
    const response = await fetch(`${PRACTICE_SERVICE_URL}/practice/check`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        frequency: frequency,
        target_note: targetNote,
        tolerance_cents: toleranceCents,
        instrument: instrument,
      }),
    });

    const duration = performance.now() - startTime;
    console.log("📥 Response:", {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: duration.toFixed(2) + "ms",
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Erro HTTP:", {
        status: response.status,
        statusText: response.statusText,
        body: errorText,
      });
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Data recebida:", {
      detected_note: data.detected_note,
      target_note: data.target_note,
      is_correct: data.is_correct,
      accuracy_score: data.accuracy_score,
      feedback_message: data.feedback_message,
      cents_diff: data.cents_diff,
    });
    console.groupEnd();
    return data;
  } catch (error) {
    const duration = performance.now() - startTime;
    console.error("❌ [PRACTICE SERVICE] Erro ao validar nota de prática:", {
      error,
      duration: duration.toFixed(2) + "ms",
    });
    console.groupEnd();
    throw error;
  }
}

/**
 * Processa áudio de uma sessão de prática e valida contra nota alvo
 */
export async function processPracticeSession(
  audioData: number[],
  targetNote: string,
  sampleRate: number = 44100,
  toleranceCents: number = 50,
  instrument?: string
): Promise<PracticeSessionResponse> {
  const startTime = performance.now();
  console.group("🎓 [PRACTICE SERVICE] processPracticeSession");
  console.log("📤 Request:", {
    url: `${PRACTICE_SERVICE_URL}/practice/session`,
    method: "POST",
    audioDataLength: audioData.length,
    targetNote,
    sampleRate,
    toleranceCents,
    instrument: instrument || "none",
    audioDataSample: audioData.slice(0, 10),
  });

  try {
    const response = await fetch(`${PRACTICE_SERVICE_URL}/practice/session`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        audio_data: audioData,
        target_note: targetNote,
        sample_rate: sampleRate,
        tolerance_cents: toleranceCents,
        instrument: instrument,
      }),
    });

    const duration = performance.now() - startTime;
    console.log("📥 Response:", {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
      duration: duration.toFixed(2) + "ms",
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("❌ Erro HTTP:", {
        status: response.status,
        statusText: response.statusText,
        body: errorText,
      });
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log("✅ Data recebida:", {
      detected_note: data.detected_note,
      target_note: data.target_note,
      is_correct: data.is_correct,
      accuracy_score: data.accuracy_score,
      feedback_message: data.feedback_message,
      is_detected: data.is_detected,
      pitch: data.pitch,
    });
    console.groupEnd();
    return data;
  } catch (error) {
    const duration = performance.now() - startTime;
    console.error("❌ [PRACTICE SERVICE] Erro ao processar sessão de prática:", {
      error,
      duration: duration.toFixed(2) + "ms",
    });
    console.groupEnd();
    throw error;
  }
}

/**
 * Verifica saúde do Practice Service
 */
export async function checkPracticeServiceHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${PRACTICE_SERVICE_URL}/health`);
    if (!response.ok) return false;
    const data = await response.json();
    return data.status === "healthy";
  } catch (error) {
    console.error("Erro ao verificar saúde do Practice Service:", error);
    return false;
  }
}

