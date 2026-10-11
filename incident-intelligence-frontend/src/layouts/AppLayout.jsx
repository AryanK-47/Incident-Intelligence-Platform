import React from 'react';
import { NavLink, Outlet, useNavigate, useLocation } from 'react-router-dom';
import {
  Activity,
  LayoutDashboard,
  Siren,
  LogOut,
  PlusCircle,
} from 'lucide-react';
import { logout } from '../api/auth';

export default function AppLayout() {
  const navigate = useNavigate();
  const location = useLocation();

  const leave = () => {
    logout();
    navigate('/login');
  };

  const page = location.pathname.startsWith('/incidents/')
    ? 'Incident details'
    : location.pathname === '/incidents'
      ? 'Incident queue'
      : 'Overview';

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Activity size={21} />
          </div>

          <div>
            <b>
              incident<span>IQ</span>
            </b>
            <small>INCIDENT INTELLIGENCE</small>
          </div>
        </div>

        <div className="workspace">
          <div className="workspace-mark">P</div>
          <div>
            <b>Production</b>
            <small>Incident workspace</small>
          </div>
        </div>

        <div className="nav-label">OPERATIONS</div>

        <nav className="nav">
          <NavLink to="/" end>
            <LayoutDashboard size={17} />
            Overview
          </NavLink>

          <NavLink to="/incidents">
            <Siren size={17} />
            Incident queue
          </NavLink>
        </nav>

        <button
          className="sidebar-create"
          onClick={() => navigate('/incidents?create=1')}
        >
          <PlusCircle size={16} />
          Create incident
        </button>

        <div className="sidebar-bottom">
          <div className="workspace-hint">
            <Activity size={15} />
            <div>
              <b>Response workspace</b>
              <small>Track, triage and resolve incidents</small>
            </div>
          </div>

          <button className="profile" onClick={leave}>
            <div className="avatar">A</div>
            <div className="profile-text">
              <b>Incident Operator</b>
              <small>Sign out</small>
            </div>
            <LogOut size={16} />
          </button>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumbs">
            <span>Workspace</span>
            <span className="crumb-slash">/</span>
            <b>{page}</b>
          </div>

          <div className="topbar-right">
            <span className="workspace-chip">
              <i />
              Production workspace
            </span>
            <span className="top-avatar">A</span>
          </div>
        </header>

        <div className="page-wrap">
          <Outlet />
        </div>

        <footer className="footer">
          <span>
            incidentIQ <span className="footer-dot">·</span>{' '}
            Incident response workspace
          </span>
          <span>Incident records are served by your API</span>
        </footer>
      </main>
    </div>
  );
}