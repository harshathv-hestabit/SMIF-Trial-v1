import { Navigate, Route, Routes } from "react-router-dom";

import { AppFrame } from "./components/AppFrame";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { ClientWorkspacePage } from "./pages/ClientWorkspacePage";
import { HomePage } from "./pages/HomePage";
import { OpsCenterPage } from "./pages/OpsCenterPage";

export function App() {
  return (
    <ErrorBoundary>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<HomePage />} />
          <Route path="/ops" element={<OpsCenterPage />} />
          <Route path="/ops/news/:newsId" element={<OpsCenterPage />} />
          <Route path="/clients" element={<ClientWorkspacePage />} />
          <Route path="/clients/:clientId" element={<ClientWorkspacePage />} />
          <Route path="/ops/overview" element={<Navigate replace to="/ops" />} />
          <Route path="/ops/news" element={<Navigate replace to="/ops" />} />
          <Route path="/ops/pipeline" element={<Navigate replace to="/ops" />} />
          <Route path="/clients/portfolio" element={<Navigate replace to="/clients" />} />
          <Route path="/clients/insights" element={<Navigate replace to="/clients" />} />
          <Route path="*" element={<Navigate replace to="/" />} />
        </Route>
      </Routes>
    </ErrorBoundary>
  );
}

function AppShell() {
  return <AppFrame />;
}
