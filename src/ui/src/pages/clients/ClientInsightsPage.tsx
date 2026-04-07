import { Card, CardContent, CardHeader, Chip, Spinner } from "@heroui/react";
import { useEffect, useState } from "react";
import { useOutletContext, useSearchParams } from "react-router-dom";

import { DataTable, StatusChip } from "../../components/DataTable";
import { DetailModal } from "../../components/DetailModal";
import { SectionHeader } from "../../components/SectionHeader";
import type { ClientsLayoutContext } from "../../layouts/ClientsLayout";
import { api } from "../../lib/api";
import type { ClientInsightListResponse } from "../../lib/types";

export function ClientInsightsPage() {
  const { selectedClient, selectedClientId } = useOutletContext<ClientsLayoutContext>();
  const [searchParams, setSearchParams] = useSearchParams();
  const [insights, setInsights] = useState<ClientInsightListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);

  const selectedInsightId = searchParams.get("insight") ?? "";
  const selectedInsight =
    insights?.items.find((item) => item.id === selectedInsightId) ??
    insights?.items[0] ??
    null;

  useEffect(() => {
    if (!selectedClientId) {
      setInsights(null);
      return;
    }

    let active = true;

    async function loadInsights() {
      setLoading(true);
      setError("");
      try {
        const response = await api.getClientInsights(selectedClientId);
        if (!active) {
          return;
        }
        setInsights(response);

        const firstInsightId = response.items[0]?.id ?? "";
        const currentInsightExists = response.items.some((item) => item.id === selectedInsightId);
        const nextParams = new URLSearchParams(searchParams);
        nextParams.set("client", selectedClientId);

        if (!selectedInsightId && firstInsightId) {
          nextParams.set("insight", firstInsightId);
          setSearchParams(nextParams, { replace: true });
        } else if (selectedInsightId && !currentInsightExists) {
          if (firstInsightId) {
            nextParams.set("insight", firstInsightId);
          } else {
            nextParams.delete("insight");
          }
          setSearchParams(nextParams, { replace: true });
        }
      } catch (err) {
        if (!active) {
          return;
        }
        setError(err instanceof Error ? err.message : "Failed to load client insights");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadInsights();
    return () => {
      active = false;
    };
  }, [selectedClientId, setSearchParams]);

  return (
    <div className="grid gap-4">
      {error ? <InlineError message={error} /> : null}

      <Card className="border border-[var(--border-1)] bg-[rgba(16,22,39,0.86)]">
        <CardHeader className="flex items-center justify-between">
          <SectionHeader
            eyebrow="Insights"
            title={selectedClient?.client_name ?? "Saved client insights"}
            description="Keep the page compact, and open the full generated narrative only when you need it."
          />
          <div className="flex items-center gap-3">
            <Chip variant="soft">{insights?.count ?? 0}</Chip>
            {loading ? <Spinner size="sm" /> : null}
          </div>
        </CardHeader>
        <CardContent className="px-4 pb-4 pt-1">
          {selectedInsight ? (
            <InsightSummary
              insight={selectedInsight}
              onOpen={() => setIsDetailModalOpen(true)}
            />
          ) : (
            <p className="rounded-2xl border border-dashed border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] p-6 text-sm text-[var(--text-3)]">
              Select a client with available insights to inspect the generated output.
            </p>
          )}
        </CardContent>
      </Card>

      <Card className="border border-[var(--border-1)] bg-[rgba(16,22,39,0.86)]">
        <CardHeader>
          <SectionHeader
            eyebrow="Browse"
            title="Insight records"
            description="Use the list below to move between generated insights for the selected client."
          />
        </CardHeader>
        <CardContent className="px-4 pb-4 pt-1">
          <DataTable
            ariaLabel="Client insights"
            rows={insights?.items ?? []}
            emptyMessage="No insights available for the selected client."
            getRowKey={(row) => row.id}
            maxHeightClassName="max-h-[28rem]"
            columns={[
              {
                key: "news_title",
                header: "News",
                cell: (row) => (
                  <button
                    type="button"
                    className="grid gap-1 text-left"
                    onClick={() => {
                      const nextParams = new URLSearchParams(searchParams);
                      nextParams.set("client", selectedClientId);
                      nextParams.set("insight", row.id);
                      setSearchParams(nextParams);
                    }}
                  >
                    <span className="font-semibold text-white">{row.news_title}</span>
                    <span className="text-xs text-[var(--text-3)]">{row.timestamp ?? "unknown"}</span>
                  </button>
                ),
              },
              {
                key: "status",
                header: "Status",
                cell: (row) => <StatusChip value={row.status} />,
              },
              {
                key: "score",
                header: "Score",
                align: "right",
                cell: (row) => row.verification_score ?? "-",
              },
            ]}
          />
        </CardContent>
      </Card>

      <DetailModal
        isOpen={isDetailModalOpen && Boolean(selectedInsight)}
        title={selectedInsight?.news_title ?? "Selected insight"}
        description="Full generated insight output."
        onClose={() => setIsDetailModalOpen(false)}
      >
        {selectedInsight ? <InsightDetail insight={selectedInsight} /> : null}
      </DetailModal>
    </div>
  );
}

function InsightSummary(props: {
  insight: ClientInsightListResponse["items"][number];
  onOpen: () => void;
}) {
  return (
    <div className="grid gap-4 rounded-2xl border border-[var(--border-1)] bg-[rgba(115,166,255,0.07)] p-5 lg:grid-cols-[minmax(0,1fr)_220px]">
      <div>
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
              Selected Insight
            </p>
            <h3 className="mt-1 line-clamp-2 text-xl font-semibold text-white">
              {props.insight.news_title}
            </h3>
          </div>
          <StatusChip value={props.insight.status} />
        </div>
        <p className="mt-4 text-sm leading-6 text-[var(--text-2)]">
          {truncateText(props.insight.insight, 220)}
        </p>
      </div>
      <div className="grid gap-3">
        <DetailStat label="Client" value={props.insight.client_id} />
        <DetailStat label="Score" value={String(props.insight.verification_score ?? "-")} />
        <DetailStat label="Timestamp" value={props.insight.timestamp ?? "unknown"} />
      </div>
      <div className="lg:col-span-2">
        <button
          type="button"
          className="rounded-full border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] px-4 py-2 text-sm font-medium text-[var(--text-2)] transition hover:border-[rgba(115,166,255,0.32)] hover:text-white"
          onClick={props.onOpen}
        >
          View Full Insight
        </button>
      </div>
    </div>
  );
}

function InsightDetail(props: { insight: ClientInsightListResponse["items"][number] }) {
  return (
    <div className="grid gap-4 rounded-2xl border border-[var(--border-1)] bg-[rgba(115,166,255,0.07)] p-5">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
            Selected Insight
          </p>
          <h3 className="mt-1 text-xl font-semibold text-white">{props.insight.news_title}</h3>
        </div>
        <StatusChip value={props.insight.status} />
      </div>
      <div className="grid gap-3 sm:grid-cols-3">
        <DetailStat label="Client" value={props.insight.client_id} />
        <DetailStat
          label="Score"
          value={String(props.insight.verification_score ?? "-")}
        />
        <DetailStat label="Timestamp" value={props.insight.timestamp ?? "unknown"} />
      </div>
      {props.insight.tickers.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {props.insight.tickers.map((ticker) => (
            <Chip key={ticker} size="sm" variant="secondary">
              {ticker}
            </Chip>
          ))}
        </div>
      ) : null}
      <div className="rounded-2xl border border-[var(--border-1)] bg-[rgba(10,14,28,0.55)] p-4 text-sm leading-6 text-[var(--text-2)]">
        {props.insight.insight}
      </div>
    </div>
  );
}

function DetailStat(props: { label: string; value: string }) {
  return (
    <div className="rounded-2xl border border-[var(--border-1)] bg-[rgba(12,18,33,0.55)] p-3">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
        {props.label}
      </p>
      <p className="mt-1 break-words text-sm text-white">{props.value}</p>
    </div>
  );
}

function InlineError(props: { message: string }) {
  return (
    <div className="rounded-2xl border border-[rgba(255,78,184,0.24)] bg-[rgba(255,78,184,0.08)] p-4 text-sm font-medium text-[var(--text-1)]">
      {props.message}
    </div>
  );
}

function truncateText(value: string, maxLength: number) {
  if (value.length <= maxLength) {
    return value;
  }

  return `${value.slice(0, maxLength).trimEnd()}...`;
}
