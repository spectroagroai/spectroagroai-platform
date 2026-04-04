// frontend/src/store/useSafiStore.ts

import { create } from 'zustand';
import { fetchPrediction } from '../api/safiApi';
import { PredictionResponse, RuntimeMode } from '../types/safi';

interface SafiStore {
  selectedCoordinate: [number, number] | null;
  prediction: PredictionResponse | null;
  mode: RuntimeMode;
  isLoading: boolean;
  error: string | null;

  setMode: (mode: RuntimeMode) => void;
  selectCoordinate: (lat: number, lon: number) => Promise<void>;
  clearPrediction: () => void;
}

export const useSafiStore = create<SafiStore>((set, get) => ({
  selectedCoordinate: null,
  prediction: null,
  mode: 'baseline',
  isLoading: false,
  error: null,

  setMode: async (mode) => {
    set({ mode });

    const current = get().selectedCoordinate;
    if (!current) return;

    await get().selectCoordinate(current[0], current[1]);
  },

  selectCoordinate: async (lat, lon) => {
    console.log('Map coordinate selected:', { lat, lon });

    set({
      selectedCoordinate: [lat, lon],
      isLoading: true,
      error: null,
    });

    try {
      const prediction = await fetchPrediction(lat, lon, get().mode);

      set({
        prediction,
        isLoading: false,
        error: null,
      });

      console.log('Prediction stored successfully.');
    } catch (error: any) {
      console.error('SAFI prediction error:', error);

      const message =
        error?.message ||
        error?.response?.data?.detail ||
        'Unable to retrieve SAFI prediction.';

      set({
        prediction: null,
        isLoading: false,
        error: message,
      });

      console.error('Displayed error message:', message);
    }
  },

  clearPrediction: () =>
    set({
      prediction: null,
      error: null,
      selectedCoordinate: null,
    }),
}));