import { useEffect, useState } from "react";

import { api } from "../lib/api";
import type { OpsInsightItem, OpsMetrics } from "../lib/types";

interface UseOpsSummaryOptions {
  insightLimit?: number;
  autoRefreshMs?: number;
}

export function useOpsSummary(options: UseOpsSummaryOptions = {}) {
  const { insightLimit = 10, autoRefreshMs } = options;
  const [metrics, setMetrics] = useState<OpsMetrics | null>(null);
  const [recentInsights, setRecentInsights] = useState<OpsInsightItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refreshNonce, setRefreshNonce] = useState(0);

  useEffect(() => {
    let active = true;

    async function loadSummary() {
      setLoading(true);
      setError("");
      try {
        const [metricsResponse, insightsResponse] = await Promise.all([
          api.getOpsMetrics(),
          api.getOpsInsights(insightLimit),
        ]);
        if (!active) {
          return;
        }
        setMetrics(metricsResponse);
        setRecentInsights(insightsResponse.items);
      } catch (err) {
        if (!active) {
          return;
        }
        setError(err instanceof Error ? err.message : "Failed to load ops summary");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadSummary();

    if (!autoRefreshMs) {
      return () => {
        active = false;
      };
    }

    const timer = window.setInterval(() => {
      void loadSummary();
    }, autoRefreshMs);

    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [autoRefreshMs, insightLimit, refreshNonce]);

  return {
    metrics,
    recentInsights,
    loading,
    error,
    refresh: () => setRefreshNonce((value) => value + 1),
  };
}
