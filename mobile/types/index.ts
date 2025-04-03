export interface User{
    id: string;
    email?: string;
}

export interface Category {
    id: string;
    user_id: string;
    name: string;
    color: string;
    created_at: string;
    updated_at: string;
}

export interface Task {
    title:string;
    description: string;
    due_date?: string;
    priority?: 'low' |'medium' | 'high';
    status?: 'pending' | 'in_progress' | 'completed';
    category_id?: string;
    voice_command?: string;
}

export interface TaskInput {
    Task:{
    title: string;
    description: string;
    due_date?: string;
    priority?: 'low' |'medium' | 'high';
    status?: 'pending' | 'in_progress' | 'completed';
    category_id?: string;
    voice_command?: string;
    }
}
export interface ViewProps {
    style?: any;
    children?: React.ReactNode;
    [key: string]: any;
  }
  
  export interface TextProps {
    style?: any;
    children?: React.ReactNode;
    [key: string]: any;
  }
  
  export interface ActivityIndicatorProps {
    size?: 'small' | 'large' | number;
    color?: string;
    [key: string]: any;
  }


export interface VoiceProcessingResult {
    original_text: string;
    task_info:{
            title: string;
            priority: 'low' | 'medium' | 'high';
            due_date: string | null;
            category: string | null;
          };
        
    }
