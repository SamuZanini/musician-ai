"""
Processador de áudio para detecção de pitch e notas musicais
Implementação usando librosa para detecção de pitch em tempo real
"""

import numpy as np
import librosa
from typing import Tuple, Optional, Dict
import logging

class AudioProcessor:
    """Classe para processamento de áudio e detecção de pitch"""
    
    def __init__(self, sample_rate: int = 44100, hop_size: int = 512):
        """
        Inicializa o processador de áudio
        
        Args:
            sample_rate: Taxa de amostragem do áudio
            hop_size: Tamanho do hop para análise
        """
        self.sample_rate = sample_rate
        self.hop_size = hop_size
        
        # Configuração de logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Notas musicais e suas frequências
        self.note_frequencies = self._generate_note_frequencies()
    
    def _generate_note_frequencies(self) -> Dict[str, float]:
        """Gera dicionário com frequências das notas musicais"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        frequencies = {}
        
        # A4 = 440Hz (nota de referência)
        a4_freq = 440.0
        
        for octave in range(0, 8):
            for i, note in enumerate(notes):
                # Cálculo da frequência usando a fórmula: f = f0 * 2^(n/12)
                # onde n é o número de semitons a partir de A4
                note_name = f"{note}{octave}"
                
                # A4 está na oitava 4, posição 9 (A)
                if octave == 4 and note == 'A':
                    frequencies[note_name] = a4_freq
                else:
                    # Cálculo do número de semitons a partir de A4
                    if octave < 4:
                        semitones = (octave - 4) * 12 + (i - 9)  # A está na posição 9
                    else:
                        semitones = (octave - 4) * 12 + (i - 9)
                    
                    freq = a4_freq * (2 ** (semitones / 12))
                    frequencies[note_name] = freq
        
        return frequencies
    
    def detect_pitch(self, audio_data: np.ndarray) -> Tuple[Optional[float], float]:
        """
        Detecta o pitch (frequência) do áudio
        
        Args:
            audio_data: Array numpy com dados de áudio
            
        Returns:
            Tuple com (frequência detectada, confiança)
        """
        try:
            # Converte para float32 se necessário
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Detecta pitch usando librosa
            pitches, magnitudes = librosa.piptrack(
                y=audio_data, 
                sr=self.sample_rate, 
                hop_length=self.hop_size,
                fmin=80,
                fmax=2000
            )
            
            # Obtém o pitch mais forte
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if pitch_values:
                pitch = np.median(pitch_values)
                confidence = min(1.0, np.mean(magnitudes) * 10)
                
                # Filtra pitches muito baixos (ruído)
                if pitch > 80:
                    return float(pitch), float(confidence)
            
            return None, 0.0
                
        except Exception as e:
            self.logger.error(f"Erro na detecção de pitch: {e}")
            return None, 0.0
    
    def frequency_to_note(self, frequency: float) -> Tuple[str, float]:
        """
        Converte frequência para nota musical
        
        Args:
            frequency: Frequência em Hz
            
        Returns:
            Tuple com (nome da nota, diferença em cents)
        """
        if frequency is None or frequency <= 0:
            return "Silêncio", 0.0
        
        # Encontra a nota mais próxima
        closest_note = None
        min_diff = float('inf')
        
        for note_name, note_freq in self.note_frequencies.items():
            diff = abs(frequency - note_freq)
            if diff < min_diff:
                min_diff = diff
                closest_note = note_name
        
        # Calcula a diferença em cents
        if closest_note and closest_note in self.note_frequencies:
            note_freq = self.note_frequencies[closest_note]
            cents = 1200 * np.log2(frequency / note_freq)
            return closest_note, cents
        else:
            return "Desconhecida", 0.0
    
    def is_in_tune(self, frequency: float, tolerance_cents: float = 50) -> bool:
        """
        Verifica se a frequência está afinada
        
        Args:
            frequency: Frequência detectada
            tolerance_cents: Tolerância em cents (padrão: 50 cents)
            
        Returns:
            True se estiver afinada, False caso contrário
        """
        if frequency is None:
            return False
        
        _, cents_diff = self.frequency_to_note(frequency)
        return abs(cents_diff) <= tolerance_cents
    
    def get_tuning_feedback(self, frequency: float) -> Dict[str, any]:
        """
        Retorna feedback completo de afinação
        
        Args:
            frequency: Frequência detectada
            
        Returns:
            Dicionário com informações de afinação
        """
        if frequency is None or frequency <= 0:
            return {
                "note": "Silêncio",
                "frequency": 0,
                "is_in_tune": False,
                "cents_diff": 0,
                "tuning_direction": "Nenhum",
                "confidence": 0
            }
        
        note, cents_diff = self.frequency_to_note(frequency)
        is_tuned = self.is_in_tune(frequency)
        
        # Determina direção de afinação
        if abs(cents_diff) <= 50:
            tuning_direction = "Afinado"
        elif cents_diff > 0:
            tuning_direction = "Muito alto"
        else:
            tuning_direction = "Muito baixo"
        
        return {
            "note": note,
            "frequency": round(frequency, 2),
            "is_in_tune": is_tuned,
            "cents_diff": round(cents_diff, 1),
            "tuning_direction": tuning_direction,
            "confidence": 0.8  # Confiança simulada
        }
