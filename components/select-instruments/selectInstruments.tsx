"use client";

import { useState } from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";

export function SelectAccordionDemo() {
  const [selectedInstrument, setSelectedInstrument] = useState("");

  const instrumentImages = {
    "item-1": "/images/intrumento-violino.png",
    "item-2": "/images/instrumento-flauta.png",
    "item-3": "/images/instrumento-trompete.png",
    "item-4": "/images/instrumento-piano.png",
    "item-5": "/images/instrumento-cello.png",
    "item-6": "/images/instrumento-violao.png",
  };

  const instrumentNames = {
    "item-1": "Violin",
    "item-2": "Flute",
    "item-3": "Trumpet",
    "item-4": "Piano",
    "item-5": "Cello",
    "item-6": "Guitar",
  };

  return (
    <div className="flex h-screen">
      {/* Accordion à esquerda */}
      <div className="w-1/2 flex items-center justify-center p-6">
        <div className="w-full max-w-md">
          <Accordion
            type="single"
            collapsible
            className="w-full"
            onValueChange={(value) => setSelectedInstrument(value || "")}
          >
            <AccordionItem value="item-1">
              <AccordionTrigger>Violin</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Although no one knows for sure, historians believe that the
                  very first violin was made by Andrea Amati in the 1500s. He
                  created at least 2 three-stringed violins in the 1540s and was
                  commissioned to create the first four-stringed violin by a
                  wealthy family, the Medici's, in the 1550s.
                </p>
                <p>
                  The word "violin" comes from the Latin word "vitula" which
                  means "calf" (a calf is a baby cow). It's fun to think that
                  the violin was named after cows, however, "vitula" has an
                  alternate meaning: stringed musical instrument (which is
                  probably more likely).
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-2">
              <AccordionTrigger>Flute</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Flute curiosities include its status as one of the world's
                  oldest instruments, with the oldest known example dating back
                  about 60,000 years, and its historical use of diverse
                  materials from animal bones and ivory to modern metals and
                  even gold.
                </p>
                <p>
                  The term "flute" was historically used for both modern
                  transverse (side-blown) flutes and vertically held recorders,
                  and a wide family of flutes exists, from the small piccolo to
                  the very large contrabass.
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-3">
              <AccordionTrigger>Trumpet</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  The trumpet is a very versatile instrument with a rich
                  history. It takes a significant place in many various music
                  genres – classical, jazz, rock, contemporary music. In
                  classical music, the trumpet often takes on majestic melodies,
                  enhancing a powerful quality of the compositions. In jazz, the
                  trumpet acts like a central instrument, allowing musicians
                  taking on stunning solos and contributing to the dynamic of
                  the genre.
                </p>
                <p>
                  The trumpet has evolved over many centuries; during this
                  period many various models have been developed to fit
                  different musical styles. Since this instrument has a lot to
                  discover, we have prepared ten interesting facts about the
                  trumpet:
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-4">
              <AccordionTrigger>Piano</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  Pianos are complex instruments with thousands of parts, a wide
                  range of tones, and a rich history, originally named
                  "pianoforte" for their ability to play both soft and loud.
                  They are technically both string and percussion instruments,
                  and their strings are under immense tension, capable of
                  lifting tons of weight.
                </p>
                <p>
                  In 1934, a leading British piano manufacturer wanted to
                  celebrate the 25 years of king George V being on the throne.
                  They accepted the challenge and built a massive piano. It
                  weighed 1270 kg and was 3.55m long! Yet this was only the
                  start of piano giants.
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-5">
              <AccordionTrigger>Cello</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  The cello is named after the Italian word "violoncello,"
                  meaning "little big viola," and its full name reflects its
                  historical relationship with the larger violone. Curious facts
                  include that it was once made with animal gut strings, early
                  cellos didn't have an endpin and were held between the legs,
                  and some modern versions are made of steel.
                </p>
                <p>
                  The cello is also known for its sound, which is considered to
                  be the closest to the human voice of any instrument, and it
                  has been adopted into many genres beyond classical music, such
                  as rock and pop
                </p>
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-6">
              <AccordionTrigger>Guitar</AccordionTrigger>
              <AccordionContent className="flex flex-col gap-4 text-balance">
                <p>
                  The English word 'guitar' was adopted from the Spanish
                  'guitarra' during the 17th century. In turn, 'guitarra' is
                  thought to have been altered from the Ancient Greek 'kithara'.
                  Kithara appears four times in the Bible and is generally
                  translated into English as 'harp'.
                </p>
                <p>
                  Historians believe that the oldest recorded guitar-like
                  musical instruments came from Ancient Egypt around 1450 BC.
                  This 3-stringed ancestor of the guitar was uncovered in the
                  Valley of Kings inside the tomb of Queen Hatshepsut.
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
                ? instrumentImages[
                    selectedInstrument as keyof typeof instrumentImages
                  ]
                : "/images/logo-png.png"
            }
            alt={
              selectedInstrument
                ? instrumentNames[
                    selectedInstrument as keyof typeof instrumentNames
                  ]
                : "Musician AI Logo"
            }
            className="max-w-full max-h-[50vh] object-contain rounded-lg shadow-lg transition-all duration-300 ease-in-out"
          />
        </div>
        {selectedInstrument && (
          <Button className="mt-4">Select Instrument</Button>
        )}
      </div>
    </div>
  );
}
