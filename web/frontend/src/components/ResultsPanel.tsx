import { Alert, Card, Loader, ScrollArea, Table, Text } from "@mantine/core";
import { IconCheck, IconInfoCircle, IconX } from "@tabler/icons-react";
import { QueryResult, ValidationDetail } from "../api/types";

interface ResultsPanelProps {
  result?: QueryResult;
  validation?: ValidationDetail | null;
  loading: boolean;
}

export const ResultsPanel = ({ result, validation, loading }: ResultsPanelProps) => {
  if (loading) {
    return (
      <Card radius="md" withBorder>
        <Loader />
      </Card>
    );
  }

  return (
    <Card radius="md" withBorder>
      <Text fw={600} mb="sm">
        Results
      </Text>
      {result && result.columns.length > 0 ? (
        <ScrollArea h={240} type="auto">
          <Table striped highlightOnHover stickyHeader>
            <Table.Thead>
              <Table.Tr>
                {result.columns.map((col) => (
                  <Table.Th key={col}>{col}</Table.Th>
                ))}
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {result.rows.map((row, idx) => (
                <Table.Tr key={idx}>
                  {row.map((cell, cellIndex) => (
                    <Table.Td key={`${idx}-${cellIndex}`}>{cell ?? "NULL"}</Table.Td>
                  ))}
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
          <Text size="xs" c="dimmed" mt="xs">
            Showing {result.row_count} row(s) in {result.execution_time_ms.toFixed(1)} ms.
          </Text>
        </ScrollArea>
      ) : (
        <Alert icon={<IconInfoCircle size={16} />} title="No rows" color="blue" variant="light">
          No results returned yet. Run a query to see data here.
        </Alert>
      )}

      {validation && (
        <Alert
          mt="md"
          icon={validation.success ? <IconCheck size={16} /> : <IconX size={16} />}
          color={validation.success ? "green" : "red"}
          title={validation.success ? "Challenge solved!" : "Validation failed"}
          variant="light"
        >
          {validation.message}
        </Alert>
      )}
    </Card>
  );
};
