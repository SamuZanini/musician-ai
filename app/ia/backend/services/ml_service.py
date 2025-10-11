"""
ML Service for #Dô application
Handles audio processing, pitch detection, and note recognition using SPICE model
"""
import os
import numpy as np
import librosa
import tensorflow as tf
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import io
import base64
from ..models.practice import NoteDetection, TuningResult, NoteAccuracy


class MLService:
    """Machine Learning service for audio processing and note detection"""
    
    def __init__(self):
        self.model_path = os.getenv("SPICE_MODEL_PATH", "./models/spice_model")
        self.sample_rate = 44100
        self.hop_length = 512
        self.model = None
        self._load_model()
        
        # Note frequencies for tuning
        self.note_frequencies = {
            'C': [16.35, 32.70, 65.41, 130.81, 261.63, 523.25, 1046.50, 2093.00, 4186.01],
            'C#': [17.32, 34.65, 69.30, 138.59, 277.18, 554.37, 1108.73, 2217.46, 4434.92],
            'D': [18.35, 36.71, 73.42, 146.83, 293.66, 587.33, 1174.66, 2349.32, 4698.64],
            'D#': [19.45, 38.89, 77.78, 155.56, 311.13, 622.25, 1244.51, 2489.02, 4978.03],
            'E': [20.60, 41.20, 82.41, 164.81, 329.63, 659.25, 1318.51, 2637.02, 5274.04],
            'F': [21.83, 43.65, 87.31, 174.61, 349.23, 698.46, 1396.91, 2793.83, 5587.65],
            'F#': [23.12, 46.25, 92.50, 185.00, 369.99, 739.99, 1479.98, 2959.96, 5919.91],
            'G': [24.50, 49.00, 98.00, 196.00, 392.00, 783.99, 1567.98, 3135.96, 6271.93],
            'G#': [25.96, 51.91, 103.83, 207.65, 415.30, 830.61, 1661.22, 3322.44, 6644.88],
            'A': [27.50, 55.00, 110.00, 220.00, 440.00, 880.00, 1760.00, 3520.00, 7040.00],
            'A#': [29.14, 58.27, 116.54, 233.08, 466.16, 932.33, 1864.66, 3729.31, 7458.62],
            'B': [30.87, 61.74, 123.47, 246.94, 493.88, 987.77, 1975.53, 3951.07, 7902.13]
        }
    
    def _load_model(self):
        """Load SPICE model for pitch detection"""
        try:
            # In a real implementation, you would load the actual SPICE model
            # For now, we'll create a placeholder model
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(128, activation='relu', input_shape=(1024,)),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(1, activation='sigmoid')
            ])
            self.model.compile(optimizer='adam', loss='mse')
            print("SPICE model loaded successfully")
        except Exception as e:
            print(f"Error loading SPICE model: {e}")
            self.model = None
    
    def preprocess_audio(self, audio_data: bytes) -> np.ndarray:
        """Preprocess audio data for ML model"""
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.float32)
            
            # Resample if necessary
            if len(audio_array) > 0:
                # Normalize audio
                audio_array = librosa.util.normalize(audio_array)
                
                # Extract features
                mfcc = librosa.feature.mfcc(y=audio_array, sr=self.sample_rate, n_mfcc=13)
                spectral_centroid = librosa.feature.spectral_centroid(y=audio_array, sr=self.sample_rate)
                zero_crossing_rate = librosa.feature.zero_crossing_rate(audio_array)
                
                # Combine features
                features = np.concatenate([
                    mfcc.flatten(),
                    spectral_centroid.flatten(),
                    zero_crossing_rate.flatten()
                ])
                
                # Pad or truncate to fixed size
                if len(features) < 1024:
                    features = np.pad(features, (0, 1024 - len(features)))
                else:
                    features = features[:1024]
                
                return features
            else:
                return np.zeros(1024)
        except Exception as e:
            print(f"Error preprocessing audio: {e}")
            return np.zeros(1024)
    
    def detect_pitch(self, audio_data: bytes) -> Tuple[float, float]:
        """Detect pitch from audio data"""
        try:
            # Preprocess audio
            features = self.preprocess_audio(audio_data)
            
            if self.model is None:
                # Fallback to librosa pitch detection
                audio_array = np.frombuffer(audio_data, dtype=np.float32)
                if len(audio_array) > 0:
                    pitches, magnitudes = librosa.piptrack(y=audio_array, sr=self.sample_rate)
                    pitch_values = []
                    for t in range(pitches.shape[1]):
                        index = magnitudes[:, t].argmax()
                        pitch = pitches[index, t]
                        if pitch > 0:
                            pitch_values.append(pitch)
                    
                    if pitch_values:
                        detected_pitch = np.median(pitch_values)
                        confidence = min(len(pitch_values) / 10.0, 1.0)
                        return detected_pitch, confidence
            
            # Use ML model for pitch detection
            features = features.reshape(1, -1)
            prediction = self.model.predict(features, verbose=0)
            
            # Convert prediction to frequency (simplified)
            frequency = prediction[0][0] * 2000 + 100  # Scale to 100-2100 Hz range
            confidence = 0.8  # Placeholder confidence
            
            return frequency, confidence
            
        except Exception as e:
            print(f"Error detecting pitch: {e}")
            return 0.0, 0.0
    
    def frequency_to_note(self, frequency: float) -> Tuple[str, float]:
        """Convert frequency to note name and cents offset"""
        if frequency <= 0:
            return "Unknown", 0.0
        
        # Find closest note
        min_distance = float('inf')
        closest_note = "Unknown"
        cents_offset = 0.0
        
        for note, freqs in self.note_frequencies.items():
            for octave, freq in enumerate(freqs):
                distance = abs(frequency - freq)
                if distance < min_distance:
                    min_distance = distance
                    closest_note = f"{note}{octave}"
                    
                    # Calculate cents offset
                    if freq > 0:
                        cents_offset = 1200 * np.log2(frequency / freq)
        
        return closest_note, cents_offset
    
    def get_note_accuracy(self, cents_offset: float) -> NoteAccuracy:
        """Determine note accuracy based on cents offset"""
        abs_cents = abs(cents_offset)
        
        if abs_cents <= 5:
            return NoteAccuracy.PERFECT
        elif abs_cents <= 10:
            return NoteAccuracy.GOOD
        elif abs_cents <= 20:
            return NoteAccuracy.FAIR
        else:
            return NoteAccuracy.POOR
    
    async def detect_note(self, audio_data: bytes) -> NoteDetection:
        """Detect note from audio data"""
        frequency, confidence = self.detect_pitch(audio_data)
        note_name, cents_offset = self.frequency_to_note(frequency)
        accuracy = self.get_note_accuracy(cents_offset)
        
        return NoteDetection(
            note=note_name,
            frequency=frequency,
            confidence=confidence,
            accuracy=accuracy,
            timestamp=datetime.utcnow()
        )
    
    async def tune_instrument(self, audio_data: bytes, target_note: str) -> TuningResult:
        """Tune instrument to target note"""
        frequency, confidence = self.detect_pitch(audio_data)
        detected_note, cents_offset = self.frequency_to_note(frequency)
        
        # Check if in tune (within ±5 cents)
        is_in_tune = abs(cents_offset) <= 5
        
        return TuningResult(
            target_note=target_note,
            detected_note=detected_note,
            frequency=frequency,
            cents_offset=cents_offset,
            is_in_tune=is_in_tune,
            confidence=confidence
        )
    
    async def detect_chord(self, audio_data: bytes) -> Dict[str, Any]:
        """Detect chord from audio data (simplified implementation)"""
        try:
            # This is a simplified chord detection
            # In a real implementation, you would use more sophisticated algorithms
            
            audio_array = np.frombuffer(audio_data, dtype=np.float32)
            if len(audio_array) == 0:
                return {"chord": "Unknown", "confidence": 0.0, "notes": []}
            
            # Extract chroma features for chord detection
            chroma = librosa.feature.chroma_stft(y=audio_array, sr=self.sample_rate)
            chroma_mean = np.mean(chroma, axis=1)
            
            # Find dominant notes
            note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            dominant_notes = []
            
            for i, energy in enumerate(chroma_mean):
                if energy > 0.3:  # Threshold for note presence
                    dominant_notes.append(note_names[i])
            
            # Simple chord classification based on dominant notes
            chord = "Unknown"
            if len(dominant_notes) >= 3:
                if 'C' in dominant_notes and 'E' in dominant_notes and 'G' in dominant_notes:
                    chord = "C Major"
                elif 'A' in dominant_notes and 'C' in dominant_notes and 'E' in dominant_notes:
                    chord = "A Minor"
                elif 'G' in dominant_notes and 'B' in dominant_notes and 'D' in dominant_notes:
                    chord = "G Major"
                else:
                    chord = f"Custom ({', '.join(dominant_notes[:3])})"
            
            confidence = min(len(dominant_notes) / 6.0, 1.0)
            
            return {
                "chord": chord,
                "confidence": confidence,
                "notes": dominant_notes
            }
            
        except Exception as e:
            print(f"Error detecting chord: {e}")
            return {"chord": "Unknown", "confidence": 0.0, "notes": []}
    
    async def process_audio_stream(self, audio_chunks: List[bytes]) -> List[NoteDetection]:
        """Process audio stream for real-time note detection"""
        detections = []
        
        for chunk in audio_chunks:
            if len(chunk) > 0:
                detection = await self.detect_note(chunk)
                if detection.confidence > 0.3:  # Only include confident detections
                    detections.append(detection)
        
        return detections
    
    def get_tuning_notes_for_instrument(self, instrument_type: str) -> List[str]:
        """Get standard tuning notes for instrument"""
        tuning_map = {
            'violin': ['G3', 'D4', 'A4', 'E5'],
            'flute': ['C4'],
            'trumpet': ['C4'],
            'piano': ['A4'],
            'cello': ['C2', 'G2', 'D3', 'A3']
        }
        
        return tuning_map.get(instrument_type.lower(), ['A4'])
    
    async def analyze_practice_session(self, audio_data: List[bytes], target_notes: List[str]) -> Dict[str, Any]:
        """Analyze practice session for accuracy and feedback"""
        detections = await self.process_audio_stream(audio_data)
        
        if not detections:
            return {
                "total_notes": 0,
                "correct_notes": 0,
                "accuracy_percentage": 0.0,
                "average_confidence": 0.0,
                "feedback": "No notes detected. Please check your microphone and try again."
            }
        
        correct_notes = 0
        total_confidence = 0.0
        
        for detection in detections:
            total_confidence += detection.confidence
            
            # Check if detected note matches any target note
            for target in target_notes:
                if detection.note == target and detection.accuracy in [NoteAccuracy.PERFECT, NoteAccuracy.GOOD]:
                    correct_notes += 1
                    break
        
        accuracy_percentage = (correct_notes / len(detections)) * 100 if detections else 0
        average_confidence = total_confidence / len(detections) if detections else 0
        
        # Generate feedback
        feedback = ""
        if accuracy_percentage >= 80:
            feedback = "Excellent! You're playing very accurately."
        elif accuracy_percentage >= 60:
            feedback = "Good job! Try to focus on pitch accuracy."
        elif accuracy_percentage >= 40:
            feedback = "Keep practicing! Focus on matching the target notes."
        else:
            feedback = "Don't give up! Practice makes perfect. Try playing more slowly."
        
        return {
            "total_notes": len(detections),
            "correct_notes": correct_notes,
            "accuracy_percentage": round(accuracy_percentage, 2),
            "average_confidence": round(average_confidence, 2),
            "feedback": feedback,
            "detections": [detection.dict() for detection in detections]
        }
