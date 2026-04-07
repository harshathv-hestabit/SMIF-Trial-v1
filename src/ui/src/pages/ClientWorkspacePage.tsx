import { startTransition, useDeferredValue, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { BarList } from "../components/BarList";
import { EmptyState } from "../components/EmptyState";
import { SectionIntro } from "../components/SectionIntro";
import { StatCard } from "../components/StatCard";
import { StatusBadge } from "../components/StatusBadge";
import { Surface } from "../components/Surface";
import { useAsyncData } from "../hooks/useAsyncData";
import { api } from "../lib/api";
import { formatCompactNumber, formatCurrency, formatDateTime, normalizeText } from "../lib/format";

export function ClientWorkspacePage() {
  const navigate = useNavigate();
  const params = useParams<{ clientId?: string }>();
  const [search, setSearch] = useState("");
  const deferredSearch = useDeferredValue(search);

  const clientsState = useAsyncData(() => api.listClients(), []);
  const selectedClientId = params.clientId ?? null;

  const filteredClients =
    clientsState.data?.items.filter((client) => {
      const needle = normalizeText(deferredSearch);
      if (!needle) {
        return true;
      }

      return (
        normalizeText(client.client_id).includes(needle) ||
        normalizeText(client.client_name).includes(needle)
      );
    }) ?? [];

  useEffect(() => {
    if (!selectedClientId && clientsState.data?.items.length) {
      navigate(`/clients/${clientsState.data.items[0].client_id}`, { replace: true });
    }
  }, [navigate, selectedClientId, clientsState.data]);

  const portfolioState = useAsyncData(
    async () => {
      if (!selectedClientId) {
        return null;
      }

      return api.getClientPortfolio(selectedClientId);
    },
    [selectedClientId],
  );

  const insightsState = useAsyncData(
    async () => {
      if (!selectedClientId) {
        return null;
      }

      return api.getClientInsights(selectedClientId);
    },
    [selectedClientId],
  );

  return (
    <div className="grid gap-6">
      <SectionIntro
        eyebrow="Clients"
        title="Start from the directory, then drop into one client at a time."
        description="This workspace keeps the client selector visible while the right side focuses on the selected portfolio, its exposure profile, and the latest generated insights."
        action={
          <button
            type="button"
            onClick={() => {
              clientsState.reload();
              portfolioState.reload();
              insightsState.reload();
            }}
            className="rounded-full border border-[var(--line)] bg-white px-4 py-2 text-sm font-medium text-[var(--ink-strong)] transition hover:border-[var(--line-strong)]"
          >
            Refresh client data
          </button>
        }
      />

      <div className="grid gap-6 xl:grid-cols-[22rem_minmax(0,1fr)]">
        <Surface className="h-fit">
          <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
            Directory
          </p>
          <h3 className="mt-2 text-xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
            Client list
          </h3>

          <label className="mt-5 block">
            <span className="sr-only">Search clients</span>
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search by name or client id"
              className="w-full rounded-[1rem] border border-[var(--line)] bg-white px-4 py-3 text-sm text-[var(--ink-strong)] outline-none transition placeholder:text-[var(--ink-soft)] focus:border-[var(--accent)]"
            />
          </label>

          <div className="mt-5 grid gap-2">
            {clientsState.error ? (
              <EmptyState
                eyebrow="Request failed"
                title="The client directory could not load."
                description={clientsState.error}
              />
            ) : null}

            {!clientsState.loading && !filteredClients.length ? (
              <EmptyState
                eyebrow="No matches"
                title="No clients matched the current search."
                description="Try a broader name fragment or use the exact client id."
              />
            ) : null}

            {filteredClients.map((client) => (
              <button
                key={client.client_id}
                type="button"
                onClick={() =>
                  startTransition(() => {
                    navigate(`/clients/${client.client_id}`);
                  })
                }
                className={[
                  "rounded-[1.25rem] border px-4 py-3 text-left transition",
                  client.client_id === selectedClientId
                    ? "border-[var(--accent)] bg-[rgba(26,110,255,0.06)]"
                    : "border-[var(--line)] bg-white hover:border-[var(--line-strong)]",
                ].join(" ")}
              >
                <p className="font-medium text-[var(--ink-strong)]">{client.client_name}</p>
                <p className="mt-1 text-sm text-[var(--ink-soft)]">{client.client_id}</p>
              </button>
            ))}
          </div>
        </Surface>

        <div className="grid gap-6">
          {portfolioState.error ? (
            <EmptyState
              eyebrow="Portfolio failed"
              title="The selected client portfolio could not be loaded."
              description={portfolioState.error}
            />
          ) : null}

          {portfolioState.data ? (
            <>
              <div className="grid gap-4 lg:grid-cols-4">
                <StatCard
                  label="Client"
                  value={portfolioState.data.client_name ?? portfolioState.data.client_id}
                  hint={portfolioState.data.client_type ?? "Client type unavailable"}
                  tone="accent"
                />
                <StatCard
                  label="AUM"
                  value={formatCurrency(portfolioState.data.total_aum_aed)}
                  hint="Total AUM in AED when available."
                />
                <StatCard
                  label="Tickers"
                  value={formatCompactNumber(portfolioState.data.ticker_count)}
                  hint="Unique ticker symbols in the stored portfolio."
                />
                <StatCard
                  label="Mandate"
                  value={portfolioState.data.mandate ?? "-"}
                  hint="Current stored mandate for the client."
                  tone="warm"
                />
              </div>

              <div className="grid gap-6 2xl:grid-cols-[1.15fr_0.85fr]">
                <Surface>
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                    <div>
                      <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
                        Portfolio Profile
                      </p>
                      <h3 className="mt-2 text-xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                        Exposure summary and watchlist context
                      </h3>
                    </div>
                    <StatusBadge
                      label={`${portfolioState.data.currencies.length || 0} currencies`}
                      tone="neutral"
                    />
                  </div>

                  <div className="mt-6 grid gap-6 lg:grid-cols-2">
                    <div>
                      <p className="text-sm font-medium text-[var(--ink-soft)]">Classification weights</p>
                      <div className="mt-4">
                        <BarList
                          items={portfolioState.data.classification_weights.map((item) => ({
                            label: item.label,
                            value: item.weight_percent,
                          }))}
                          emptyMessage="No classification weights available."
                        />
                      </div>
                    </div>

                    <div>
                      <p className="text-sm font-medium text-[var(--ink-soft)]">Asset type weights</p>
                      <div className="mt-4">
                        <BarList
                          items={portfolioState.data.asset_type_weights.map((item) => ({
                            label: item.label,
                            value: item.weight_percent,
                          }))}
                          emptyMessage="No asset type weights available."
                        />
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 grid gap-4 lg:grid-cols-2">
                    <article className="rounded-[1.35rem] border border-[var(--line)] bg-white px-4 py-4">
                      <p className="text-sm font-medium text-[var(--ink-soft)]">Tags of interest</p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        {portfolioState.data.tags_of_interest.length ? (
                          portfolioState.data.tags_of_interest.map((tag) => (
                            <span
                              key={tag}
                              className="rounded-full bg-[var(--track)] px-3 py-1 text-sm font-medium text-[var(--ink-strong)]"
                            >
                              {tag}
                            </span>
                          ))
                        ) : (
                          <span className="text-sm text-[var(--ink-soft)]">No tags stored</span>
                        )}
                      </div>
                    </article>

                    <article className="rounded-[1.35rem] border border-[var(--line)] bg-white px-4 py-4">
                      <p className="text-sm font-medium text-[var(--ink-soft)]">Currencies</p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        {portfolioState.data.currencies.length ? (
                          portfolioState.data.currencies.map((currency) => (
                            <span
                              key={currency}
                              className="rounded-full bg-[var(--track)] px-3 py-1 text-sm font-medium text-[var(--ink-strong)]"
                            >
                              {currency}
                            </span>
                          ))
                        ) : (
                          <span className="text-sm text-[var(--ink-soft)]">No currencies stored</span>
                        )}
                      </div>
                    </article>
                  </div>

                  {portfolioState.data.query ? (
                    <article className="mt-4 rounded-[1.35rem] border border-[var(--line)] bg-white px-4 py-4">
                      <p className="text-sm font-medium text-[var(--ink-soft)]">Generated search query</p>
                      <p className="mt-3 font-mono text-sm leading-6 text-[var(--ink-strong)]">
                        {portfolioState.data.query}
                      </p>
                    </article>
                  ) : null}
                </Surface>

                <Surface>
                  <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
                    Portfolio Contents
                  </p>
                  <h3 className="mt-2 text-xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                    Tickers and asset descriptions
                  </h3>

                  <div className="mt-6">
                    <p className="text-sm font-medium text-[var(--ink-soft)]">Ticker symbols</p>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {portfolioState.data.ticker_symbols.length ? (
                        portfolioState.data.ticker_symbols.map((symbol) => (
                          <span
                            key={symbol}
                            className="rounded-full bg-[var(--track)] px-3 py-1 text-sm font-medium text-[var(--ink-strong)]"
                          >
                            {symbol}
                          </span>
                        ))
                      ) : (
                        <span className="text-sm text-[var(--ink-soft)]">No ticker symbols stored</span>
                      )}
                    </div>
                  </div>

                  <div className="mt-6">
                    <p className="text-sm font-medium text-[var(--ink-soft)]">Asset descriptions</p>
                    <div className="mt-3 grid gap-2">
                      {portfolioState.data.asset_descriptions.length ? (
                        portfolioState.data.asset_descriptions.map((description) => (
                          <article
                            key={description}
                            className="rounded-[1rem] border border-[var(--line)] bg-white px-4 py-3 text-sm leading-6 text-[var(--ink-soft)]"
                          >
                            {description}
                          </article>
                        ))
                      ) : (
                        <p className="text-sm text-[var(--ink-soft)]">No asset descriptions stored</p>
                      )}
                    </div>
                  </div>
                </Surface>
              </div>
            </>
          ) : (
            <EmptyState
              eyebrow="Select a client"
              title="Choose a client from the directory to load portfolio detail."
              description="The right-hand workspace becomes active once a client is selected and the portfolio endpoint returns data."
            />
          )}

          <Surface>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-[0.28em] text-[var(--accent)]">
                  Insight History
                </p>
                <h3 className="mt-2 text-xl font-semibold tracking-[-0.04em] text-[var(--ink-strong)]">
                  Client-specific generated insights
                </h3>
              </div>
              <StatusBadge
                label={insightsState.data ? `${insightsState.data.count} items` : "Waiting"}
                tone="neutral"
              />
            </div>

            {insightsState.error ? (
              <div className="mt-5">
                <EmptyState
                  eyebrow="Insights failed"
                  title="The client insight feed could not be loaded."
                  description={insightsState.error}
                />
              </div>
            ) : null}

            <div className="mt-5 grid gap-3">
              {!insightsState.loading && !insightsState.data?.items.length ? (
                <EmptyState
                  eyebrow="No insights"
                  title="No stored insights were returned for this client."
                  description="The endpoint is reachable, but there are no generated insights for the selected client yet."
                />
              ) : null}

              {insightsState.data?.items.map((item) => (
                <article
                  key={item.id}
                  className="rounded-[1.4rem] border border-[var(--line)] bg-white px-4 py-4"
                >
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <p className="text-sm font-medium text-[var(--ink-soft)]">
                      {formatDateTime(item.timestamp)}
                    </p>
                    <StatusBadge
                      label={item.status}
                      tone={item.status === "saved" ? "good" : item.status === "failed" ? "bad" : "warn"}
                    />
                  </div>
                  <h4 className="mt-3 text-lg font-semibold leading-7 text-[var(--ink-strong)]">
                    {item.news_title}
                  </h4>
                  <p className="mt-3 text-sm leading-7 text-[var(--ink-soft)]">{item.insight}</p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {item.tickers.map((ticker) => (
                      <span
                        key={ticker}
                        className="rounded-full bg-[var(--track)] px-3 py-1 text-sm font-medium text-[var(--ink-strong)]"
                      >
                        {ticker}
                      </span>
                    ))}
                  </div>
                </article>
              ))}
            </div>
          </Surface>
        </div>
      </div>
    </div>
  );
}
