import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { ModeToggle } from "@/components/mode-toggle";

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
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="relative flex min-h-screen flex-col overflow-hidden bg-background text-foreground">
            <div className="pointer-events-none absolute inset-0 z-0">
              <div className="rainbow-bubbles">
                <span className="rainbow-bubble bubble-a" aria-hidden />
                <span className="rainbow-bubble bubble-b" aria-hidden />
                <span className="rainbow-bubble bubble-c" aria-hidden />
                <span className="rainbow-bubble bubble-d" aria-hidden />
              </div>
            </div>
            <header className="relative z-10 border-b border-border bg-card/80 backdrop-blur">
              <div className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-4">
                <Link
                  href="/"
                  className="text-lg font-semibold tracking-tight text-foreground"
                >
                  Ticker Watch
                </Link>
                <nav className="flex items-center gap-4 text-sm font-medium text-muted-foreground">
                  <Link href="/" className="transition hover:text-foreground">
                    Home
                  </Link>
                  <Link href="/tickers" className="transition hover:text-foreground">
                    Tickers
                  </Link>
                  <ModeToggle />
                </nav>
              </div>
            </header>
            <main className="relative z-10 flex-1">{children}</main>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
