import { Button, Card, CardContent, CardHeader, Input, Spinner } from "@heroui/react";
import { useDeferredValue, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { DataTable, StatusChip } from "../../components/DataTable";
import { DetailModal } from "../../components/DetailModal";
import { SectionHeader } from "../../components/SectionHeader";
import { api } from "../../lib/api";
import type { OpsNewsDetail, OpsNewsItem } from "../../lib/types";

const REFRESH_INTERVAL_MS = 10_000;

export function OpsNewsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [news, setNews] = useState<OpsNewsItem[]>([]);
  const [selectedNews, setSelectedNews] = useState<OpsNewsDetail | null>(null);
  const [newsLimit, setNewsLimit] = useState("50");
  const [newsFilter, setNewsFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [detailLoading, setDetailLoading] = useState(false);
  const [error, setError] = useState("");
  const [refreshNonce, setRefreshNonce] = useState(0);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);

  const selectedNewsId = searchParams.get("news") ?? "";
  const deferredFilter = useDeferredValue(newsFilter);
  const filteredNews = news.filter((item) => {
    const query = deferredFilter.trim().toLowerCase();
    if (!query) {
      return true;
    }
    return (
      item.title.toLowerCase().includes(query) ||
      item.source.toLowerCase().includes(query) ||
      item.stage.toLowerCase().includes(query) ||
      item.status.toLowerCase().includes(query)
    );
  });

  useEffect(() => {
    let active = true;

    async function loadNews() {
      setLoading(true);
      setError("");
      try {
        const response = await api.getOpsNews(Number(newsLimit));
        if (!active) {
          return;
        }
        setNews(response.items);

        const currentSelectedExists = response.items.some((item) => item.id === selectedNewsId);
        const firstNewsId = response.items[0]?.id ?? "";

        if (!selectedNewsId || !currentSelectedExists) {
          const nextParams = new URLSearchParams(searchParams);
          if (firstNewsId) {
            nextParams.set("news", firstNewsId);
          } else {
            nextParams.delete("news");
          }
          setSearchParams(nextParams, { replace: true });
        }
      } catch (err) {
        if (!active) {
          return;
        }
        setError(err instanceof Error ? err.message : "Failed to load news documents");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadNews();
    const timer = window.setInterval(() => {
      void loadNews();
    }, REFRESH_INTERVAL_MS);

    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, [newsLimit, refreshNonce, setSearchParams]);

  useEffect(() => {
    if (!selectedNewsId) {
      setSelectedNews(null);
      return;
    }

    let active = true;

    async function loadNewsDetail() {
      setDetailLoading(true);
      setError("");
      try {
        const detail = await api.getOpsNewsDetail(selectedNewsId);
        if (!active) {
          return;
        }
        setSelectedNews(detail);
      } catch (err) {
        if (!active) {
          return;
        }
        setSelectedNews(null);
        setError(err instanceof Error ? err.message : "Failed to load news detail");
      } finally {
        if (active) {
          setDetailLoading(false);
        }
      }
    }

    void loadNewsDetail();
    return () => {
      active = false;
    };
  }, [selectedNewsId]);

  return (
    <div className="grid gap-4">
      {error ? <InlineError message={error} /> : null}

      <Card className="border border-[var(--border-1)] bg-[rgba(16,22,39,0.86)]">
        <CardHeader className="grid gap-3 border-b border-[rgba(139,163,255,0.12)] pb-4">
          <SectionHeader
            eyebrow="Lifecycle"
            title="News explorer"
            description="A dedicated view for document discovery, filtering, and selection."
            action={
              <Button
                variant="ghost"
                className="border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] text-[var(--text-2)]"
                onPress={() => setRefreshNonce((value) => value + 1)}
              >
                Refresh Now
              </Button>
            }
          />
          <div className="grid gap-3 md:grid-cols-[minmax(0,1fr)_220px_auto]">
            <Input
              aria-label="Filter news rows"
              placeholder="Filter by title, source, stage, or status"
              className="rounded-2xl border border-[var(--border-1)] bg-[rgba(255,255,255,0.04)] px-4 py-3 text-[var(--text-1)] placeholder:text-[var(--text-3)]"
              value={newsFilter}
              onChange={(event) => setNewsFilter(event.currentTarget.value)}
            />
            <LimitPicker
              label="Rows"
              value={newsLimit}
              options={["10", "25", "50", "100", "200"]}
              onChange={setNewsLimit}
            />
            <div className="flex items-center justify-end">
              {loading ? <Spinner size="sm" /> : null}
            </div>
          </div>
        </CardHeader>
        <CardContent className="px-4 pb-4 pt-3">
          <DataTable
            ariaLabel="Live news documents"
            rows={filteredNews}
            emptyMessage="No news documents found for the current filters."
            getRowKey={(row) => row.id}
            maxHeightClassName="max-h-[34rem]"
            columns={[
              {
                key: "title",
                header: "Document",
                cell: (row) => (
                  <button
                    type="button"
                    className="grid gap-1 text-left"
                    onClick={() => {
                      const nextParams = new URLSearchParams(searchParams);
                      nextParams.set("news", row.id);
                      setSearchParams(nextParams);
                    }}
                  >
                    <span className="font-semibold text-white">{row.title}</span>
                    <span className="text-xs text-[var(--text-3)]">{row.id}</span>
                  </button>
                ),
              },
              {
                key: "source",
                header: "Source",
                cell: (row) => row.source,
              },
              {
                key: "stage",
                header: "Stage",
                cell: (row) => row.stage,
              },
              {
                key: "status",
                header: "Status",
                cell: (row) => <StatusChip value={row.status} />,
              },
              {
                key: "published_at",
                header: "Published",
                cell: (row) => row.published_at,
              },
              {
                key: "updated_at",
                header: "Updated",
                cell: (row) => row.updated_at,
              },
            ]}
          />
        </CardContent>
      </Card>

      <Card className="border border-[var(--border-1)] bg-[rgba(16,22,39,0.86)]">
        <CardHeader className="flex items-center justify-between">
          <SectionHeader
            eyebrow="Detail"
            title="Selected document"
            description="Keep the page compact and open the full lifecycle only when needed."
          />
          <div className="flex items-center gap-3">
            {detailLoading ? <Spinner size="sm" /> : null}
            <Button
              variant="ghost"
              className="border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] text-[var(--text-2)]"
              isDisabled={!selectedNews}
              onPress={() => setIsDetailModalOpen(true)}
            >
              View Full Timeline
            </Button>
          </div>
        </CardHeader>
        <CardContent className="px-4 pb-4 pt-1">
          {selectedNews ? (
            <div className="grid gap-4 rounded-2xl border border-[var(--border-1)] bg-[rgba(115,166,255,0.07)] p-5 lg:grid-cols-[minmax(0,1fr)_260px]">
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-[var(--text-3)]">
                  Selected document
                </p>
                <h3 className="mt-2 line-clamp-2 text-xl font-semibold text-white">
                  {selectedNews.title}
                </h3>
                <p className="mt-2 text-sm text-[var(--text-2)]">{selectedNews.source}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  <StatusChip value={selectedNews.current_status} />
                  <StatusChip value={selectedNews.current_stage} />
                </div>
              </div>
              <div className="grid gap-3 text-sm text-[var(--text-2)]">
                <DetailStat label="Document ID" value={selectedNews.id} />
                <DetailStat label="Published" value={selectedNews.published_at} />
                <DetailStat label="Events" value={String(selectedNews.timeline.length)} />
                <DetailStat
                  label="Symbols"
                  value={selectedNews.symbols.length > 0 ? selectedNews.symbols.join(", ") : "None"}
                />
              </div>
            </div>
          ) : (
            <p className="rounded-2xl border border-dashed border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] p-6 text-sm text-[var(--text-3)]">
              Select a news document to inspect its timeline.
            </p>
          )}
        </CardContent>
      </Card>

      <DetailModal
        isOpen={isDetailModalOpen && Boolean(selectedNews)}
        title={selectedNews?.title ?? "Selected document"}
        description="Lifecycle history and document metadata."
        onClose={() => setIsDetailModalOpen(false)}
      >
        {selectedNews ? (
          <div className="grid gap-4">
            <div className="grid gap-4 rounded-2xl border border-[var(--border-1)] bg-[rgba(115,166,255,0.07)] p-5 lg:grid-cols-[minmax(0,1fr)_260px]">
              <div>
                <p className="text-sm text-[var(--text-2)]">{selectedNews.source}</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  <StatusChip value={selectedNews.current_status} />
                  <StatusChip value={selectedNews.current_stage} />
                </div>
              </div>
              <div className="grid gap-3 text-sm text-[var(--text-2)]">
                <DetailStat label="Document ID" value={selectedNews.id} />
                <DetailStat label="Published" value={selectedNews.published_at} />
                <DetailStat label="Updated" value={selectedNews.updated_at} />
                <DetailStat
                  label="Symbols"
                  value={selectedNews.symbols.length > 0 ? selectedNews.symbols.join(", ") : "None"}
                />
              </div>
            </div>

            <DataTable
              ariaLabel="News lifecycle timeline"
              rows={selectedNews.timeline}
              emptyMessage="No lifecycle events yet."
              getRowKey={(row, index) => `${row.timestamp ?? "event"}-${index}`}
              maxHeightClassName="max-h-[32rem]"
              columns={[
                {
                  key: "timestamp",
                  header: "Timestamp",
                  cell: (row) => row.timestamp ?? "-",
                },
                {
                  key: "stage",
                  header: "Stage",
                  cell: (row) => row.stage,
                },
                {
                  key: "status",
                  header: "Status",
                  cell: (row) => <StatusChip value={row.status ?? "unknown"} />,
                },
                {
                  key: "details",
                  header: "Details",
                  cell: (row) => (
                    <span className="block whitespace-pre-wrap break-words text-xs text-[var(--text-3)]">
                      {row.details}
                    </span>
                  ),
                },
              ]}
            />
          </div>
        ) : null}
      </DetailModal>
    </div>
  );
}

function LimitPicker(props: {
  label: string;
  value: string;
  options: string[];
  onChange: (value: string) => void;
}) {
  return (
    <div className="grid gap-2 rounded-2xl border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] p-3">
      <p className="text-[11px] font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
        {props.label}
      </p>
      <div className="flex flex-wrap gap-2">
        {props.options.map((option) => (
          <Button
            key={option}
            size="sm"
            variant={option === props.value ? "primary" : "ghost"}
            className={
              option === props.value
                ? ""
                : "border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] text-[var(--text-2)]"
            }
            onPress={() => props.onChange(option)}
          >
            {option}
          </Button>
        ))}
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
