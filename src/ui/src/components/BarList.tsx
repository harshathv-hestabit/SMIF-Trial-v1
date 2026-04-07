import { formatPercent } from "../lib/format";

export interface BarListItem {
  label: string;
  value: number;
}

export function BarList(props: {
  items: BarListItem[];
  emptyMessage: string;
}) {
  if (!props.items.length) {
    return <p className="text-sm text-[var(--ink-soft)]">{props.emptyMessage}</p>;
  }

  const maxValue = Math.max(...props.items.map((item) => item.value), 1);

  return (
    <div className="grid gap-3">
      {props.items.map((item) => (
        <div key={item.label} className="grid gap-2">
          <div className="flex items-center justify-between gap-3 text-sm">
            <span className="font-medium text-[var(--ink-strong)]">{item.label}</span>
            <span className="text-[var(--ink-soft)]">{formatPercent(item.value)}</span>
          </div>
          <div className="h-2 rounded-full bg-[var(--track)]">
            <div
              className="h-2 rounded-full bg-[linear-gradient(90deg,var(--accent),var(--accent-warm))]"
              style={{ width: `${Math.max((item.value / maxValue) * 100, 7)}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
