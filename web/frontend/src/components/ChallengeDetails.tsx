import { Badge, Card, Divider, Group, List, Stack, Text, Title } from "@mantine/core";
import { ChallengeDetail } from "../api/types";
import { Markdown } from "./Markdown";

interface ChallengeDetailsProps {
  challenge: ChallengeDetail;
}

export const ChallengeDetails = ({ challenge }: ChallengeDetailsProps) => {
  return (
    <Card radius="md" withBorder>
      <Stack gap="md">
        <Group justify="space-between" align="flex-start">
          <div>
            <Title order={3}>{challenge.title}</Title>
            <Badge mt="xs" size="sm" variant="light" color="blue">
              {challenge.difficulty}
            </Badge>
          </div>
        </Group>

        <div>
          <Text fw={600} mb="xs">
            Overview
          </Text>
          <Markdown content={challenge.description} />
        </div>

        <Divider label="Your Task" labelPosition="center" />
        <Markdown content={challenge.task} />

        {challenge.expected_columns.length > 0 && (
          <div>
            <Text fw={600} mb="xs">
              Expected Columns
            </Text>
            <List spacing="xs" size="sm">
              {challenge.expected_columns.map((col) => (
                <List.Item key={col}>{col}</List.Item>
              ))}
            </List>
          </div>
        )}

        {challenge.hints.length > 0 && (
          <div>
            <Text fw={600} mb="xs">
              Hints
            </Text>
            <List spacing="xs" size="sm" c="yellow.4">
              {challenge.hints.map((hint, index) => (
                <List.Item key={index}>{hint}</List.Item>
              ))}
            </List>
          </div>
        )}
      </Stack>
    </Card>
  );
};
