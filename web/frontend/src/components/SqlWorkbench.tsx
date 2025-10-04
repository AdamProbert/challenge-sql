import { useCallback } from "react";
import { Button, Group, Paper, Stack } from "@mantine/core";
import Editor from "@monaco-editor/react";

interface SqlWorkbenchProps {
  value: string;
  onChange: (value: string) => void;
  onRun: (options: { validate: boolean }) => void;
  disabled?: boolean;
  isRunning: boolean;
}

export const SqlWorkbench = ({ value, onChange, onRun, disabled = false, isRunning }: SqlWorkbenchProps) => {
  const handleRun = useCallback(() => onRun({ validate: false }), [onRun]);
  const handleValidate = useCallback(() => onRun({ validate: true }), [onRun]);

  return (
    <Stack gap="sm">
      <Paper radius="md" withBorder>
        <Editor
          height="320px"
          defaultLanguage="sql"
          theme="vs-dark"
          value={value}
          onChange={(val: string | undefined) => onChange(val ?? "")}
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            wordWrap: "on",
            readOnly: disabled,
            automaticLayout: true,
          }}
        />
      </Paper>
      <Group justify="flex-end">
        <Button variant="default" onClick={handleRun} disabled={disabled || isRunning}>
          Run query
        </Button>
        <Button onClick={handleValidate} loading={isRunning} disabled={disabled}>
          Run & validate
        </Button>
      </Group>
    </Stack>
  );
};
