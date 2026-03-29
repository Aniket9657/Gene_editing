import { useState } from "react";

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const res = await fetch(`http://127.0.0.1:8000/chat?q=${input.trim()}`);
      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        { role: "bot", text: data.response || "No response from server." },
      ]);
    } catch (err) {
      console.error("Chat fetch error:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "❌ Sorry, I couldn't reach the backend. Is the server running on http://127.0.0.1:8000?",
        },
      ]);
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", color: "#e8f5e8" }}>
      {/* Messages area */}
      <div
        style={{
          flex: "1",
          padding: "1.5rem",
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
        }}
      >
        {messages.length === 0 ? (
          <div
            style={{
              textAlign: "center",
              color: "#90be6d",
              fontSize: "1.1rem",
              marginTop: "2rem",
              opacity: 0.8,
            }}
          >
            🌿 Ask me about Gondia, Nagzira Wildlife, Hazra Falls...
          </div>
        ) : (
          messages.map((m, i) => (
            <div
              key={i}
              style={{
                alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                maxWidth: "75%",
                padding: "1rem 1.2rem",
                borderRadius: "20px",
                background: m.role === "user" 
                  ? "linear-gradient(135deg, #4a7c59, #667eea)" 
                  : "rgba(40, 60, 40, 0.8)",
                color: "white",
                fontSize: "0.95rem",
                lineHeight: 1.5,
                boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
              }}
            >
              {m.text}
            </div>
          ))
        )}
      </div>

      {/* Input area */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          padding: "1.2rem",
          background: "rgba(18, 35, 18, 0.9)",
          borderTop: "1px solid rgba(144, 190, 109, 0.3)",
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about Gondia nature..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{
            flex: "1",
            padding: "0.9rem 1.2rem",
            borderRadius: "25px",
            background: "rgba(50, 70, 50, 0.9)",
            border: "1px solid rgba(144, 190, 109, 0.3)",
            color: "#e8f5e8",
            outline: "none",
            fontSize: "1rem",
          }}
        />
        <button
          onClick={sendMessage}
          disabled={!input.trim()}
          style={{
            padding: "0.9rem 1.5rem",
            borderRadius: "25px",
            background: input.trim() 
              ? "linear-gradient(135deg, #4a7c59, #90be6d)" 
              : "rgba(74, 124, 89, 0.4)",
            color: "white",
            border: "none",
            fontWeight: "600",
            cursor: input.trim() ? "pointer" : "not-allowed",
            opacity: input.trim() ? 1 : 0.6,
            transition: "all 0.2s ease",
            fontSize: "0.95rem",
            minWidth: "80px",
          }}
        >
          Send →
        </button>
      </div>
    </div>
  );
}