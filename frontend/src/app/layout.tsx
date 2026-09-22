import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import { Suspense } from "react";

const outfit = Outfit({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Disaster Relief Allocation",
  description: "Right Resource. Right Place. Right Time.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body suppressHydrationWarning className={`${outfit.className} min-h-screen text-slate-800 bg-slate-50 selection:bg-blue-200 selection:text-blue-900`}>
        <div className="flex relative">
          <Suspense fallback={<div className="w-64 bg-white border-r border-slate-200 h-screen fixed">Loading...</div>}>
            <Sidebar />
          </Suspense>
          <div className="ml-64 flex-1 p-8 relative z-10 bg-slate-50">
            <Suspense fallback={<div className="animate-pulse text-blue-600">Loading data...</div>}>
              {children}
            </Suspense>
          </div>
        </div>
      </body>
    </html>
  );
}
