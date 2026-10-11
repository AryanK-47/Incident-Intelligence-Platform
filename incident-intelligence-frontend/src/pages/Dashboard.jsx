import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Activity,
  ArrowRight,
  Clock3,
  Plus,
  RefreshCw,
  ShieldAlert,
  Siren,
  CheckCircle2,
  AlertTriangle,
  CircleAlert,
} from 'lucide-react';
import { getIncidents, createIncident } from '../api/incidents';
import { errorMessage } from '../api/client';
import { SeverityBadge, StatusBadge } from '../components/Badge';
import Modal from '../components/Modal';

const timeAgo = (value) => {
  if (!value) return '—';

  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return '—';

  const mins = Math.max(
    0,
    Math.floor((Date.now() - date.getTime()) / 60000),
  );

  if (mins < 60) return `${mins}m ago`;
  if (mins < 1440) return `${Math.floor(mins / 60)}h ago`;

  return `${Math.floor(mins / 1440)}d ago`;
};

const active = (incident) =>
  !['RESOLVED', 'CLOSED'].includes(
    String(incident.status || '').toUpperCase(),
  );

const statuses = [
  'OPEN',
  'INVESTIGATING',
  'IDENTIFIED',
  'MITIGATING',
  'RESOLVED',
  'CLOSED',
];

const severities = ['SEV1', 'SEV2', 'SEV3', 'SEV4'];

const emptyForm = {
  title: '',
  description: '',
  service: '',
  severity: 'SEV3',
};

