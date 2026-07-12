// Charts.jsx — Advanced infographics: bar, pie, trend (line), radar, area — rendered with
// Recharts from the REAL exported data (model metrics, feature importance, class balance,
// loss curve, threshold sweep).
import React, { useMemo } from 'react'
import { parseCSV } from './csv.js'
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid,
  PieChart, Pie, Cell, LineChart, Line, RadarChart, Radar, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, AreaChart, Area,
} from 'recharts'

const COLORS = ['#6366f1', '#059669', '#dc2626', '#d97706', '#7c3aed', '#0891b2', '#db2777', '#65a30d']

function Card({ title, subtitle, children }) {
  return (
    <div className="card" style={{ padding: 14, cursor: 'default' }}>
      <div className="card-title" style={{ fontSize: 14, marginBottom: 2 }}>{title}</div>
      <div className="card-meta" style={{ marginBottom: 8 }}>{subtitle}</div>
      <div style={{ width: '100%', height: 240 }}>
        <ResponsiveContainer>{children}</ResponsiveContainer>
      </div>
    </div>
  )
}

export default function Charts({ datasets }) {
  const get = (n) => { const d = datasets.find((x) => x.name === n); return d ? parseCSV(d.text).rows : [] }
  const metrics = useMemo(() => get('eeg_model_metrics.csv'), [datasets])
  const feats = useMemo(() => get('eeg_feature_importance.csv'), [datasets])
  const balance = useMemo(() => get('eeg_class_balance.csv'), [datasets])
  const loss = useMemo(() => get('eeg_loss_curve.csv'), [datasets])
  const sweep = useMemo(() => get('eeg_threshold_sweep.csv'), [datasets])

  // BAR: accuracy metrics per model
  const barData = metrics.map((m) => ({ model: (m.model || '').slice(0, 12),
    AUC: +m.cv_auc, accuracy: +m.accuracy, F1: +m.f1, recall: +m.recall_sens }))
  // PIE: class balance (after)
  const bal = balance.find((b) => b.stage === 'after') || balance[0] || {}
  const pieData = bal.ictal ? [{ name: 'ictal', value: +bal.ictal }, { name: 'interictal', value: +bal.interictal }] : []
  // TREND: MLP loss curve
  const lossData = loss.map((r) => ({ iter: +r.iter, loss: +r.log_loss }))
  // TREND: threshold sweep (sensitivity/specificity)
  const sweepData = sweep.map((r) => ({ threshold: +r.threshold, sensitivity: +r.sensitivity, specificity: +r.specificity, precision: +r.precision }))
  // RADAR: best model across metric dimensions
  const best = metrics[0] || {}
  const radarData = best.model ? [
    { dim: 'AUC', v: +best.cv_auc }, { dim: 'Accuracy', v: +best.accuracy },
    { dim: 'Precision', v: +best.precision }, { dim: 'Recall', v: +best.recall_sens },
    { dim: 'Specificity', v: +best.specificity }, { dim: 'F1', v: +best.f1 },
  ] : []
  // BAR (horizontal): top features by mutual information
  const featData = feats.slice(0, 8).map((f) => ({ feature: f.feature, mi: +f.mutual_info }))

  const has = metrics.length || feats.length || balance.length

  return (
    <main className="content home">
      <h1 className="home-h1">📈 Charts — bar · pie · trend · radar</h1>
      <p className="home-sub">Advanced infographics rendered with Recharts from the real exported EEG datasets.</p>
      {!has && <div className="crumb">Run analysis/secondary_eeg_full.py to generate the chart datasets.</div>}
      <div className="cards" style={{ gridTemplateColumns: 'repeat(auto-fill,minmax(340px,1fr))' }}>

        {barData.length > 0 && (
          <Card title="Bar — model accuracy metrics" subtitle="eeg_model_metrics.csv">
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="model" fontSize={11} /><YAxis domain={[0, 1]} fontSize={11} />
              <Tooltip /><Legend />
              <Bar dataKey="AUC" fill={COLORS[0]} /><Bar dataKey="accuracy" fill={COLORS[1]} />
              <Bar dataKey="F1" fill={COLORS[3]} /><Bar dataKey="recall" fill={COLORS[4]} />
            </BarChart>
          </Card>
        )}

        {pieData.length > 0 && (
          <Card title="Pie — class balance (after SMOTE)" subtitle="eeg_class_balance.csv">
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" outerRadius={80} label>
                {pieData.map((e, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie><Tooltip /><Legend />
            </PieChart>
          </Card>
        )}

        {lossData.length > 0 && (
          <Card title="Trend — MLP training loss" subtitle="eeg_loss_curve.csv">
            <LineChart data={lossData}>
              <CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="iter" fontSize={11} /><YAxis fontSize={11} /><Tooltip />
              <Line type="monotone" dataKey="loss" stroke={COLORS[2]} dot={false} strokeWidth={2} />
            </LineChart>
          </Card>
        )}

        {sweepData.length > 0 && (
          <Card title="Trend — sensitivity/specificity vs threshold" subtitle="eeg_threshold_sweep.csv">
            <AreaChart data={sweepData}>
              <CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="threshold" fontSize={11} /><YAxis domain={[0, 1]} fontSize={11} /><Tooltip /><Legend />
              <Area type="monotone" dataKey="sensitivity" stroke={COLORS[0]} fill={COLORS[0]} fillOpacity={0.2} />
              <Area type="monotone" dataKey="specificity" stroke={COLORS[1]} fill={COLORS[1]} fillOpacity={0.2} />
            </AreaChart>
          </Card>
        )}

        {radarData.length > 0 && (
          <Card title={`Radar — ${(best.model || '').slice(0, 16)} metric profile`} subtitle="eeg_model_metrics.csv">
            <RadarChart data={radarData} outerRadius={80}>
              <PolarGrid /><PolarAngleAxis dataKey="dim" fontSize={11} /><PolarRadiusAxis domain={[0, 1]} fontSize={9} />
              <Radar dataKey="v" stroke={COLORS[4]} fill={COLORS[4]} fillOpacity={0.4} /><Tooltip />
            </RadarChart>
          </Card>
        )}

        {featData.length > 0 && (
          <Card title="Bar — top features (mutual information)" subtitle="eeg_feature_importance.csv">
            <BarChart data={featData} layout="vertical" margin={{ left: 30 }}>
              <CartesianGrid strokeDasharray="3 3" /><XAxis type="number" fontSize={11} /><YAxis type="category" dataKey="feature" fontSize={10} width={90} /><Tooltip />
              <Bar dataKey="mi" fill={COLORS[5]} />
            </BarChart>
          </Card>
        )}

      </div>
    </main>
  )
}
