"use client";

import { Ripple } from "@/components/ui/ripple";
import { motion } from "motion/react";

export default function Tuning() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 200 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.0 }}
      className="relative h-screen w-full overflow-hidden flex items-center justify-center"
    >
      <Ripple />
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <span className="text-white text-2xl font-semibold">Listening...</span>
      </div>
    </motion.div>
  );
}
