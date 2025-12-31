export function validateEmail(email) {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@gmail\.com$/;
  return emailRegex.test(email.trim().toLowerCase());
}

export function validatePassword(password) {
  // Password must be at least 8 characters
  return typeof password === 'string' && password.length >= 8;
}

export async function handleLogin(email, password) {
  if (!validateEmail(email)) {
    return { success: false, message: "Please enter a valid email address." };
  }
  if (!validatePassword(password)) {
    return { success: false, message: "Password must be at least 8 characters long." };
  }

  try {
    const NODE_API_URL = import.meta.env.VITE_NODE_API_URL || 'http://localhost:5002/api/summaries';
    const apiBase = NODE_API_URL.replace('/api/summaries', '/api');
    const response = await fetch(`${apiBase}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // Store user email in localStorage for future use
      localStorage.setItem('userEmail', email);
      return { success: true, message: data.message, user: data.user };
    } else {
      return { success: false, message: data.message };
    }
  } catch (error) {
    return { success: false, message: "Failed to connect to server. Please try again." };
  }
}
