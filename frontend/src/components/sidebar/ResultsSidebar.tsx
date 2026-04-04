import {
  AlertTriangle,
  Check,
  TriangleAlert,
} from 'lucide-react'
import { useSafiStore } from '../../store/useSafiStore'

export function ResultsSidebar() {
  const { prediction, error, isLoading } = useSafiStore()

  return (
    <aside className="flex h-full w-[430px] flex-col gap-3 overflow-y-auto pr-1">
      {error && (
        <div className="rounded-3xl border border-rose-500/30 bg-rose-500/10 p-5 text-rose-200">
          <div className="mb-2 flex items-center gap-3 text-sm font-semibold uppercase tracking-[0.2em]">
            <AlertTriangle className="h-5 w-5" />
            Error
          </div>

          <div>{error}</div>
        </div>
      )}

      {isLoading && (
        <div className="animate-pulse rounded-3xl border border-cyan-400/20 bg-[#0b141d] p-10 text-center text-cyan-300">
          Running SAFI Analysis...
        </div>
      )}

      {prediction && (
        <>
          <div className="rounded-3xl border border-[#223648] bg-[#0c141d] p-5">
            <div className="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
              Location Synopsis
            </div>

            <div className="text-sm text-slate-300">
              <div className="text-slate-500">Geographic</div>

              <div className="mt-1 font-mono text-lg text-slate-100">
                {prediction.metadata.requested_coordinates[0].toFixed(3)},{' '}
                {prediction.metadata.requested_coordinates[1].toFixed(3)}
              </div>
            </div>
          </div>

          <div className="rounded-3xl border border-[#223648] bg-[#0c141d] p-5">
            <div className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
              Land Suitability Index
            </div>

            <div className="space-y-4">
              {[
                ['Conservative', prediction.lsi.conservative],
                ['Expected', prediction.lsi.expected],
                ['Opportunity', prediction.lsi.opportunity],
              ].map(([label, value]) => (
                <div key={String(label)}>
                  <div className="mb-1 flex justify-between text-[11px] uppercase tracking-[0.16em] text-slate-500">
                    <span>{label}</span>
                    <span>{(Number(value) * 100).toFixed(1)}%</span>
                  </div>

                  <div className="h-3 overflow-hidden rounded-full bg-slate-800">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-cyan-400 to-emerald-400"
                      style={{ width: `${Number(value) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-[#223648] bg-[#0c141d] p-5">
            <div className="mb-4 text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
              Scientific Confidence
            </div>

            <div className="flex gap-1">
              {Array.from({ length: 8 }).map((_, i) => (
                <div
                  key={i}
                  className={`h-10 flex-1 rounded-md ${
                    i < Math.round(prediction.confidence.score * 8)
                      ? 'bg-cyan-300 shadow-[0_0_18px_rgba(34,211,238,0.8)]'
                      : 'bg-slate-800'
                  }`}
                />
              ))}
            </div>
          </div>

          <div className="rounded-3xl border border-[#223648] bg-[#0c141d] p-5">
            <div className="mb-3 text-sm font-semibold uppercase tracking-[0.18em] text-slate-300">
              Domain Validity Status
            </div>

            <div
              className={`flex items-center gap-3 rounded-2xl border px-4 py-3 ${
                prediction.domain.status === 'supported'
                  ? 'border-emerald-500/30 bg-emerald-500/10'
                  : prediction.domain.status === 'borderline'
                    ? 'border-amber-500/30 bg-amber-500/10'
                    : 'border-rose-500/30 bg-rose-500/10'
              }`}
            >
              {prediction.domain.status === 'supported' ? (
                <Check className="h-5 w-5 shrink-0 text-emerald-300" />
              ) : (
                <TriangleAlert className="h-5 w-5 shrink-0 text-amber-300" />
              )}

              <div className="min-w-0">
                <div className="mb-1 text-[10px] uppercase tracking-[0.18em] text-slate-500">
                  Status
                </div>

                <div className="text-sm font-medium uppercase tracking-[0.08em] text-slate-100">
                  {prediction.domain.status.replaceAll('_', ' ')}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </aside>
  )
}