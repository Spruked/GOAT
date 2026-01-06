import React, { useState } from 'react';
import './OnboardingFlow.css';

const steps = [
  'welcome',
  'dataSafety',
  'storagePreference',
  'artifactGoal',
  'audience',
  'structure',
  'legal',
  'caleonIntro',
  'begin',
];

export default function OnboardingFlow({ onComplete }) {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState({
    storage: 'temporary',
    goal: '',
    audience: '',
    structure: '',
    legal: [],
  });

  const next = () => setStep((s) => Math.min(s + 1, steps.length - 1));
  const prev = () => setStep((s) => Math.max(s - 1, 0));
  const setField = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  return (
    <div className="onboarding-flow">
      {steps[step] === 'welcome' && (
        <div className="onboarding-card fade-in">
          <h1>Welcome to GOAT — Greatest Of All Time</h1>
          <p>The Engine That Immortalizes Your Greatest Work. Transform your skill, story, and experience into permanent, publishable legacy.</p>
          <button onClick={next}>Begin My Legacy</button>
        </div>
      )}
      {steps[step] === 'dataSafety' && (
        <div className="onboarding-card fade-in">
          <h2>Your Data, Your Rules</h2>
          <ul>
            <li>GOAT does not permanently store your files.</li>
            <li>You can purge anytime.</li>
            <li>You can download all working files.</li>
            <li>You decide if GOAT saves your project temporarily, locally, or not at all.</li>
            <li>Blockchain storage is optional and permanent only when YOU mint it.</li>
          </ul>
          <button onClick={next}>I Understand</button>
        </div>
      )}
      {steps[step] === 'storagePreference' && (
        <div className="onboarding-card fade-in">
          <h2>Choose how your project is stored:</h2>
          <label><input type="radio" name="storage" checked={form.storage==='temporary'} onChange={()=>setField('storage','temporary')} /> Temporary (Default — Private & Secure)</label>
          <label><input type="radio" name="storage" checked={form.storage==='local'} onChange={()=>setField('storage','local')} /> Save on this device only</label>
          <label><input type="radio" name="storage" checked={form.storage==='server'} onChange={()=>setField('storage','server')} /> Long-term (Encrypted GOAT server storage)</label>
          <label><input type="radio" name="storage" checked={form.storage==='blockchain'} onChange={()=>setField('storage','blockchain')} /> Permanent Blockchain Storage (IPFS/Arweave)</label>
          <button onClick={next}>Continue</button>
        </div>
      )}
      {steps[step] === 'artifactGoal' && (
        <div className="onboarding-card fade-in">
          <h2>What do you want to create?</h2>
          <select value={form.goal} onChange={e=>setField('goal',e.target.value)}>
            <option value="">Select...</option>
            <option>Book</option>
            <option>Blueprint Archive</option>
            <option>Audio Legacy</option>
            <option>Personal History / Biography</option>
            <option>Poem Collection</option>
            <option>Content Series</option>
            <option>NFT Archive</option>
            <option>Time Capsule</option>
            <option>Mixed Project</option>
            <option>I’m not sure (Caleon guides)</option>
          </select>
          <button onClick={next} disabled={!form.goal}>Continue</button>
        </div>
      )}
      {steps[step] === 'audience' && (
        <div className="onboarding-card fade-in">
          <h2>Who is this project for?</h2>
          <select value={form.audience} onChange={e=>setField('audience',e.target.value)}>
            <option value="">Select...</option>
            <option>Myself</option>
            <option>My Family</option>
            <option>My Kids/Heirs</option>
            <option>My Audience</option>
            <option>My Customers</option>
            <option>Public Release</option>
            <option>A Private Archive</option>
            <option>I’m not sure</option>
          </select>
          <button onClick={next} disabled={!form.audience}>Continue</button>
        </div>
      )}
      {steps[step] === 'structure' && (
        <div className="onboarding-card fade-in">
          <h2>Choose a structure:</h2>
          <select value={form.structure} onChange={e=>setField('structure',e.target.value)}>
            <option value="">Select...</option>
            <option>Chronological</option>
            <option>Thematic</option>
            <option>Story arc</option>
            <option>Blueprint technical breakdown</option>
            <option>Chapter-based</option>
            <option>Folder-based</option>
            <option>Auto-organized (AI clustering)</option>
            <option>Manual control</option>
          </select>
          <button onClick={next} disabled={!form.structure}>Continue</button>
        </div>
      )}
      {steps[step] === 'legal' && (
        <div className="onboarding-card fade-in">
          <h2>Legal & IP Options</h2>
          <ul>
            <li><label><input type="checkbox" checked={form.legal.includes('copyright')} onChange={e=>setField('legal',e.target.checked?[...form.legal,'copyright']:form.legal.filter(x=>x!=='copyright'))}/> Download copyright form packet</label></li>
            <li><label><input type="checkbox" checked={form.legal.includes('patent')} onChange={e=>setField('legal',e.target.checked?[...form.legal,'patent']:form.legal.filter(x=>x!=='patent'))}/> Download provisional patent packet</label></li>
            <li><label><input type="checkbox" checked={form.legal.includes('workforhire')} onChange={e=>setField('legal',e.target.checked?[...form.legal,'workforhire']:form.legal.filter(x=>x!=='workforhire'))}/> Download work-for-hire agreements</label></li>
            <li><label><input type="checkbox" checked={form.legal.includes('release')} onChange={e=>setField('legal',e.target.checked?[...form.legal,'release']:form.legal.filter(x=>x!=='release'))}/> Download release forms</label></li>
            <li><label><input type="checkbox" checked={form.legal.includes('ipchecklist')} onChange={e=>setField('legal',e.target.checked?[...form.legal,'ipchecklist']:form.legal.filter(x=>x!=='ipchecklist'))}/> Add IP protection checklist</label></li>
            <li><label><input type="checkbox" checked={form.legal.includes('skip')} onChange={e=>setField('legal',e.target.checked?[...form.legal,'skip']:form.legal.filter(x=>x!=='skip'))}/> Skip for now</label></li>
          </ul>
          <button onClick={next}>Continue</button>
        </div>
      )}
      {steps[step] === 'caleonIntro' && (
        <div className="onboarding-card fade-in">
          <h2>Meet Caleon, Your Creation Guide</h2>
          <p>"My purpose is simple: I help you create the greatest work of your life — and preserve it forever.<br />Tell me what you want to build, and I will guide you step by step."</p>
          <button onClick={next}>Start My Legacy</button>
        </div>
      )}
      {steps[step] === 'begin' && (
        <div className="onboarding-card fade-in">
          <h2>Ready to Create Your Legacy</h2>
          <p>Upload your data, share your knowledge, or start fresh.<br />Together with Caleon, we'll build something that lasts forever.</p>
          <button onClick={()=>onComplete(form)}>Begin My Greatest Work</button>
        </div>
      )}
      {step > 0 && step < steps.length-1 && (
        <button className="onboarding-back" onClick={prev}>Back</button>
      )}
    </div>
  );
}
