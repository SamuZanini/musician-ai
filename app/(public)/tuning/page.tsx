"use client";

import { Ripple } from "@/components/ui/ripple";

export default function Tuning() {
  return (
    <div className="relative h-screen w-full overflow-hidden flex items-center justify-center">
      <Ripple />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <span className="text-white text-2xl font-semibold">Listening...</span>
      </div>
    </div>
  );
}
