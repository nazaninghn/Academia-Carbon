'use client';

export type Locale = 'en' | 'tr';

const OPTIONS: { value: Locale; label: string; name: string }[] = [
  { value: 'en', label: 'EN', name: 'English' },
  { value: 'tr', label: 'TR', name: 'Türkçe' },
];

type Props = {
  value: Locale;
  onChange: (locale: Locale) => void;
};

/** Two-option segmented switch; the highlight slides to the active language. */
export default function LanguageToggle({ value, onChange }: Props) {
  const activeIndex = OPTIONS.findIndex((o) => o.value === value);

  return (
    <div
      role="group"
      aria-label="Language / Dil"
      className="relative inline-grid h-9 grid-cols-2 rounded-full bg-white/[0.04] p-1 ring-1 ring-inset ring-white/10"
    >
      <span
        aria-hidden
        className="absolute inset-y-1 left-1 w-[calc(50%-4px)] rounded-full bg-white/15 transition-transform duration-300 ease-out motion-reduce:transition-none"
        style={{ transform: `translateX(${activeIndex * 100}%)` }}
      />
      {OPTIONS.map((option) => {
        const active = option.value === value;
        return (
          <button
            key={option.value}
            type="button"
            lang={option.value}
            aria-pressed={active}
            title={option.name}
            onClick={() => onChange(option.value)}
            className={`relative z-10 w-10 rounded-full text-xs font-semibold tracking-wide transition-colors duration-200 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-300 ${
              active ? 'text-white' : 'text-white/50 hover:text-white/80'
            }`}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
