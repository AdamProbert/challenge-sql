import { Accordion, Badge, Box, Center, Group, Loader, Paper, ScrollArea, Stack, Text } from "@mantine/core";
import { IconCheck } from "@tabler/icons-react";

import { ChallengeListResponse } from "../api/types";

interface ChallengeNavigationProps {
  data?: ChallengeListResponse;
  loading: boolean;
  selectedId: string | null;
  onSelect: (challengeId: string) => void;
  completedIds: ReadonlySet<string>;
}

const difficultyLabels: Record<string, string> = {
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced",
};

export const ChallengeNavigation = ({ data, loading, selectedId, onSelect, completedIds }: ChallengeNavigationProps) => {
  if (loading && !data) {
    return (
      <Center py="xl">
        <Loader />
      </Center>
    );
  }

  if (!data || Object.keys(data.challenges).length === 0) {
    return (
      <Box py="lg" px="md">
        <Text c="dimmed">No challenges found.</Text>
      </Box>
    );
  }

  return (
    <ScrollArea h="100%">
      <Accordion chevronPosition="right" multiple defaultValue={["beginner"]}>
        {Object.entries(data.challenges).map(([difficulty, challenges]) => (
          <Accordion.Item value={difficulty} key={difficulty}>
            <Accordion.Control>
              <Group gap="xs">
                <Text fw={600}>{difficultyLabels[difficulty] ?? difficulty}</Text>
                <Badge size="sm" variant="light" color="blue">
                  {challenges.length}
                </Badge>
              </Group>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack gap="xs">
                {challenges.map((challenge) => {
                  const isSelected = challenge.id === selectedId;
                  const isCompleted = completedIds.has(challenge.id);
                  return (
                    <Paper
                      key={challenge.id}
                      px="md"
                      py="sm"
                      style={{
                        cursor: "pointer",
                        backgroundColor: isSelected ? "rgba(59, 130, 246, 0.15)" : "transparent",
                        border: isSelected ? "1px solid rgba(59, 130, 246, 0.4)" : "1px solid transparent",
                      }}
                      onClick={() => onSelect(challenge.id)}
                    >
                      <Group justify="space-between" align="center">
                        <Text fw={500}>{challenge.title}</Text>
                        {isCompleted && <IconCheck size="1rem" color="var(--mantine-color-green-6)" />}
                      </Group>
                      <Text size="xs" c="dimmed">
                        #{challenge.order.toString().padStart(2, "0")}
                      </Text>
                    </Paper>
                  );
                })}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>
        ))}
      </Accordion>
    </ScrollArea>
  );
};