export default function Dashboard() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');

    try {
      const result = await getIncidents({
        page: 1,
        page_size: 100,
      });

      setItems(Array.isArray(result.items) ? result.items : []);
    } catch (e) {
      setError(errorMessage(e));
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const open = useMemo(
    () => items.filter(active),
    [items],
  );

  const critical = useMemo(
    () =>
      open.filter((incident) =>
        ['SEV1', 'SEV2'].includes(
          String(incident.severity || '').toUpperCase(),
        ),
      ),
    [open],
  );

  const resolved = useMemo(
    () =>
      items.filter(
        (incident) =>
          String(incident.status || '').toUpperCase() === 'RESOLVED',
      ),
    [items],
  );

  const stale = useMemo(
    () =>
      open.filter((incident) => {
        if (!incident.created_at) return false;

        const created = new Date(incident.created_at).getTime();

        return (
          Number.isFinite(created) &&
          Date.now() - created > 60 * 60 * 1000
        );
      }),
    [open],
  );

  const statusCounts = useMemo(
    () =>
      statuses.map((status) => ({
        status,
        count: items.filter(
          (incident) =>
            String(incident.status || '').toUpperCase() === status,
        ).length,
      })),
    [items],
  );

  const recentIncidents = useMemo(
    () =>
      [...items]
        .sort(
          (a, b) =>
            new Date(b.created_at || 0) -
            new Date(a.created_at || 0),
        )
        .slice(0, 6),
    [items],
  );

  const submit = async (e) => {
    e.preventDefault();

    setSaving(true);
    setNotice('');

    try {
      await createIncident(form);

      setShowCreate(false);
      setForm(emptyForm);
      setNotice('Incident created successfully.');

      await load();
    } catch (e) {
      setNotice(errorMessage(e));
    } finally {
      setSaving(false);
    }
  };

  const updateForm = (field, value) => {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  };

  return (
    <>
      <div className="page-heading">
        <div>
          <div className="eyebrow">OPERATIONS / OVERVIEW</div>

          <h1>
            Incident overview
            <span className="heading-period">.</span>
          </h1>

          <p>
            Monitor incident records, prioritize critical issues, and
            track response progress.
          </p>
        </div>

        <div className="heading-actions">
          <button
            className="secondary-btn"
            onClick={load}
            disabled={loading}
          >
            <RefreshCw
              size={15}
              className={loading ? 'spin' : ''}
            />
            Refresh data
          </button>

          <button
            className="primary-btn"
            onClick={() => {
              setNotice('');
              setShowCreate(true);
            }}
          >
            <Plus size={17} />
            Create incident
          </button>
        </div>
      </div>

      {notice && (
        <div
          className={`alert ${
            notice === 'Incident created successfully.'
              ? 'success'
              : 'error'
          }`}
          role="status"
        >
          {notice}
        </div>
      )}

      {error && (
        <div className="alert error" role="alert">
          <AlertTriangle size={16} />
          <span>{error}</span>

          <button
            className="inline-retry"
            onClick={load}
            disabled={loading}
          >
            Retry
          </button>
        </div>
      )}

      <div className="metric-grid">
        <Metric
          label="Active incidents"
          value={loading ? '—' : open.length}
          icon={<Siren size={18} />}
          color="purple"
          note="Not resolved or closed"
        />

        <Metric
          label="High priority"
          value={loading ? '—' : critical.length}
          icon={<ShieldAlert size={18} />}
          color="red"
          note="Active SEV1 and SEV2"
        />

        <Metric
          label="Needs attention"
          value={loading ? '—' : stale.length}
          icon={<Clock3 size={18} />}
          color="blue"
          note="Active for over one hour"
        />

        <Metric
          label="Resolved"
          value={loading ? '—' : resolved.length}
          icon={<CheckCircle2 size={18} />}
          color="green"
          note="Currently marked resolved"
        />
      </div>

      <div className="overview-grid real-overview-grid">
        <section className="panel priority-panel">
          <div className="panel-heading">
            <div>
              <h2>
                <CircleAlert size={17} />
                Priority incidents
              </h2>
              <p>Active SEV1 and SEV2 incidents</p>
            </div>

            <Link
              className="text-link"
              to="/incidents?severity=SEV1"
            >
              Open queue
              <ArrowRight size={15} />
            </Link>
          </div>

          {loading ? (
            <div className="empty-state compact">
              <RefreshCw className="spin" />
              Loading incidents…
            </div>
          ) : critical.length > 0 ? (
            <div className="priority-list">
              {critical.slice(0, 5).map((item) => (
                <Link
                  className="priority-item"
                  to={`/incidents/${item.id}`}
                  key={item.id}
                >
                  <span
                    className={`priority-rail ${String(
                      item.severity || '',
                    ).toLowerCase()}`}
                  />

                  <div className="priority-copy">
                    <b>{item.title || 'Untitled incident'}</b>
                    <span>
                      {item.service || 'Unknown service'}
                      {' · '}
                      {timeAgo(item.created_at)}
                    </span>
                  </div>

                  <SeverityBadge value={item.severity} />

                  <ArrowRight
                    size={15}
                    className="priority-arrow"
                  />
                </Link>
              ))}
            </div>
          ) : (
            <div className="subtle-empty priority-none">
              <CheckCircle2 size={17} />
              No active SEV1 or SEV2 incidents in the loaded records.
            </div>
          )}
        </section>

        <section className="panel breakdown-panel">
          <div className="panel-heading">
            <div>
              <h2>Incident status</h2>
              <p>Breakdown of loaded API records</p>
            </div>

            <Activity size={17} className="muted-icon" />
          </div>

          <div className="posture-total">
            <strong>{loading ? '—' : items.length}</strong>
            <span>total records</span>
          </div>

          {statusCounts.map(({ status, count }, index) => (
            <div className="posture-row" key={status}>
              <span className={`posture-dot p${index}`} />

              <span>{status.toLowerCase()}</span>

              <b>{loading ? '—' : count}</b>

              <div className="posture-track">
                <i
                  style={{
                    width: `${
                      !loading && items.length
                        ? (count / items.length) * 100
                        : 0
                    }%`,
                  }}
                />
              </div>
            </div>
          ))}
        </section>
      </div>

      <section className="panel incidents-panel">
        <div className="panel-heading">
          <div>
            <h2>Recently reported</h2>
            <p>Latest incident records returned by the backend</p>
          </div>

          <Link className="text-link" to="/incidents">
            View incident queue
            <ArrowRight size={15} />
          </Link>
        </div>

        {loading ? (
          <div className="empty-state">
            <RefreshCw className="spin" />
            Loading incidents…
          </div>
        ) : recentIncidents.length > 0 ? (
          <IncidentTable items={recentIncidents} />
        ) : (
          <div className="empty-state">
            <div className="empty-icon">
              <Activity />
            </div>

            <b>No incidents to show</b>

            <span>
              {error
                ? 'The API did not return incident records.'
                : 'Create the first incident to start tracking response.'}
            </span>

            {!error && (
              <button
                className="primary-btn"
                onClick={() => setShowCreate(true)}
              >
                <Plus size={15} />
                Create incident
              </button>
            )}
          </div>
        )}
      </section>

      {showCreate && (
        <Modal
          title="Create incident"
          onClose={() => {
            if (!saving) setShowCreate(false);
          }}
        >
          <form className="stack-form" onSubmit={submit}>
            <label>
              Incident title
              <input
                required
                maxLength={200}
                value={form.title}
                onChange={(e) => updateForm('title', e.target.value)}
                placeholder="e.g. Payment API latency spike"
              />
            </label>

            <label>
              Service name
              <input
                required
                maxLength={100}
                value={form.service}
                onChange={(e) => updateForm('service', e.target.value)}
                placeholder="payment-service"
              />
            </label>

            <label>
              Severity
              <select
                value={form.severity}
                onChange={(e) => updateForm('severity', e.target.value)}
              >
                {severities.map((severity) => (
                  <option key={severity} value={severity}>
                    {severity}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Description
              <textarea
                required
                minLength={10}
                rows={4}
                value={form.description}
                onChange={(e) =>
                  updateForm('description', e.target.value)
                }
                placeholder="Symptoms, impact, and when it started"
              />
            </label>

            <div className="modal-actions">
              <button
                type="button"
                className="secondary-btn"
                disabled={saving}
                onClick={() => setShowCreate(false)}
              >
                Cancel
              </button>

              <button
                type="submit"
                className="primary-btn"
                disabled={saving}
              >
                {saving ? 'Creating…' : 'Create incident'}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}

function Metric({ label, value, icon, color, note }) {
  return (
    <div className="metric-card">
      <div className="metric-top">
        <span>{label}</span>
        <span className={`metric-icon ${color}`}>{icon}</span>
      </div>

      <div className="metric-value">{value}</div>
      <div className="metric-note">{note}</div>
    </div>
  );
}

export function IncidentTable({ items }) {
  return (
    <div className="table-scroll">
      <table className="incident-table">
        <thead>
          <tr>
            <th>INCIDENT</th>
            <th>SERVICE</th>
            <th>SEVERITY</th>
            <th>STATUS</th>
            <th>CREATED</th>
            <th />
          </tr>
        </thead>

        <tbody>
          {items.map((incident) => (
            <tr key={incident.id}>
              <td>
                <Link
                  className="incident-title"
                  to={`/incidents/${incident.id}`}
                >
                  {incident.title || 'Untitled incident'}
                </Link>

                <small className="incident-id">
                  INC-{String(incident.id).slice(0, 8).toUpperCase()}
                </small>
              </td>

              <td>
                <span className="service-name">
                  {incident.service || '—'}
                </span>
              </td>

              <td>
                <SeverityBadge value={incident.severity} />
              </td>

              <td>
                <StatusBadge value={incident.status} />
              </td>

              <td>
                <span className="time-text">
                  <Clock3 size={13} />
                  {timeAgo(incident.created_at)}
                </span>
              </td>

              <td>
                <Link
                  className="row-arrow"
                  to={`/incidents/${incident.id}`}
                  aria-label="Open incident"
                >
                  <ArrowRight size={16} />
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}