import { Link } from "react-router-dom";

import { EmptyState } from "../components/EmptyState";
import { SectionIntro } from "../components/SectionIntro";
import { StatCard } from "../components/StatCard";
import { StatusBadge } from "../components/StatusBadge";
import { Surface } from "../components/Surface";
import { useAsyncData } from "../hooks/useAsyncData";
import { api } from "../lib/api";
import { formatCompactNumber, formatDateTime } from "../lib/format";

export function HomePage() {
  const state = useAsyncData(async () => {
    const [health, metrics, clients, insights] = await Promise.all([
      api.health(),
      api.getOpsMetrics(),
      api.listClients(),
      api.getOpsInsights(6),
    ]);

    return {
      health,
      metrics,
      clients: clients.items,
      insights: insights.items,
    };
  }, []);

  return (
    <div className="grid gap-6">
      <SectionIntro
        eyebrow="System Overview"
        title="A single entry point for the workflows that actually matter."
        description="Use the ops workspace to triage ingestion and article flow, then move into the client workspace to inspect a portfolio and the insights generated against it."
        action={
          <button
            type="button"
            onClick={state.reload}
            className="rounded-full border border-[var(--line)] bg-white px-4 py-2 text-sm font-medium text-[var(--ink-strong)] transition hover:border-[var(--line-strong)]"
          >
            Refresh data
          </button>
        }
      />

      <div className="grid gap-4 lg:grid-cols-4">
        <StatCard
          label="API health"
          value={state.data?.health.status === "ok" ? "Online" : state.loading ? "..." : "Check"}
          hint="Smoke test for the UI API service."
          tone="accent"
        />
        <StatCard
          label="Tracked clients"
          value={formatCompactNumber(state.data?.clients.length)}
          hint="Available in the client portfolio collection."
        />
        <StatCard
          label="News documents"
          value={formatCompactNumber(state.data?.metrics.news_docs)}
          hint="Documents currently available for downstream processing."
        />
        <StatCard
          label="Insights stored"
          value={formatCompactNumber(state.data?.metrics.insights_saved)}
          hint="Persisted insights available for review."
          tone="warm"
        />
      </div>

      {state.error ? (
        <EmptyState
          eyebrow="Request failed"
          title="The overview could not load live data."
          description={state.error}
        />
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[1.2fr_1fr]">
        <Surface>
          <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
            Workspaces
          </p>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <Link
              to="/ops"
              className="group rounded-[1.5rem] border border-[var(--line)] bg-white px-5 py-5 transition hover:-translate-y-0.5 hover:border-[var(--line-strong)] hover:shadow-[0_16px_36px_rgba(8,28,48,0.1)]"
            >
              <p className="text-sm font-medium text-[var(--ink-soft)]">Ops Center</p>
              <h3 className="mt-2 text-2xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                Watch the news pipeline and inspect a document’s journey.
              </h3>
              <p className="mt-3 text-sm leading-6 text-[var(--ink-soft)]">
                Metrics, current queue status, article detail, and recent generated insights in one workspace.
              </p>
              <p className="mt-4 text-sm font-medium text-[var(--accent)]">Open ops workspace</p>
            </Link>

            <Link
              to="/clients"
              className="group rounded-[1.5rem] border border-[var(--line)] bg-white px-5 py-5 transition hover:-translate-y-0.5 hover:border-[var(--line-strong)] hover:shadow-[0_16px_36px_rgba(8,28,48,0.1)]"
            >
              <p className="text-sm font-medium text-[var(--ink-soft)]">Client Workspace</p>
              <h3 className="mt-2 text-2xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                Move from a directory of clients into a focused portfolio review.
              </h3>
              <p className="mt-3 text-sm leading-6 text-[var(--ink-soft)]">
                Portfolio metadata, exposures, tickers, tags, and client-specific insight history.
              </p>
              <p className="mt-4 text-sm font-medium text-[var(--accent)]">
                Open client workspace
              </p>
            </Link>
          </div>
        </Surface>

        <Surface>
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
                Recent Insights
              </p>
              <h3 className="mt-2 text-xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                Latest generated outputs across clients
              </h3>
            </div>
            <StatusBadge
              label={state.data?.insights.length ? `${state.data.insights.length} loaded` : "Waiting"}
              tone="neutral"
            />
          </div>

          <div className="mt-5 grid gap-3">
            {!state.loading && !state.data?.insights.length ? (
              <EmptyState
                eyebrow="No results"
                title="No recent insights were returned."
                description="The insights collection is reachable, but there is nothing recent to show here yet."
              />
            ) : null}

            {state.data?.insights.map((item) => (
              <article
                key={`${item.client_id}-${item.news_doc_id ?? item.timestamp ?? item.news_title}`}
                className="rounded-[1.4rem] border border-[var(--line)] bg-white px-4 py-4"
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <p className="text-sm font-medium text-[var(--ink-soft)]">{item.client_id}</p>
                  <StatusBadge
                    label={item.status}
                    tone={item.status === "saved" ? "good" : item.status === "failed" ? "bad" : "warn"}
                  />
                </div>
                <h4 className="mt-3 text-base font-semibold text-[var(--ink-strong)]">
                  {item.news_title}
                </h4>
                <p className="mt-2 text-sm text-[var(--ink-soft)]">
                  {formatDateTime(item.timestamp)}
                </p>
              </article>
            ))}
          </div>
        </Surface>
      </div>
    </div>
  );
}
