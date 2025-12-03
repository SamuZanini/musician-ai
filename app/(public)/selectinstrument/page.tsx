"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import NavbarFinal from "@/components/navbar";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import appData from "../../../app-data.json";

interface Instrument {
  id: string;
  name: string;
  type: string;
  description: string;
  imageUrl: string;
}

export default function SelectInstrument() {
  const router = useRouter();
  const [instruments, setInstruments] = useState<Instrument[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const instrumentsList = (appData as any).instruments || [];
    setInstruments(instrumentsList);

    // Verificar se o usuário já tem um instrumento favorito selecionado
    const localUser = localStorage.getItem("user");
    if (localUser) {
      try {
        const userObj = JSON.parse(localUser);
        if (userObj?.favoriteInstrumentId) {
          setSelectedId(userObj.favoriteInstrumentId);
        }
      } catch (e) {
        console.warn("Erro ao parsear usuário:", e);
      }
    }
  }, []);

  const handleSelectInstrument = async (instrumentId: string) => {
    setSelectedId(instrumentId);

    // Atualizar no localStorage
    const localUser = localStorage.getItem("user");
    if (localUser) {
      try {
        const userObj = JSON.parse(localUser);
        userObj.favoriteInstrumentId = instrumentId;
        localStorage.setItem("user", JSON.stringify(userObj));

        // Atualizar no JSON
        const users = (appData as any).users || [];
        const userIndex = users.findIndex((u: any) => u.id === userObj.id);
        if (userIndex !== -1) {
          users[userIndex].favoriteInstrumentId = instrumentId;
          // Fazer uma chamada API para salvar no backend
          try {
            await fetch("/api/save-app-data", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ appData }),
            });
          } catch (e) {
            console.warn("Erro ao salvar no backend:", e);
          }
        }
      } catch (e) {
        console.error("Erro ao atualizar instrumento:", e);
      }
    }
  };

  const handleConfirm = () => {
    if (selectedId) {
      router.push("/practice");
    }
  };

  if (!mounted) return null;

  return (
    <div className="min-h-screen w-full bg-black">
      <NavbarFinal />

      <div className="pt-20 px-6 pb-20">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-5xl font-bold text-white mb-4">Selecione seu Instrumento</h1>
          <p className="text-gray-400 mb-12 text-lg">Escolha o instrumento que deseja praticar</p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {instruments.map((instrument) => (
              <Card
                key={instrument.id}
                className={`cursor-pointer border-2 transition-all ${
                  selectedId === instrument.id
                    ? "border-yellow-400 bg-gray-900/80"
                    : "border-gray-700 bg-gray-900/60 hover:border-gray-600"
                }`}
                onClick={() => handleSelectInstrument(instrument.id)}
              >
                <div className="p-6">
                  {instrument.imageUrl && (
                    <img
                      src={instrument.imageUrl}
                      alt={instrument.name}
                      className="w-full h-48 object-cover rounded-lg mb-4"
                    />
                  )}

                  <h2 className="text-2xl font-bold text-white mb-2">{instrument.name}</h2>
                  <p className="text-gray-400 text-sm mb-4">{instrument.type.toUpperCase()}</p>
                  <p className="text-gray-300 text-sm">{instrument.description}</p>

                  {selectedId === instrument.id && (
                    <div className="mt-4 pt-4 border-t border-gray-700">
                      <span className="text-yellow-400 font-semibold">✓ Selecionado</span>
                    </div>
                  )}
                </div>
              </Card>
            ))}
          </div>

          <div className="flex gap-4 justify-center">
            <Button
              onClick={() => router.push("/home")}
              variant="outline"
              className="border-gray-600 text-gray-300 hover:bg-gray-800 px-8 py-6 text-lg"
            >
              Voltar
            </Button>
            <Button
              onClick={handleConfirm}
              disabled={!selectedId}
              className="bg-yellow-400 hover:bg-yellow-500 text-black font-bold px-8 py-6 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Confirmar Seleção
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
