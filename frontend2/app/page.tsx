'use client';

import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight, BarChart3, ShieldCheck, Zap, Sparkles } from 'lucide-react';
import Button from './components/Button';
import LanguageToggle, { type Locale } from './components/LanguageToggle';

export default function Page() {
  const [locale, setLocale] = useState<Locale>('en');

  useEffect(() => {
    document.documentElement.lang = locale;
  }, [locale]);

  const text = {
    en: {
      login: 'Log In',
      getStarted: 'Get Started',
      badge: 'Carbon Platform v2.0',
      heroTitle: 'Carbon Intelligence for Modern Organizations',
      heroSubtitle: 'Track emissions, generate reports, and achieve sustainability goals with precision.',
      cta: 'Start Free Trial',
      secondary: 'View Demo',
      totalEmissions: 'Total Emissions',
      monthlyChange: '↓ 18% this month',
      features: [
        { title: 'Real-Time Analytics', body: 'Instant emission calculations and dynamic dashboards.' },
        { title: 'Secure Infrastructure', body: 'Enterprise-grade encryption and access control.' },
        { title: 'Automation Engine', body: 'Automate reporting and emission tracking workflows.' },
      ],
    },
    tr: {
      login: 'Giriş Yap',
      getStarted: 'Hemen Başlayın',
      badge: 'Karbon Platformu v2.0',
      heroTitle: 'Modern Kurumlar için Karbon Zekâsı',
      heroSubtitle: 'Emisyonlarınızı takip edin, raporlar oluşturun ve sürdürülebilirlik hedeflerinize hassasiyetle ulaşın.',
      cta: 'Ücretsiz Denemeye Başlayın',
      secondary: 'Demoyu Görüntüle',
      totalEmissions: 'Toplam Emisyon',
      monthlyChange: '↓ Bu ay %18',
      features: [
        { title: 'Gerçek Zamanlı Analitik', body: 'Anında emisyon hesaplamaları ve dinamik kontrol panelleri.' },
        { title: 'Güvenli Altyapı', body: 'Kurumsal düzeyde şifreleme ve erişim kontrolü.' },
        { title: 'Otomasyon Motoru', body: 'Raporlama ve emisyon takibi iş akışlarını otomatikleştirin.' },
      ],
    },
  };

  const t = text[locale];

  return (
    <div className="relative min-h-screen bg-[#030712] text-white overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute w-[600px] h-[600px] bg-emerald-500/30 blur-[120px] rounded-full top-[-200px] left-[-200px]" />
        <div className="absolute w-[600px] h-[600px] bg-cyan-500/30 blur-[120px] rounded-full bottom-[-200px] right-[-200px]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.1),transparent_70%)]" />
      </div>

      {/* NAVBAR */}
      <header className="border-b border-white/10 backdrop-blur-xl bg-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link
            href="/"
            aria-label="Academia Carbon"
            className="group flex items-center gap-3 rounded-full focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-emerald-300"
          >
            <span className="grid size-10 place-items-center rounded-full bg-white p-1 shadow-[0_0_0_1px_rgba(255,255,255,0.1),0_6px_20px_-6px_rgba(52,211,153,0.5)] transition-transform duration-500 ease-out group-hover:rotate-[20deg] motion-reduce:transition-none">
              <Image src="/logo.png" alt="" width={32} height={32} priority className="size-8" />
            </span>
            <span className="hidden text-[15px] font-semibold tracking-tight text-white sm:block">
              Academia Carbon
            </span>
          </Link>
          <nav className="flex items-center gap-2 sm:gap-3">
            <LanguageToggle value={locale} onChange={setLocale} />

            <span className="hidden sm:contents">
              <Button href="/auth/login" variant="ghost" size="sm">
                {t.login}
              </Button>
            </span>

            <Button href="/auth/login" size="sm">
              {t.getStarted}
            </Button>
          </nav>
        </div>
      </header>

      {/* HERO */}
      <section className="max-w-7xl mx-auto px-6 pt-24 pb-32 grid md:grid-cols-2 gap-16 items-center">
        <div>
          <div className="inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1 rounded-full mb-6 text-sm text-emerald-400">
            <Sparkles size={14} />
            {t.badge}
          </div>
          <h1 className="text-5xl md:text-6xl font-bold leading-tight">
            {t.heroTitle}
          </h1>
          <p className="text-white/70 mt-6 text-lg max-w-xl">
            {t.heroSubtitle}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button href="/auth/login" size="lg" icon={<ArrowRight size={18} />}>
              {t.cta}
            </Button>

            <Button href="/auth/login" variant="secondary" size="lg">
              {t.secondary}
            </Button>
          </div>
        </div>
        {/* Floating card */}
        <div className="relative">
          <div className="bg-white/5 backdrop-blur-xl border border-white/10 p-6 rounded-2xl shadow-2xl">
            <div className="text-sm text-white/60 mb-2">
              {t.totalEmissions}
            </div>
            <div className="text-4xl font-bold text-emerald-400">
              {locale === 'tr' ? '1.248' : '1,248'} tCO₂e
            </div>
            <div className="text-sm text-white/50 mt-2">
              {t.monthlyChange}
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="max-w-7xl mx-auto px-6 pb-32">
        <div className="grid md:grid-cols-3 gap-8">
          {[BarChart3, ShieldCheck, Zap].map((Icon, i) => (
            <div
              key={t.features[i].title}
              className="bg-white/5 border border-white/10 backdrop-blur-xl rounded-2xl p-6 hover:border-emerald-400/40 transition group"
            >
              <Icon className="text-emerald-400 mb-4 group-hover:scale-110 transition" />
              <h3 className="font-semibold text-lg mb-2">
                {t.features[i].title}
              </h3>
              <p className="text-white/60">
                {t.features[i].body}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}