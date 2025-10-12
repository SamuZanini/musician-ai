"use client";

import { CometCard } from "@/components/ui/comet-card";
import { motion } from "framer-motion";
import TextComponent from "@/components/text-rotate/text-rotate-componente";
import { ScrollArea } from "@/components/ui/scroll-area";
import PricingTab from "@/components/tab/tab-price";
import { useState } from "react";

export function PricingCard() {
  const [period, setPeriod] = useState<"month" | "year">("month");

  const prices = {
    month: {
      copper: 5,
      silver: 10,
      gold: 15,
    },
    year: {
      copper: 45,
      silver: 65,
      gold: 75,
    },
  };

  const currentPrices = prices[period];
  const periodText = period === "month" ? "month" : "year";

  return (
    <ScrollArea className="h-screen w-full">
      <div className="flex flex-col items-center min-h-screen w-full">
        <motion.div
          initial={{ opacity: 0, y: 200 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.0 }}
        >
          <TextComponent />
          <div className="mt-8">
            <PricingTab onPeriodChange={setPeriod} />
          </div>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 200 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.0 }}
          className="flex flex-col lg:flex-row items-center gap-6 justify-center flex-1 px-4 py-8"
        >
          <CometCard>
            <button
              type="button"
              className="my-4 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 bg-[#B87333] p-2 md:my-8 md:p-4"
              aria-label="View invite F7RA"
              style={{
                transformStyle: "preserve-3d",
                transform: "none",
                opacity: 1,
              }}
            >
              <div className="mx-2 flex-1">
                <div className="relative mt-2 aspect-[3/4] w-full">
                  <img
                    loading="lazy"
                    className="absolute inset-0 h-full w-full rounded-[16px] bg-[#000000] object-cover contrast-75"
                    alt="Copper"
                    src="/images/copper.png"
                    style={{
                      boxShadow: "rgba(0, 0, 0, 0.05) 0px 5px 6px 0px",
                      opacity: 1,
                    }}
                  />
                </div>
              </div>
              <div className="mt-2 flex flex-shrink-0 items-center justify-between p-4 font-mono text-black">
                <div className="text-xs">
                  <h1>Copper</h1>
                </div>
                <div className="text-xs text-black opacity-50">
                  ${currentPrices.copper},00/{periodText}
                </div>
              </div>
            </button>
          </CometCard>
          <CometCard>
            <button
              type="button"
              className="my-4 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 bg-[#C0C0C0] p-2 md:my-8 md:p-4"
              aria-label="View invite F7RA"
              style={{
                transformStyle: "preserve-3d",
                transform: "none",
                opacity: 1,
              }}
            >
              <div className="mx-2 flex-1">
                <div className="relative mt-2 aspect-[3/4] w-full">
                  <img
                    loading="lazy"
                    className="absolute inset-0 h-full w-full rounded-[16px] bg-[#000000] object-cover contrast-75"
                    alt="Silver"
                    src="/images/silver.png"
                    style={{
                      boxShadow: "rgba(0, 0, 0, 0.05) 0px 5px 6px 0px",
                      opacity: 1,
                    }}
                  />
                </div>
              </div>
              <div className="mt-2 flex flex-shrink-0 items-center justify-between p-4 font-mono text-black">
                <div className="text-xs">
                  <h1>Silver</h1>
                </div>
                <div className="text-xs text-black opacity-50">
                  ${currentPrices.silver},00/{periodText}
                </div>
              </div>
            </button>
          </CometCard>
          <CometCard>
            <button
              type="button"
              className="my-4 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 bg-[#FFD700] p-2 md:my-8 md:p-4"
              aria-label="View invite F7RA"
              style={{
                transformStyle: "preserve-3d",
                transform: "none",
                opacity: 1,
              }}
            >
              <div className="mx-2 flex-1">
                <div className="relative mt-2 aspect-[3/4] w-full">
                  <img
                    loading="lazy"
                    className="absolute inset-0 h-full w-full rounded-[16px] bg-[#000000] object-cover contrast-75"
                    alt="Gold"
                    src="/images/gold.png"
                    style={{
                      boxShadow: "rgba(0, 0, 0, 0.05) 0px 5px 6px 0px",
                      opacity: 1,
                    }}
                  />
                </div>
              </div>
              <div className="mt-2 flex flex-shrink-0 items-center justify-between p-4 font-mono text-black">
                <div className="text-xs">
                  <h1>Gold</h1>
                </div>
                <div className="text-xs text-black opacity-50">
                  ${currentPrices.gold},00/{periodText}
                </div>
              </div>
            </button>
          </CometCard>
        </motion.div>
      </div>
    </ScrollArea>
  );
}
