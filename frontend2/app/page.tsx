'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Globe2, ArrowRight, BarChart3, ShieldCheck, Zap, Sparkles } from 'lucide-react';

export default function Page() {
  const [locale, setLocale] = useState<'en' | 'tr'>('en');

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
          <Link href="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl overflow-hidden shadow-lg bg-emerald-500 flex items-center justify-center">
              <img 
                src="/logo.png" 
                alt="Academia Carbon Logo" 
                className="w-full h-full object-contain"
                onError={(e) => {
                  e.currentTarget.style.display = 'none';
                  e.currentTarget.parentElement!.innerHTML = '<div class="text-black font-bold text-xs">AC</div>';
                }}
              />
            </div>
          </Link>
          <div className="flex items-center gap-4">
            <button
              onClick={() => setLocale(locale === 'en' ? 'tr' : 'en')}
              className="px-3 py-1 rounded-lg bg-white/10 hover:bg-white/20 transition flex gap-2 items-center text-sm"
            >
              <Globe2 size={16} />
              {locale.toUpperCase()}
            </button>

            <Link
              href="/auth/login"
              className="px-4 py-2 text-sm hover:text-emerald-400"
            >
              {t.login}
            </Link>

            <Link
              href="/auth/login"
              className="px-5 py-2 bg-emerald-500 hover:bg-emerald-400 rounded-xl font-semibold text-black"
            >
              {t.getStarted}
            </Link>
          </div>
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
          <div className="flex gap-4 mt-8">
            <Link
              href="/auth/login"
              className="px-6 py-3 bg-emerald-500 hover:bg-emerald-400 rounded-xl font-semibold text-black flex items-center gap-2"
            >
              {t.cta}
              <ArrowRight size={18} />
            </Link>

            <Link
              href="/auth/login"
              className="px-6 py-3 border border-white/20 hover:border-white/40 rounded-xl"
            >
              {t.secondary}
            </Link>
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