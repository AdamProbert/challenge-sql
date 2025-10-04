import { useEffect, useState } from "react";
import { Alert, Center, Grid, Loader, Paper, Stack } from "@mantine/core";
import { IconAlertTriangle } from "@tabler/icons-react";

import { useChallengeDetail, useChallengeList, useQueryExecutor, useSessionSchema } from "../api/hooks";
import { QueryResponse } from "../api/types";
import { ChallengeDetails } from "../components/ChallengeDetails";
import { ChallengeNavigation } from "../components/ChallengeNavigation";
import { ResultsPanel } from "../components/ResultsPanel";
import { SchemaPanel } from "../components/SchemaPanel";
import { SqlWorkbench } from "../components/SqlWorkbench";
import { useSession } from "../session/SessionProvider";

const DEFAULT_SQL = "-- Write your SQL query here\n";

const ChallengesPage = () => {
  const { sessionId, loading: sessionLoading, prepareChallenge, refreshSession } = useSession();
  const { data: challengeList, isLoading: challengesLoading } = useChallengeList();
  const [selectedChallengeId, setSelectedChallengeId] = useState<string | null>(null);
  const [sql, setSql] = useState(DEFAULT_SQL);
  const [lastResponse, setLastResponse] = useState<QueryResponse | null>(null);
  const [completedIds, setCompletedIds] = useState<Set<string>>(new Set());
  const [preparing, setPreparing] = useState(false);

  const executor = useQueryExecutor();
  const challengeDetailQuery = useChallengeDetail(selectedChallengeId);

  const {
    data: schemaData = [],
    isFetching: schemaFetching,
    refetch: refetchSchema,
  } = useSessionSchema(sessionId ?? "", Boolean(sessionId && selectedChallengeId));

  useEffect(() => {
    if (!selectedChallengeId && challengeList) {
      const firstDifficulty = Object.keys(challengeList.challenges)[0];
      const firstChallenge = challengeList.challenges[firstDifficulty]?.[0];
      if (firstChallenge) {
        setSelectedChallengeId(firstChallenge.id);
      }
    }
  }, [challengeList, selectedChallengeId]);

  useEffect(() => {
    if (selectedChallengeId && sessionId) {
      setPreparing(true);
      setSql(DEFAULT_SQL);
      setLastResponse(null);
      void prepareChallenge(selectedChallengeId)
        .then(() => refetchSchema())
        .catch(async () => {
          await refreshSession();
        })
        .finally(() => setPreparing(false));
    }
  }, [selectedChallengeId, sessionId, prepareChallenge, refreshSession, refetchSchema]);

  useEffect(() => {
    setCompletedIds(new Set());
  }, [sessionId]);

  const handleRun = async ({ validate }: { validate: boolean }) => {
    if (!sessionId || !selectedChallengeId) return;
    const activeChallengeId = selectedChallengeId;
    try {
      const data = await executor.mutateAsync({
        sessionId,
        sql,
        challengeId: activeChallengeId,
        validate,
      });
      setLastResponse(data);
      if (data.validation) {
        setCompletedIds((prev) => {
          const next = new Set(prev);
          if (data.validation?.success) {
            next.add(activeChallengeId);
          } else {
            next.delete(activeChallengeId);
          }
          return next;
        });
      }
    } catch (error) {
      console.error(error);
    }
  };

  const showPreparationNotice =
  preparing || schemaFetching || challengeDetailQuery.isFetching || sessionLoading;

  if (!challengeList && (sessionLoading || challengesLoading)) {
    return (
      <Center h="60vh">
        <Loader size="lg" />
      </Center>
    );
  }

  const challenge = challengeDetailQuery.data;

  return (
    <Grid gutter="md">
      <Grid.Col span={{ base: 12, md: 4, lg: 3 }}>
        <Paper radius="md" withBorder h="100%">
          <ChallengeNavigation
            data={challengeList}
            loading={challengesLoading}
            selectedId={selectedChallengeId}
            onSelect={setSelectedChallengeId}
            completedIds={completedIds}
          />
        </Paper>
      </Grid.Col>

      <Grid.Col span={{ base: 12, md: 8, lg: 9 }}>
        {challenge ? (
          <Stack gap="md">
            <ChallengeDetails challenge={challenge} />
            <Grid gutter="md">
              <Grid.Col span={{ base: 12, md: 6 }}>
                <SchemaPanel schema={schemaData} />
              </Grid.Col>
              <Grid.Col span={{ base: 12, md: 6 }}>
                <ResultsPanel
                  result={lastResponse?.result ?? undefined}
                  validation={lastResponse?.validation}
                  loading={executor.isPending}
                />
              </Grid.Col>
            </Grid>
            <SqlWorkbench
              value={sql}
              onChange={setSql}
              onRun={handleRun}
              disabled={!sessionId || preparing}
              isRunning={executor.isPending}
            />
            {showPreparationNotice && (
              <Alert icon={<IconAlertTriangle size={16} />} color="yellow" variant="light">
                Preparing challenge data...
              </Alert>
            )}
          </Stack>
        ) : (
          <Alert color="yellow" icon={<IconAlertTriangle size={16} />}
 variant="light">
            Select a challenge to get started.
          </Alert>
        )}
      </Grid.Col>
    </Grid>
  );
};

export default ChallengesPage;
