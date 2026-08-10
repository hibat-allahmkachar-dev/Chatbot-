import { useState, useEffect, useRef } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { text: input, sender: 'user' }]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input }),
      });
      const data = await response.json();
      setMessages((prev) => [...prev, { text: data.response, sender: 'bot', intent: data.intent }]);
    } catch {
      setMessages((prev) => [...prev, { text: 'Erreur de connexion.', sender: 'bot' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="messages">
        {messages.map((m, i) => <div key={i} className={m.sender}>{m.text}</div>)}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={sendMessage}>
        <input value={input} onChange={(e) => setInput(e.target.value)} disabled={loading} />
        <button type="submit" disabled={loading}>Envoyer</button>
      </form>
    </div>
  );
}

export default App;