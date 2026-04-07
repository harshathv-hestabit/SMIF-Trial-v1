import { Button } from "@heroui/react";
import type { ReactNode } from "react";
import { useEffect } from "react";
import { createPortal } from "react-dom";

interface DetailModalProps {
  isOpen: boolean;
  title: string;
  description?: string;
  onClose: () => void;
  children: ReactNode;
}

export function DetailModal(props: DetailModalProps) {
  useEffect(() => {
    if (!props.isOpen) {
      return;
    }

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        props.onClose();
      }
    }

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [props.isOpen, props.onClose]);

  if (!props.isOpen) {
    return null;
  }

  return createPortal(
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-[rgba(3,7,18,0.72)] p-4 backdrop-blur-md"
      role="presentation"
      onClick={props.onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={props.title}
        className="grid max-h-[85vh] w-full max-w-5xl gap-4 overflow-hidden rounded-[1.75rem] border border-[var(--border-1)] bg-[linear-gradient(180deg,rgba(12,18,33,0.96),rgba(15,20,37,0.94))] shadow-[0_24px_80px_rgba(1,5,20,0.5)]"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4 border-b border-[var(--border-1)] px-5 py-4">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-[var(--text-3)]">
              Detail View
            </p>
            <h2 className="mt-1 text-xl font-semibold text-white">{props.title}</h2>
            {props.description ? (
              <p className="mt-1 text-sm text-[var(--text-3)]">{props.description}</p>
            ) : null}
          </div>
          <Button
            variant="ghost"
            className="border border-[var(--border-1)] bg-[rgba(255,255,255,0.03)] text-[var(--text-2)]"
            onPress={props.onClose}
          >
            Close
          </Button>
        </div>
        <div className="overflow-y-auto px-5 pb-5">{props.children}</div>
      </div>
    </div>,
    document.body,
  );
}
