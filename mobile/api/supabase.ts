// src/services/supabes.js
import { TaskInput } from '@/types';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.VITE_SUPABASE_URL;
const supabaseAnonKey = process.env.VITE_SUPABASE_ANON_KEY;

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
    auth: {
        storage: AsyncStorage,
        autoRefreshToken: true,
        persistSession: true,
        detectSessionInUrl: false,
    },
});

// Task related API functions
export const taskApi = {
    // Get all tasks for the current user
    getTasks: async () => {
      const { data, error } = await supabase
        .from('tasks')
        .select(`
          *,
          category:categories(*)
        `)
        .order('created_at', { ascending: false });
        
      if (error) throw error;
      return data;
    },
    
    // Get a single task by ID
    getTask: async (id: string) => {
      const { data, error } = await supabase
        .from('tasks')
        .select(`
          *,
          category:categories(*)
        `)
        .eq('id', id)
        .single();
        
      if (error) throw error;
      return data;
    },
    
    // Create a new task
    createTask: async (task: TaskInput) => {
      const { data, error } = await supabase
        .from('tasks')
        .insert(task)
        .select();
        
      if (error) throw error;
      return data[0];
    },
    
    // Update a task
    updateTask: async (id: string, updates: Partial<TaskInput>) => {
      const { data, error } = await supabase
        .from('tasks')
        .update(updates)
        .eq('id', id)
        .select();
        
      if (error) throw error;
      return data[0];
    },
    
    // Delete a task
    deleteTask: async (id: string) => {
      const { error } = await supabase
        .from('tasks')
        .delete()
        .eq('id', id);
        
      if (error) throw error;
      return true;
    },
    
    // Get categories for the current user
    getCategories: async () => {
      const { data, error } = await supabase
        .from('categories')
        .select('*')
        .order('name', { ascending: true });
        
      if (error) throw error;
      return data;
    },
  };
        