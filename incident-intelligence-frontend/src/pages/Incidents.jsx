import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  AlertCircle,
  ArrowDownUp,
  Download,
  Plus,
  RefreshCw,
  Search,
  SlidersHorizontal,
  X,
  Activity,
  ShieldAlert,
  CheckCircle2,
  Clock3,
} from 'lucide-react';

import { getIncidents, createIncident } from '../api/incidents';
import { errorMessage } from '../api/client';
import { IncidentTable } from './Dashboard';
import Modal from '../components/Modal';

const INITIAL_FORM = {
  title: '',
  description: '',
  service: '',
  severity: 'SEV3',
};

const SEVERITIES = ['SEV1', 'SEV2', 'SEV3', 'SEV4'];
const STATUSES = [
  'OPEN',
  'INVESTIGATING',
  'IDENTIFIED',
  'MITIGATING',
  'RESOLVED',
  'CLOSED',
];

function Metric({ label, value, detail, icon: Icon, tone = '' }) {
  return (
    <div className="metric-card">
      <div className="metric-top">
        <span>{label}</span>
        <span className={`metric-icon ${tone}`}>
          <Icon size={17} />
        </span>
      </div>
      <div className="metric-value">{value}</div>
      <div className="metric-note">{detail}</div>
    </div>
  );
}

