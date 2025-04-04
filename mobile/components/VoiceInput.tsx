import React, { useState, useEffect } from 'react';
import { View, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { setupVoiceRecognition, startListening, stopListening } from '../services/voiceRecognition';
import { parseCommand, generateConfirmation } from '../services/commandParser';
import { TaskStorage } from '../services/taskStorage';
import { IconSymbol } from './ui/IconSymbol';
import { ThemedText } from './ThemedText';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Colors } from '@/constants/Colors';
interface VoiceInputProps {
  onTaskAdded: (task: any, isList?: boolean) => void;
}
export default function VoiceInput({ onTaskAdded }: VoiceInputProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [error, setError] = useState('');
  const colorScheme = useColorScheme() ?? 'light';
  // Initialize voice recognition
  useEffect(() => {
    const initialize = async () => {
      try {
        const result = await setupVoiceRecognition();
        if (!result) {
          setError('Failed to set up voice recognition.');
        }
      } catch (e) {
        setError('Error initializing voice recognition: ' + (e instanceof Error ? e.message : 'Unknown error'));
      } finally {
        setIsLoading(false);
      }
    };
    initialize();
  }, []);
  // Handle voice input
  const handleVoiceInput = async () => {
    if (isListening) {
      // Stop listening
      await stopListening();
      setIsListening(false);
      // Process the transcript if we have one
      if (transcript) {
        processCommand(transcript);
      }
    } else {
      // Start listening
      setTranscript('');
      setConfirmation('');
      setError('');
      setIsListening(true);
      const success = await startListening((text) => {
        setTranscript(text);
      });
      if (!success) {
        setIsListening(false);
        setError('Failed to start voice recognition');
      }
    }
  };
  // Process the command from transcript
  const processCommand = async (text: string) => {
    try {
      const parsedCommand = parseCommand(text);
      if (!parsedCommand) {
        setError("I couldn't understand that command");
        return;
      }
      // Handle the command based on type
      switch (parsedCommand.commandType) {
        case 'add':
          const savedTask = await TaskStorage.saveTask(parsedCommand);
          if (onTaskAdded) onTaskAdded(savedTask);
          break;
        case 'complete':
          // In a real app, we'd need to find the task by name or show a selection UI
          // For MVP, we'll just show a confirmation
          break;
        case 'delete':
          // Similar to complete, we'd need task selection in a real app
          break;
        case 'list':
          // The parent component should handle showing the list
          if (onTaskAdded) onTaskAdded(null, true);
          break;
      }
      // Show confirmation message
      setConfirmation(generateConfirmation(parsedCommand));
    } catch (e) {
      setError('Error processing command: ' + (e instanceof Error ? e.message : 'Unknown error'));
    }
  };
  return (
    <View style={styles.container}>
      {/* Status messages */}
      {error ? (
        <ThemedText style={styles.errorText}>{error}</ThemedText>
      ) : confirmation ? (
        <ThemedText style={styles.confirmationText}>{confirmation}</ThemedText>
      ) : transcript ? (
        <ThemedText style={styles.transcriptText}>"{transcript}"</ThemedText>
      ) : (
        <ThemedText style={styles.helpText}>
          {isListening ? 'Listening...' : 'Tap to speak'}
        </ThemedText>
      )}
      {/* Voice button */}
      <TouchableOpacity
        style={[
          styles.voiceButton,
          isListening ? styles.voiceButtonActive : {},
          { backgroundColor: Colors[colorScheme].tint }
        ]}
        onPress={handleVoiceInput}
        disabled={isLoading}>
        {isLoading ? (
          <ActivityIndicator color="#FFFFFF" size="large" />
        ) : (
          <IconSymbol 
            name={isListening ? "pause.fill" : "mic.fill"} 
            size={28} 
            color="#FFFFFF"
          />
        )}
      </TouchableOpacity>
    </View>
  );
}
const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    padding: 16,
  },
  voiceButton: {
    width: 64,
    height: 64,
    borderRadius: 32,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    marginTop: 16,
  },
  voiceButtonActive: {
    transform: [{ scale: 1.1 }],
  },
  helpText: {
    marginBottom: 8,
  },
  transcriptText: {
    marginBottom: 8,
    fontStyle: 'italic',
  },
  confirmationText: {
    marginBottom: 8,
    fontWeight: 'bold',
  },
  errorText: {
    marginBottom: 8,
    color: 'red',
  }
});