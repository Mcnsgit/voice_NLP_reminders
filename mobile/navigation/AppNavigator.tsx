// Finish the AppNavigator.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { useAuth } from '@/context/AuthContext';

// screens
// import AuthScreen from '../screens/AuthScreen';
import HomeScreen from '@/app/(tabs)';
// import TaskDetailScreen from '../screens/TaskDetailScreen.tsx';
import VoiceInputScreen from '../screens/VoiceInputScreen';

// define stack navigator param list 
export type RootStackParamList = {
    Auth: undefined;
    Home: undefined;
    TaskDetail: { taskId: string };
    VoiceInput: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

const AppNavigator = () => {
    const { user, isLoading } = useAuth();
    
    if (isLoading) {
        // Return a loading screen
        return null; // Replace with a proper loading component
    }
    
    return (
        <NavigationContainer>
            <Stack.Navigator>
                {!user ? (
                    <Stack.Screen 
                        name="Auth" 
                        component={AuthScreen} 
                        options={{ headerShown: false }}
                    />
                ) : (
                    <>
                        <Stack.Screen 
                            name="Home" 
                            component={HomeScreen} 
                            options={{ headerShown: false }}
                        />
                        <Stack.Screen 
                            name="TaskDetail" 
                            component={TaskDetailScreen} 
                            options={{ title: "Task Details" }}
                        />
                        <Stack.Screen 
                            name="VoiceInput" 
                            component={VoiceInputScreen} 
                            options={{ title: "Voice Input" }}
                        />
                    </>
                )}
            </Stack.Navigator>
        </NavigationContainer>
    );
};

export default AppNavigator;