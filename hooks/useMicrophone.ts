import { useState, useEffect, useRef, useCallback } from "react";

interface UseMicrophoneReturn {
  isRecording: boolean;
  error: string | null;
  startRecording: () => Promise<void>;
  stopRecording: () => void;
  audioContext: AudioContext | null;
  analyser: AnalyserNode | null;
  stream: MediaStream | null;
}

export function useMicrophone(): UseMicrophoneReturn {
  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [audioContext, setAudioContext] = useState<AudioContext | null>(null);
  const [analyser, setAnalyser] = useState<AnalyserNode | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  
  const streamRef = useRef<MediaStream | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const sourceRef = useRef<MediaStreamAudioSourceNode | null>(null);

  const startRecording = useCallback(async () => {
    try {
      setError(null);
      
      console.group("🎤 [MICROPHONE] Iniciando gravação");
      console.log("📋 Configuração:", {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        sampleRate: 44100,
      });
      
      // Solicitar acesso ao microfone
      console.log("🔐 Solicitando permissão de microfone...");
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 44100,
        },
      });

      console.log("✅ Permissão concedida");
      console.log("📊 Stream de mídia:", {
        id: mediaStream.id,
        active: mediaStream.active,
        tracks: mediaStream.getTracks().map(t => ({
          id: t.id,
          kind: t.kind,
          enabled: t.enabled,
          readyState: t.readyState,
          settings: t.getSettings(),
        })),
      });

      streamRef.current = mediaStream;
      setStream(mediaStream);

      // Criar AudioContext
      const AudioContextClass = 
        (window.AudioContext as typeof AudioContext) || 
        ((window as any).webkitAudioContext as typeof AudioContext);
      const ctx = new AudioContextClass({ sampleRate: 44100 });
      audioContextRef.current = ctx;
      setAudioContext(ctx);

      console.log("🎵 AudioContext criado:", {
        sampleRate: ctx.sampleRate,
        state: ctx.state,
        baseLatency: ctx.baseLatency,
        outputLatency: ctx.outputLatency,
      });

      // Criar AnalyserNode para análise de áudio
      // FFT size maior = maior resolução de frequência
      const analyserNode = ctx.createAnalyser();
      analyserNode.fftSize = 8192; // Aumentado para melhor resolução (4096 bins)
      analyserNode.smoothingTimeConstant = 0.3; // Reduzido para resposta mais rápida
      analyserNode.minDecibels = -90;
      analyserNode.maxDecibels = -10;
      analyserRef.current = analyserNode;
      setAnalyser(analyserNode);

      console.log("🔍 AnalyserNode configurado:", {
        fftSize: analyserNode.fftSize,
        frequencyBinCount: analyserNode.frequencyBinCount,
        smoothingTimeConstant: analyserNode.smoothingTimeConstant,
        minDecibels: analyserNode.minDecibels,
        maxDecibels: analyserNode.maxDecibels,
      });

      // Conectar o stream ao analyser
      const source = ctx.createMediaStreamSource(mediaStream);
      sourceRef.current = source;
      source.connect(analyserNode);

      console.log("🔗 Stream conectado ao AnalyserNode");
      console.log("✅ Gravação iniciada com sucesso");
      console.groupEnd();

      setIsRecording(true);
    } catch (err: any) {
      console.group("❌ [MICROPHONE] Erro ao iniciar gravação");
      console.error("Erro:", err);
      console.error("Mensagem:", err.message);
      console.error("Nome:", err.name);
      if (err.constraint) {
        console.error("Constraint:", err.constraint);
      }
      console.groupEnd();
      setError(err.message || "Erro ao acessar o microfone. Verifique as permissões.");
      setIsRecording(false);
    }
  }, []);

  const stopRecording = useCallback(() => {
    console.group("🛑 [MICROPHONE] Parando gravação");
    
    // Parar todas as tracks do stream
    if (streamRef.current) {
      const tracks = streamRef.current.getTracks();
      console.log(`🛑 Parando ${tracks.length} track(s) de áudio`);
      tracks.forEach((track) => {
        track.stop();
        console.log(`  ✓ Track ${track.id} parada (${track.kind})`);
      });
      streamRef.current = null;
      setStream(null);
    }

    // Fechar AudioContext
    if (audioContextRef.current) {
      console.log("🔒 Fechando AudioContext...");
      audioContextRef.current.close()
        .then(() => {
          console.log("✅ AudioContext fechado");
        })
        .catch((err) => {
          console.error("❌ Erro ao fechar AudioContext:", err);
        });
      audioContextRef.current = null;
      setAudioContext(null);
    }

    // Limpar referências
    if (sourceRef.current) {
      console.log("🔌 Desconectando source...");
      sourceRef.current.disconnect();
      sourceRef.current = null;
    }

    analyserRef.current = null;
    setAnalyser(null);
    setIsRecording(false);
    
    console.log("✅ Gravação parada");
    console.groupEnd();
  }, []);

  // Cleanup ao desmontar
  useEffect(() => {
    return () => {
      stopRecording();
    };
  }, [stopRecording]);

  return {
    isRecording,
    error,
    startRecording,
    stopRecording,
    audioContext,
    analyser,
    stream,
  };
}

