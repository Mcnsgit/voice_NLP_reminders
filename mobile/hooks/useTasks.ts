import { useQuery, useMutation, useQueryClient} from 'react-query';
import { taskApi } from '@/api/supabase';
import { Task, TaskInput} from '@/types'

export const useTasks = () => {
    const queryClient = useQueryClient();

    //get all taks
    const { data: tasks, isLoading, error} = useQuery<Task[], Error>(
        'tasks',
        taskApi.getTasks
    );

 // Create task mutation
 const createTask = useMutation(
    (newTask: TaskInput) => taskApi.createTask(newTask),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
      },
    }
  );
  
  // Update task mutation
  const updateTask = useMutation(
    ({ id, updates }: { id: string; updates: Partial<TaskInput> }) => 
      taskApi.updateTask(id, updates),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
      },
    }
  );
  
  // Delete task mutation
  const deleteTask = useMutation(
    (id: string) => taskApi.deleteTask(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks');
      },
    }
  );
  
  return {
    tasks: tasks || [],
    isLoading,
    error,
    createTask,
    updateTask,
    deleteTask,
  };
};

export const useTask = (id: string) => {
  return useQuery<Task, Error>(
    ['task', id],
    () => taskApi.getTask(id)
  );
};

export const useCategories = () => {
  return useQuery('categories', taskApi.getCategories);
};