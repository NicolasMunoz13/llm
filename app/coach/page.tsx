import type { Metadata } from "next";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { CoachEmbed } from "@/components/CoachEmbed";
import { Eyebrow } from "@/components/ui";
import { coach } from "@/lib/content";

export const metadata: Metadata = {
  title: "Coach IA · FORGED",
  description:
    "Habla con el Coach IA de FORGED: técnica, programación y nutrición fundamentadas en el conocimiento de la marca. 24/7, sin excusas.",
};

export default function CoachPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-6xl px-6 py-16">
        <Eyebrow>{coach.eyebrow}</Eyebrow>
        <h1 className="mt-3 text-4xl font-bold uppercase sm:text-6xl">{coach.title}</h1>
        <p className="mt-4 max-w-2xl text-lg text-muted">{coach.body}</p>

        <div className="mt-10">
          <CoachEmbed height={720} />
        </div>

        <p className="mt-6 text-sm text-muted">
          El Coach usa RAG sobre el conocimiento de FORGED y cita sus fuentes. No sustituye
          consejo médico. Si algo duele de verdad, ve al médico, no al foro.
        </p>
      </main>
      <Footer />
    </>
  );
}
