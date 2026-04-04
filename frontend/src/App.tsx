import { Header } from './components/shared/Header'
import { MapView } from './components/map/MapView'
import { ResultsSidebar } from './components/sidebar/ResultsSidebar'
import { SoilPropertyAnalytics } from './components/sidebar/SoilPropertyAnalytics'

export default function App() {
  return (
    <div className="h-screen overflow-hidden bg-[#03070c] text-slate-100">
      <div className="flex h-full flex-col gap-2 p-2">
        <Header />

        <main className="flex min-h-0 flex-1 gap-2 items-stretch">
          <section className="flex min-w-0 flex-1 flex-col gap-2">
            <div className="min-h-0 flex-[6] overflow-hidden rounded-[28px] border border-[#223446] bg-[#050b12] shadow-[0_0_80px_rgba(0,0,0,0.55)]">
              <MapView />
            </div>

            <div className="min-h-0 flex-[4]">
              <SoilPropertyAnalytics />
            </div>
          </section>

          <ResultsSidebar />
        </main>
      </div>
    </div>
  )
}