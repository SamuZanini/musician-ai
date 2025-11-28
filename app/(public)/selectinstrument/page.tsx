"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import NavbarFinal from "@/components/navbar";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Ripple } from "@/components/ui/ripple";
import { useSidebar } from "@/components/ui/sidebar";
import appData from "../../../app-data.json";

type InstrumentJson = {
  id: string;
  name: string;
  type: string;
  description: string;
  faqContent?: { faq: Array<{ question: string; answer: string }> };
  imageUrl?: string;
  comoAfinar?: string;
  melhorTecnica?: string;
};

const INSTRUMENTS: InstrumentJson[] = (appData as any).instruments || [];

export default function SelectInstrument() {
  const router = useRouter();
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [selectedInstrument, setSelectedInstrument] = useState<string | null>(null);

  useEffect(() => {
    // On mount, load selection from localStorage.user if present
    const localUser = localStorage.getItem("user");
    if (localUser) {
      try {
        const userObj = JSON.parse(localUser);
        if (userObj && userObj.favoriteInstrumentId) {
          setSelectedInstrument(userObj.favoriteInstrumentId);
        }
      } catch (e) {
        // ignore parse errors
      }
    }
    setMounted(true);
  }, []);

  const handleConfirm = () => {
    if (selectedInstrument) {
      // Update localStorage.user with selected instrument
      const localUser = localStorage.getItem("user");
      let userObj: any = {};
      if (localUser) {
        try {
          userObj = JSON.parse(localUser);
        } catch (e) {
          userObj = {};
        }
      }
      userObj.favoriteInstrumentId = selectedInstrument;
      localStorage.setItem("user", JSON.stringify(userObj));
      router.push("/tuning");
    }
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full relative bg-black overflow-y-auto overflow-x-hidden">
      <NavbarFinal />

      <div className="fixed left-0 top-1/2 -translate-y-1/2 z-0">
        <Ripple />
      </div>

      <div className={`fixed inset-0 transition-all duration-300 ${
        open || openMobile ? "backdrop-blur-md bg-black/30 pointer-events-auto" : "pointer-events-none"
      }`} style={{ zIndex: 5 }} />

      <div className="relative z-10 pt-20 px-6 pb-20">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-5xl font-bold text-white mb-4">Selecione seu Instrumento</h1>
          <p className="text-gray-400 mb-12 text-lg">
            Escolha o instrumento que você deseja praticar e veja as dicas para começar.
          </p>

          {/* Instruments Grid */}
          <div className="grid grid-cols-2 gap-6 mb-12">
            {INSTRUMENTS.map((instrument) => (
              <Card
                key={instrument.id}
                className={`cursor-pointer transition-all duration-300 border overflow-hidden ${
                  selectedInstrument === instrument.id
                    ? "border-yellow-400 bg-gray-900/80 ring-2 ring-yellow-400"
                    : "border-gray-700 bg-gray-900/40 hover:bg-gray-900/60 hover:border-gray-600"
                }`}
                onClick={() => setSelectedInstrument(instrument.id)}
              >
                {/* Instrument Image */}
                <div className="w-full h-48 bg-gray-800 overflow-hidden">
                  {instrument.imageUrl ? (
                    <img
                      src={instrument.imageUrl}
                      alt={instrument.name}
                      className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                    />
                  ) : (
                    <div className="flex items-center justify-center h-full bg-gradient-to-br from-gray-700 to-gray-800">
                      <span className="text-5xl">🎵</span>
                    </div>
                  )}
                </div>

                {/* Instrument Info */}
                <div className="p-6">
                  <h2 className="text-2xl font-bold text-white mb-2">{instrument.name}</h2>
                  <p className="text-gray-400 text-sm mb-4">{instrument.description}</p>

                  {/* FAQ Accordion */}
                  <Accordion type="single" collapsible className="w-full">
                    {instrument.faqContent?.faq?.map((faq, idx) => (
                      <AccordionItem key={idx} value={`${instrument.id}-faq-${idx}`}>
                        <AccordionTrigger className="text-sm text-gray-300 hover:text-white py-2">
                          {faq.question}
                        </AccordionTrigger>
                        <AccordionContent className="text-gray-400 text-sm pb-3">
                          {faq.answer}
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>

                  {/* Selection Indicator */}
                  {selectedInstrument === instrument.id && (
                    <div className="mt-4 pt-4 border-t border-gray-700">
                      <span className="text-yellow-400 font-semibold">✓ Selecionado</span>
                    </div>
                  )}
                </div>
              </Card>
            ))}
          </div>

          {/* Confirm Button */}
          <div className="flex gap-4 justify-center">
            <Button
              variant="outline"
              size="lg"
              className="border-gray-600 text-gray-300 hover:bg-gray-800"
              onClick={() => router.back()}
            >
              Voltar
            </Button>
            <Button
              size="lg"
              className="bg-yellow-400 hover:bg-yellow-500 text-black font-semibold disabled:opacity-50"
              onClick={handleConfirm}
              disabled={!selectedInstrument}
            >
              Confirmar Instrumento
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
