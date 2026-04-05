import Link from 'next/link';
import { ArrowRight, BrainCircuit, ChartNoAxesCombined, ShieldCheck, Sprout } from 'lucide-react';

import { SiteFooter } from '@/components/sections/site-footer';
import { HeroSection } from '@/components/ui/hero-section-5';
import { Button } from '@/components/ui/button';

const featureCards = [
  {
    title: 'AI diagnosis flow',
    description: 'Upload leaf imagery and review ranked disease predictions with a streamlined inspection UI.',
    image:
      'https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1200&q=80',
  },
  {
    title: 'Field-ready monitoring',
    description: 'Surface health signals fast enough for agronomists, farm operators, and greenhouse teams.',
    image:
      'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1200&q=80',
  },
  {
    title: 'Model-backed confidence',
    description: 'Pair predictions with confidence bars and disease library references for better decisions.',
    image:
      'https://images.unsplash.com/photo-1471193945509-9ad0617afabf?auto=format&fit=crop&w=1200&q=80',
  },
];

const pillars = [
  {
    icon: BrainCircuit,
    title: 'Inference that feels instant',
    description: 'A clean frontend that is ready to post images to your FastAPI endpoint and display ranked results.',
  },
  {
    icon: ChartNoAxesCombined,
    title: 'Confidence you can inspect',
    description: 'Progress bars, summary cards, and disease references make model output understandable instead of opaque.',
  },
  {
    icon: ShieldCheck,
    title: 'Built for production handoff',
    description: 'The project now has TypeScript, Tailwind, and shadcn-compatible structure for scalable UI work.',
  },
];

export default function HomePage() {
  return (
    <div className="min-h-screen">
      <HeroSection />

      <section className="mx-auto max-w-7xl px-6 py-24 lg:px-12">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-primary">
              Frontend Experience
            </p>
            <h2 className="mt-4 text-4xl tracking-tight md:text-5xl">
              A sharper product story for your plant disease platform.
            </h2>
          </div>
          <p className="max-w-xl text-muted-foreground">
            The old repo had model and API foundations but no real React app. This new
            frontend creates a cohesive experience around detection, disease education,
            and deployment readiness.
          </p>
        </div>

        <div className="mt-12 grid gap-6 lg:grid-cols-3">
          {featureCards.map((card) => (
            <article
              key={card.title}
              className="group overflow-hidden rounded-[2rem] border border-border/60 bg-white/90 shadow-xl shadow-lime-900/5"
            >
              <img
                src={card.image}
                alt={card.title}
                className="h-64 w-full object-cover transition duration-500 group-hover:scale-105"
              />
              <div className="p-6">
                <h3 className="text-2xl">{card.title}</h3>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">{card.description}</p>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 lg:px-12">
        <div className="rounded-[2.5rem] border border-border/60 bg-slate-950 p-8 text-white shadow-2xl shadow-lime-950/10 md:p-12">
          <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-lime-300/70">
                Why this frontend works
              </p>
              <h2 className="mt-4 text-4xl tracking-tight md:text-5xl">
                Designed for diagnosis, not just decoration.
              </h2>
              <p className="mt-4 max-w-xl text-sm leading-7 text-slate-300">
                The interface keeps the visual polish of the provided template, but shifts the
                content, actions, and layout around your actual product goals.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Button asChild size="lg" className="rounded-full">
                  <Link href="/analyze">
                    Open Analyzer
                    <ArrowRight className="ml-2 size-4" />
                  </Link>
                </Button>
                <Button asChild size="lg" variant="outline" className="rounded-full border-white/20 bg-transparent text-white hover:bg-white/10 hover:text-white">
                  <Link href="/about">Read Architecture</Link>
                </Button>
              </div>
            </div>
            <div className="grid gap-4">
              {pillars.map((item) => (
                <div key={item.title} className="rounded-[1.75rem] border border-white/10 bg-white/5 p-5">
                  <item.icon className="size-6 text-lime-300" />
                  <p className="mt-4 text-xl font-semibold">{item.title}</p>
                  <p className="mt-2 text-sm leading-6 text-slate-300">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 pb-24 lg:px-12">
        <div className="grid gap-6 rounded-[2.5rem] border border-border/60 bg-white/80 p-8 shadow-xl shadow-lime-900/5 lg:grid-cols-[0.9fr_1.1fr] lg:p-12">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-primary">
              Project readiness
            </p>
            <h2 className="mt-4 text-4xl tracking-tight md:text-5xl">
              Multi-page product structure for the full workflow.
            </h2>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {[
              'Landing page for product narrative and entry points',
              'Analyzer page for image uploads and model response',
              'Disease library page for supported classes and sample crops',
              'About page for stack, API, and deployment guidance',
            ].map((item) => (
              <div key={item} className="rounded-[1.5rem] bg-secondary/60 p-5 text-sm leading-6">
                <Sprout className="mb-3 size-5 text-primary" />
                {item}
              </div>
            ))}
          </div>
        </div>
      </section>

      <SiteFooter />
    </div>
  );
}
