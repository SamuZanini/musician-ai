"use client";

import React, { useState, useEffect } from "react";
import NavbarFinal from "@/components/navbar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import { Check } from "lucide-react";
import appData from "../../../app-data.json";

type PricingPlanFromJson = {
  id: string;
  name: string;
  monthlyPrice: number;
  yearlyPrice: number;
  features: string[];
};

// Map JSON plans to UI plans with styling preserved
const colorMap: Record<string, { color: string; textColor: string; buttonClass: string; highlighted?: boolean }> = {
  copper: {
    color: "bg-orange-600",
    textColor: "text-black",
    buttonClass: "bg-gray-700 hover:bg-gray-600 text-white",
  },
  silver: {
    color: "bg-gray-400",
    textColor: "text-black",
    buttonClass: "bg-white hover:bg-gray-100 text-black border border-gray-300",
  },
  gold: {
    color: "bg-yellow-400",
    textColor: "text-black",
    buttonClass: "bg-gray-900 hover:bg-gray-800 text-white",
    highlighted: true,
  },
};

const PRICING_PLANS: Array<PricingPlanFromJson & { color: string; textColor: string; buttonClass: string; highlighted?: boolean }> =
  (appData && (appData as any).pricingPlans ? (appData as any).pricingPlans : []).map((p: any) => ({
    ...p,
    ...(colorMap[p.id] || { color: "bg-gray-800", textColor: "text-white", buttonClass: "bg-gray-700 text-white" }),
  }));

export default function Pricing() {
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [isYearly, setIsYearly] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full relative bg-black">
      <NavbarFinal />

      <div
        className={`fixed inset-0 transition-all duration-300 ${
          open || openMobile
            ? "backdrop-blur-md bg-black/30 pointer-events-auto"
            : "pointer-events-none"
        }`}
        style={{ zIndex: 5 }}
      />

      <div className="relative z-10 min-h-screen overflow-y-auto overflow-x-hidden pt-20 px-6 pb-20">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-5xl font-bold text-white mb-6">
              Escolha seu plano
            </h1>
            <p className="text-gray-400 text-xl mb-8">
              Encontre o plano perfeito para seus objetivos musicais
            </p>

            {/* Toggle Monthly/Yearly */}
            <div className="flex items-center justify-center gap-4">
              <button
                onClick={() => setIsYearly(false)}
                className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                  !isYearly
                    ? "bg-white text-black"
                    : "bg-gray-800 text-gray-400 hover:text-white"
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setIsYearly(true)}
                className={`px-6 py-2 rounded-lg font-semibold transition-all ${
                  isYearly
                    ? "bg-white text-black"
                    : "bg-gray-800 text-gray-400 hover:text-white"
                }`}
              >
                Yearly
              </button>
            </div>

            {isYearly && (
              <p className="text-yellow-400 text-sm mt-4">
                ✓ Economize 17% com plano anual!
              </p>
            )}
          </div>

          {/* Pricing Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            {PRICING_PLANS.map((plan) => (
              <Card
                key={plan.id}
                className={`overflow-hidden transition-transform duration-300 hover:scale-105 ${
                  plan.highlighted ? "md:scale-105" : ""
                } ${plan.color} ${plan.textColor}`}
              >
                <div className="p-8">
                  {/* Plan Name */}
                  <h3 className="text-3xl font-bold mb-4">{plan.name}</h3>

                  {/* Price */}
                  <div className="mb-8">
                    <span className="text-4xl font-bold">
                      ${isYearly ? plan.yearlyPrice : plan.monthlyPrice}
                    </span>
                    <span className="text-lg ml-2">
                      /{isYearly ? "year" : "mo"}
                    </span>
                  </div>

                  {/* Features */}
                  <ul className="space-y-3 mb-8">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-start gap-3">
                        <Check className="w-5 h-5 flex-shrink-0 mt-0.5" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>

                  {/* Button */}
                  <Button
                    className={`w-full py-6 font-bold text-lg rounded-lg ${plan.buttonClass}`}
                  >
                    {plan.highlighted ? "Get Started Now" : "Choose Plan"}
                  </Button>
                </div>
              </Card>
            ))}
          </div>

          {/* FAQ Section */}
          <div className="max-w-2xl mx-auto mt-16">
            <h2 className="text-3xl font-bold text-white mb-8 text-center">
              Dúvidas frequentes
            </h2>
            <div className="space-y-4">
              <div className="bg-gray-900/60 rounded-lg p-6 border border-gray-700">
                <h3 className="text-white font-semibold mb-2">
                  Posso trocar de plano a qualquer momento?
                </h3>
                <p className="text-gray-400">
                  Sim, você pode fazer upgrade ou downgrade de plano a qualquer
                  momento. As mudanças entrarão em vigor no próximo período de
                  cobrança.
                </p>
              </div>
              <div className="bg-gray-900/60 rounded-lg p-6 border border-gray-700">
                <h3 className="text-white font-semibold mb-2">
                  Há período de teste gratuito?
                </h3>
                <p className="text-gray-400">
                  Oferecemos 7 dias de teste gratuito para todos os planos. Não
                  é necessário adicionar cartão de crédito.
                </p>
              </div>
              <div className="bg-gray-900/60 rounded-lg p-6 border border-gray-700">
                <h3 className="text-white font-semibold mb-2">
                  Como funciona o cancelamento?
                </h3>
                <p className="text-gray-400">
                  Você pode cancelar a qualquer momento sem penalidades. O
                  acesso continuará até o final do período pago.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
