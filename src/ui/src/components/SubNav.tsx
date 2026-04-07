import { NavLink } from "react-router-dom";

interface SubNavItem {
  to: string;
  label: string;
  description: string;
}

interface SubNavProps {
  items: SubNavItem[];
}

export function SubNav(props: SubNavProps) {
  return (
    <div className="grid gap-3 lg:grid-cols-3">
      {props.items.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          end
          className={({ isActive }) =>
            [
              "rounded-[1.5rem] border p-4 transition",
              isActive
                ? "border-[rgba(255,78,184,0.28)] bg-[linear-gradient(135deg,rgba(89,118,255,0.22),rgba(255,78,184,0.18))] shadow-[0_14px_40px_rgba(6,10,26,0.28)]"
                : "border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] hover:border-[rgba(115,166,255,0.32)] hover:bg-[rgba(115,166,255,0.07)]",
            ].join(" ")
          }
        >
          <p className="text-sm font-semibold text-white">{item.label}</p>
          <p className="mt-1 text-sm text-[var(--text-3)]">{item.description}</p>
        </NavLink>
      ))}
    </div>
  );
}
