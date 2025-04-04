//mobile/services/taskStorage
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';
const TASK_STORAGE_KEY = '@voice_tasks';
const SYNC_QUEUE_KEY = '@sync_queue';
interface Task {
    id: string;
    createdAt: string;
    status: 'pending' | 'completed';
    updatedAt?: string;
    completedAt?: string;
    [key: string]: any; // Allow additional properties
}
export const TaskStorage = {
    async getTasks(): Promise<Task[]> {
        try {
            const tasksJson = await AsyncStorage.getItem(TASK_STORAGE_KEY);
            return tasksJson ? JSON.parse(tasksJson) : [];
        } catch (error) {
            console.error('Failed to get tasks from storage', error);
            return [];
        }
    },
    async saveTask(taskData: Omit<Task, 'id' | 'createdAt' | 'status'>): Promise<Task> {
        try {
            const tasks = await this.getTasks();
            const newTask: Task = {
                ...taskData,
                id: Date.now().toString(),
                createdAt: new Date().toISOString(),
                status: 'pending'
            };
            tasks.push(newTask);
            await AsyncStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(tasks));
            this.queueForSync({ type: 'ADD_TASK', data: newTask });
            return newTask;
        } catch (error) {
            console.error('Failed to save task:', error);
            throw error;
        }
    },
    async updatedTask(taskId: string, updates: Partial<Task>): Promise<Task | null> {
        try {
            const tasks = await this.getTasks();
            const taskIndex = tasks.findIndex(task => task.id === taskId);
            if (taskIndex === -1) {
                console.error('Task not found:', taskId);
                return null;
            }
            const updatedTask: Task = {
                ...tasks[taskIndex],
                ...updates,
                updatedAt: new Date().toISOString()
            };
            tasks[taskIndex] = updatedTask;
            await AsyncStorage.setItem(TASK_STORAGE_KEY, JSON.stringify(tasks));
            this.queueForSync({ type: 'UPDATE_TASK', data: updatedTask });
            return updatedTask;
        } catch (error) {
            console.error('Failed to update task', error);
            throw error; 
        }
    },
    async completeTask(taskId: string): Promise<Task | null> {
        return this.updatedTask(taskId, {
            status: 'completed',
            completedAt: new Date().toISOString()
        });
    },
    async queueForSync(operations: { type: string; data: any }): Promise<void> {
        try {
            const syncQueueJson = await AsyncStorage.getItem(SYNC_QUEUE_KEY);
            const syncQueue = syncQueueJson ? JSON.parse(syncQueueJson) : [];
            syncQueue.push({
                ...operations,
                queuedAt: new Date().toISOString()
            });
            await AsyncStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(syncQueue));
            this.attemptSync();
        } catch (error) {
            console.error('Failed to queue for sync', error);
        }
    },
    async attemptSync(): Promise<boolean> {
        try {
            // Check if we're online
            const netInfo = await NetInfo.fetch();
            if (!netInfo.isConnected) {
                console.log('Device is offline, sync postponed');
                return false;
            }
            // Get the sync queue
            const syncQueueJson = await AsyncStorage.getItem(SYNC_QUEUE_KEY);
            const syncQueue = syncQueueJson ? JSON.parse(syncQueueJson) : [];
            if (syncQueue.length === 0) {
                return true; // Nothing to sync
            }
            // In a real implementation, you would send these operations to your backend
            // For MVP, we'll just log them and clear the queue
            console.log('Would sync operations:', syncQueue);
            // Clear the sync queue
            await AsyncStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify([]));
            return true;
        } catch (error) {
            console.error('Sync failed:', error);
            return false;
        }
    }
};
// Set up a listener for connectivity changes
NetInfo.addEventListener(state => {
    if (state.isConnected) {
        // Try to sync when we come back online
        TaskStorage.attemptSync();
    }
});