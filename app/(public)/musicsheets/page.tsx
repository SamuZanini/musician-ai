"use client";

import React, { useState, useEffect } from "react";
import NavbarFinal from "@/components/navbar";
import { useSidebar } from "@/components/ui/sidebar";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Ripple } from "@/components/ui/ripple";
import { X } from "lucide-react";
import appData from "../../../app-data.json";

// Mapa de URLs de partituras reais de obras clássicas
const SHEET_IMAGE_MAP: { [key: string]: string } = {
  "nocturne-001": "https://musescore.com/static/musescore/scoredata/g/370d640b4d2cb88f8c509871cc353d6e52fcb006/score_0.svg?no-cache=1715699512",
  "prelude-001": "https://cdn.hoffmanacademy.com/product/638/images/1j4I0UE08uAGMmZaotAaCSQjr8UtxwEhxdi84ypv.jpg?width=1500&height=1500",
  "moonlight-001": "https://musescore.com/static/musescore/scoredata/g/7cf4e6a7f40abfcf4902d39772c3360a47c8bf4d/score_0.svg?no-cache=1744851136",
  "caprice-001": "https://musescore.com/static/musescore/scoredata/g/d8413e5d788a0421d7d9570630f75f1c918d7446/score_0.svg?no-cache=1715693890",
  "four-seasons-001": "https://image.slidesharecdn.com/violino-partitura-vivaldi-asquatroestaes-primaverafourseasons-violinoepiano-120807201906-phpapp02/75/Violino-partitura-vivaldi-as-quatro-estacoes-primavera-four-seasons-violino-e-piano-6-2048.jpg",
  "waltz-001": "https://i.etsystatic.com/38581300/r/il/4bda03/4371260631/il_fullxfull.4371260631_e076.jpg",
  "ballade-001": "https://musescore.com/static/musescore/scoredata/g/d5e64262c556276f81c6c72dc121224c106b278c/score_0.svg?no-cache=1715688287",
  "fugue-001": "https://musescore.com/static/musescore/scoredata/g/fee711ab7f4ae2011c4ce50d6ea116888a1a91e6/score_0.svg?no-cache=1715694364",
  "invention-001": "https://i.etsystatic.com/40439475/r/il/cefc29/5423342651/il_fullxfull.5423342651_ep5f.jpg",
  "pathetique-001": "https://musescore.com/static/musescore/scoredata/g/5fe052b40aa39e164cc993079707c42efcdc634c/score_0.svg?no-cache=1715687199",
  "fur-elise-001": "https://musescore.com/static/musescore/scoredata/g/7c367716ea7e9fad53ef1de034c13e5c21111b86/score_0.svg?no-cache=1715687036",
  "caprice-005": "https://musescore.com/static/musescore/scoredata/g/5124289070404126174dc6b0b3b49a96fb05f567/score_0.svg?no-cache=1715702501",
  "spring-001": "https://image.slidesharecdn.com/violino-partitura-vivaldi-asquatroestaes-primaverafourseasons-violinoepiano-120807201906-phpapp02/75/Violino-partitura-vivaldi-as-quatro-estacoes-primavera-four-seasons-violino-e-piano-4-2048.jpg",
  "winter-001": "https://content.tomplay.com/preview/2017/08/Vivaldi_WinterII_EasyIntermediate_Piano-Partitioncompl%C3%83%C2%A8te.png",
};

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
  imageUrl?: string;
  description?: string;
}

