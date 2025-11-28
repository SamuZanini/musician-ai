"use client";

import React, { useState, useEffect } from "react";
import NavbarFinal from "@/components/navbar";
import { useSidebar } from "@/components/ui/sidebar";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Ripple } from "@/components/ui/ripple";
import appData from "../../../app-data.json";

interface Composer {
  id: string;
  name: string;
  bio: string;
  image: string;
}

interface SheetMusic {
  id: string;
  title: string;
  composerId: string;
  difficulty: string;
  isPremium: boolean;
}

export default function MusicSheets() {
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [composers, setComposers] = useState<Composer[]>([]);
  const [sheetMusic, setSheetMusic] = useState<{ [key: string]: SheetMusic[] }>({});

  useEffect(() => {
    setMounted(true);
    
    // Buscar compositores e partituras do JSON
    const loadData = () => {
      // Buscar compositores do JSON
      const composersData = (appData as any).composers || [];
      const composersList: Composer[] = composersData.map((composer: any) => ({
        id: composer.id,
        name: composer.name,
        bio: composer.biography || "",
        image: composer.imageUrl || "/images/chopin.png",
      }));
      setComposers(composersList);

      // Buscar partituras do JSON
      const sheetMusicData = (appData as any).sheetMusic || [];
      const sheetMusicMap: { [key: string]: SheetMusic[] } = {};
      
      sheetMusicData.forEach((sheet: any) => {
        if (!sheetMusicMap[sheet.composerId]) {
          sheetMusicMap[sheet.composerId] = [];
        }
        
        // Mapear dificuldade do JSON para português
        const difficultyMap: { [key: string]: string } = {
          "beginner": "Iniciante",
          "intermediate": "Intermediário",
          "advanced": "Avançado",
        };
        
        sheetMusicMap[sheet.composerId].push({
          id: sheet.id,
          title: sheet.title,
          composerId: sheet.composerId,
          difficulty: difficultyMap[sheet.difficulty] || sheet.difficulty,
          isPremium: sheet.isPremium || false,
        });
      });
      
      setSheetMusic(sheetMusicMap);
    };

    loadData();
  }, []);

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
        <div className="max-w-7xl mx-auto">
          <h1 className="text-5xl font-bold text-white mb-4">Partituras Musicais</h1>
          <p className="text-gray-400 mb-12">Explore partituras de grandes compositores</p>

          {/* Composers Accordion */}
          <Accordion type="single" collapsible className="w-full space-y-3">
            {composers.map((composer) => (
              <Card key={composer.id} className="border-gray-700 bg-gray-900/40 overflow-hidden">
                <AccordionItem value={composer.id} className="border-0">
                  <AccordionTrigger className="px-6 py-4 hover:bg-gray-900/60 transition-colors">
                    <div className="flex items-center gap-4 text-left w-full">
                      <img
                        src={composer.image}
                        alt={composer.name}
                        className="w-16 h-16 rounded-full object-cover"
                      />
                      <div>
                        <h3 className="text-xl font-bold text-white">{composer.name}</h3>
                        <p className="text-gray-400 text-sm">{composer.bio}</p>
                      </div>
                    </div>
                  </AccordionTrigger>

                  <AccordionContent className="px-6 py-4 bg-gray-900/20 border-t border-gray-700">
                    <div className="space-y-3">
                      {sheetMusic[composer.id]?.map((sheet) => (
                        <Card key={sheet.id} className="border-gray-600 bg-gray-800/40 p-4 hover:bg-gray-800/60 transition-colors">
                          <div className="flex justify-between items-start">
                            <div>
                              <h4 className="text-white font-semibold text-lg">{sheet.title}</h4>
                              <p className="text-gray-400 text-sm mt-1">Dificuldade: {sheet.difficulty}</p>
                            </div>
                            <div className="flex gap-2">
                              {sheet.isPremium && (
                                <span className="bg-yellow-500/20 text-yellow-400 text-xs px-3 py-1 rounded-full">Premium</span>
                              )}
                              <Button className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold">
                                Ver Partitura
                              </Button>
                            </div>
                          </div>
                        </Card>
                      ))}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Card>
            ))}
          </Accordion>
        </div>
      </div>
    </div>
  );
}
