import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = "http://localhost:8000"; // <--- CHANGE THIS

export default function App() {
  const [recording, setRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [transcription, setTranscription] = useState("");
  const [assistantReply, setAssistantReply] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);

  /* 🎙️ Start recording */
  const startRecording = async () => {
    setRecording(true);
    audioChunks.current = [];

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorderRef.current = mediaRecorder;

    mediaRecorder.ondataavailable = (e) => audioChunks.current.push(e.data);

    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks.current, { type: "audio/webm" });
      const url = URL.createObjectURL(blob);
      setAudioURL(url);

      uploadAudio(blob);
    };

    mediaRecorder.start();
  };

  /* ⏹ Stop */
  const stopRecording = () => {
    setRecording(false);
    mediaRecorderRef.current.stop();
  };

  /* ⬆️ Upload audio */
  const uploadAudio = async (blob) => {
    const fd = new FormData();
    fd.append("file", blob, "audio.webm");

    const res = await axios.post(`${BACKEND_URL}/upload_audio/`, fd);
    setTranscription(res.data.transcription);
  };

  /* 🤖 Ask AI */
  const sendToAI = async () => {
    setIsTyping(true);
    const fd = new FormData();
    fd.append("message", transcription);

    const res = await axios.post(`${BACKEND_URL}/chat/`, fd);

    setTimeout(() => {
      setAssistantReply(res.data.reply);
      setIsTyping(false);
    }, 500);
  };

  /* ⏰ Save reminder */
  const saveReminder = async () => {
    const fd = new FormData();
    fd.append("message", transcription);

    const res = await axios.post(`${BACKEND_URL}/set_reminder/`, fd);

    if (res.data.error) {
      alert("⚠️ " + res.data.error);
    } else {
      alert("✅ Reminder saved! Twilio will call you at the time you set.");
    }
  };

  return (
    <div className="min-h-screen px-4 py-8 flex flex-col items-center text-white relative">

      {/* Background glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-800/20 via-black to-purple-900/20 blur-3xl"></div>

      <h1 className="text-4xl font-bold mb-10 text-center bg-gradient-to-r from-purple-400 to-blue-400 text-transparent bg-clip-text">
        Nexora Voice Productivity Assistant
      </h1>

      <div className="w-full max-w-2xl bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl p-7 shadow-2xl">

        {/* Mic Section */}
        <div className="flex flex-col items-center mb-6">
          <button
            onClick={recording ? stopRecording : startRecording}
            className={`
              w-32 h-32 rounded-full flex items-center justify-center shadow-xl transition-all
              ${recording 
                ? "bg-red-500 animate-pulse shadow-red-500/50" 
                : "bg-gradient-to-r from-purple-500 to-indigo-500 hover:scale-110 shadow-purple-500/40"
              }
            `}
          >
            <span className="text-4xl">{recording ? "⏹" : "🎤"}</span>
          </button>

          <p className="mt-4 text-gray-300">
            {recording ? "Listening..." : "Tap the mic to speak"}
          </p>

          {/* Wave animation */}
          {recording && (
            <div className="mt-4 flex gap-1">
              {[1,2,3,4,5].map((i) => (
                <div key={i} className="w-2 h-8 bg-purple-500 animate-bounce"
                     style={{ animationDelay: `${i * 0.1}s` }}></div>
              ))}
            </div>
          )}
        </div>

        {/* Audio Preview */}
        {audioURL && (
          <audio controls src={audioURL} className="w-full mb-5 rounded-lg" />
        )}

        {/* Transcription Bubble */}
        {transcription && (
          <div className="bg-black/40 p-4 rounded-xl border border-purple-700/40 mb-4 animate-fadeIn">
            <h2 className="font-semibold mb-1 text-purple-300">📝 You said</h2>
            <p className="text-gray-200">{transcription}</p>
          </div>
        )}

        {/* AI Response */}
        {isTyping && (
          <div className="bg-black/40 p-4 rounded-xl border border-blue-700/40 mb-4 animate-fadeIn">
            <p className="text-blue-300 italic">Assistant is typing...</p>
          </div>
        )}

        {assistantReply && (
          <div className="bg-black/40 p-4 rounded-xl border border-blue-700/40 mb-4 animate-fadeIn">
            <h2 className="font-semibold mb-1 text-blue-300">🤖 Assistant</h2>
            <p className="text-gray-200">{assistantReply}</p>
          </div>
        )}

        {/* Buttons */}
        {transcription && (
          <div className="flex gap-4 mt-6">
            <button
              onClick={sendToAI}
              className="flex-1 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:scale-105 transition text-lg shadow-lg"
            >
              Ask AI 💬
            </button>

            <button
              onClick={saveReminder}
              className="flex-1 py-3 rounded-xl bg-gradient-to-r from-green-600 to-teal-600 hover:scale-105 transition text-lg shadow-lg"
            >
              Save Reminder ⏰
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
