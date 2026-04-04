import { Leaf } from 'lucide-react'

export function Header() {
  return (
    <header className="flex h-[63px] items-center rounded-[26px] border border-[#203445] bg-[linear-gradient(180deg,rgba(12,22,32,0.96),rgba(7,13,20,0.96))] px-6 shadow-[0_0_45px_rgba(0,0,0,0.35)] backdrop-blur-2xl">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-emerald-400/30 bg-emerald-400/10 shadow-[0_0_24px_rgba(52,211,153,0.35)]">
          <Leaf className="h-6 w-6 text-emerald-300" />
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[22px] font-semibold tracking-wide text-emerald-300">
            SAFI
          </span>

          <span className="text-slate-500">—</span>

          <span className="text-[14px] uppercase tracking-[0.22em] text-slate-200">
            SpectroAgro Fusion AI
          </span>
        </div>
      </div>
    </header>
  )
}
