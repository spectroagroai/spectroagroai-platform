export type RuntimeMode = 'baseline' | 'nowcast';

export interface PredictionInterval {
  mean: number;
  lower: number;
  upper: number;
}

export interface Predictions {
  lab__CECPH7: PredictionInterval;
  lab__TOTC: PredictionInterval;
  lab__ORGC: PredictionInterval;
  lab__ORGM: PredictionInterval;
  lab__BDFIOD: PredictionInterval;
}

export interface Confidence {
  base_score?: number;
  domain_support_score?: number;
  score: number;
  level: 'high' | 'medium' | 'low';
}

export interface Domain {
  status: 'supported' | 'borderline' | 'out_of_distribution';
  ood_score: number;
  support_score: number;
  distance_km: number;
  valid_feature_count: number;
  reasons: string[];
}

export interface LSI {
  conservative: number;
  expected: number;
  opportunity: number;
}

export interface Metadata {
  source: string;
  requested_coordinates: [number, number];
  effective_coordinates: [number, number];
  feature_count: number;
}

export interface PredictionResponse {
  metadata: Metadata;
  predictions: Predictions;
  warnings: string[];
  confidence: Confidence;
  domain: Domain;
  lsi: LSI;
  mode: RuntimeMode;
}