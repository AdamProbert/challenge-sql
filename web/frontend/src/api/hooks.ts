import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { notifications } from "@mantine/notifications";

import { apiClient } from "./client";
import {
  ChallengeDetail,
  ChallengeListResponse,
  ChallengeSchemaTable,
  QueryResponse,
} from "./types";

export const queryKeys = {
  challenges: ["challenges"] as const,
  challenge: (id: string) => ["challenge", id] as const,
  sessionSchema: (sessionId: string) => ["schema", sessionId] as const,
};

export const useChallengeList = () => {
  return useQuery({
    queryKey: queryKeys.challenges,
    queryFn: async () => {
      const { data } = await apiClient.get<ChallengeListResponse>("/challenges");
      return data;
    },
  });
};

export const useChallengeDetail = (challengeId: string | null) => {
  return useQuery({
    queryKey: challengeId ? queryKeys.challenge(challengeId) : ["challenge", null],
    queryFn: async () => {
      if (!challengeId) return null;
      const { data } = await apiClient.get<ChallengeDetail>(`/challenges/${challengeId}`);
      return data;
    },
    enabled: Boolean(challengeId),
  });
};

export const useSessionSchema = (sessionId: string, enabled: boolean) => {
  return useQuery({
    queryKey: queryKeys.sessionSchema(sessionId),
    queryFn: async () => {
      const { data } = await apiClient.get<ChallengeSchemaTable[]>(`/sessions/${sessionId}/schema`);
      return data;
    },
    enabled,
  });
};

export interface QueryVariables {
  sessionId: string;
  sql: string;
  challengeId?: string;
  validate?: boolean;
}

export const useQueryExecutor = () => {
  const client = useQueryClient();
  return useMutation<QueryResponse, AxiosError<{ detail: string }>, QueryVariables>({
    mutationFn: async ({ sessionId, sql, challengeId, validate }: QueryVariables) => {
      const { data } = await apiClient.post<QueryResponse>(
        `/sessions/${sessionId}/query`,
        { sql, challenge_id: challengeId, validate }
      );
      return data;
    },
  onError: (error: AxiosError<{ detail: string }>) => {
      const message = error.response?.data?.detail ?? error.message;
      notifications.show({
        color: "red",
        title: "SQL Error",
        message,
      });
    },
  onSuccess: (_data: QueryResponse, variables: QueryVariables) => {
      if (variables.challengeId) {
        client.invalidateQueries({ queryKey: queryKeys.sessionSchema(variables.sessionId) });
      }
    },
  });
};
