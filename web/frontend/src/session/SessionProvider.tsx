import { createContext, ReactNode, useCallback, useContext, useEffect, useState } from "react";
import { notifications } from "@mantine/notifications";
import { apiClient } from "../api/client";
import { SessionCreateResponse } from "../api/types";

interface SessionContextValue {
  sessionId: string | null;
  loading: boolean;
  refreshSession: () => Promise<string | undefined>;
  prepareChallenge: (challengeId: string) => Promise<void>;
}

const SessionContext = createContext<SessionContextValue | undefined>(undefined);

const STORAGE_KEY = "pokedex-session-id";

export const SessionProvider = ({ children }: { children: ReactNode }) => {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const createSession = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await apiClient.post<SessionCreateResponse>("/sessions");
      setSessionId(data.session_id);
      localStorage.setItem(STORAGE_KEY, data.session_id);
      return data.session_id;
    } catch (error) {
      notifications.show({
        color: "red",
        title: "Unable to create session",
        message: error instanceof Error ? error.message : "Unknown error",
      });
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      setSessionId(stored);
      setLoading(false);
    } else {
      void createSession();
    }
  }, [createSession]);

  const refreshSession = useCallback(async () => {
    return createSession();
  }, [createSession]);

  const prepareChallenge = useCallback(
    async (challengeId: string) => {
      let activeSessionId = sessionId;
      if (!activeSessionId) {
        activeSessionId = await refreshSession();
        if (!activeSessionId) return;
      }

      try {
        await apiClient.post(`/sessions/${activeSessionId}/reset`, {
          challenge_id: challengeId,
        });
      } catch (error) {
        const status = (error as { response?: { status?: number } })?.response?.status;
        if (status === 404) {
          const newSession = await refreshSession();
          if (newSession) {
            await apiClient.post(`/sessions/${newSession}/reset`, {
              challenge_id: challengeId,
            });
            return;
          }
        }

        notifications.show({
          color: "red",
          title: "Unable to set up challenge",
          message: error instanceof Error ? error.message : "Unknown error",
        });
        throw error;
      }
    },
    [sessionId, refreshSession]
  );

  const value: SessionContextValue = {
    sessionId,
    loading,
    refreshSession,
    prepareChallenge,
  };

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
};

export const useSession = () => {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error("useSession must be used within a SessionProvider");
  }
  return context;
};
