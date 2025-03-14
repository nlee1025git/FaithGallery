'use client';
import { useEffect, useState } from 'react';

export default function Home() {
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    fetch('/api')  // Relative URL, should resolve to https://myaddress.com/api
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => {
        console.error('Fetch error:', error);
        setMessage('Error connecting to backend');
      });
  }, []);

  return (
    <div>
      <h1>My Web App!</h1>
      <p>{message}</p>
    </div>
  );
}
