import { Button, Card, CardContent, CardHeader, Input, Spinner } from "@heroui/react";
import { Outlet } from "react-router-dom";

import { SectionHeader } from "../components/SectionHeader";
import { SubNav } from "../components/SubNav";
import { useClientsDirectory } from "../hooks/useClientsDirectory";
import type { ClientListItem } from "../lib/types";

const CLIENT_NAV_ITEMS = [
  {
    to: "/clients/portfolio",
    label: "Portfolio",
    description: "Allocation, identifiers, and mandate context.",
  },
  {
    to: "/clients/insights",
    label: "Insights",
    description: "Saved outputs and selected insight detail.",
  },
];

export interface ClientsLayoutContext {
  clients: ClientListItem[];
  selectedClient: ClientListItem | null;
  selectedClientId: string;
  loading: boolean;
  error: string;
  selectClient: (clientId: string) => void;
}

export function ClientsLayout() {
  const {
    clients,
    filteredClients,
    selectedClient,
    selectedClientId,
    searchValue,
    setSearchValue,
    loading,
    error,
    selectClient,
  } = useClientsDirectory();

  return (
    <section className="grid gap-4">
      <div className="grid gap-4 rounded-[1.75rem] border border-[var(--border-1)] bg-[linear-gradient(180deg,rgba(14,20,38,0.88),rgba(18,24,44,0.72))] p-5 shadow-[0_18px_70px_rgba(1,5,20,0.3)]">
        <SectionHeader
          eyebrow="Clients"
          title="Client workspace"
          description="Use a persistent selector, then move between portfolio review and saved insight analysis."
        />
        <SubNav items={CLIENT_NAV_ITEMS} />
      </div>

      <div className="grid gap-4 xl:grid-cols-[320px_minmax(0,1fr)]">
        <Card className="border border-[var(--border-1)] bg-[rgba(16,22,39,0.86)]">
          <CardHeader>
            <SectionHeader
              eyebrow="Directory"
              title="Active client"
              description="Search once and keep the same context across client pages."
            />
          </CardHeader>
          <CardContent className="grid gap-3 px-4 pb-4 pt-1">
            <Input
              aria-label="Search clients"
              placeholder="Search by name or ID"
              className="rounded-2xl border border-[var(--border-1)] bg-[rgba(255,255,255,0.04)] px-4 py-3 text-[var(--text-1)] placeholder:text-[var(--text-3)]"
              value={searchValue}
              onChange={(event) => setSearchValue(event.currentTarget.value)}
            />
            <div className="rounded-2xl border border-[var(--border-1)] bg-[rgba(115,166,255,0.07)] p-4">
              <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-[var(--text-3)]">
                Selected
              </p>
              <p className="mt-2 font-semibold text-white">
                {selectedClient?.client_name ?? "No client selected"}
              </p>
              <p className="mt-1 text-sm text-[var(--text-3)]">
                {selectedClientId || `${clients.length} clients available`}
              </p>
            </div>
            {loading ? (
              <div className="flex items-center gap-2 text-sm text-[var(--text-3)]">
                <Spinner size="sm" />
                <span>Loading clients</span>
              </div>
            ) : filteredClients.length === 0 ? (
              <p className="rounded-2xl border border-dashed border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] p-4 text-sm text-[var(--text-3)]">
                No clients matched the current search.
              </p>
            ) : (
              filteredClients.map((client) => (
                <Button
                  key={client.client_id}
                  variant={client.client_id === selectedClientId ? "primary" : "ghost"}
                  className={
                    client.client_id === selectedClientId
                      ? "justify-start"
                      : "justify-start border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] text-[var(--text-2)]"
                  }
                  onPress={() => selectClient(client.client_id)}
                >
                  <span className="truncate">{client.client_name}</span>
                </Button>
              ))
            )}
            {error ? (
              <div className="rounded-2xl border border-[rgba(255,78,184,0.24)] bg-[rgba(255,78,184,0.08)] p-4 text-sm font-medium text-[var(--text-1)]">
                {error}
              </div>
            ) : null}
          </CardContent>
        </Card>

        <Outlet
          context={{
            clients,
            selectedClient,
            selectedClientId,
            loading,
            error,
            selectClient,
          } satisfies ClientsLayoutContext}
        />
      </div>
    </section>
  );
}
