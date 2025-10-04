import { AppShell, Group, Text, ThemeIcon } from "@mantine/core";
import { IconDatabase } from "@tabler/icons-react";
import { Route, Routes } from "react-router-dom";
import ChallengesPage from "./pages/ChallengesPage";

const App = () => {
  return (
    <AppShell header={{ height: 56 }} padding="md">
      <AppShell.Header>
        <Group h="100%" px="md" gap="xs">
          <ThemeIcon size="lg" radius="xl" variant="light" color="red">
            <IconDatabase size="1.2rem" />
          </ThemeIcon>
          <div>
            <Text fw={600}>Pokedex SQL Trainer</Text>
            <Text size="xs" c="dimmed">
              Practice Pokémon-themed SQL challenges in your browser
            </Text>
          </div>
        </Group>
      </AppShell.Header>

      <AppShell.Main>
        <Routes>
          <Route path="/" element={<ChallengesPage />} />
        </Routes>
      </AppShell.Main>
    </AppShell>
  );
};

export default App;
