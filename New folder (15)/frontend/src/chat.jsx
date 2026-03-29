import { useState } from "react";

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input) return;

    const userMsg = { role: "user", text: input };
    setMessages([...messages, userMsg]);

    const res = await fetch(`http://127.0.0.1:8000/chat?q=${input}`);
    const data = await res.json();

    const botMsg = { role: "bot", text: data.response };

    setMessages((prev) => [...prev, botMsg]);
    setInput("");
  };

  return (
    <div className="chat-container">
      <h1 className="title">⚡ AI RAG Assistant</h1>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role}>
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-box">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}