// Host Bubble API utility
export async function hostBubbleGreet(userId) {
  const res = await fetch('/api/v1/host_bubble/greet', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId }),
  });
  if (!res.ok) throw new Error('Failed to greet user');
  return res.json();
}

export async function hostBubbleMessage(userId, message, contextHints = null) {
  const res = await fetch('/api/v1/host_bubble/message', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, message, context_hints: contextHints }),
  });
  if (!res.ok) throw new Error('Failed to send message');
  return res.json();
}
