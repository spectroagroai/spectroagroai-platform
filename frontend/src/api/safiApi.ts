import axios from 'axios';
import { PredictionResponse, RuntimeMode } from '../types/safi';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

console.log('SAFI API baseURL:', api.defaults.baseURL);

export async function fetchPrediction(
  latitude: number,
  longitude: number,
  mode: RuntimeMode,
): Promise<PredictionResponse> {
  try {
    const response = await api.post<PredictionResponse>('/predict', {
      latitude,
      longitude,
      mode,
    });

    return response.data;
  } catch (error: any) {
    console.error('Axios error:', error);

    if (error.response) {
      throw new Error(
        error.response.data?.detail ||
          `API request failed with status ${error.response.status}`,
      );
    }

    if (error.request) {
      throw new Error(
        'Unable to connect to the SAFI backend service.',
      );
    }

    throw new Error(error.message || 'Unknown error occurred.');
  }
}