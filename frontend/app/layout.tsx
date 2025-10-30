import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Ticker Watch",
  description: "Track stock symbols under coverage",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-zinc-50 text-zinc-900`}
      >
        <div className="flex min-h-screen flex-col">
          <header className="border-b border-zinc-200 bg-white/90 backdrop-blur">
            <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-4">
              <Link
                href="/"
                className="text-lg font-semibold tracking-tight text-zinc-900"
              >
                Ticker Watch
              </Link>
              <nav className="flex items-center gap-6 text-sm font-medium text-zinc-600">
                <Link href="/" className="transition hover:text-zinc-900">
                  Home
                </Link>
                <Link href="/tickers" className="transition hover:text-zinc-900">
                  Tickers
                </Link>
              </nav>
            </div>
          </header>
          <main className="flex-1">{children}</main>
        </div>
      </body>
    </html>
  );
}
