import React, { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import {
  ArrowLeft,
  Bot,
  CheckCircle2,
  Clock3,
  FileText,
  GitBranch,
  RefreshCw,
  ShieldAlert,
  BrainCircuit,
  Users,
  UserPlus,
  UserMinus,
} from 'lucide-react';

import {
  getIncident,
  updateIncident,
  getIncidentAssignees,
  assignIncidentUser,
  unassignIncidentUser,
} from '../api/incidents';

import {
  getAnalysis,
  getAnalysisVersions,
  getIncidentEvents,
} from '../api/analysis';

import { getUsers } from '../api/users';
import { errorMessage } from '../api/client';
import { SeverityBadge, StatusBadge } from '../components/Badge';

export default function IncidentDetail() {
  const { id } = useParams();

  const [incident, setIncident] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [versions, setVersions] = useState([]);
  const [events, setEvents] = useState([]);

  const [users, setUsers] = useState([]);
  const [assignees, setAssignees] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState('');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);
  const [assignmentSaving, setAssignmentSaving] = useState(false);
  const [assignmentError, setAssignmentError] = useState('');
  const [usersUnavailable, setUsersUnavailable] = useState(false);

  const [notice, setNotice] = useState('');
  const [edit, setEdit] = useState(false);

  const [form, setForm] = useState({
    status: 'OPEN',
    severity: 'SEV3',
    cause: '',
  });

  const load = async () => {
    setLoading(true);
    setError('');

    try {
      const data = await getIncident(id);

      setIncident(data);
      setForm({
        status: data.status || 'OPEN',
        severity: data.severity || 'SEV3',
        cause: data.cause || '',
      });

      const results = await Promise.allSettled([
        getAnalysis(id),
        getAnalysisVersions(id),
        getIncidentEvents(id),
        getIncidentAssignees(id),
        getUsers(),
      ]);

      if (results[0].status === 'fulfilled') {
        setAnalysis(results[0].value);
      }

      if (results[1].status === 'fulfilled') {
        const value = results[1].value;
        setVersions(
          Array.isArray(value)
            ? value
            : value?.items || value?.versions || []
        );
      }

      if (results[2].status === 'fulfilled') {
        const value = results[2].value;
        setEvents(
          Array.isArray(value)
            ? value
            : value?.items || value?.events || []
        );
      }

      if (results[3].status === 'fulfilled') {
        const value = results[3].value;
        setAssignees(
          Array.isArray(value) ? value : value?.items || []
        );
        setAssignmentError('');
      } else {
        setAssignmentError(errorMessage(results[3].reason));
      }

      if (results[4].status === 'fulfilled') {
        const value = results[4].value;
        setUsers(
          Array.isArray(value) ? value : value?.items || []
        );
        setUsersUnavailable(false);
      } else {
        setUsers([]);
        setUsersUnavailable(true);
      }
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [id]);

  const save = async (e) => {
    e.preventDefault();
    setSaving(true);
    setNotice('');

    try {
      const payload = {
        status: form.status,
        severity: form.severity,
      };

      if (form.cause.trim()) {
        payload.cause = form.cause.trim();
      }

      const data = await updateIncident(id, payload);

      setIncident(data);
      setEdit(false);
      setNotice('Incident updated.');

      await load();
    } catch (err) {
      setNotice(errorMessage(err));
    } finally {
      setSaving(false);
    }
  };

  const handleAssign = async () => {
    if (!selectedUserId) return;

    setAssignmentSaving(true);
    setAssignmentError('');

    try {
      await assignIncidentUser(id, selectedUserId);

      setSelectedUserId('');

      const data = await getIncidentAssignees(id);
      setAssignees(
        Array.isArray(data) ? data : data?.items || []
      );
    } catch (err) {
      setAssignmentError(errorMessage(err));
    } finally {
      setAssignmentSaving(false);
    }
  };

  const handleUnassign = async (userId) => {
    setAssignmentSaving(true);
    setAssignmentError('');

    try {
      await unassignIncidentUser(id, userId);

      const data = await getIncidentAssignees(id);
      setAssignees(
        Array.isArray(data) ? data : data?.items || []
      );
    } catch (err) {
      setAssignmentError(errorMessage(err));
    } finally {
      setAssignmentSaving(false);
    }
  };

  const activeAssignees = assignees.filter(
    (item) => !item.unassigned_at
  );

  const availableUsers = users.filter(
    (user) =>
      !activeAssignees.some(
        (item) => item.user_id === user.id
      )
  );

  if (loading) {
    return (
      <div className="empty-state page-loading">
        <RefreshCw className="spin" /> Loading incident…
      </div>
    );
  }

  if (error || !incident) {
    return (
      <div className="detail-error">
        <div className="empty-icon">
          <ShieldAlert />
        </div>
        <h2>Could not load incident</h2>
        <p>{error || 'Incident not found.'}</p>
        <Link to="/incidents" className="secondary-btn">
          <ArrowLeft size={15} /> Back to incidents
        </Link>
      </div>
    );
  }

  const rootCause = analysis?.root_cause;
  const remediations = analysis?.suggested_remediation;

  return (
    <>
      <div className="detail-back">
        <Link to="/incidents">
          <ArrowLeft size={15} /> Back to incidents
        </Link>

        <span className="detail-id">
          INC-{String(incident.id).slice(0, 8).toUpperCase()}
        </span>
      </div>

      <div className="page-heading detail-heading">
        <div>
          <div className="eyebrow">
            INCIDENT DETAILS / INVESTIGATION
          </div>

          <h1>
            {incident.title}
            <span className="heading-period">.</span>
          </h1>

          <p>
            {incident.service}
            <span className="meta-separator"> · </span>
            Created{' '}
            {incident.created_at
              ? new Date(incident.created_at).toLocaleString()
              : '—'}
          </p>
        </div>

        <div className="heading-actions">
          <button
            className="secondary-btn"
            onClick={() => setEdit(!edit)}
          >
            {edit ? 'Cancel' : 'Update incident'}
          </button>
        </div>
      </div>

      {notice && <div className="alert success">{notice}</div>}

      <div className="detail-badges">
        <SeverityBadge value={incident.severity} />
        <StatusBadge value={incident.status} />

        <span className="detail-created">
          <Clock3 size={14} />
          {incident.resolved_at
            ? `Resolved ${new Date(
                incident.resolved_at
              ).toLocaleString()}`
            : 'Resolution time not set'}
        </span>
      </div>

      <div className="detail-grid">
        <div className="detail-main">
          {/* Incident summary */}
          <section className="panel detail-card">
            <div className="panel-heading">
              <div>
                <h2>
                  <FileText size={17} /> Incident summary
                </h2>
                <p>Reported symptoms and service impact</p>
              </div>
            </div>

            <div className="detail-description">
              {incident.description}
            </div>

            <div className="detail-facts">
              <div>
                <span>Service</span>
                <b>{incident.service}</b>
              </div>

              <div>
                <span>Severity</span>
                <b>{incident.severity}</b>
              </div>

              <div>
                <span>Status</span>
                <b>{incident.status}</b>
              </div>

              <div>
                <span>Incident ID</span>
                <b className="mono">{incident.id}</b>
              </div>
            </div>

            {incident.cause && (
              <div className="cause-block">
                <span>Recorded cause</span>
                <p>{incident.cause}</p>
              </div>
            )}

            {edit && (
              <form className="stack-form edit-form" onSubmit={save}>
                <h3>Update incident</h3>

                <label>
                  Status
                  <select
                    value={form.status}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        status: e.target.value,
                      })
                    }
                  >
                    {[
                      'OPEN',
                      'INVESTIGATING',
                      'IDENTIFIED',
                      'MITIGATING',
                      'RESOLVED',
                      'CLOSED',
                    ].map((value) => (
                      <option key={value} value={value}>
                        {value}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  Severity
                  <select
                    value={form.severity}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        severity: e.target.value,
                      })
                    }
                  >
                    {['SEV1', 'SEV2', 'SEV3', 'SEV4'].map(
                      (value) => (
                        <option key={value} value={value}>
                          {value}
                        </option>
                      )
                    )}
                  </select>
                </label>

                <label>
                  Cause
                  <input
                    value={form.cause}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        cause: e.target.value,
                      })
                    }
                    placeholder="Known or suspected cause"
                  />
                </label>

                <button className="primary-btn" disabled={saving}>
                  {saving ? 'Saving…' : 'Save changes'}
                </button>
              </form>
            )}
          </section>

          {/* Event timeline */}
          <section className="panel detail-card">
            <div className="panel-heading">
              <div>
                <h2>
                  <GitBranch size={17} /> Event timeline
                </h2>
                <p>Recorded lifecycle changes</p>
              </div>

              <button className="icon-btn" onClick={load}>
                <RefreshCw size={15} />
              </button>
            </div>

            {events.length === 0 ? (
              <div className="subtle-empty">
                No event records returned by the event endpoint yet.
              </div>
            ) : (
              <div className="timeline">
                {events.map((event, index) => (
                  <div
                    className="timeline-item"
                    key={event.id || index}
                  >
                    <div className="timeline-marker">
                      <CheckCircle2 size={15} />
                    </div>

                    <div className="timeline-content">
                      <b>
                        {(
                          event.event_type ||
                          event.type ||
                          'INCIDENT_EVENT'
                        ).replaceAll('_', ' ')}
                      </b>

                      <p>
                        {event.new_value
                          ? `${event.old_value || '—'} → ${event.new_value}`
                          : event.description ||
                            event.message ||
                            'Incident event recorded'}
                      </p>

                      <small>
                        {event.created_at
                          ? new Date(
                              event.created_at
                            ).toLocaleString()
                          : 'Timestamp unavailable'}
                      </small>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>

        <aside className="detail-side">
          {/* Incident assignments */}
          <section className="panel detail-card">
            <div className="panel-heading">
              <div>
                <h2>
                  <Users size={17} /> Incident assignees
                </h2>
                <p>Manage incident ownership</p>
              </div>
            </div>

            {assignmentError && (
              <div className="alert">{assignmentError}</div>
            )}

            {usersUnavailable ? (
              <div className="subtle-empty">
                <p>
                  The user directory could not be loaded. Sign in
                  with an admin account to select users.
                </p>
              </div>
            ) : (
              <div className="stack-form">
                <label>
                  Select user
                  <select
                    value={selectedUserId}
                    onChange={(e) =>
                      setSelectedUserId(e.target.value)
                    }
                  >
                    <option value="">Choose a user</option>

                    {availableUsers.map((user) => (
                      <option key={user.id} value={user.id}>
                        {user.name} ({user.email})
                      </option>
                    ))}
                  </select>
                </label>

                <button
                  type="button"
                  className="primary-btn"
                  disabled={
                    !selectedUserId ||
                    assignmentSaving ||
                    Boolean(assignmentError)
                  }
                  onClick={handleAssign}
                >
                  <UserPlus size={15} />
                  {assignmentSaving ? 'Saving…' : 'Assign user'}
                </button>
              </div>
            )}

            <div className="assignment-list">
              <h3>
                Currently assigned ({activeAssignees.length})
              </h3>

              {activeAssignees.length === 0 ? (
                <div className="subtle-empty">
                  No users assigned to this incident.
                </div>
              ) : (
                activeAssignees.map((item) => {
                  const user = users.find(
                    (candidate) => candidate.id === item.user_id
                  );

                  return (
                    <div className="version-row" key={item.id}>
                      <div>
                        <b>{user?.name || 'Assigned user'}</b>
                        <small>
                          {user?.email || item.user_id}
                        </small>
                      </div>

                      <button
                        type="button"
                        className="secondary-btn"
                        disabled={assignmentSaving}
                        onClick={() =>
                          handleUnassign(item.user_id)
                        }
                      >
                        <UserMinus size={14} /> Unassign
                      </button>
                    </div>
                  );
                })
              )}
            </div>
          </section>

          {/* AI analysis */}
          <section className="panel ai-panel">
            <div className="ai-panel-top">
              <div className="ai-icon">
                <BrainCircuit size={19} />
              </div>

              <div>
                <span className="ai-overline">
                  ASSISTED INVESTIGATION
                </span>
                <h2>AI analysis</h2>
              </div>

              <span className="beta-pill">BETA</span>
            </div>

            <p className="ai-intro">
              Review analysis persisted by the backend. Model
              inference is not assumed to be active.
            </p>

            {analysis ? (
              <div className="analysis-result">
                <div className="analysis-status">
                  <span className="tiny-dot" /> Stored analysis
                  available
                </div>

                {analysis.analysis_type && (
                  <div className="analysis-section">
                    <h3>Analysis type</h3>
                    <p>{analysis.analysis_type}</p>
                  </div>
                )}

                {analysis.root_cause && (
                  <div className="analysis-section">
                    <h3>Root cause</h3>
                    {(Array.isArray(rootCause)
                      ? rootCause
                      : [rootCause]
                    ).map((value, index) => (
                      <p key={index}>{value}</p>
                    ))}
                  </div>
                )}

                {analysis.root_cause_analysis && (
                  <div className="analysis-section">
                    <h3>Root-cause analysis</h3>
                    <p>{analysis.root_cause_analysis}</p>
                  </div>
                )}

                {analysis.suggested_remediation && (
                  <div className="analysis-section">
                    <h3>Suggested remediation</h3>
                    {(Array.isArray(remediations)
                      ? remediations
                      : [remediations]
                    ).map((value, index) => (
                      <p key={index}>{value}</p>
                    ))}
                  </div>
                )}

                {analysis.impact_analysis && (
                  <div className="analysis-section">
                    <h3>Impact</h3>
                    <p>{analysis.impact_analysis}</p>
                  </div>
                )}

                {analysis.confidence != null && (
                  <div className="confidence-row">
                    <span>Confidence</span>
                    <b>
                      {Math.round(
                        Number(analysis.confidence) * 100
                      )}
                      %
                    </b>
                  </div>
                )}

                {analysis.model && (
                  <small className="model-label">
                    Model: {analysis.model}
                  </small>
                )}
              </div>
            ) : (
              <div className="ai-empty">
                <div className="ai-empty-art">
                  <Bot size={25} />
                </div>
                <b>No saved analysis found</b>
                <span>
                  When inference is connected, analysis results can
                  be stored and versioned here.
                </span>
              </div>
            )}

            <div className="analysis-readonly-note">
              <BrainCircuit size={15} />
              <span>
                Analysis is read-only here. Model inference will be
                enabled when the backend ML service is connected.
              </span>
            </div>
          </section>

          {/* Analysis history */}
          <section className="panel version-panel">
            <div className="panel-heading">
              <div>
                <h2>Analysis history</h2>
                <p>Saved versions</p>
              </div>
            </div>

            {versions.length ? (
              versions.map((version, index) => (
                <div
                  className="version-row"
                  key={version.id || index}
                >
                  <span className="version-number">
                    v
                    {version.version_number ||
                      version.version ||
                      index + 1}
                  </span>

                  <div>
                    <b>
                      {version.analysis_type || 'Analysis snapshot'}
                    </b>
                    <small>
                      {version.created_at
                        ? new Date(
                            version.created_at
                          ).toLocaleString()
                        : 'Saved version'}
                    </small>
                  </div>
                </div>
              ))
            ) : (
              <div className="subtle-empty">
                No version history returned.
              </div>
            )}
          </section>
        </aside>
      </div>
    </>
  );
}