import { useEffect, useRef, useCallback } from "react";

interface AudioData {
  frequency: number;
  note: string;
  confidence: number;
}

interface UseAudioProcessorOptions {
  analyser: AnalyserNode | null;
  isRecording: boolean;
  onAudioData?: (data: AudioData) => void;
  interval?: number; // Intervalo em ms para processar áudio
}

export function useAudioProcessor({
  analyser,
  isRecording,
  onAudioData,
  interval = 100, // Processar a cada 100ms
}: UseAudioProcessorOptions) {
  const animationFrameRef = useRef<number | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const frequencyDataRef = useRef<Uint8Array | null>(null);
  const timeDataRef = useRef<Float32Array | null>(null);

  // Função para detectar frequência usando FFT (Fast Fourier Transform)
  const detectFrequencyFFT = useCallback((
    frequencyData: Uint8Array,
    sampleRate: number,
    fftSize: number
  ): { frequency: number; confidence: number } | null => {
    const bufferLength = frequencyData.length;
    if (bufferLength < 2) return null;

    // Encontrar o pico de frequência
    let maxValue = 0;
    let maxIndex = 0;

    // Procurar pico na faixa de frequências musicais (80 Hz a 2000 Hz)
    const minBin = Math.floor((80 * fftSize) / sampleRate);
    const maxBin = Math.floor((2000 * fftSize) / sampleRate);

    for (let i = minBin; i < Math.min(maxBin, bufferLength); i++) {
      if (frequencyData[i] > maxValue) {
        maxValue = frequencyData[i];
        maxIndex = i;
      }
    }

    // Se não encontrou pico significativo, retorna null
    if (maxValue < 50) return null;

    // Calcular frequência do bin
    const frequency = (maxIndex * sampleRate) / fftSize;

    // Calcular confiança baseada na magnitude
    const confidence = Math.min(maxValue / 255, 1.0);

    // Refinamento usando interpolação parabólica para maior precisão
    if (maxIndex > 0 && maxIndex < bufferLength - 1) {
      const y1 = frequencyData[maxIndex - 1];
      const y2 = frequencyData[maxIndex];
      const y3 = frequencyData[maxIndex + 1];

      // Interpolação parabólica
      const denom = 2 * (2 * y2 - y1 - y3);
      if (denom !== 0) {
        const delta = (y3 - y1) / denom;
        const refinedFrequency = ((maxIndex + delta) * sampleRate) / fftSize;
        
        // Só usar frequência refinada se estiver na faixa válida
        if (refinedFrequency >= 80 && refinedFrequency <= 2000) {
          return {
            frequency: refinedFrequency,
            confidence: confidence
          };
        }
      }
    }

    return {
      frequency: frequency,
      confidence: confidence
    };
  }, []);

  // Função para detectar frequência usando autocorrelação (fallback)
  const detectFrequencyAutocorr = useCallback((
    buffer: Float32Array,
    sampleRate: number
  ): { frequency: number; confidence: number } | null => {
    const bufferLength = buffer.length;
    if (bufferLength < 2) return null;

    // Normalizar o buffer
    const normalized = new Float32Array(bufferLength);
    let max = 0;
    for (let i = 0; i < bufferLength; i++) {
      const abs = Math.abs(buffer[i]);
      if (abs > max) max = abs;
    }
    if (max === 0) return null;
    for (let i = 0; i < bufferLength; i++) {
      normalized[i] = buffer[i] / max;
    }

    // Autocorrelação melhorada
    let maxCorrelation = 0;
    let maxPeriod = 0;

    // Limitar busca a frequências entre 80 Hz e 2000 Hz
    const minPeriod = Math.floor(sampleRate / 2000);
    const maxPeriodSearch = Math.floor(sampleRate / 80);

    for (let period = minPeriod; period < Math.min(maxPeriodSearch, bufferLength / 2); period++) {
      let correlation = 0;
      let count = 0;

      for (let i = 0; i < bufferLength - period; i++) {
        correlation += normalized[i] * normalized[i + period];
        count++;
      }

      if (count > 0) {
        correlation /= count;

        // Aplicar janela para reduzir falsos positivos
        const window = 1 - Math.abs(period - (bufferLength / 4)) / (bufferLength / 2);
        correlation *= Math.max(0, window);

        if (correlation > maxCorrelation) {
          maxCorrelation = correlation;
          maxPeriod = period;
        }
      }
    }

    if (maxPeriod > 0 && maxCorrelation > 0.15) {
      const frequency = sampleRate / maxPeriod;
      if (frequency >= 80 && frequency <= 2000) {
        return {
          frequency: frequency,
          confidence: Math.min(maxCorrelation * 2, 1.0)
        };
      }
    }

    return null;
  }, []);

  // Função para converter frequência em nota musical
  const frequencyToNote = useCallback((frequency: number): { note: string; cents: number } => {
    const A4 = 440.0;
    const C0 = A4 * Math.pow(2, -4.75);
    const h = Math.round(12 * Math.log2(frequency / C0));
    const octave = Math.floor(h / 12);
    const n = h % 12;
    const noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const note = `${noteNames[n]}${octave}`;

    // Calcular cents de diferença
    const noteFrequency = C0 * Math.pow(2, h / 12);
    const cents = 1200 * Math.log2(frequency / noteFrequency);

    return { note, cents: Math.round(cents) };
  }, []);

  // Processar áudio
  const processAudio = useCallback(() => {
    if (!analyser || !isRecording) return;

    const bufferLength = analyser.frequencyBinCount;
    const sampleRate = analyser.context.sampleRate;
    const fftSize = analyser.fftSize;

    // Obter dados de frequência (FFT)
    if (!frequencyDataRef.current || frequencyDataRef.current.length !== bufferLength) {
      frequencyDataRef.current = new Uint8Array(bufferLength);
    }
    analyser.getByteFrequencyData(frequencyDataRef.current as unknown as Uint8Array<ArrayBuffer>);

    // Obter dados de tempo (para autocorrelação como fallback)
    if (!timeDataRef.current || timeDataRef.current.length !== bufferLength) {
      timeDataRef.current = new Float32Array(bufferLength);
    }
    analyser.getFloatTimeDomainData(timeDataRef.current as unknown as Float32Array<ArrayBuffer>);

    // Calcular volume médio para verificar se há som
    let sum = 0;
    for (let i = 0; i < bufferLength; i++) {
      sum += Math.abs(timeDataRef.current[i]);
    }
    const average = sum / bufferLength;

    // Se houver som suficiente, detectar frequência
    if (average > 0.01 && onAudioData) {
      // Tentar FFT primeiro (mais preciso)
      let result = detectFrequencyFFT(
        frequencyDataRef.current,
        sampleRate,
        fftSize
      );
      let method = "FFT";

      // Se FFT não funcionou bem, usar autocorrelação como fallback
      if (!result || result.confidence < 0.3) {
        result = detectFrequencyAutocorr(timeDataRef.current, sampleRate);
        method = "Autocorr";
      }

      if (result && result.frequency >= 80 && result.frequency <= 2000) {
        const { note, cents } = frequencyToNote(result.frequency);
        
        // Combinar confiança de volume e detecção
        const combinedConfidence = Math.min(
          (result.confidence * 0.7) + (Math.min(average * 5, 1) * 0.3),
          1.0
        );

        const audioData = {
          frequency: result.frequency,
          note,
          confidence: combinedConfidence,
        };

        // Debug logs
        console.log("🎵 [AUDIO PROCESSOR] Detecção:", {
          frequency: result.frequency.toFixed(2) + " Hz",
          note,
          cents: cents.toFixed(1) + " cents",
          confidence: (combinedConfidence * 100).toFixed(1) + "%",
          method,
          volume: (average * 100).toFixed(1) + "%",
          sampleRate,
          fftSize,
        });

        onAudioData(audioData);
      } else if (average > 0.01) {
        // Log quando há som mas não detectou frequência válida
        console.warn("⚠️ [AUDIO PROCESSOR] Som detectado mas frequência inválida:", {
          average: (average * 100).toFixed(1) + "%",
          result: result ? {
            frequency: result.frequency,
            confidence: result.confidence,
          } : "null",
        });
      }
    }
  }, [
    analyser,
    isRecording,
    onAudioData,
    detectFrequencyFFT,
    detectFrequencyAutocorr,
    frequencyToNote
  ]);

  useEffect(() => {
    if (isRecording && analyser) {
      // Processar áudio em intervalos regulares
      intervalRef.current = setInterval(() => {
        processAudio();
      }, interval);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isRecording, analyser, interval, processAudio]);
}

