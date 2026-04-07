import { Button, Card, CardContent, CardHeader, Spinner } from "@heroui/react";
import { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";

import { DataTable } from "../../components/DataTable";
import { DetailModal } from "../../components/DetailModal";
import { MetricTile } from "../../components/MetricTile";
import { SectionHeader } from "../../components/SectionHeader";
import type { ClientsLayoutContext } from "../../layouts/ClientsLayout";
import { api } from "../../lib/api";
import type { ClientPortfolio, WeightEntry } from "../../lib/types";

export function ClientPortfolioPage() {
  const { selectedClient, selectedClientId } = useOutletContext<ClientsLayoutContext>();
  const [portfolio, setPortfolio] = useState<ClientPortfolio | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeModal, setActiveModal] = useState<"weights" | "references" | null>(null);

  useEffect(() => {
    if (!selectedClientId) {
      setPortfolio(null);
      return;
    }

    let active = true;

    async function loadPortfolio() {
      setLoading(true);
      setError("");
      try {
        const response = await api.getClientPortfolio(selectedClientId);
        if (!active) {
          return;
        }
        setPortfolio(response);
      } catch (err) {
        if (!active) {
          return;
        }
        setError(err instanceof Error ? err.message : "Failed to load client portfolio");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadPortfolio();
    return () => {
      active = false;
    };
  }, [selectedClientId]);

  return (
    <div className="grid gap-4">
      {error ? <InlineError message={error} /> : null}

      <Card className="border border-[var(--border-1)] bg-[rgba(16,22,39,0.86)]">
        <CardHeader className="flex items-center justify-between">
          <SectionHeader
            eyebrow="Portfolio"
            title={portfolio?.client_name ?? selectedClient?.client_name ?? "Portfolio review"}
            description="Keep the portfolio page focused on allocation, mandate, and reference data."
          />
          {loading ? <Spinner size="sm" /> : null}
        </CardHeader>
        <CardContent className="grid gap-4 px-4 pb-4 pt-1">
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
            <MetricTile label="Client Type" value={portfolio?.client_type ?? "-"} />
            <MetricTile label="Mandate" value={portfolio?.mandate ?? "-"} />
            <MetricTile
              label="AUM"
              value={
                portfolio?.total_aum_aed !== undefined
                  ? `AED ${portfolio.total_aum_aed.toLocaleString()}`
                  : "-"
              }
            />
            <MetricTile label="Tickers" value={String(portfolio?.ticker_count ?? 0)} />
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <InfoCard
              title="Portfolio Summary"
              value={truncateText(portfolio?.query ?? "No portfolio summary available.", 180)}
            />
            <InfoCard
              title="Ticker Symbols"
              value={joinPreview(portfolio?.ticker_symbols ?? [], "No ticker symbols available.")}
            />
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <InfoCard
              title="Currencies"
              value={joinPreview(portfolio?.currencies ?? [], "No currencies available.")}
            />
            <InfoCard
              title="Tags Of Interest"
              value={joinPreview(portfolio?.tags_of_interest ?? [], "No derived tags available.")}
            />
          </div>

          <div className="grid gap-4 lg:grid-cols-2">
            <ActionCard
              title="Allocation tables"
              description="Asset class and asset type weights are kept off-page until requested."
              buttonLabel="View allocations"
              onOpen={() => setActiveModal("weights")}
            />
            <ActionCard
              title="Reference lists"
              description="Identifiers and asset descriptions open in a modal instead of extending the page."
              buttonLabel="View references"
              onOpen={() => setActiveModal("references")}
            />
          </div>
        </CardContent>
      </Card>

      <DetailModal
        isOpen={activeModal === "weights"}
        title={`${portfolio?.client_name ?? selectedClient?.client_name ?? "Client"} allocations`}
        description="Allocation tables moved into a modal to keep the main page short."
        onClose={() => setActiveModal(null)}
      >
        <div className="grid gap-4 xl:grid-cols-2">
          <WeightTable
            title="Asset Class Weights"
            rows={portfolio?.classification_weights ?? []}
            emptyMessage="No asset class weights available."
          />
          <WeightTable
            title="Asset Type Weights"
            rows={portfolio?.asset_type_weights ?? []}
            emptyMessage="No asset type weights available."
          />
        </div>
      </DetailModal>

      <DetailModal
        isOpen={activeModal === "references"}
        title={`${portfolio?.client_name ?? selectedClient?.client_name ?? "Client"} references`}
        description="Full asset description and identifier lists."
        onClose={() => setActiveModal(null)}
      >
        <div className="grid gap-4 xl:grid-cols-2">
          <SimpleListTable
            title="Top Asset Descriptions"
            rows={portfolio?.asset_descriptions ?? []}
            columnLabel="Asset Description"
            emptyMessage="No asset descriptions available."
          />
          <SimpleListTable
            title="Identifiers"
            rows={portfolio?.isins ?? []}
            columnLabel="ISIN"
            emptyMessage="No ISINs available."
          />
        </div>
      </DetailModal>
    </div>
  );
}

function InfoCard(props: { title: string; value: string }) {
  return (
    <div className="rounded-2xl border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
        {props.title}
      </p>
      <p className="mt-2 text-sm leading-6 text-[var(--text-2)]">{props.value}</p>
    </div>
  );
}

function ActionCard(props: {
  title: string;
  description: string;
  buttonLabel: string;
  onOpen: () => void;
}) {
  return (
    <div className="rounded-2xl border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] p-4">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
        {props.title}
      </p>
      <p className="mt-2 text-sm leading-6 text-[var(--text-2)]">{props.description}</p>
      <Button
        variant="ghost"
        className="mt-4 border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] text-[var(--text-2)]"
        onPress={props.onOpen}
      >
        {props.buttonLabel}
      </Button>
    </div>
  );
}

function WeightTable(props: {
  title: string;
  rows: WeightEntry[];
  emptyMessage: string;
}) {
  return (
    <div className="grid gap-3">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
        {props.title}
      </p>
      <DataTable
        rows={props.rows}
        emptyMessage={props.emptyMessage}
        maxHeightClassName="max-h-[24rem]"
        columns={[
          {
            key: "label",
            header: "Label",
            cell: (row) => row.label,
          },
          {
            key: "weight",
            header: "Weight %",
            align: "right",
            cell: (row) => row.weight_percent.toFixed(2),
          },
        ]}
      />
    </div>
  );
}

function SimpleListTable(props: {
  title: string;
  rows: string[];
  columnLabel: string;
  emptyMessage: string;
}) {
  return (
    <div className="grid gap-3">
      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-[var(--text-3)]">
        {props.title}
      </p>
      <DataTable
        rows={props.rows.map((value) => ({ value }))}
        emptyMessage={props.emptyMessage}
        maxHeightClassName="max-h-[24rem]"
        columns={[
          {
            key: "value",
            header: props.columnLabel,
            cell: (row) => row.value,
          },
        ]}
      />
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

function joinPreview(values: string[], fallback: string) {
  if (values.length === 0) {
    return fallback;
  }

  const joined = values.join(", ");
  return truncateText(joined, 180);
}