export default function MusicSheets() {
  const { open, openMobile } = useSidebar();
  const [mounted, setMounted] = useState(false);
  const [composers, setComposers] = useState<Composer[]>([]);
  const [sheetMusic, setSheetMusic] = useState<{ [key: string]: SheetMusic[] }>({});
  const [selectedSheet, setSelectedSheet] = useState<SheetMusic | null>(null);
  const [sheetImageUrl, setSheetImageUrl] = useState<string>("");

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
          imageUrl: sheet.imageUrl,
          description: sheet.description,
        });
      });
      
      setSheetMusic(sheetMusicMap);
    };

    loadData();
  }, []);

  const handleViewSheet = (sheet: SheetMusic) => {
    setSelectedSheet(sheet);
    setSheetImageUrl(SHEET_IMAGE_MAP[sheet.id] || "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=1200&fit=crop");
  };

  const closeModal = () => {
    setSelectedSheet(null);
    setSheetImageUrl("");
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
                    <div className="space-y-4">
                      {sheetMusic[composer.id]?.map((sheet) => {
                        const sheetImage = sheet.imageUrl || "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=600&fit=crop";
                        
                        return (
                          <Card key={sheet.id} className="border-gray-600 bg-gray-800/40 overflow-hidden hover:bg-gray-800/60 transition-colors">
                            <div className="flex gap-4 p-4">
                              {/* Imagem da partitura */}
                              <div className="flex-shrink-0">
                                <img
                                  src={sheetImage}
                                  alt={sheet.title}
                                  className="w-32 h-48 object-cover rounded-lg border border-gray-700 shadow-lg"
                                  onError={(e) => {
                                    // Fallback para imagem padrão se a URL falhar
                                    (e.target as HTMLImageElement).src = "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=600&fit=crop";
                                  }}
                                />
                              </div>
                              
                              {/* Informações da partitura */}
                              <div className="flex-1 flex flex-col justify-between">
                                <div>
                                  <h4 className="text-white font-semibold text-lg mb-2">{sheet.title}</h4>
                                  <p className="text-gray-400 text-sm mb-1">
                                    Dificuldade: <span className={`font-semibold ${
                                      sheet.difficulty === "Iniciante" ? "text-green-400" :
                                      sheet.difficulty === "Intermediário" ? "text-yellow-400" :
                                      "text-red-400"
                                    }`}>{sheet.difficulty}</span>
                                  </p>
                                  {sheet.description && (
                                    <p className="text-gray-500 text-xs mt-2">{sheet.description}</p>
                                  )}
                                </div>
                                
                                <div className="flex items-center justify-between mt-4">
                                  <div className="flex gap-2">
                                    {sheet.isPremium && (
                                      <span className="bg-yellow-500/20 text-yellow-400 text-xs px-3 py-1 rounded-full border border-yellow-500/30">
                                        Premium
                                      </span>
                                    )}
                                  </div>
                                  <Button 
                                    onClick={() => handleViewSheet(sheet)}
                                    className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold"
                                  >
                                    Ver Partitura
                                  </Button>
                                </div>
                              </div>
                            </div>
                          </Card>
                        );
                      })}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Card>
            ))}
          </Accordion>
        </div>
      </div>

      {/* Modal da Partitura */}
      {selectedSheet && (
        <div 
          className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4 backdrop-blur-sm"
          onClick={closeModal}
        >
          <div 
            className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-auto relative border border-gray-700 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header do Modal */}
            <div className="sticky top-0 bg-gray-800/95 border-b border-gray-700 px-6 py-4 flex justify-between items-center">
              <div>
                <h2 className="text-2xl font-bold text-white">{selectedSheet.title}</h2>
                <p className="text-gray-400 text-sm mt-1">
                  Dificuldade: <span className={`font-semibold ${
                    selectedSheet.difficulty === "Iniciante" ? "text-green-400" :
                    selectedSheet.difficulty === "Intermediário" ? "text-yellow-400" :
                    "text-red-400"
                  }`}>{selectedSheet.difficulty}</span>
                </p>
              </div>
              <button
                onClick={closeModal}
                className="text-gray-400 hover:text-white transition-colors p-2"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Conteúdo da Partitura */}
            <div className="p-6 flex flex-col items-center gap-4">
              <img
                src={sheetImageUrl}
                alt={selectedSheet.title}
                className="w-full max-w-2xl rounded-lg border border-gray-600 shadow-xl"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=1200&fit=crop";
                }}
              />
              
              <p className="text-gray-400 text-sm mt-4 text-center max-w-2xl">
                {selectedSheet.description || "Partitura musical"}
              </p>

              <Button
                onClick={closeModal}
                className="mt-4 bg-gray-700 hover:bg-gray-600 text-white px-8 py-3"
              >
                Fechar
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
