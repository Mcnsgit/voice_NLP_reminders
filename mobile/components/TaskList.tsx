// mobile/components/TaskList.tsx
import React, { useState, useEffect } from 'react';
import { 
  View, 
  FlatList, 
  StyleSheet, 
  TouchableOpacity, 
  ActivityIndicator 
} from 'react-native';
import { TaskStorage } from '../services/taskStorage';
import { ThemedText } from './ThemedText';
import { ThemedView } from './ThemedView';
import { IconSymbol } from './ui/IconSymbol';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';

export default function TaskList({ refresh }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const colorScheme = useColorScheme() ?? 'light';
  
  // Load tasks when component mounts or refresh changes
  useEffect(() => {
    loadTasks();
  }, [refresh]);
  
  // Load tasks from storage
  const loadTasks = async () => {
    try {
      setLoading(true);
      const storedTasks = await TaskStorage.getTasks();
      
      // Sort tasks: incomplete first, then by due date
      const sortedTasks = storedTasks.sort((a, b) => {
        // First by status (pending first)
        if (a.status === 'pending' && b.status !== 'pending') return -1;
        if (a.status !== 'pending' && b.status === 'pending') return 1;
        
        // Then by due date if available
        if (a.dueDate && b.dueDate) {
          return new Date(a.dueDate) - new Date(b.dueDate);
        }
        
        // Finally by creation date
        return new Date(b.createdAt) - new Date(a.createdAt);
      });
      
      setTasks(sortedTasks);
    } catch (error) {
      console.error('Error loading tasks:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Complete a task
  const handleCompleteTask = async (taskId) => {
    try {
      await TaskStorage.completeTask(taskId);
      loadTasks(); // Reload to update the list
    } catch (error) {
      console.error('Error completing task:', error);
    }
  };
  
  // Delete a task
  const handleDeleteTask = async (taskId) => {
    try {
      await TaskStorage.deleteTask(taskId);
      loadTasks(); // Reload to update the list
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };
  
  // Get appropriate icon color for priority
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#e74c3c';
      case 'medium': return '#f39c12';
      case 'low': return '#3498db';
      default: return '#95a5a6';
    }
  };
  
  // Format the due date for display
  const formatDueDate = (dueDate) => {
    if (!dueDate) return 'No due date';
    
    // Handle special keywords
    if (['today', 'tomorrow', 'nextWeek'].includes(dueDate)) {
      return dueDate.charAt(0).toUpperCase() + dueDate.slice(1);
    }
    
    // Handle specific days like "Monday"
    if (/^[A-Z][a-z]+$/.test(dueDate)) {
      return dueDate;
    }
    
    // For dates like "January 15th", return as is
    return dueDate;
  };
  
  // Render each task item
  const renderTask = ({ item }) => {
    const isCompleted = item.status === 'completed';
    
    return (
      <ThemedView style={styles.taskItem}>
        <View style={styles.taskContent}>
          <View style={styles.taskHeader}>
            <ThemedText 
              style={[
                styles.taskTitle, 
                isCompleted && styles.completedTask
              ]}
              type={isCompleted ? 'default' : 'defaultSemiBold'}
            >
              {item.task}
            </ThemedText>
            
            <View style={[
              styles.priorityIndicator, 
              { backgroundColor: getPriorityColor(item.priority) }
            ]} />
          </View>
          
          <ThemedText style={styles.taskDate}>
            {formatDueDate(item.dueDate)}
          </ThemedText>
        </View>
        
        <View style={styles.taskActions}>
          {!isCompleted && (
            <TouchableOpacity
              style={styles.actionButton}
              onPress={() => handleCompleteTask(item.id)}>
              <IconSymbol 
                name="checkmark.circle" 
                size={24} 
                color={Colors[colorScheme].tint} 
              />
            </TouchableOpacity>
          )}
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => handleDeleteTask(item.id)}>
            <IconSymbol 
              name="trash" 
              size={24} 
              color="#e74c3c" 
            />
          </TouchableOpacity>
        </View>
      </ThemedView>
    );
  };
  
  // Display empty state if no tasks
  const renderEmptyList = () => {
    if (loading) {
      return (
        <View style={styles.emptyContainer}>
          <ActivityIndicator size="large" color={Colors[colorScheme].tint} />
          <ThemedText style={styles.emptyText}>Loading tasks...</ThemedText>
        </View>
      );
    }
    
    return (
      <View style={styles.emptyContainer}>
        <IconSymbol 
          name="tray.fill" 
          size={48} 
          color={Colors[colorScheme].icon} 
        />
        <ThemedText style={styles.emptyText}>
          No tasks yet. Try adding one with voice!
        </ThemedText>
      </View>
    );
  };
  
  return (
    <FlatList
      data={tasks}
      renderItem={renderTask}
      keyExtractor={item => item.id}
      contentContainerStyle={styles.list}
      ListEmptyComponent={renderEmptyList}
      ItemSeparatorComponent={() => <View style={styles.separator} />}
    />
  );
}

const styles = StyleSheet.create({
  list: {
    flexGrow: 1,
    padding: 16,
  },
  taskItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  taskContent: {
    flex: 1,
  },
  taskHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  taskTitle: {
    fontSize: 16,
    flex: 1,
  },
  completedTask: {
    textDecorationLine: 'line-through',
    opacity: 0.6,
  },
  taskDate: {
    fontSize: 14,
    marginTop: 4,
    opacity: 0.6,
  },
  priorityIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginLeft: 8,
  },
  taskActions: {
    flexDirection: 'row',
  },
  actionButton: {
    padding: 8,
  },
  separator: {
    height: 1,
    backgroundColor: '#E0E0E0',
    opacity: 0.5,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 32,
    height: 300,
  },
  emptyText: {
    marginTop: 16,
    textAlign: 'center',
    opacity: 0.7,
  }
})