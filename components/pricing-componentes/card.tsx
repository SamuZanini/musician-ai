import { CometCard } from "@/components/ui/comet-card";
import { motion } from "framer-motion";

export function PricingCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 200 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.0 }}
      className="flex flex-col-3 items-center h-screen w-screen gap-10 justify-center"
    >
      <CometCard>
        <button
          type="button"
          className="my-10 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 bg-[#B87333] p-2 md:my-20 md:p-4"
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
                src="public\images\copper.png"
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
            <div className="text-xs text-black opacity-50">$5,00/month</div>
          </div>
        </button>
      </CometCard>
      <CometCard>
        <button
          type="button"
          className="my-10 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 bg-[#C0C0C0] p-2 md:my-20 md:p-4"
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
                src="public\images\silver.png"
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
            <div className="text-xs text-black opacity-50">$10,00/month</div>
          </div>
        </button>
      </CometCard>
      <CometCard>
        <button
          type="button"
          className="my-10 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 bg-[#FFD700] p-2 md:my-20 md:p-4"
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
                src="public\images\gold.png"
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
            <div className="text-xs text-black opacity-50">$15,00/month</div>
          </div>
        </button>
      </CometCard>
    </motion.div>
  );
}
