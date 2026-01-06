import axios from 'axios';

export async function createProjectFromOnboarding(form) {
  // Map onboarding form to backend payload
  const payload = {
    project_id: form.project_id || (form.owner + '_' + Date.now()),
    owner: form.owner || 'user',
    title: form.title || 'Untitled Project',
    artifact_goal: form.goal,
    audience: form.audience,
    structure_type: form.structure,
    retention_mode: form.storage,
    onboarding_selections: form,
  };
  const res = await axios.post('/api/project/create_from_onboarding', payload, {
    headers: { 'X-API-Key': 'goat_dev_key' },
  });
  return res.data;
}
