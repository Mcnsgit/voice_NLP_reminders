// mobile/app/(tabs)/index.tsx
import React, { useState } from 'react';
import { StyleSheet, ScrollView, SafeAreaView } from 'react-native';
import VoiceInput from '@/components/VoiceInput';
import TaskList from '@/components/TaskList';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function TaskManagerScreen() {
  const [refreshKey, setRefreshKey] = useState(0);
  
  // Handle new task added - refresh the task list
  const handleTaskAdded = (newTask, forceRefresh = false) => {
    if (newTask || forceRefresh) {
      setRefreshKey(prev => prev + 1); // Trigger a refresh of the task list
    }
  };
  
  return (
    <SafeAreaView style={styles.container}>
      <ThemedView style={styles.header}>
        <ThemedText type="title">Voice Tasks</ThemedText>
        <ThemedText>Speak to add a new task</ThemedText>
      </ThemedView>
      
      <TaskList refresh={refreshKey} />
      
      <ThemedView style={styles.footer}>
        <VoiceInput onTaskAdded={handleTaskAdded} />
      </ThemedView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 16,
    paddingTop: 24,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(0,0,0,0.1)',
  },
  footer: {
    borderTopWidth: 1,
    borderTopColor: 'rgba(0,0,0,0.1)',
    padding: 16,
  },
});
