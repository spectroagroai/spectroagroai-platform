import type { Map as LeafletMap } from 'leaflet'
import { Search } from 'lucide-react'
import { useState } from 'react'
import { useSafiStore } from '../../store/useSafiStore'

type Props = {
  map: LeafletMap
}

export function MapSearchOverlay({ map }: Props) {
  const selectCoordinate = useSafiStore((state) => state.selectCoordinate)

  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSearch() {
    const value = query.trim()

    if (!value) return

    const coordinateMatch = value.match(
      /^(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)$/,
    )

    if (coordinateMatch) {
      const lat = parseFloat(coordinateMatch[1])
      const lon = parseFloat(coordinateMatch[3])

      map.flyTo([lat, lon], 7, {
        duration: 1.4,
      })

      await selectCoordinate(lat, lon)
      return
    }

    try {
      setLoading(true)

      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&limit=1&q=${encodeURIComponent(value)}`,
      )

      const data = await response.json()

      if (!data.length) return

      const lat = parseFloat(data[0].lat)
      const lon = parseFloat(data[0].lon)

      map.flyTo([lat, lon], 6, {
        duration: 1.4,
      })

      await selectCoordinate(lat, lon)
    } catch (error) {
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="absolute left-1/2 top-5 z-[1000] w-[min(420px,calc(100%-140px))] -translate-x-1/2">
      <div className="flex items-center gap-3 rounded-2xl border border-[#29445a] bg-[#0d1721]/92 px-4 py-3 shadow-[0_10px_35px_rgba(0,0,0,0.45)] backdrop-blur-2xl">
        <Search className="h-4 w-4 shrink-0 text-slate-500" />

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSearch()
            }
          }}
          placeholder="Search coordinates, city, country..."
          className="w-full bg-transparent text-sm text-slate-200 outline-none placeholder:text-slate-500"
        />

        {loading && (
          <div className="h-4 w-4 rounded-full border-2 border-cyan-400/30 border-t-cyan-300 animate-spin" />
        )}
      </div>
    </div>
  )
}