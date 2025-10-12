"use client";

import { CalendarIcon, ClockIcon } from "lucide-react";
import { useState } from "react";
import { motion } from "motion/react";

interface PricingTabProps {
  onPeriodChange: (period: "month" | "year") => void;
}

export default function PricingTab({ onPeriodChange }: PricingTabProps) {
  const [activeTab, setActiveTab] = useState<"month" | "year">("month");

  const handleTabChange = (period: "month" | "year") => {
    setActiveTab(period);
    onPeriodChange(period);
  };

  return (
    <div className="flex justify-center mb-0.5">
      <div className="flex bg-gray-100 dark:bg-gray-800 rounded-full p-1 gap-1">
        <button
          type="button"
          onClick={() => handleTabChange("month")}
          className={`relative px-6 py-3 rounded-full flex items-center gap-2 transition-all duration-200 ${
            activeTab === "month"
              ? "text-black"
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-700"
          }`}
        >
          {activeTab === "month" && (
            <motion.div
              layoutId="activeTab"
              className="absolute inset-0 bg-primary rounded-full"
              transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            />
          )}
          <ClockIcon className="relative z-10" size={16} aria-hidden="true" />
          <span className="relative z-10 font-medium">Month</span>
        </button>
        <button
          type="button"
          onClick={() => handleTabChange("year")}
          className={`relative px-6 py-3 rounded-full flex items-center gap-2 transition-all duration-200 ${
            activeTab === "year"
              ? "text-black"
              : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-700"
          }`}
        >
          {activeTab === "year" && (
            <motion.div
              layoutId="activeTab"
              className="absolute inset-0 bg-primary rounded-full"
              transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
            />
          )}
          <CalendarIcon
            className="relative z-10"
            size={16}
            aria-hidden="true"
          />
          <span className="relative z-10 font-medium">Year</span>
        </button>
      </div>
    </div>
  );
}
