"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";

type Stock = {
  id: number;
  ticker: string;
  name?: string | null;
  exchange?: string | null;
};

type StockPayload = {
  ticker: string;
  name?: string;
  exchange?: string;
};

export default function TickersPage() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [ticker, setTicker] = useState("");
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [triggering, setTriggering] = useState<number | null>(null);
  const [info, setInfo] = useState<string | null>(null);

  const loadStocks = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/stocks", { cache: "no-store" });

      if (!res.ok) {
        throw new Error("Failed to load tickers");
      }

      const data = (await res.json()) as Stock[];
      setStocks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadStocks();
  }, [loadStocks]);

  const handleSubmit = useCallback(
    async (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      if (!ticker.trim()) {
        setError("Ticker is required");
        return;
      }

      setPending(true);
      setError(null);
      setInfo(null);

      try {
        const res = await fetch(`/api/stocks?ticker=${encodeURIComponent(ticker.trim().toUpperCase())}`, {
          method: "POST",
        });

        if (!res.ok) {
          const message = await res
            .json()
            .then((data) => data.detail ?? data.error ?? "Failed to add ticker")
            .catch(() => "Failed to add ticker");
          throw new Error(message);
        }

        setTicker("");
        const data = await res.json();
        await loadStocks();
        setInfo(`Ticker ${ticker.toUpperCase()} added and refresh scheduled (Task ID: ${data.task_id})`);
        setTicker("");
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      } finally {
        setPending(false);
      }
    },
    [loadStocks, ticker]
  );

  return (
    <div className="min-h-screen bg-zinc-50 p-6 text-zinc-900">
      <div className="mx-auto flex w-full max-w-3xl flex-col gap-8">
        <header className="flex flex-col gap-2">
          <h1 className="text-3xl font-semibold tracking-tight">Tracked Tickers</h1>
          <p className="text-sm text-zinc-600">
            Review everything we monitor and quickly add new symbols.
          </p>
        </header>

        <section className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-medium">Add Ticker</h2>
          <form className="mt-4 flex flex-col gap-4" onSubmit={handleSubmit}>
            <div className="flex gap-4">
              <label className="flex flex-col gap-2 text-sm font-medium text-zinc-700">
                Ticker Symbol
                <input
                  className="rounded-lg border border-zinc-300 px-3 py-2 text-base shadow-sm focus:border-zinc-500 focus:outline-none focus:ring-2 focus:ring-zinc-200"
                  value={ticker}
                  onChange={(event) => setTicker(event.target.value)}
                  placeholder="AAPL"
                  maxLength={12}
                  required
                />
              </label>
            </div>

            <div className="flex items-center gap-3">
              <button
                type="submit"
                className="inline-flex items-center justify-center rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-zinc-700 disabled:cursor-not-allowed disabled:bg-zinc-400"
                disabled={pending}
              >
                {pending ? "Adding…" : "Add"}
              </button>
              {error ? (
                <p className="text-sm text-red-600">{error}</p>
              ) : info ? (
                <p className="text-sm text-emerald-600">{info}</p>
              ) : (
                <p className="text-sm text-zinc-500">
                  Ticker codes are uppercased automatically.
                </p>
              )}
            </div>
          </form>
        </section>

        <section className="rounded-xl border border-zinc-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-medium">Current List</h2>
            <button
              type="button"
              onClick={() => void loadStocks()}
              className="text-sm font-medium text-zinc-500 hover:text-zinc-700"
              disabled={loading || pending}
            >
              Refresh
            </button>
          </div>

          <div className="mt-4 overflow-hidden rounded-lg border border-zinc-200">
            <table className="min-w-full divide-y divide-zinc-200 text-sm">
              <thead className="bg-zinc-100 text-left text-xs font-semibold uppercase tracking-wide text-zinc-600">
                <tr>
                  <th className="px-4 py-2">Ticker</th>
                  <th className="px-4 py-2">Name</th>
                  <th className="px-4 py-2">Exchange</th>
              <th className="px-4 py-2" />
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200">
                {loading ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-zinc-500" colSpan={3}>
                      Loading…
                    </td>
                  </tr>
                ) : stocks.length === 0 ? (
                  <tr>
                    <td className="px-4 py-6 text-center text-zinc-500" colSpan={3}>
                      Nothing tracked yet.
                    </td>
                  </tr>
                ) : (
                  stocks.map((stock) => (
                    <tr key={stock.id}>
                      <td className="px-4 py-2 font-medium text-zinc-900">
                        {stock.ticker}
                      </td>
                      <td className="px-4 py-2 text-zinc-700">
                        {stock.name || <span className="text-zinc-400">—</span>}
                      </td>
                      <td className="px-4 py-2 text-zinc-700">
                        {stock.exchange || <span className="text-zinc-400">—</span>}
                      </td>
                      <td className="px-4 py-2 text-right">
                        <button
                          type="button"
                          className="rounded-lg border border-zinc-200 px-3 py-1.5 text-xs font-medium text-zinc-600 transition hover:border-zinc-400 hover:text-zinc-800 disabled:cursor-not-allowed disabled:text-zinc-400"
                          onClick={async () => {
                            setTriggering(stock.id);
                            setError(null);
                            setInfo(null);
                            try {
                              const res = await fetch(`/api/stocks/${stock.id}/start`, {
                                method: "POST",
                              });

                              if (!res.ok) {
                                const message = await res
                                  .json()
                                  .then((data) => data.detail ?? data.error ?? "Failed to start job")
                                  .catch(() => "Failed to start job");
                                throw new Error(message);
                              }

                              setInfo(`Refresh queued for ${stock.ticker}`);
                            } catch (err) {
                              setError(err instanceof Error ? err.message : "Unknown error");
                            } finally {
                              setTriggering(null);
                            }
                          }}
                          disabled={triggering === stock.id}
                        >
                          {triggering === stock.id ? "Scheduling…" : "Start"}
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}

