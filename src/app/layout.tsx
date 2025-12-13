import type { Metadata } from "next";
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
  title: "MCOP Framework 2.0 | Meta-Cognitive Optimization Protocol",
  description: "Advanced framework for cognitive enhancement and system optimization with crystalline entropy state (0.07), perfect confidence calibration, and dialectical synthesis.",
  keywords: ["MCOP", "cognitive optimization", "meta-cognitive", "framework", "Next.js"],
  authors: [{ name: "KullAI Labs" }],
  openGraph: {
    title: "MCOP Framework 2.0",
    description: "Meta-Cognitive Optimization Protocol - Advanced framework for cognitive enhancement",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
