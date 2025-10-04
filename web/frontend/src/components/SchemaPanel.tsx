import { Card, ScrollArea, Table, Text } from "@mantine/core";
import { ChallengeSchemaTable } from "../api/types";

interface SchemaPanelProps {
  schema: ChallengeSchemaTable[];
}

export const SchemaPanel = ({ schema }: SchemaPanelProps) => {
  if (schema.length === 0) {
    return (
      <Card radius="md" withBorder>
        <Text c="dimmed">Schema will appear after you prepare the challenge.</Text>
      </Card>
    );
  }

  return (
    <Card radius="md" withBorder>
      <Text fw={600} mb="sm">
        Available Tables
      </Text>
      <ScrollArea h={240} type="always">
        {schema.map((table) => (
          <div key={table.table_name} style={{ marginBottom: "1rem" }}>
            <Text fw={500}>{table.table_name}</Text>
            <Table striped highlightOnHover withRowBorders={false} horizontalSpacing="md">
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Column</Table.Th>
                  <Table.Th>Type</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {table.columns.map((column) => (
                  <Table.Tr key={column.name}>
                    <Table.Td>{column.name}</Table.Td>
                    <Table.Td>{column.data_type}</Table.Td>
                  </Table.Tr>
                ))}
              </Table.Tbody>
            </Table>
          </div>
        ))}
      </ScrollArea>
    </Card>
  );
};
