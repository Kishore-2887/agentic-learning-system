import {
  ContentListItem,
  ContentDetail,
  EvaluationReport,
  RevisionHistory,
  WorkflowStatus,
  AnalyticsData,
  SettingsData
} from '../types';

const API_BASE = '/api';

export async function fetchAnalytics(): Promise<AnalyticsData> {
  const res = await fetch(`${API_BASE}/analytics`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export async function fetchContentList(search?: string, status?: string): Promise<ContentListItem[]> {
  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (status) params.append('status', status);
  const res = await fetch(`${API_BASE}/content?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch content list');
  return res.json();
}

export async function fetchContentDetail(id: string): Promise<ContentDetail> {
  const res = await fetch(`${API_BASE}/content/${id}`);
  if (!res.ok) throw new Error('Failed to fetch content detail');
  return res.json();
}

export async function fetchContentEvaluations(id: string): Promise<EvaluationReport[]> {
  const res = await fetch(`${API_BASE}/content/${id}/evaluation`);
  if (!res.ok) throw new Error('Failed to fetch evaluations');
  return res.json();
}

export async function fetchContentHistory(id: string): Promise<RevisionHistory[]> {
  const res = await fetch(`${API_BASE}/content/${id}/history`);
  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}

export async function generateContent(payload: {
  topic: string;
  target_audience: string;
  education_level: string;
  learning_objectives: string[];
  content_type: string;
  quality_threshold?: number;
  max_retries?: number;
}): Promise<{ request_id: string; status: string; message: string }> {
  const res = await fetch(`${API_BASE}/content/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to submit generation request');
  }
  return res.json();
}

export async function fetchWorkflowStatus(id: string): Promise<WorkflowStatus> {
  const res = await fetch(`${API_BASE}/workflow/${id}/status`);
  if (!res.ok) throw new Error('Failed to fetch workflow status');
  return res.json();
}

export async function fetchSettings(): Promise<SettingsData> {
  const res = await fetch(`${API_BASE}/settings`);
  if (!res.ok) throw new Error('Failed to fetch settings');
  return res.json();
}

export async function updateSettings(payload: Partial<SettingsData>): Promise<SettingsData> {
  const res = await fetch(`${API_BASE}/settings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to update settings');
  return res.json();
}

