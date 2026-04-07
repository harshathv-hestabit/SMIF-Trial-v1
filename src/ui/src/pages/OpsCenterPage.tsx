import { Link, useParams } from "react-router-dom";

import { EmptyState } from "../components/EmptyState";
import { SectionIntro } from "../components/SectionIntro";
import { StatCard } from "../components/StatCard";
import { StatusBadge } from "../components/StatusBadge";
import { Surface } from "../components/Surface";
import { useAsyncData } from "../hooks/useAsyncData";
import { api } from "../lib/api";
import { formatCompactNumber, formatDateTime } from "../lib/format";

export function OpsCenterPage() {
  const params = useParams<{ newsId?: string }>();

  const dashboardState = useAsyncData(async () => {
    const [metrics, news, insights] = await Promise.all([
      api.getOpsMetrics(),
      api.getOpsNews(24),
      api.getOpsInsights(10),
    ]);

    return {
      metrics,
      news: news.items,
      insights: insights.items,
    };
  }, []);

  const activeNewsId = params.newsId ?? dashboardState.data?.news[0]?.id ?? null;

  const detailState = useAsyncData(
    async () => {
      if (!activeNewsId) {
        return null;
      }

      return api.getOpsNewsDetail(activeNewsId);
    },
    [activeNewsId],
  );

  return (
    <div className="grid gap-6">
      <SectionIntro
        eyebrow="Operations"
        title="News ingestion, pipeline status, and investigation in one view."
        description="Use this workspace to watch operational health, inspect article state transitions, and verify what the latest insight generation activity looks like."
        action={
          <button
            type="button"
            onClick={() => {
              dashboardState.reload();
              detailState.reload();
            }}
            className="rounded-full border border-[var(--line)] bg-white px-4 py-2 text-sm font-medium text-[var(--ink-strong)] transition hover:border-[var(--line-strong)]"
          >
            Refresh ops data
          </button>
        }
      />

      <div className="grid gap-4 xl:grid-cols-5">
        <StatCard
          label="News docs"
          value={formatCompactNumber(dashboardState.data?.metrics.news_docs)}
          hint="Total monitored documents available in the news collection."
          tone="accent"
        />
        <StatCard
          label="Queued to MAS"
          value={formatCompactNumber(dashboardState.data?.metrics.queued_to_mas)}
          hint="Documents waiting to be routed to MAS."
        />
        <StatCard
          label="In insight generation"
          value={formatCompactNumber(dashboardState.data?.metrics.in_insight_generation)}
          hint="Documents currently inside the insight generation stage."
        />
        <StatCard
          label="Insights saved"
          value={formatCompactNumber(dashboardState.data?.metrics.insights_saved)}
          hint="Insights already persisted in storage."
          tone="warm"
        />
        <StatCard
          label="Failed docs"
          value={formatCompactNumber(dashboardState.data?.metrics.failed_news_docs)}
          hint="Documents whose current status is marked as failed."
          tone="critical"
        />
      </div>

      {dashboardState.error ? (
        <EmptyState
          eyebrow="Request failed"
          title="The ops dashboard could not load."
          description={dashboardState.error}
        />
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[0.95fr_1.25fr]">
        <Surface className="min-h-[32rem]">
          <div className="flex items-start justify-between gap-3">
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
                News Queue
              </p>
              <h3 className="mt-2 text-xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                Recent news documents
              </h3>
            </div>
            <StatusBadge
              label={dashboardState.data?.news.length ? `${dashboardState.data.news.length} rows` : "Waiting"}
              tone="neutral"
            />
          </div>

          <div className="mt-5 grid gap-3">
            {!dashboardState.loading && !dashboardState.data?.news.length ? (
              <EmptyState
                eyebrow="No news rows"
                title="No operational documents were returned."
                description="The UI API did not return any recent documents for the current limit."
              />
            ) : null}

            {dashboardState.data?.news.map((item) => (
              <Link
                key={item.id}
                to={`/ops/news/${item.id}`}
                className={[
                  "rounded-[1.45rem] border px-4 py-4 transition",
                  item.id === activeNewsId
                    ? "border-[var(--accent)] bg-[rgba(26,110,255,0.06)] shadow-[0_14px_32px_rgba(26,110,255,0.08)]"
                    : "border-[var(--line)] bg-white hover:border-[var(--line-strong)]",
                ].join(" ")}
              >
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <p className="text-sm font-medium text-[var(--ink-soft)]">{item.source}</p>
                  <StatusBadge
                    label={item.status}
                    tone={item.status === "completed" ? "good" : item.status === "failed" ? "bad" : "warn"}
                  />
                </div>
                <h4 className="mt-3 text-base font-semibold leading-6 text-[var(--ink-strong)]">
                  {item.title}
                </h4>
                <div className="mt-3 flex flex-wrap gap-2 text-xs text-[var(--ink-soft)]">
                  <span className="rounded-full bg-[var(--track)] px-3 py-1">{item.stage}</span>
                  <span className="rounded-full bg-[var(--track)] px-3 py-1">
                    {item.symbols_preview}
                  </span>
                </div>
                <p className="mt-3 text-sm text-[var(--ink-soft)]">
                  Updated {formatDateTime(item.updated_at)}
                </p>
              </Link>
            ))}
          </div>
        </Surface>

        <Surface className="min-h-[32rem]">
          {detailState.error ? (
            <EmptyState
              eyebrow="Detail failed"
              title="The selected news document could not be loaded."
              description={detailState.error}
            />
          ) : detailState.data ? (
            <div>
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="max-w-3xl">
                  <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
                    News Detail
                  </p>
                  <h3 className="mt-2 text-2xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                    {detailState.data.title}
                  </h3>
                  <p className="mt-3 text-sm leading-6 text-[var(--ink-soft)]">
                    Source {detailState.data.source} • Published {formatDateTime(detailState.data.published_at)}
                  </p>
                </div>

                <div className="flex flex-wrap gap-2">
                  <StatusBadge label={detailState.data.current_stage} tone="neutral" />
                  <StatusBadge
                    label={detailState.data.current_status}
                    tone={
                      detailState.data.current_status === "completed"
                        ? "good"
                        : detailState.data.current_status === "failed"
                          ? "bad"
                          : "warn"
                    }
                  />
                </div>
              </div>

              <div className="mt-5 grid gap-4 md:grid-cols-2">
                <article className="rounded-[1.35rem] border border-[var(--line)] bg-white px-4 py-4">
                  <p className="text-sm font-medium text-[var(--ink-soft)]">Tracked symbols</p>
                  <div className="mt-3 flex flex-wrap gap-2">
                    {detailState.data.symbols.length ? (
                      detailState.data.symbols.map((symbol) => (
                        <span
                          key={symbol}
                          className="rounded-full bg-[var(--track)] px-3 py-1 text-sm font-medium text-[var(--ink-strong)]"
                        >
                          {symbol}
                        </span>
                      ))
                    ) : (
                      <span className="text-sm text-[var(--ink-soft)]">No symbols attached</span>
                    )}
                  </div>
                </article>

                <article className="rounded-[1.35rem] border border-[var(--line)] bg-white px-4 py-4">
                  <p className="text-sm font-medium text-[var(--ink-soft)]">Last updated</p>
                  <p className="mt-3 text-lg font-semibold text-[var(--ink-strong)]">
                    {formatDateTime(detailState.data.updated_at)}
                  </p>
                </article>
              </div>

              <div className="mt-6">
                <p className="text-sm font-medium text-[var(--ink-soft)]">Timeline</p>
                <div className="mt-4 grid gap-3">
                  {!detailState.data.timeline.length ? (
                    <EmptyState
                      eyebrow="No timeline"
                      title="This document has no recorded stage history."
                      description="The monitoring payload is present but did not include any timeline events."
                    />
                  ) : null}

                  {detailState.data.timeline.map((event, index) => (
                    <article
                      key={`${event.stage}-${event.timestamp ?? index}`}
                      className="rounded-[1.35rem] border border-[var(--line)] bg-white px-4 py-4"
                    >
                      <div className="flex flex-wrap items-center justify-between gap-3">
                        <p className="font-semibold text-[var(--ink-strong)]">{event.stage}</p>
                        {event.status ? (
                          <StatusBadge
                            label={event.status}
                            tone={
                              event.status === "completed"
                                ? "good"
                                : event.status === "failed"
                                  ? "bad"
                                  : "warn"
                            }
                          />
                        ) : null}
                      </div>
                      <p className="mt-2 text-sm text-[var(--ink-soft)]">
                        {formatDateTime(event.timestamp)}
                      </p>
                      <p className="mt-3 overflow-x-auto rounded-[1rem] bg-[var(--track)] px-3 py-3 font-mono text-xs leading-6 text-[var(--ink-soft)]">
                        {event.details}
                      </p>
                    </article>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <EmptyState
              eyebrow="Select a document"
              title="Choose a news document to inspect its operational timeline."
              description="When a document is selected, this panel shows its current stage, latest status, tracked symbols, and the full monitoring timeline."
            />
          )}
        </Surface>
      </div>

      <Surface>
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
              Insight Feed
            </p>
            <h3 className="mt-2 text-xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
              Recent generation results
            </h3>
          </div>
          <StatusBadge
            label={dashboardState.data?.insights.length ? `${dashboardState.data.insights.length} recent` : "Waiting"}
            tone="neutral"
          />
        </div>

        <div className="mt-5 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          {!dashboardState.loading && !dashboardState.data?.insights.length ? (
            <EmptyState
              eyebrow="No insights"
              title="No recent insight rows were returned."
              description="The ops insight endpoint is reachable, but there are no recent entries to display."
            />
          ) : null}

          {dashboardState.data?.insights.map((item) => (
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
              <h4 className="mt-3 text-base font-semibold leading-6 text-[var(--ink-strong)]">
                {item.news_title}
              </h4>
              <p className="mt-3 text-sm text-[var(--ink-soft)]">
                {formatDateTime(item.timestamp)}
              </p>
            </article>
          ))}
        </div>
      </Surface>
    </div>
  );
}
