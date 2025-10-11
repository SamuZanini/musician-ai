"use client";

import { useState } from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { motion } from "motion/react";

export function MusicSheetSelectAccordion() {
  const [selectedInstrument, setSelectedInstrument] = useState("");
  const [openItem, setOpenItem] = useState<string>("");

  const artistsPictures = {
    "item-1": "/images/chopin.png",
    "item-2": "/images/bach.png",
    "item-3": "/images/beethoven.jpg",
    "item-4": "/images/paganini.jpg",
    "item-5": "/images/vivaldi.jpg",
    "item-6": "/images/dmitri.jpg",
  };

  const musicSheets = {
    "item-1": "/images/nocturne.jpg",
    "item-2": "/images/cellosuite.jpg",
    "item-3": "/images/sonata.png",
    "item-4": "/images/caprice24.png",
    "item-5": "/images/summer.png",
    "item-6": "/images/waltz2.png",
  };

  const artistsNames = {
    "item-1": "Frédéric Chopin",
    "item-2": "Johann Sebastian Bach",
    "item-3": "Ludwig van Beethoven",
    "item-4": "Niccolò Paganini",
    "item-5": "Antonio Vivaldi",
    "item-6": "Dmitri Shostakovitch",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 200 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1.0 }}
      className="flex h-screen"
    >
      {/* Accordion à esquerda */}
      <div className="w-1/2 flex items-center justify-center p-6">
        <div className="w-full max-w-md">
          <Accordion
            type="single"
            collapsible
            className="w-full"
            onValueChange={(value) => {
              setSelectedInstrument(value || "");
              setOpenItem(value || "");
            }}
          >
            <AccordionItem value="item-1">
              <AccordionTrigger className="flex items-center gap-3">
                <Avatar
                  className={`transition-all duration-300 ${
                    openItem === "item-1" ? "h-12 w-12" : "h-8 w-8"
                  }`}
                >
                  <AvatarImage
                    src={artistsPictures["item-1"]}
                    alt="Frédéric Chopin"
                    className="object-cover"
                  />
                  <AvatarFallback>FC</AvatarFallback>
                </Avatar>
                <span>Frédéric Chopin</span>
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Frédéric François Chopin (born Fryderyk Franciszek Chopin; 1
                  March 1810 – 17 October 1849) was a Polish composer and
                  virtuoso pianist of the Romantic period who wrote primarily
                  for solo piano. He has maintained worldwide renown as a
                  leading composer of his era whose "poetic genius was based on
                  a professional technique that was without equal in his
                  generation".
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-2">
              <AccordionTrigger className="flex items-center gap-3">
                <Avatar
                  className={`transition-all duration-300 ${
                    openItem === "item-2" ? "h-12 w-12" : "h-8 w-8"
                  }`}
                >
                  <AvatarImage
                    src={artistsPictures["item-2"]}
                    alt="Johann Sebastian Bach"
                    className="object-cover"
                  />
                  <AvatarFallback>JSB</AvatarFallback>
                </Avatar>
                <span>Johann Sebastian Bach</span>
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Johann Sebastian Bach (31 March [O.S. 21 March] 1685 – 28 July
                  1750) was a German composer and musician of the late Baroque
                  period. He is known for his prolific output across a variety
                  of instruments and forms, including the orchestral Brandenburg
                  Concertos; solo instrumental works such as the cello suites
                  and sonatas and partitas for solo violin; keyboard works such
                  as the Goldberg Variations and The Well-Tempered Clavier;
                  organ works such as the Schübler Chorales and the Toccata and
                  Fugue in D minor; and choral works such as the St Matthew
                  Passion and the Mass in B minor. Since the 19th-century Bach
                  Revival, he has been widely regarded as one of the greatest
                  composers in the history of Western music.
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-3">
              <AccordionTrigger className="flex items-center gap-3">
                <Avatar
                  className={`transition-all duration-300 ${
                    openItem === "item-3" ? "h-12 w-12" : "h-8 w-8"
                  }`}
                >
                  <AvatarImage
                    src={artistsPictures["item-3"]}
                    alt="Ludwig van Beethoven"
                    className="object-cover"
                  />
                  <AvatarFallback>LvB</AvatarFallback>
                </Avatar>
                <span>Ludwig van Beethoven</span>
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Ludwig van Beethoven (baptised 17 December 1770 – 26 March
                  1827) was a German composer and pianist. One of the most
                  revered figures in the history of Western music, his works
                  rank among the most performed of the classical music
                  repertoire and span the transition from the Classical period
                  to the Romantic era. Beethoven's early period, during which he
                  forged his craft, is typically considered to have lasted until
                  1802. From 1802 to around 1812, his middle period showed an
                  individual development from the styles of Joseph Haydn and
                  Wolfgang Amadeus Mozart, and is sometimes characterised as
                  heroic. During this time, Beethoven began to grow increasingly
                  deaf. In his late period, from 1812 to 1827, he extended his
                  innovations in musical form and expression.
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-4">
              <AccordionTrigger className="flex items-center gap-3">
                <Avatar
                  className={`transition-all duration-300 ${
                    openItem === "item-4" ? "h-12 w-12" : "h-8 w-8"
                  }`}
                >
                  <AvatarImage
                    src={artistsPictures["item-4"]}
                    alt="Niccolò Paganini"
                    className="object-cover"
                  />
                  <AvatarFallback>NP</AvatarFallback>
                </Avatar>
                <span>Niccolò Paganini</span>
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Niccolò (or Nicolò) Paganini (/pæɡəˈniːni, pɑːɡə-/; Italian:
                  [ni(k)koˈlɔ ppaɡaˈniːni] ⓘ; 27 October 1782 – 27 May 1840) was
                  an Italian violinist and composer. He was the most celebrated
                  violin virtuoso of his time, and left his mark as one of the
                  pillars of modern violin technique. His 24 Caprices for Solo
                  Violin Op. 1 are among the best known of his compositions and
                  have served as an inspiration for many prominent composers.
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-5">
              <AccordionTrigger className="flex items-center gap-3">
                <Avatar
                  className={`transition-all duration-300 ${
                    openItem === "item-5" ? "h-12 w-12" : "h-8 w-8"
                  }`}
                >
                  <AvatarImage
                    src={artistsPictures["item-5"]}
                    alt="Antonio Vivaldi"
                    className="object-cover"
                  />
                  <AvatarFallback>AV</AvatarFallback>
                </Avatar>
                <span>Antonio Vivaldi</span>
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Antonio Lucio Vivaldi (4 March 1678 – 28 July 1741) was an
                  Italian composer, virtuoso violinist, impresario of Baroque
                  music and Roman Catholic priest. Regarded as one of the
                  greatest Baroque composers, Vivaldi's influence during his
                  lifetime was widespread across Europe, giving origin to many
                  imitators and admirers. He pioneered many developments in
                  orchestration, violin technique and programmatic music. He
                  consolidated the emerging concerto form, especially the solo
                  concerto, into a widely accepted and followed idiom.
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-6">
              <AccordionTrigger className="flex items-center gap-3">
                <Avatar
                  className={`transition-all duration-300 ${
                    openItem === "item-6" ? "h-12 w-12" : "h-8 w-8"
                  }`}
                >
                  <AvatarImage
                    src={artistsPictures["item-6"]}
                    alt="Dmitri Shostakovitch"
                    className="object-cover"
                  />
                  <AvatarFallback>DS</AvatarFallback>
                </Avatar>
                <span>Dmitri Shostakovitch</span>
              </AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Dmitri Dmitriyevich Shostakovich (25 September [O.S. 12
                  September] 1906 – 9 August 1975) was a Soviet-era Russian
                  composer and pianist who became internationally known after
                  the premiere of his First Symphony in 1926 and thereafter was
                  regarded as a major composer.
                </p>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>

      {/* Linha separadora vertical */}
      <div className="w-px bg-gray-300 h-3/4 self-center"></div>

      {/* Área das imagens à direita */}
      <div className="w-1/2 p-6 flex flex-col items-center justify-center gap-6">
        <div className="relative">
          <img
            src={
              selectedInstrument
                ? musicSheets[selectedInstrument as keyof typeof musicSheets]
                : "/images/logo-png.png"
            }
            alt={
              selectedInstrument
                ? artistsNames[selectedInstrument as keyof typeof artistsNames]
                : "Musician AI Logo"
            }
            className="max-w-full max-h-[70vh] object-contain rounded-lg shadow-lg transition-all duration-300 ease-in-out"
          />
        </div>
      </div>
    </motion.div>
  );
}
