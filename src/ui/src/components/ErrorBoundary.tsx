import type { ReactNode } from "react";
import { Component } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  message: string;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = {
    hasError: false,
    message: "",
  };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      message: error.message || "Unexpected UI error",
    };
  }

  componentDidCatch(error: Error) {
    console.error("SMIF UI render failure", error);
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="grid min-h-screen place-items-center bg-[var(--canvas)] p-6 text-[var(--ink-strong)]">
          <div className="grid max-w-xl gap-4 rounded-[2rem] border border-[var(--line)] bg-[var(--panel-strong)] p-8 shadow-[0_20px_80px_rgba(15,23,42,0.08)]">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.25em] text-[var(--critical)]">
                UI Error
              </p>
              <h1 className="mt-2 text-2xl font-semibold">The page hit a render failure.</h1>
            </div>
            <p className="text-sm text-[var(--ink-soft)]">{this.state.message}</p>
            <div>
              <button
                type="button"
                onClick={this.handleReload}
                className="rounded-full bg-[var(--accent)] px-4 py-2 text-sm font-medium text-white transition hover:bg-[var(--accent-strong)]"
              >
                Reload Page
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
