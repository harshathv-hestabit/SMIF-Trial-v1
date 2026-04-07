import { useDeferredValue, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { api } from "../lib/api";
import type { ClientListItem } from "../lib/types";

export function useClientsDirectory() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [clients, setClients] = useState<ClientListItem[]>([]);
  const [searchValue, setSearchValue] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const selectedClientId = searchParams.get("client") ?? "";
  const deferredSearch = useDeferredValue(searchValue);
  const filteredClients = clients.filter((client) => {
    const query = deferredSearch.trim().toLowerCase();
    if (!query) {
      return true;
    }
    return (
      client.client_name.toLowerCase().includes(query) ||
      client.client_id.toLowerCase().includes(query)
    );
  });
  const selectedClient =
    clients.find((client) => client.client_id === selectedClientId) ?? null;

  useEffect(() => {
    let active = true;

    async function loadClients() {
      setLoading(true);
      setError("");
      try {
        const response = await api.listClients();
        if (!active) {
          return;
        }

        setClients(response.items);

        const currentSelectedExists = response.items.some(
          (item) => item.client_id === selectedClientId,
        );
        const firstClientId = response.items[0]?.client_id ?? "";

        if (!selectedClientId || !currentSelectedExists) {
          const nextParams = new URLSearchParams(searchParams);
          if (firstClientId) {
            nextParams.set("client", firstClientId);
          } else {
            nextParams.delete("client");
          }
          nextParams.delete("insight");
          setSearchParams(nextParams, { replace: true });
        }
      } catch (err) {
        if (!active) {
          return;
        }
        setError(err instanceof Error ? err.message : "Failed to load clients");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadClients();
    return () => {
      active = false;
    };
  }, [selectedClientId, setSearchParams]);

  function selectClient(clientId: string) {
    const nextParams = new URLSearchParams(searchParams);
    nextParams.set("client", clientId);
    nextParams.delete("insight");
    setSearchParams(nextParams);
  }

  return {
    clients,
    filteredClients,
    selectedClient,
    selectedClientId,
    searchValue,
    setSearchValue,
    loading,
    error,
    selectClient,
  };
}
