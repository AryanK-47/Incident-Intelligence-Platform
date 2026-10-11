import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Activity, ArrowRight, Eye, EyeOff, LockKeyhole, RadioTower } from 'lucide-react';
import { login } from '../api/auth';
import { errorMessage } from '../api/client';

export default function Login() {
  const [form, setForm] = useState({ username: '', password: '' });
  const [show, setShow] = useState(false); const [busy, setBusy] = useState(false); const [error, setError] = useState('');
  const navigate = useNavigate();
  const submit = async (e) => {
    e.preventDefault(); setBusy(true); setError('');
    try { const data = await login(form); if (!localStorage.getItem('access_token')) { setError('Login response mein access token nahi mila. /docs mein response schema check karo.'); return; } navigate('/'); }
    catch (err) { setError(errorMessage(err)); } finally { setBusy(false); }
  };
  return <div className="login-page"><div className="login-visual"><div className="login-brand"><div className="brand-icon"><RadioTower size={22}/></div><b>incident<span>IQ</span></b></div><div className="visual-content"><div className="eyebrow"><span className="pulse-dot"/> INCIDENT RESPONSE, REIMAGINED</div><h1>When systems fail,<br/><em>clarity comes first.</em></h1><p>One workspace to detect, investigate, and resolve production incidents with confidence.</p><div className="visual-stats"><div><b><Activity size={16}/> Real-time visibility</b><small>See your incidents at a glance</small></div><div><b><LockKeyhole size={16}/> Secure by design</b><small>Authenticated access to your workspace</small></div></div></div><div className="visual-footer">INCIDENT INTELLIGENCE PLATFORM <span>·</span> V1.0</div></div><div className="login-panel"><form className="login-form" onSubmit={submit}><div className="mobile-login-brand"><div className="brand-icon"><RadioTower size={20}/></div><b>incident<span>IQ</span></b></div><div className="form-kicker">WELCOME BACK</div><h2>Sign in to your workspace</h2><p className="muted">Enter your account details to continue.</p>{error && <div className="alert error">{error}</div>}<label>Username or email<input autoComplete="username" required value={form.username} onChange={e=>setForm({...form, username:e.target.value})} placeholder="Enter your username"/></label><label>Password<div className="password-wrap"><input autoComplete="current-password" type={show?'text':'password'} required value={form.password} onChange={e=>setForm({...form,password:e.target.value})} placeholder="Enter your password"/><button type="button" className="password-toggle" onClick={()=>setShow(!show)}>{show?<EyeOff size={17}/>:<Eye size={17}/>}</button></div></label><button className="primary-btn login-submit" disabled={busy}>{busy?'Signing in…':'Sign in'} <ArrowRight size={17}/></button><div className="login-note"><LockKeyhole size={14}/> Your session is protected by token-based authentication.</div></form><div className="login-bottom">Having trouble? Check that the backend is running at your configured API URL.</div></div></div>;
}
