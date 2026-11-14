import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';

interface DimensionChartProps {
  data: {
    factual_accuracy: number;
    relevance: number;
    completeness: number;
    clarity_readability: number;
    educational_effectiveness: number;
    structure_organization: number;
  };
  chartType?: 'radar' | 'bar';
}

export const DimensionChart: React.FC<DimensionChartProps> = ({ data, chartType = 'bar' }) => {
  const chartData = [
    { subject: 'Factual Accuracy', score: data.factual_accuracy, weight: '25%', fullMark: 100 },
    { subject: 'Relevance', score: data.relevance, weight: '20%', fullMark: 100 },
    { subject: 'Completeness', score: data.completeness, weight: '20%', fullMark: 100 },
    { subject: 'Clarity & Flow', score: data.clarity_readability, weight: '15%', fullMark: 100 },
    { subject: 'Pedagogy', score: data.educational_effectiveness, weight: '10%', fullMark: 100 },
    { subject: 'Structure', score: data.structure_organization, weight: '10%', fullMark: 100 },
  ];

  if (chartType === 'radar') {
    return (
      <div className="w-full h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
            <PolarGrid stroke="#334155" />
            <PolarAngleAxis dataKey="subject" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 11 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" />
            <Radar
              name="Evaluation Score"
              dataKey="score"
              stroke="#6366f1"
              fill="#6366f1"
              fillOpacity={0.4}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    );
  }

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
          <XAxis type="number" domain={[0, 100]} stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <YAxis
            type="category"
            dataKey="subject"
            stroke="#475569"
            tick={{ fill: '#cbd5e1', fontSize: 12 }}
            width={110}
          />
          <Tooltip
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#f8fafc' }}
            formatter={(value: any, name: any, item: any) => [`${value}/100 (Weight: ${item.payload.weight})`, 'Score']}
          />
          <Bar dataKey="score" radius={[0, 4, 4, 0]}>
            {chartData.map((entry, index) => {
              const color = entry.score >= 80 ? '#10b981' : entry.score >= 70 ? '#f59e0b' : '#f43f5e';
              return <Cell key={`cell-${index}`} fill={color} />;
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

