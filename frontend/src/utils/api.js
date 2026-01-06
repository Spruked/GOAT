// Utility for project API calls
export async function downloadProjectZip(projectId) {
  const res = await fetch(`/api/project/export?project_id=${encodeURIComponent(projectId)}`, {
    method: 'POST',
    headers: { 'X-API-Key': 'goat_dev_key' },
  });
  if (!res.ok) throw new Error('Failed to download project ZIP');
  return res;
}

export async function uploadProjectZip(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch('/api/project/resume', {
    method: 'POST',
    headers: { 'X-API-Key': 'goat_dev_key' },
    body: formData,
  });
  if (!res.ok) throw new Error('Failed to resume project');
  return res.json();
}
