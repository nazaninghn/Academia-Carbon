import Link from 'next/link';
import type { ComponentPropsWithoutRef, ReactNode } from 'react';

type Variant = 'primary' | 'secondary' | 'ghost';
type Size = 'sm' | 'md' | 'lg';

type CommonProps = {
  variant?: Variant;
  size?: Size;
  /** Icon shown after the label; it nudges forward on hover. */
  icon?: ReactNode;
  /** Shows a spinner, disables the button and sets aria-busy. */
  loading?: boolean;
  className?: string;
  children: ReactNode;
};

type LinkButtonProps = CommonProps &
  Omit<ComponentPropsWithoutRef<typeof Link>, keyof CommonProps> & { href: string };
type NativeButtonProps = CommonProps &
  Omit<ComponentPropsWithoutRef<'button'>, keyof CommonProps> & { href?: undefined };

export type ButtonProps = LinkButtonProps | NativeButtonProps;

const base =
  'group relative isolate inline-flex select-none items-center justify-center gap-2 overflow-hidden ' +
  'rounded-full font-medium tracking-tight whitespace-nowrap ' +
  'transition-[background-color,color,box-shadow,transform] duration-200 ease-out ' +
  'active:scale-[0.97] motion-reduce:transition-none motion-reduce:active:scale-100 ' +
  'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-300 ' +
  'disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50';

const variants: Record<Variant, string> = {
  primary:
    'bg-emerald-400 text-emerald-950 shadow-[0_0_0_0_rgba(52,211,153,0)] ' +
    'hover:bg-emerald-300 hover:shadow-[0_8px_30px_-6px_rgba(52,211,153,0.55)]',
  secondary:
    'bg-white/[0.03] text-white ring-1 ring-inset ring-white/15 ' +
    'hover:bg-white/[0.07] hover:ring-white/30',
  ghost: 'text-white/70 hover:bg-white/[0.06] hover:text-white',
};

const sizes: Record<Size, string> = {
  sm: 'h-9 px-4 text-sm',
  md: 'h-11 px-5 text-sm',
  lg: 'h-12 px-6 text-[15px]',
};

function Spinner() {
  return (
    <span
      aria-hidden
      className="size-4 animate-spin rounded-full border-2 border-current border-r-transparent motion-reduce:animate-none"
    />
  );
}

export default function Button(props: ButtonProps) {
  const {
    variant = 'primary',
    size = 'md',
    icon,
    loading = false,
    className = '',
    children,
    ...rest
  } = props;

  const classes = `${base} ${variants[variant]} ${sizes[size]} ${className}`;

  const content = (
    <>
      {/* Light sweep across the primary button on hover */}
      {variant === 'primary' && (
        <span
          aria-hidden
          className="pointer-events-none absolute inset-0 -z-10 -translate-x-full bg-gradient-to-r from-transparent via-white/40 to-transparent transition-transform duration-700 ease-out group-hover:translate-x-full motion-reduce:hidden"
        />
      )}
      {loading && <Spinner />}
      <span>{children}</span>
      {icon && !loading && (
        <span
          aria-hidden
          className="-mr-1 inline-flex transition-transform duration-200 ease-out group-hover:translate-x-0.5 motion-reduce:transition-none"
        >
          {icon}
        </span>
      )}
    </>
  );

  if (typeof rest.href === 'string') {
    const linkProps = rest as Omit<LinkButtonProps, keyof CommonProps>;
    return (
      <Link
        {...linkProps}
        className={classes}
        aria-disabled={loading || undefined}
        aria-busy={loading || undefined}
      >
        {content}
      </Link>
    );
  }

  const { type = 'button', disabled, ...buttonProps } = rest as Omit<NativeButtonProps, keyof CommonProps>;
  return (
    <button
      {...buttonProps}
      type={type}
      disabled={disabled || loading}
      aria-busy={loading || undefined}
      className={classes}
    >
      {content}
    </button>
  );
}
