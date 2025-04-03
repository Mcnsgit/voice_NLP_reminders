import { useState, useEffect} from 'react';
import { Audio } from 'expo-av';
import  { voiceApi } from '../api/voiceApi';
import  { VoiceProcessingResult } from '@/types'

export const useVoiceRecorder = () => {
    const [recording, setRecording] = useState<Audio.Recording | null>(null);
    const [recordingUri, setRecordingUri] = useState<string | null>(null);
    const [isRecording, setIsRecording] = useState(false);
    const [processingResult, setProcessingResult] = useState<VoiceProcessingResult | null>(null);

    const [error, setError] = useState<string | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    
    useEffect(() => {
      // Request permissions on component mount
      const getPermissions = async () => {
        const { granted } = await Audio.requestPermissionsAsync();
        if (!granted) {
          setError('Permission to access microphone is required');
        }
      };
      
      getPermissions();
      
      // Clean up recording when component unmounts
      return () => {
        if (recording) {
          recording.stopAndUnloadAsync();
        }
      };
    }, []);
    
    const startRecording = async () => {
      try {
        // Clear previous state
        setError(null);
        setProcessingResult(null);
        
        // Configure audio session
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: true,
          playsInSilentModeIOS: true,
        });
        
        // Start recording
        const { recording: newRecording } = await Audio.Recording.createAsync(
          Audio.RecordingOptionsPresets.HIGH_QUALITY
        );
        
        setRecording(newRecording);
        setIsRecording(true);
      } catch (err) {
        setError('Failed to start recording');
        console.error('Error starting recording:', err);
      }
    };
    
    const stopRecording = async () => {
      try {
        if (!recording) return;
        
        // Stop recording
        await recording.stopAndUnloadAsync();
        setIsRecording(false);
        
        // Get recording URI
        const uri = recording.getURI();
        if (uri) {
          setRecordingUri(uri);
        }
        
        // Reset recording object
        setRecording(null);
        
        // Reset audio mode
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: false,
        });
        
        return uri;
      } catch (err) {
        setError('Failed to stop recording');
        console.error('Error stopping recording:', err);
      }
    };
    
    const processRecording = async () => {
      if (!recordingUri) {
        setError('No recording to process');
        return null;
      }
      
      try {
        setIsProcessing(true);
        
        // Process the audio file
        const result = await voiceApi.processVoice(recordingUri);
        setProcessingResult(result);
        
        return result;
      } catch (err) {
        setError('Failed to process voice recording');
        console.error('Error processing recording:', err);
        return null;
      } finally {
        setIsProcessing(false);
      }
    };
    
    return {
      isRecording,
      startRecording,
      stopRecording,
      recordingUri,
      processingResult,
      processRecording,
      isProcessing,
      error,
    };
  };