import React, { createContext, useState, useEffect, useContext, ReactNode, Children} from 'react'
import { supabase } from '@/api/supabase'
import { User } from '../types';
import { getInitialURL } from 'expo-router/build/link/linking';

interface AuthContextType {
    user: User | null ;
session: any | null;
    isLoading: boolean;
    signIn: (email:string, password: string) =>Promise<void>;
    signUp: (email:string, password: string) =>Promise<void>;
    signOut: () =>Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user,setUser] = useState<User | null>(null);
const [sessions, setSession] = useState<any | null>(null);
const [isLoading, setIsLoading] = useState(true);

useEffect(() => {
    //get initial session
    const getInitiaSession = async () => {
        try {
            const { data: { session } } = await supabase.auth.getSession();
            setSession(session);
            setUser(session?.user ?? null);
        } finally {
          setIsLoading(false);
        }
      };
      
      getInitiaSession();
      
      // Set up auth state change listener
      const { data: { subscription } } = supabase.auth.onAuthStateChange(
        (_event, session) => {
          setSession(session);
          setUser(session?.user ?? null);
          setIsLoading(false);
        }
      );
      
      // Clean up subscription
      return () => {
        subscription.unsubscribe();
      };
    }, []);
    
    const signIn = async (email: string, password: string) => {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;
    };
    
    const signUp = async (email: string, password: string) => {
      const { error } = await supabase.auth.signUp({ email, password });
      if (error) throw error;
    };
    
    const signOut = async () => {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
    };
    
    return (
      <AuthContext.Provider value={{ user, session: sessions, isLoading, signIn, signUp, signOut }}>
        {children}
      </AuthContext.Provider>
    );
  };
  
  export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
      throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
  };