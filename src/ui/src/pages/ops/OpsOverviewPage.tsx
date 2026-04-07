import { Button, Card, CardContent, CardHeader, Spinner } from "@heroui/react";

import { DataTable, StatusChip } from "../../components/DataTable";
import { MetricTile } from "../../components/MetricTile";
import { SectionHeader } from "../../components/SectionHeader";
import { useOpsSummary } from "../../hooks/useOpsSummary";

const REFRESH_INTERVAL_MS = 10_000;

export function OpsOverviewPage() {
  const { metrics, recentInsights, loading, error, refresh } = useOpsSummary({
    insightLimit: 10,
    autoRefreshMs: REFRESH_INTERVAL_MS,
  });

  return (
    <div className="grid gap-4">
      {error ? (
        <InlineError message={error} />
      ) : null}

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
        <MetricTile label="News Docs" value={loading ? "-" : metrics?.news_docs ?? 0} />
        <MetricTile label="Queued To MAS" value={loading ? "-" : metrics?.queued_to_mas ?? 0} />
        <MetricTile
          label="In Insight Gen"
          value={loading ? "-" : metrics?.in_insight_generation ?? 0}
        />
        <MetricTile label="Insights Saved" value={loading ? "-" : metrics?.insights_saved ?? 0} />
        <MetricTile
          label="Failed"
          value={loading ? "-" : metrics?.failed_news_docs ?? 0}
          accent="text-rose-700"
        />
      </section>

      <section className="grid gap-4 lg:grid-cols-[minmax(0,1.35fr)_minmax(280px,0.65fr)]">
        <Card className="border border-[var(--border-1)] bg-[rgba(16,22,39,0.86)]">
          <CardHeader className="flex items-center justify-between">
            <SectionHeader
              eyebrow="Outputs"
              title="Recent insight results"
              description="Live view of the most recent generated insight records."
            />
            <div className="flex items-center gap-3">
              {loading ? <Spinner size="sm" /> : null}
              <Button
                variant="ghost"
                className="border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] text-[var(--text-2)]"
                onPress={refresh}
              >
                Refresh Now
              </Button>
            </div>
          </CardHeader>
          <CardContent className="px-4 pb-4 pt-1">
            <DataTable
              ariaLabel="Recent insights"
              rows={recentInsights}
              emptyMessage="No insights generated yet."
              getRowKey={(row, index) => `${row.news_doc_id ?? row.client_id}-${index}`}
              columns={[
                {
                  key: "news_title",
                  header: "Insight",
                  cell: (row) => (
                    <div className="grid gap-1">
                      <span className="font-semibold text-white">{row.news_title}</span>
                      <span className="text-xs text-[var(--text-3)]">{row.news_doc_id ?? "-"}</span>
                    </div>
                  ),
                },
                {
                  key: "client_id",
                  header: "Client",
                  cell: (row) => row.client_id,
                },
                {
                  key: "score",
                  header: "Score",
                  align: "right",
                  cell: (row) => row.verification_score ?? "-",
                },
                {
                  key: "status",
                  header: "Status",
                  cell: (row) => <StatusChip value={row.status} />,
                },
                {
                  key: "timestamp",
                  header: "Timestamp",
                  cell: (row) => row.timestamp ?? "-",
                },
              ]}
            />
          </CardContent>
        </Card>

        <Card className="border border-[var(--border-1)] bg-[linear-gradient(180deg,rgba(24,30,52,0.92),rgba(17,21,37,0.86))]">
          <CardHeader>
            <SectionHeader
              eyebrow="Pulse"
              title="Runtime summary"
              description="Operational context without opening the heavier explorer pages."
            />
          </CardHeader>
          <CardContent className="grid gap-3 px-4 pb-4 pt-1 text-sm text-[var(--text-2)]">
            <div className="rounded-2xl border border-[var(--border-1)] bg-[rgba(115,166,255,0.07)] p-4">
              Tracking {metrics?.news_docs ?? 0} news records with {metrics?.insights_saved ?? 0} saved insights.
            </div>
            <div className="rounded-2xl border border-[rgba(255,78,184,0.18)] bg-[rgba(255,78,184,0.06)] p-4">
              Auto-refresh runs every 10 seconds on this page so the overview stays current.
            </div>
            <div className="rounded-2xl border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] p-4">
              Use News Explorer for lifecycle triage and Pipeline for manual document ingestion.
            </div>
          </CardContent>
        </Card>
      </section>
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
