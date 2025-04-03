import React, { useState } from "react";
import { View, StyleSheet, Text, ActivityIndicator } from 'react-native';
import { Button } from "react-native-paper";
import { useVoiceRecorder } from "@/hooks/useVoiceRecorder";
import { useTasks } from "@/hooks/useTasks";
import { useNavigation } from "@react-navigation/native";
const VoiceInputScreen: React.FC = () => {
    const {
        isRecording,
        startRecording,
        stopRecording,
        processingResult,
        processRecording,
        isProcessing,
        error
    } = useVoiceRecorder();
    
    const { createTask } = useTasks();
    const navigation = useNavigation();
    const [recognizedText, setRecognizedText] = useState<string | null>(null);
    const handleStartRecording = async () => {
        setRecognizedText(null);
        await startRecording();
    };
    const handleStopRecording = async () => {
        await stopRecording();
        await processAudio();
    };
    const processAudio = async () => {
        const result = await processRecording();
        if (result) {
            setRecognizedText(result.original_text);
            // Create a task from the voice processing result
            if (result.task_info) {
                createTask.mutate({
                    Task: {
                        title: result.task_info.title,
                        description: "",
                        priority: result.task_info.priority,
                        due_date: result.task_info.due_date || undefined, // Ensure it's undefined if null
                        status: "pending",
                        voice_command: result.original_text
                    }
                }, {
                    onSuccess: () => {
                        // Navigate back to the tasks list after a brief delay
                        setTimeout(() => {
                            navigation.goBack();
                        }, 1500);
                    }
                });
            }
        }
    };
    return (
        <View style={{ flex: 1 }}>

        <View style={styles.container}>
            <View style={styles.resultContainer}>
                {isProcessing ? (
                    <ActivityIndicator size="large" color="#0000ff" />
                ) : recognizedText ? (
                    <View>
                        <Text style={styles.title}>Recognized:</Text>
                        <Text style={styles.text}>{recognizedText}</Text>
                    </View>
                ) : (
                    <Text style={styles.instruction}>
                        Press the button and speak to create a task
                    </Text>
                )}
                {error && <Text style={styles.error}>{error}</Text>}
            </View>
            <Button
                mode="contained"
                onPress={isRecording ? handleStopRecording : handleStartRecording}
                loading={isProcessing}
                disabled={isProcessing}
                style={styles.button}
                >
                {isRecording ? "Stop Recording" : "Start Recording"}
            </Button>
        </View>
</View>
    );
};
const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        justifyContent: 'center',
    },
    resultContainer: {
        marginBottom: 40,
        padding: 20,
        backgroundColor: '#f9f9f9',
        borderRadius: 8,
        minHeight: 150,
        justifyContent: 'center'
    },
    title: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    text: {
        fontSize: 16,
        lineHeight: 24,
    },
    instruction: {
        textAlign: 'center',
        fontSize: 16,
        color: '#666',
    },
    button: {
        paddingVertical: 8,
    },
    error: {
        color: 'red',
        marginTop: 10,
    }
});
export default VoiceInputScreen;