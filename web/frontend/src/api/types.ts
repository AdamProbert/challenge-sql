export interface ChallengeSummary {
  id: string;
  title: string;
  difficulty: string;
  order: number;
}

export interface ChallengeListResponse {
  challenges: Record<string, ChallengeSummary[]>;
}

export interface ChallengeSchemaColumn {
  name: string;
  data_type: string;
}

export interface ChallengeSchemaTable {
  table_name: string;
  columns: ChallengeSchemaColumn[];
}

export interface ChallengeDetail {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  task: string;
  hints: string[];
  expected_columns: string[];
  schema: ChallengeSchemaTable[];
}

export interface SessionCreateResponse {
  session_id: string;
}

export interface QueryResult {
  columns: string[];
  rows: (string | null)[][];
  row_count: number;
  execution_time_ms: number;
}

export interface ValidationDetail {
  success: boolean;
  message: string;
}

export interface QueryResponse {
  result?: QueryResult;
  validation?: ValidationDetail;
}