export default function Incidents() {
  const location = useLocation();
  const navigate = useNavigate();

  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [severity, setSeverity] = useState('ALL');
  const [status, setStatus] = useState('ALL');
  const [sort, setSort] = useState('newest');
  const [show, setShow] = useState(false);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState('');
  const [form, setForm] = useState(INITIAL_FORM);

  const load = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const response = await getIncidents({ page: 1, page_size: 100 });
      const records = Array.isArray(response)
        ? response
        : Array.isArray(response?.items)
          ? response.items
          : [];

      setItems(records);
    } catch (err) {
      setError(errorMessage(err));
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    const params = new URLSearchParams(location.search);

    if (params.get('create') === '1') {
      setShow(true);
    }

    if (SEVERITIES.includes(params.get('severity'))) {
      setSeverity(params.get('severity'));
    }
  }, [location.search]);

  const closeCreate = () => {
    if (saving) return;
    setShow(false);

    const params = new URLSearchParams(location.search);
    params.delete('create');

    navigate(
      {
        pathname: location.pathname,
        search: params.toString() ? `?${params.toString()}` : '',
      },
      { replace: true },
    );
  };

  const filtered = useMemo(() => {
    const query = search.trim().toLowerCase();

    const result = items.filter((incident) => {
      const searchable = [
        incident.title,
        incident.service,
        incident.id,
        incident.description,
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();

      return (
        (!query || searchable.includes(query)) &&
        (severity === 'ALL' || incident.severity === severity) &&
        (status === 'ALL' || incident.status === status)
      );
    });

    return result.sort((a, b) => {
      if (sort === 'oldest') {
        return new Date(a.created_at || 0) - new Date(b.created_at || 0);
      }

      if (sort === 'severity') {
        const rank = { SEV1: 1, SEV2: 2, SEV3: 3, SEV4: 4 };
        return (rank[a.severity] || 99) - (rank[b.severity] || 99);
      }

      return new Date(b.created_at || 0) - new Date(a.created_at || 0);
    });
  }, [items, search, severity, status, sort]);

  const metrics = useMemo(() => {
    const active = items.filter(
      (x) => !['RESOLVED', 'CLOSED'].includes(x.status),
    );
    const critical = active.filter(
      (x) => ['SEV1', 'SEV2'].includes(x.severity),
    );
    const resolved = items.filter(
      (x) => ['RESOLVED', 'CLOSED'].includes(x.status),
    );

    return {
      active: active.length,
      critical: critical.length,
      resolved: resolved.length,
      total: items.length,
    };
  }, [items]);

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setNotice('');
    setError('');

    try {
      await createIncident({
        title: form.title.trim(),
        description: form.description.trim(),
        service: form.service.trim(),
        severity: form.severity,
      });

      setForm(INITIAL_FORM);
      setShow(false);
      setNotice('Incident created successfully.');

      const params = new URLSearchParams(location.search);
      params.delete('create');

      navigate(
        {
          pathname: location.pathname,
          search: params.toString() ? `?${params.toString()}` : '',
        },
        { replace: true },
      );

      await load();
    } catch (err) {
      setNotice('');
      setError(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const exportCsv = () => {
    if (!filtered.length) return;

    const columns = [
      'id',
      'title',
      'service',
      'severity',
      'status',
      'created_at',
      'description',
    ];

    const escapeCsv = (value) =>
      `"${String(value ?? '').replace(/"/g, '""')}"`;

    const csv = [
      columns.join(','),
      ...filtered.map((incident) =>
        columns.map((column) => escapeCsv(incident[column])).join(','),
      ),
    ].join('\r\n');

    const blob = new Blob(['\uFEFF', csv], {
      type: 'text/csv;charset=utf-8;',
    });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');

    anchor.href = url;
    anchor.download = 'incident-queue.csv';
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  };

  const clearFilters = () => {
    setSearch('');
    setSeverity('ALL');
    setStatus('ALL');
    setSort('newest');
  };

  return (
    <>
      <div className="page-heading">
        <div>
          <div className="eyebrow">OPERATIONS / INCIDENTS</div>
          <h1>
            Incident queue<span className="heading-period">.</span>
          </h1>
          <p>Search, prioritise and track incidents from your API.</p>
        </div>

        <div className="heading-actions">
          <button
            className="secondary-btn"
            onClick={load}
            disabled={loading}
          >
            <RefreshCw size={15} className={loading ? 'spin' : ''} />
            Refresh
          </button>

          <button className="primary-btn" onClick={() => setShow(true)}>
            <Plus size={17} />
            Create incident
          </button>
        </div>
      </div>

      {notice && (
        <div className="alert success">
          <CheckCircle2 size={16} />
          {notice}
          <button
            className="icon-btn"
            aria-label="Dismiss notification"
            onClick={() => setNotice('')}
          >
            <X size={15} />
          </button>
        </div>
      )}

      {error && (
        <div className="alert error">
          <AlertCircle size={16} />
          <span>{error}</span>
          <button className="secondary-btn" onClick={load}>
            Retry
          </button>
        </div>
      )}

      <div className="metrics-grid">
        <Metric
          label="Total incidents"
          value={loading ? '—' : metrics.total}
          detail="Records returned by API"
          icon={Activity}
        />
        <Metric
          label="Active incidents"
          value={loading ? '—' : metrics.active}
          detail="Not resolved or closed"
          icon={Clock3}
          tone="warning"
        />
        <Metric
          label="High priority"
          value={loading ? '—' : metrics.critical}
          detail="Active SEV1 and SEV2"
          icon={ShieldAlert}
          tone="danger"
        />
        <Metric
          label="Resolved"
          value={loading ? '—' : metrics.resolved}
          detail="Resolved or closed"
          icon={CheckCircle2}
          tone="success"
        />
      </div>

      <section className="panel incidents-panel queue-panel">
        <div className="panel-heading">
          <div>
            <h2>All incidents</h2>
            <p>Filter and inspect incident records</p>
          </div>

          <button
            className="secondary-btn"
            onClick={exportCsv}
            disabled={!filtered.length || loading}
          >
            <Download size={15} />
            Export CSV
          </button>
        </div>

        <div className="queue-toolbar">
          <div className="search-box">
            <Search size={16} />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Search title, service, ID or description…"
              aria-label="Search incidents"
            />
            {search && (
              <button
                className="icon-btn"
                onClick={() => setSearch('')}
                aria-label="Clear search"
              >
                <X size={14} />
              </button>
            )}
          </div>

          <div className="filter-wrap">
            <SlidersHorizontal size={15} />

            <select
              value={severity}
              onChange={(event) => setSeverity(event.target.value)}
              aria-label="Filter by severity"
            >
              <option value="ALL">All severities</option>
              {SEVERITIES.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>

            <select
              value={status}
              onChange={(event) => setStatus(event.target.value)}
              aria-label="Filter by status"
            >
              <option value="ALL">All statuses</option>
              {STATUSES.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>

            <select
              value={sort}
              onChange={(event) => setSort(event.target.value)}
              aria-label="Sort incidents"
            >
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
              <option value="severity">Highest severity</option>
            </select>
          </div>
        </div>

        <div className="queue-meta">
          <span>
            <b>{loading ? '…' : filtered.length}</b> of {loading ? '…' : items.length}{' '}
            incidents
          </span>
          <span>Filters apply to loaded records</span>
        </div>

        {loading ? (
          <div className="empty-state">
            <RefreshCw className="spin" />
            Loading incidents…
          </div>
        ) : filtered.length ? (
          <IncidentTable items={filtered} />
        ) : (
          <div className="empty-state">
            <div className="empty-icon">
              <Search />
            </div>
            <b>{items.length ? 'No matching incidents' : 'No incidents found'}</b>
            <span>
              {items.length
                ? 'Try changing your search or filters.'
                : 'Create an incident or check your API connection.'}
            </span>

            {items.length > 0 && (
              <button className="secondary-btn" onClick={clearFilters}>
                Clear filters
              </button>
            )}

            {!items.length && (
              <button className="secondary-btn" onClick={load}>
                Try again
              </button>
            )}
          </div>
        )}
      </section>

      {show && (
        <Modal title="Create incident" onClose={closeCreate}>
          <form className="stack-form" onSubmit={submit}>
            <label>
              Incident title
              <input
                required
                maxLength={200}
                value={form.title}
                onChange={(event) =>
                  setForm({ ...form, title: event.target.value })
                }
                placeholder="e.g. Payment API latency spike"
              />
            </label>

            <label>
              Service name
              <input
                required
                maxLength={100}
                value={form.service}
                onChange={(event) =>
                  setForm({ ...form, service: event.target.value })
                }
                placeholder="payment-service"
              />
            </label>

            <label>
              Severity
              <select
                value={form.severity}
                onChange={(event) =>
                  setForm({ ...form, severity: event.target.value })
                }
              >
                {SEVERITIES.map((value) => (
                  <option key={value} value={value}>
                    {value}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Description
              <textarea
                required
                minLength={10}
                maxLength={5000}
                rows={4}
                value={form.description}
                onChange={(event) =>
                  setForm({ ...form, description: event.target.value })
                }
                placeholder="Describe the impact and symptoms…"
              />
            </label>

            <div className="modal-actions">
              <button
                type="button"
                className="secondary-btn"
                onClick={closeCreate}
                disabled={saving}
              >
                Cancel
              </button>
              <button className="primary-btn" disabled={saving}>
                {saving ? 'Creating…' : 'Create incident'}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}