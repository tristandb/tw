export default function Home() {
  return (
    <section className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-6 py-16">
      <div className="rounded-2xl border border-zinc-200 bg-white p-10 shadow-sm">
        <div className="flex flex-col gap-4">
          <span className="inline-flex w-fit items-center gap-2 rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium uppercase tracking-wide text-zinc-600">
            Overview
          </span>
          <h1 className="text-4xl font-semibold tracking-tight text-zinc-900">
            Monitor the symbols that matter.
          </h1>
          <p className="max-w-2xl text-lg text-zinc-600">
            Use the tickers dashboard to keep an eye on coverage, spot gaps, and
            onboard new names in seconds.
          </p>
        </div>

        <div className="mt-8 grid gap-6 sm:grid-cols-3">
          <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-6">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
              Add instantly
            </h2>
            <p className="mt-2 text-sm text-zinc-600">
              Capture a new ticker with optional metadata, automatically
              standardized to uppercase.
            </p>
          </div>
          <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-6">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
              Prevent duplication
            </h2>
            <p className="mt-2 text-sm text-zinc-600">
              Backend guards ensure you never add the same symbol twice.
            </p>
          </div>
          <div className="rounded-xl border border-zinc-200 bg-zinc-50 p-6">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-500">
              Stay organized
            </h2>
            <p className="mt-2 text-sm text-zinc-600">
              See your entire coverage universe at a glance and use exchange/name
              tags to keep context.
            </p>
          </div>
        </div>

        <div className="mt-10 flex flex-wrap items-center gap-4 text-sm font-medium">
          <a
            href="/tickers"
            className="inline-flex items-center justify-center rounded-lg bg-zinc-900 px-4 py-2 text-white transition hover:bg-zinc-700"
          >
            Go to Tickers
          </a>
          <span className="text-zinc-500">
            Need something else? Drop it in the backlog and we&apos;ll wire it up.
          </span>
        </div>
      </div>
    </section>
  );
}
