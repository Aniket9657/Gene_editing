import { useState, useEffect } from "react";
import Chat from "./Chat";

export default function App() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div style={{ minHeight: "100vh", position: "relative", fontFamily: "'Inter', system-ui, sans-serif", color: "#e8f5e8", overflowX: "hidden" }}>
      
      {/* Background images - put your images in src/assets/ */}
      <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", zIndex: 1, pointerEvents: "none" }}>
        <div style={{
          position: "absolute", top: "10%", right: "5%", width: "400px", height: "500px",
          backgroundImage: `url(/src/assets/hazra-fall.jpg)`, backgroundSize: "cover", backgroundPosition: "center",
          filter: "brightness(0.4) blur(1px)", opacity: 0.6, transform: `translateY(${scrollY * 0.2}px)`, borderRadius: "20px"
        }} />
        <div style={{
          position: "absolute", bottom: "15%", left: "8%", width: "300px", height: "400px",
          backgroundImage: `url(/src/assets/nagzira-wildlife-sanctuary.jpg)`, backgroundSize: "cover", backgroundPosition: "center",
          filter: "brightness(0.35) blur(0.8px)", opacity: 0.5, transform: `translateY(${scrollY * 0.1}px) rotate(-2deg)`, borderRadius: "24px"
        }} />
        <div style={{
          position: "absolute", top: "20%", left: "15%", width: "250px", height: "300px",
          backgroundImage: `url(/src/assets/beautiful-cave-it-is.jpg)`, backgroundSize: "cover", backgroundPosition: "center",
          filter: "brightness(0.45) blur(1px)", opacity: 0.4, transform: `translateY(${scrollY * 0.3}px) rotate(3deg)`, borderRadius: "20px"
        }} />
      </div>

      <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none", zIndex: 2, opacity: 0.3 }}>
        <div style={{ position: "absolute", width: "20px", height: "30px", background: "#4a7c59", clipPath: "polygon(50% 0%, 0% 60%, 20% 100%, 80% 100%, 100% 60%)", animation: "float 8s ease-in-out infinite", left: "10%", top: "20%", animationDelay: "0s" }} />
        <div style={{ position: "absolute", width: "18px", height: "28px", background: "#5d9a6a", clipPath: "polygon(50% 0%, 0% 60%, 20% 100%, 80% 100%, 100% 60%)", animation: "float 10s ease-in-out infinite reverse", right: "20%", top: "40%", animationDelay: "3s" }} />
      </div>

      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          33% { transform: translateY(-15px) rotate(120deg); }
          66% { transform: translateY(-8px) rotate(240deg); }
        }
      `}</style>

      <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", background: "linear-gradient(135deg, rgba(6, 27, 14, 0.75), rgba(12, 44, 22, 0.85))", zIndex: 3 }} />

      <div style={{ position: "relative", zIndex: 10, maxWidth: "1000px", margin: "0 auto", padding: "2rem 1.5rem", minHeight: "100vh", display: "flex", flexDirection: "column", justifyContent: "center" }}>
       {/* Header - Fixed clipping */}
<header
  style={{
    textAlign: "center",
    marginBottom: "2.5rem",
    padding: "2rem 1rem 1rem",
    position: "relative",
    zIndex: 20,
  }}
>
  <div
    style={{
      fontSize: "clamp(2rem, 6vw, 3.2rem)", // Responsive + prevents overflow
      fontWeight: "800",
      lineHeight: 1.1,
      background: "linear-gradient(135deg, #4a7c59, #90be6d, #2d5a3a)",
      WebkitBackgroundClip: "text",
      WebkitTextFillColor: "transparent",
      textShadow: "0 8px 32px rgba(74, 124, 89, 0.6)",
      marginBottom: "1rem",
      padding: "0.5rem 1rem", // Extra padding around text
      display: "inline-block",
    }}
  >
    🌿 Gondia AI Guide
  </div>
  <p
    style={{
      fontSize: "clamp(1rem, 3vw, 1.25rem)",
      opacity: 0.95,
      maxWidth: "550px",
      margin: "0 auto",
      lineHeight: 1.6,
      padding: "0 1rem",
    }}
  >
    Discover Nagzira, Hazra Falls & Gondia's wilderness
  </p>
</header>

        <main style={{
          background: "rgba(12, 44, 22, 0.95)", backdropFilter: "blur(25px)",
          border: "1px solid rgba(144, 190, 109, 0.4)", borderRadius: "28px",
          boxShadow: "0 25px 70px rgba(0,0,0,0.7), 0 0 0 1px rgba(144, 190, 109, 0.3), inset 0 1px 0 rgba(144, 190, 109, 0.2)",
          maxWidth: "850px", margin: "0 auto", height: "600px", overflow: "hidden"
        }}>
          <Chat />
        </main>
      </div>
    </div>
  );
}