"use client";

import { useState, useEffect } from "react";
import NavbarFinal from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  Clock,
  TrendingUp,
  Trophy,
  Star,
  Music,
  User,
  Mail,
  Lock,
  Settings,
  Pencil,
} from "lucide-react";
import { CometCard } from "@/components/ui/comet-card";

type TabType = "my-signature" | "profile-picture" | "email" | "password";

export default function Profile() {
  const [activeTab, setActiveTab] = useState<TabType>("profile-picture");
  const [selectedInstrument, setSelectedInstrument] = useState("item-1"); // Violin por padrão
  const [selectedPlan, setSelectedPlan] = useState<{
    plan: "copper" | "silver" | "gold";
    period: "month" | "year";
    price: number;
    periodText: string;
  } | null>(null);
  const [userName, setUserName] = useState("Fulano");
  const [isEditingName, setIsEditingName] = useState(false);
  const [tempName, setTempName] = useState("Fulano");

  // Carregar instrumento selecionado do localStorage
  useEffect(() => {
    const savedInstrument = localStorage.getItem("selectedInstrument");
    if (savedInstrument) {
      setSelectedInstrument(savedInstrument);
    }

    // Carregar plano selecionado do localStorage
    const savedPlan = localStorage.getItem("selectedPlan");
    if (savedPlan) {
      setSelectedPlan(JSON.parse(savedPlan));
    }

    // Carregar nome do usuário do localStorage
    const savedName = localStorage.getItem("userName");
    if (savedName) {
      setUserName(savedName);
      setTempName(savedName);
    }
  }, []);

  // Funções para editar nome
  const handleEditName = () => {
    setIsEditingName(true);
    setTempName(userName);
  };

  const handleSaveName = () => {
    setUserName(tempName);
    localStorage.setItem("userName", tempName);
    setIsEditingName(false);
  };

  const handleCancelEdit = () => {
    setTempName(userName);
    setIsEditingName(false);
  };

  const instrumentImages = {
    "item-1": "/images/violin-star.jpg", // Violin
    "item-2": "/images/flute-star.jpg", // Flute
    "item-3": "/images/trumpet-star.jpg", // Trumpet
    "item-4": "/images/piano-star.jpg", // Piano
    "item-5": "/images/cello-star.jpg", // Cello
    "item-6": "/images/guitar-star.jpg", // Guitar
  };

  const instrumentNames = {
    "item-1": "Violin",
    "item-2": "Flute",
    "item-3": "Trumpet",
    "item-4": "Piano",
    "item-5": "Cello",
    "item-6": "Guitar",
  };

  const menuItems = [
    { id: "my-signature", label: "My Signature", icon: Music },
    { id: "profile-picture", label: "Profile", icon: User },
    { id: "email", label: "E-mail", icon: Mail },
    { id: "password", label: "Password", icon: Lock },
  ];

  // Função para renderizar card dinâmico
  const renderPlanCard = () => {
    if (!selectedPlan) {
      // Plano padrão se nenhum foi selecionado
      return (
        <CometCard>
          <button
            type="button"
            className="my-4 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 bg-[#FFD700] p-2 md:my-8 md:p-4"
            aria-label="View Gold Plan"
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
              <div className="text-xs text-black opacity-50">$15,00/month</div>
            </div>
          </button>
        </CometCard>
      );
    }

    const planConfig = {
      copper: { bg: "#B87333", img: "/images/copper.png", name: "Copper" },
      silver: { bg: "#C0C0C0", img: "/images/silver.png", name: "Silver" },
      gold: { bg: "#FFD700", img: "/images/gold.png", name: "Gold" },
    };

    const config = planConfig[selectedPlan.plan as keyof typeof planConfig];

    return (
      <CometCard>
        <button
          type="button"
          className="my-4 flex w-80 cursor-pointer flex-col items-stretch rounded-[16px] border-0 p-2 md:my-8 md:p-4"
          style={{
            backgroundColor: config.bg,
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
                alt={config.name}
                src={config.img}
                style={{
                  boxShadow: "rgba(0, 0, 0, 0.05) 0px 5px 6px 0px",
                  opacity: 1,
                }}
              />
            </div>
          </div>
          <div className="mt-2 flex flex-shrink-0 items-center justify-between p-4 font-mono text-black">
            <div className="text-xs">
              <h1>{config.name}</h1>
            </div>
            <div className="text-xs text-black opacity-50">
              ${selectedPlan.price},00/{selectedPlan.periodText}
            </div>
          </div>
        </button>
      </CometCard>
    );
  };

  const renderContent = () => {
    switch (activeTab) {
      case "my-signature":
        return (
          <div className="flex w-full h-full items-center">
            {/* Perfil à esquerda */}
            <div className="w-1/3 flex flex-col items-center justify-center">
              <div className="w-100 h-100 rounded-full bg-muted mb-4 flex items-center justify-center overflow-hidden">
                <img
                  src="/images/profile.jpg"
                  alt="Profile"
                  className="w-full h-full object-cover"
                />
              </div>
              <h2 className="text-2xl font-bold text-foreground">{userName}</h2>
            </div>

            {/* Card da Assinatura */}
            <div className="flex-1 flex flex-col items-center justify-center gap-6">
              {renderPlanCard()}

              {/* Botões de Ação */}
              <div className="flex gap-4">
                <Button className="bg-primary text-primary-foreground hover:bg-primary/90 px-6">
                  Extend
                </Button>
                <Button
                  variant="outline"
                  className="border-border text-foreground hover:bg-muted px-6"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </div>
        );

      case "profile-picture":
        return (
          <div className="flex w-full h-full items-center">
            {/* Perfil à esquerda */}
            <div className="w-1/3 flex flex-col items-center justify-center">
              <div className="w-100 h-100 rounded-full bg-muted mb-4 flex items-center justify-center overflow-hidden">
                <img
                  src="/images/profile.jpg"
                  alt="Profile"
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Nome editável */}
              <div className="flex flex-col items-center gap-2">
                {isEditingName ? (
                  <div className="flex flex-col items-center gap-2">
                    <Input
                      value={tempName}
                      onChange={(e) => setTempName(e.target.value)}
                      className="text-center text-2xl font-bold bg-input border-border text-foreground"
                      autoFocus
                    />
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        onClick={handleSaveName}
                        className="bg-primary text-primary-foreground hover:bg-primary/90"
                      >
                        Save
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={handleCancelEdit}
                        className="border-border text-foreground hover:bg-muted"
                      >
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <h2 className="text-2xl font-bold text-foreground">
                      {userName}
                    </h2>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={handleEditName}
                      className="text-muted-foreground hover:text-foreground"
                    >
                      <Pencil className="w-4 h-4" />
                    </Button>
                  </div>
                )}
              </div>
            </div>

            {/* Bento Grid de Estatísticas */}
            <div className="flex-1 p-8">
              <div className="grid grid-cols-2 gap-4 mb-4">
                {/* Tempo de Prática */}
                <Card className="bg-card p-6">
                  <div className="flex flex-col items-center text-center">
                    <Clock className="w-8 h-8 text-muted-foreground mb-2" />
                    <div className="text-3xl font-bold text-card-foreground">
                      100
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Practice time
                    </div>
                  </div>
                </Card>

                {/* Streak de Dias */}
                <Card className="bg-card p-6">
                  <div className="flex flex-col items-center text-center">
                    <TrendingUp className="w-8 h-8 text-muted-foreground mb-2" />
                    <div className="text-3xl font-bold text-card-foreground">
                      100
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Day Streak
                    </div>
                  </div>
                </Card>

                {/* Divisão */}
                <Card className="bg-card p-6">
                  <div className="flex flex-col items-center text-center">
                    <Trophy className="w-8 h-8 text-muted-foreground mb-2" />
                    <div className="text-3xl font-bold text-card-foreground">
                      100
                    </div>
                    <div className="text-sm text-muted-foreground">
                      Division
                    </div>
                  </div>
                </Card>

                {/* Estrelas */}
                <Card className="bg-card p-6">
                  <div className="flex flex-col items-center text-center">
                    <Star className="w-8 h-8 text-muted-foreground mb-2" />
                    <div className="text-3xl font-bold text-card-foreground">
                      100
                    </div>
                    <div className="text-sm text-muted-foreground">Stars</div>
                  </div>
                </Card>
              </div>

              {/* Instrumento Preferido */}
              <Card className="bg-card p-6">
                <div className="flex flex-col space-y-4">
                  <div className="text-center">
                    <div className="text-sm text-muted-foreground">
                      Favorite Instrument:
                    </div>
                    <div className="text-xl font-bold text-card-foreground">
                      {
                        instrumentNames[
                          selectedInstrument as keyof typeof instrumentNames
                        ]
                      }
                    </div>
                  </div>
                  <div className="w-full h-32 rounded-lg overflow-hidden">
                    <img
                      src={
                        instrumentImages[
                          selectedInstrument as keyof typeof instrumentImages
                        ]
                      }
                      alt={
                        instrumentNames[
                          selectedInstrument as keyof typeof instrumentNames
                        ]
                      }
                      className="w-full h-full object-cover"
                    />
                  </div>
                </div>
              </Card>
            </div>
          </div>
        );

      case "email":
        return (
          <div className="flex h-full">
            <div className="flex flex-col items-center justify-center w-1/3">
              <div className="w-100 h-100 rounded-full bg-muted mb-4 flex items-center justify-center overflow-hidden">
                <img
                  src="/images/profile.jpg"
                  alt="Profile"
                  className="w-full h-full object-cover"
                />
              </div>
              <h2 className="text-2xl font-bold text-foreground">{userName}</h2>
            </div>
            <div className="flex-1 flex flex-col justify-center px-8">
              <div className="space-y-6">
                <div>
                  <label
                    htmlFor="current-email"
                    className="text-foreground text-sm mb-2 block"
                  >
                    Current e-mail
                  </label>
                  <Input
                    id="current-email"
                    type="email"
                    value="teste@teste.com.br"
                    className="bg-input border-border text-foreground"
                    readOnly
                  />
                </div>
                <div>
                  <label
                    htmlFor="new-email"
                    className="text-foreground text-sm mb-2 block"
                  >
                    New e-mail
                  </label>
                  <Input
                    id="new-email"
                    type="email"
                    placeholder="teste@teste.com.br"
                    className="bg-input border-border text-foreground"
                  />
                </div>
                <div>
                  <label
                    htmlFor="confirm-email"
                    className="text-foreground text-sm mb-2 block"
                  >
                    Confirm new e-mail
                  </label>
                  <Input
                    id="confirm-email"
                    type="email"
                    placeholder="teste@teste.com.br"
                    className="bg-input border-border text-foreground"
                  />
                </div>
                <div className="flex gap-4">
                  <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                    Cancel
                  </Button>
                  <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                    Confirm
                  </Button>
                </div>
              </div>
            </div>
          </div>
        );

      case "password":
        return (
          <div className="flex h-full">
            <div className="flex flex-col items-center justify-center w-1/3">
              <div className="w-100 h-100 rounded-full bg-muted mb-4 flex items-center justify-center overflow-hidden">
                <img
                  src="/images/profile.jpg"
                  alt="Profile"
                  className="w-full h-full object-cover"
                />
              </div>
              <h2 className="text-2xl font-bold text-foreground">{userName}</h2>
            </div>
            <div className="flex-1 flex flex-col justify-center px-8">
              <div className="space-y-6">
                <div>
                  <label
                    htmlFor="current-password"
                    className="text-foreground text-sm mb-2 block"
                  >
                    Current Password
                  </label>
                  <Input
                    id="current-password"
                    type="password"
                    value="************"
                    className="bg-input border-border text-foreground"
                    readOnly
                  />
                </div>
                <div>
                  <label
                    htmlFor="new-password"
                    className="text-foreground text-sm mb-2 block"
                  >
                    New Password
                  </label>
                  <Input
                    id="new-password"
                    type="password"
                    placeholder="************"
                    className="bg-input border-border text-foreground"
                  />
                </div>
                <div>
                  <label
                    htmlFor="confirm-password"
                    className="text-foreground text-sm mb-2 block"
                  >
                    Confirm new Password
                  </label>
                  <Input
                    id="confirm-password"
                    type="password"
                    placeholder="************"
                    className="bg-input border-border text-foreground"
                  />
                </div>
                <div className="flex gap-4">
                  <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                    Cancel
                  </Button>
                  <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                    Confirm
                  </Button>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-background">
        <NavbarFinal />

        <div className="flex h-screen pt-16">
          {/* Conteúdo Principal */}
          <div className="flex-1 flex pr-20">
            {/* Conteúdo de todas as abas */}
            <div className="flex-1">{renderContent()}</div>
          </div>

          {/* Menu Lateral Fixo */}
          <div className="fixed right-4 top-1/2 transform -translate-y-1/2 z-50">
            <div className="bg-primary/10 backdrop-blur-sm border border-border rounded-2xl shadow-lg w-16">
              <div className="p-3">
                {/* Botão de Configurações */}
                <div className="mb-3">
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="w-10 h-10 rounded-full bg-background/80 hover:bg-background text-foreground border border-border"
                      >
                        <Settings className="w-5 h-5" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent side="left">
                      <p>Settings</p>
                    </TooltipContent>
                  </Tooltip>
                </div>

                {/* Itens do Menu */}
                <div className="space-y-2">
                  {menuItems.map((item) => {
                    const Icon = item.icon;
                    return (
                      <Tooltip key={item.id}>
                        <TooltipTrigger asChild>
                          <Button
                            variant="ghost"
                            onClick={() => setActiveTab(item.id as TabType)}
                            className={`w-10 h-10 rounded-full text-foreground hover:bg-background/80 border border-border ${
                              activeTab === item.id
                                ? "bg-background/80"
                                : "bg-transparent"
                            }`}
                          >
                            <Icon className="w-5 h-5" />
                          </Button>
                        </TooltipTrigger>
                        <TooltipContent side="left">
                          <p>{item.label}</p>
                        </TooltipContent>
                      </Tooltip>
                    );
                  })}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </TooltipProvider>
  );
}
