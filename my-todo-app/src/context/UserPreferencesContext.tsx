// context/UserPreferencesContext.tsx
import React, { createContext, useState} from 'react';
import type { ReactNode } from 'react';

interface Preferences {
  theme: 'light' | 'dark';
  language: string;
}

interface PreferencesContextValue {
  preferences: Preferences;
  setPreferences: React.Dispatch<React.SetStateAction<Preferences>>;
}

export const UserPreferencesContext = createContext<PreferencesContextValue | undefined>(undefined);

export const UserPreferencesProvider = ({ children }: { children: ReactNode }) => {
  const [preferences, setPreferences] = useState<Preferences>({
    theme: 'light',
    language: 'en',
  });

  return (
    <UserPreferencesContext.Provider value={{ preferences, setPreferences }}>
      {children}
    </UserPreferencesContext.Provider>
  );
};
