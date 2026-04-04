// SoilPropertyAnalytics.tsx

import { useSafiStore } from '../../store/useSafiStore'

function PropertyRow({
  label,
  value,
}: {
  label: string
  value: { mean: number; lower: number; upper: number }
}) {
  const center =
    ((value.mean - value.lower) / (value.upper - value.lower || 1)) * 100

  return (
    <div className="rounded-2xl border border-[#223648] bg-[#0e1721]/95 p-4">
      <div className="mb-3 flex items-center justify-between">
        <div>
          <div className="text-sm font-semibold text-slate-100">{label}</div>
          <div className="text-[10px] uppercase tracking-[0.15em] text-slate-500">
            90% Prediction Interval
          </div>
        </div>

        <div className="text-right">
          <div className="text-xl font-bold text-cyan-300">
            {value.mean.toFixed(2)}
          </div>
          <div className="text-[10px] text-slate-500">
            {value.lower.toFixed(2)} – {value.upper.toFixed(2)}
          </div>
        </div>
      </div>

      <div className="relative h-10 overflow-hidden rounded-xl bg-[#081018]">
        <div className="absolute left-4 right-4 top-1/2 h-[2px] -translate-y-1/2 rounded-full bg-cyan-400/20" />

        <div
          className="absolute top-1/2 h-7 w-[3px] -translate-y-1/2 rounded-full bg-cyan-300 shadow-[0_0_18px_rgba(34,211,238,0.9)]"
          style={{ left: `calc(${center}% - 2px)` }}
        />
      </div>
    </div>
  )
}

export function SoilPropertyAnalytics() {
  const prediction = useSafiStore((state) => state.prediction)

  if (!prediction) return null

  return (
    <div className="mt-2 rounded-[28px] border border-[#223446] bg-[linear-gradient(180deg,rgba(12,18,26,0.97),rgba(7,12,18,0.97))] p-3 shadow-[0_0_50px_rgba(0,0,0,0.45)]">
      <div className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
        Soil Property Analytics
      </div>

      <div className="grid grid-cols-5 gap-3">
        <PropertyRow
          label="CECPH7"
          value={prediction.predictions.lab__CECPH7}
        />
        <PropertyRow
          label="TOTC"
          value={prediction.predictions.lab__TOTC}
        />
        <PropertyRow
          label="ORGC"
          value={prediction.predictions.lab__ORGC}
        />
        <PropertyRow
          label="ORGM"
          value={prediction.predictions.lab__ORGM}
        />
        <PropertyRow
          label="BDFIOD"
          value={prediction.predictions.lab__BDFIOD}
        />
      </div>
    </div>
  )
}