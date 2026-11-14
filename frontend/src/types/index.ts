export interface RubricCheckpoint {
  name: string;
  label: string;
  passed: boolean;
  reason: string;
}

export interface RejectionLogItem {
  iteration: number;
  failed_checkpoints: string[];
  critique: string;
  changes_made_on_retry: string;
  timestamp: string;
}

export interface ContentListItem {
  id: string;
  request_id: string;
  title: string;
  topic: string;
  education_level: string;
  version: number;
  status: 'draft' | 'approved' | 'manual_review' | 'failed';
  is_published: boolean;
  overall_score?: number;
  all_checkpoints_passed?: boolean;
  created_at: string;
}

export interface PracticeQuestion {
  question: string;
  options?: string[];
  answer: string;
  explanation: string;
}

export interface ContentSection {
  title: string;
  explanation: string;
  examples: string[];
  callout_note?: string;
  key_terms: string[];
}

export interface EducationalContent {
  title: string;
  topic: string;
  target_audience: string;
  education_level: string;
  summary: string;
  core_analogy: string;
  key_concepts: string[];
  sections: ContentSection[];
  practice_questions: PracticeQuestion[];
  key_takeaways: string[];
  references_and_further_reading: string[];
}

export interface IdentifiedError {
  section: string;
  severity: 'minor' | 'moderate' | 'critical';
  description: string;
  unsupported_claim?: boolean;
}

export interface EvaluationReport {
  id: string;
  iteration: number;
  all_checkpoints_passed: boolean;
  checkpoints: RubricCheckpoint[];
  factual_accuracy: number;
  relevance: number;
  completeness: number;
  clarity_readability: number;
  educational_effectiveness: number;
  structure_organization: number;
  overall_score: number;
  passed: boolean;
  identified_errors: IdentifiedError[];
  missing_concepts: string[];
  improvement_recommendations: string[];
  unsupported_claims: string[];
  created_at: string;
}

export interface RevisionHistory {
  id: string;
  iteration: number;
  changes_summary: string;
  previous_score: number;
  new_score: number;
  modified_sections: string[];
  created_at: string;
}

export interface ContentDetail {
  id: string;
  request_id: string;
  version: number;
  title: string;
  raw_json: EducationalContent;
  markdown_text: string;
  word_count: number;
  is_published: boolean;
  status: string;
  created_at: string;
  latest_evaluation?: EvaluationReport;
  rejection_log?: RejectionLogItem[];
}

export interface WorkflowLogItem {
  timestamp: string;
  agent: string;
  action: string;
  message: string;
  status: string;
  details?: Record<string, any>;
}

export interface WorkflowStatus {
  request_id: string;
  status: 'pending' | 'running' | 'completed' | 'manual_review' | 'failed';
  current_agent: string;
  retry_count: number;
  max_retries: number;
  quality_threshold: number;
  latest_score?: number;
  passed?: boolean;
  all_checkpoints_passed?: boolean;
  checkpoints: RubricCheckpoint[];
  rejection_log: RejectionLogItem[];
  logs: WorkflowLogItem[];
  content_id?: string;
  unresolved_issues: string[];
  final_decision?: string;
}

export interface AnalyticsData {
  total_generated: number;
  approved_count: number;
  manual_review_count: number;
  failed_count: number;
  average_quality_score: number;
  pass_rate_percentage: number;
  dimension_averages: Record<string, number>;
  score_distribution: Record<string, number>;
  recent_activity: {
    id: string;
    title: string;
    status: string;
    score: number;
    is_published: boolean;
    created_at: string;
  }[];
  learned_rules_count?: number;
}

export interface SettingsData {
  llm_provider: string;
  available_providers: string[];
  openai_model: string;
  gemini_model: string;
  default_quality_threshold: number;
  max_improvement_attempts: number;
  openai_key_configured: boolean;
  gemini_key_configured: boolean;
  persistent_memory_enabled?: boolean;
  learned_rules?: string[];
}
