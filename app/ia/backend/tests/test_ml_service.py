"""
Unit tests for MLService
"""
import pytest
import numpy as np
from unittest.mock import Mock, patch
from ..services.ml_service import MLService
from ..models.practice import NoteAccuracy


class TestMLService:
    """Test cases for MLService"""
    
    @pytest.fixture
    def ml_service(self):
        """Create MLService instance for testing"""
        with patch('tensorflow.keras.Sequential'), \
             patch('tensorflow.keras.layers.Dense'):
            return MLService()
    
    @pytest.fixture
    def mock_audio_data(self):
        """Mock audio data for testing"""
        # Generate synthetic audio data (1 second of 440Hz sine wave)
        sample_rate = 44100
        duration = 1.0
        frequency = 440.0
        
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        return audio_data.astype(np.float32).tobytes()
    
    def test_preprocess_audio(self, ml_service, mock_audio_data):
        """Test audio preprocessing"""
        features = ml_service.preprocess_audio(mock_audio_data)
        
        assert isinstance(features, np.ndarray)
        assert len(features) == 1024  # Fixed feature size
        assert not np.isnan(features).any()
    
    def test_preprocess_empty_audio(self, ml_service):
        """Test preprocessing empty audio data"""
        empty_audio = b""
        features = ml_service.preprocess_audio(empty_audio)
        
        assert isinstance(features, np.ndarray)
        assert len(features) == 1024
        assert np.all(features == 0)
    
    def test_frequency_to_note(self, ml_service):
        """Test frequency to note conversion"""
        # Test A4 (440 Hz)
        note, cents = ml_service.frequency_to_note(440.0)
        assert note == "A4"
        assert abs(cents) < 5  # Should be very close to 0 cents
        
        # Test C4 (261.63 Hz)
        note, cents = ml_service.frequency_to_note(261.63)
        assert note == "C4"
        assert abs(cents) < 5
    
    def test_frequency_to_note_invalid(self, ml_service):
        """Test frequency to note with invalid frequency"""
        note, cents = ml_service.frequency_to_note(0.0)
        assert note == "Unknown"
        assert cents == 0.0
        
        note, cents = ml_service.frequency_to_note(-100.0)
        assert note == "Unknown"
        assert cents == 0.0
    
    def test_get_note_accuracy(self, ml_service):
        """Test note accuracy determination"""
        # Perfect accuracy
        accuracy = ml_service.get_note_accuracy(3.0)
        assert accuracy == NoteAccuracy.PERFECT
        
        # Good accuracy
        accuracy = ml_service.get_note_accuracy(8.0)
        assert accuracy == NoteAccuracy.GOOD
        
        # Fair accuracy
        accuracy = ml_service.get_note_accuracy(15.0)
        assert accuracy == NoteAccuracy.FAIR
        
        # Poor accuracy
        accuracy = ml_service.get_note_accuracy(25.0)
        assert accuracy == NoteAccuracy.POOR
    
    @patch('librosa.piptrack')
    @patch('librosa.util.normalize')
    async def test_detect_pitch_with_librosa(self, mock_normalize, mock_piptrack, ml_service, mock_audio_data):
        """Test pitch detection using librosa fallback"""
        # Mock librosa functions
        mock_normalize.return_value = np.array([0.1, 0.2, 0.3])
        mock_piptrack.return_value = (np.array([[440.0, 440.0]]), np.array([[0.8, 0.9]]))
        
        # Mock model as None to trigger librosa fallback
        ml_service.model = None
        
        frequency, confidence = ml_service.detect_pitch(mock_audio_data)
        
        assert frequency > 0
        assert 0 <= confidence <= 1
    
    async def test_detect_note(self, ml_service, mock_audio_data):
        """Test note detection"""
        detection = await ml_service.detect_note(mock_audio_data)
        
        assert detection.note is not None
        assert detection.frequency >= 0
        assert 0 <= detection.confidence <= 1
        assert detection.accuracy in [NoteAccuracy.PERFECT, NoteAccuracy.GOOD, NoteAccuracy.FAIR, NoteAccuracy.POOR]
    
    async def test_tune_instrument(self, ml_service, mock_audio_data):
        """Test instrument tuning"""
        result = await ml_service.tune_instrument(mock_audio_data, "A4")
        
        assert result.target_note == "A4"
        assert result.detected_note is not None
        assert result.frequency >= 0
        assert isinstance(result.cents_offset, float)
        assert isinstance(result.is_in_tune, bool)
        assert 0 <= result.confidence <= 1
    
    @patch('librosa.feature.chroma_stft')
    async def test_detect_chord(self, mock_chroma, ml_service, mock_audio_data):
        """Test chord detection"""
        # Mock chroma features
        mock_chroma.return_value = np.random.rand(12, 100)
        
        result = await ml_service.detect_chord(mock_audio_data)
        
        assert "chord" in result
        assert "confidence" in result
        assert "notes" in result
        assert isinstance(result["chord"], str)
        assert 0 <= result["confidence"] <= 1
        assert isinstance(result["notes"], list)
    
    async def test_process_audio_stream(self, ml_service):
        """Test audio stream processing"""
        # Create mock audio chunks
        audio_chunks = [
            b"chunk1",
            b"chunk2",
            b"chunk3"
        ]
        
        detections = await ml_service.process_audio_stream(audio_chunks)
        
        assert isinstance(detections, list)
        # Should filter out low confidence detections
    
    def test_get_tuning_notes_for_instrument(self, ml_service):
        """Test getting tuning notes for instruments"""
        # Test violin
        violin_notes = ml_service.get_tuning_notes_for_instrument("violin")
        assert violin_notes == ['G3', 'D4', 'A4', 'E5']
        
        # Test piano
        piano_notes = ml_service.get_tuning_notes_for_instrument("piano")
        assert piano_notes == ['A4']
        
        # Test unknown instrument
        unknown_notes = ml_service.get_tuning_notes_for_instrument("unknown")
        assert unknown_notes == ['A4']  # Default
    
    async def test_analyze_practice_session(self, ml_service):
        """Test practice session analysis"""
        # Create mock audio data
        audio_data = [b"audio1", b"audio2", b"audio3"]
        target_notes = ["A4", "B4", "C5"]
        
        result = await ml_service.analyze_practice_session(audio_data, target_notes)
        
        assert "total_notes" in result
        assert "correct_notes" in result
        assert "accuracy_percentage" in result
        assert "average_confidence" in result
        assert "feedback" in result
        assert "detections" in result
        
        assert isinstance(result["total_notes"], int)
        assert isinstance(result["correct_notes"], int)
        assert isinstance(result["accuracy_percentage"], float)
        assert isinstance(result["average_confidence"], float)
        assert isinstance(result["feedback"], str)
        assert isinstance(result["detections"], list)
    
    def test_note_frequencies_structure(self, ml_service):
        """Test that note frequencies are properly structured"""
        assert "C" in ml_service.note_frequencies
        assert "A" in ml_service.note_frequencies
        assert "B" in ml_service.note_frequencies
        
        # Check that each note has 9 octaves
        for note, frequencies in ml_service.note_frequencies.items():
            assert len(frequencies) == 9
            assert all(freq > 0 for freq in frequencies)
    
    def test_sample_rate_and_hop_length(self, ml_service):
        """Test that sample rate and hop length are set correctly"""
        assert ml_service.sample_rate == 44100
        assert ml_service.hop_length == 512
