import { useState } from 'react'
import { MapSearchOverlay } from './MapSearchOverlay'
import L from 'leaflet'
import { Minus, Plus } from 'lucide-react'
import {
  MapContainer,
  Marker,
  TileLayer,
  useMap,
  useMapEvents,
} from 'react-leaflet'
import type { Map as LeafletMap } from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useSafiStore } from '../../store/useSafiStore'

const crosshairIcon = new L.DivIcon({
  className: 'border-0 bg-transparent',
  html: `
    <div class="relative flex h-20 w-20 items-center justify-center">
      <div class="absolute h-16 w-16 rounded-full border border-cyan-300/20 animate-ping"></div>
      <div class="absolute h-10 w-10 rounded-full border border-cyan-300/70"></div>
      <div class="absolute h-[2px] w-16 bg-cyan-200/70"></div>
      <div class="absolute h-16 w-[2px] bg-cyan-200/70"></div>
      <div class="absolute h-4 w-4 rounded-full border border-cyan-100 bg-cyan-300/20 shadow-[0_0_20px_rgba(34,211,238,0.9)]"></div>
    </div>
  `,
  iconSize: [80, 80],
  iconAnchor: [40, 40],
})

function ClickHandler() {
  const selectCoordinate = useSafiStore((state) => state.selectCoordinate)

  useMapEvents({
    click(event) {
      selectCoordinate(event.latlng.lat, event.latlng.lng)
    },
  })

  return null
}

function MapControls() {
  const map = useMap()

  return (
    <div className="absolute left-5 top-5 z-[700] flex flex-col gap-3">
      <button
        onClick={() => map.zoomIn()}
        className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#2b4355] bg-[#0d1721]/95 text-slate-300"
      >
        <Plus className="h-5 w-5" />
      </button>

      <button
        onClick={() => map.zoomOut()}
        className="flex h-12 w-12 items-center justify-center rounded-2xl border border-[#2b4355] bg-[#0d1721]/95 text-slate-300"
      >
        <Minus className="h-5 w-5" />
      </button>
    </div>
  )
}

export function MapView() {
  const [map, setMap] = useState<LeafletMap | null>(null)

  const selectedCoordinate = useSafiStore(
    (state) => state.selectedCoordinate,
  )

  return (
    <div className="relative h-full w-full overflow-hidden rounded-[28px]">
      {map && <MapSearchOverlay map={map} />}

      <MapContainer
        center={[20, 0]}
        zoom={2}
        minZoom={2}
        maxZoom={18}
        zoomControl={false}
        worldCopyJump={false}
        whenReady={(event) => setMap(event.target)}
        maxBounds={[
          [-85, -180],
          [85, 180],
        ]}
        maxBoundsViscosity={1}
        className="h-full w-full"
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution="&copy; CARTO"
          noWrap={true}
        />

        <ClickHandler />
        <MapControls />

        {selectedCoordinate && (
          <Marker position={selectedCoordinate} icon={crosshairIcon} />
        )}
      </MapContainer>
    </div>
  )
}