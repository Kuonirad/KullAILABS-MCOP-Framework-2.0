"use client";

import { useState, useEffect } from "react";

interface CopyableCodeProps {
  children: string;
}

export function CopyableCode({ children }: CopyableCodeProps) {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (copied) {
      const timeout = setTimeout(() => setCopied(false), 2000);
      return () => clearTimeout(timeout);
    }
  }, [copied]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(children);
      setCopied(true);
    } catch (err) {
      console.error("Failed to copy!", err);
    }
  };

  return (
    <button
      onClick={handleCopy}
      className={`
        bg-black/[.05] dark:bg-white/[.06] font-mono font-semibold px-1 py-0.5 rounded cursor-pointer
        hover:bg-black/[.1] dark:hover:bg-white/[.1] transition-colors
        focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-foreground
        relative inline-block
      `}
      title="Click to copy"
      aria-label={copied ? "Copied code" : `Copy code: ${children}`}
      type="button"
    >
      {children}
      {copied && (
        <span
          className="absolute -top-8 left-1/2 -translate-x-1/2 bg-foreground text-background text-xs px-2 py-1 rounded shadow-sm whitespace-nowrap animate-in fade-in zoom-in duration-200"
          role="status"
          aria-live="polite"
        >
          Copied!
        </span>
      )}
    </button>
  );
}
