import { useState } from "react";
import Message from "./Message";
import InputBox from "./InputBox";
import Loader from "./Loader";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text) => {
    if (!text) return;

    // add user message
    setMessages(prev => [...prev, { role: "user", text }]);
    setLoading(true);

    try {
      const res = await fetch(`http://127.0.0.1:8000/chat?q=${text}`);
      const data = await res.json();

      setMessages(prev => [...prev, { role: "bot", text: data.response }]);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, i) => (
          <Message key={i} role={msg.role} text={msg.text} />
        ))}

        {loading && <Loader />}
      </div>

      <InputBox onSend={sendMessage} />
    </div>
  );
}