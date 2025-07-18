// // this UI is for using playwright
// import React, { useState, useEffect, useRef } from 'react';
// import axios from 'axios';

// function Chat() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState('');
//   const [isListening, setIsListening] = useState(false);
//   const [isLoading, setIsLoading] = useState(false);
//   const [screenshots, setScreenshots] = useState([]);
//   const recognitionRef = useRef(null);
//   const messagesEndRef = useRef(null);

//   useEffect(() => {
//     if ('webkitSpeechRecognition' in window) {
//       recognitionRef.current = new window.webkitSpeechRecognition();
//       recognitionRef.current.continuous = false;
//       recognitionRef.current.interimResults = false;
//       recognitionRef.current.onresult = (event) => {
//         const transcript = event.results[0][0].transcript;
//         setInput(transcript);
//         handleSend(transcript);
//       };
//       recognitionRef.current.onend = () => setIsListening(false);
//     }
//   }, []);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   const handleSend = async (text = input) => {
//     if (!text.trim()) return;

//     const userMessage = { text, sender: 'user' };
//     setMessages((prev) => [...prev, userMessage]);
//     setInput('');
//     setIsLoading(true);

//     try {
//       const response = await axios.post('http://localhost:8000/chat', { message: text });
//       const { reply, screenshots } = response.data;
//       let botMessage = 'Error: Invalid response format';
//       if (typeof reply === 'string') {
//         botMessage = reply;
//       } else if (reply && typeof reply === 'object') {
//         botMessage = reply.reply || JSON.stringify(reply);
//       }
//       setMessages((prev) => [...prev, { text: botMessage, sender: 'bot' }]);
//       if (screenshots && Array.isArray(screenshots)) {
//         setScreenshots((prev) => [...prev, ...screenshots]);
//       }
//     } catch (error) {
//       console.error('Error fetching response:', error.response?.data || error.message);
//       let errorMessage = 'Error: Could not connect to backend or send email. Please try again.';
//       if (error.response?.data) {
//         if (error.response.data.detail && typeof error.response.data.detail === 'string') {
//           errorMessage = error.response.data.detail;
//         } else if (error.response.data.detail && Array.isArray(error.response.data.detail)) {
//           errorMessage = error.response.data.detail.map((d) => d.msg).join(', ');
//         } else {
//           errorMessage = JSON.stringify(error.response.data);
//         }
//       } else if (error.message) {
//         errorMessage = error.message;
//       }
//       setMessages((prev) => [...prev, { text: errorMessage, sender: 'bot' }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const toggleVoiceInput = () => {
//     if (!recognitionRef.current) {
//       setMessages((prev) => [
//         ...prev,
//         { text: 'Voice input not supported in this browser.', sender: 'bot' },
//       ]);
//       return;
//     }

//     if (isListening) {
//       recognitionRef.current.stop();
//     } else {
//       recognitionRef.current.start();
//       setIsListening(true);
//     }
//   };

//   return (
//     <div className="flex flex-col h-[80vh] bg-white rounded-lg shadow-lg">
//       <div className="flex-1 p-4 overflow-y-auto">
//         {messages.map((msg, index) => (
//           <div
//             key={index}
//             className={`mb-3 p-3 rounded-lg max-w-md ${
//               msg.sender === 'user' ? 'bg-blue-500 text-white ml-auto' : 'bg-gray-200 text-black mr-auto'
//             }`}
//           >
//             {msg.text}
//           </div>
//         ))}
//         {isLoading && (
//           <div className="mb-3 p-3 rounded-lg max-w-md bg-gray-200 text-black mr-auto">
//             Bot is thinking...
//           </div>
//         )}
//         {screenshots.map((src, index) => (
//           <div key={`screenshot-${index}`} className="mb-3 max-w-md mx-auto">
//             <img src={src} alt={`Screenshot ${index + 1}`} className="w-full rounded-lg shadow" />
//           </div>
//         ))}
//         <div ref={messagesEndRef} />
//       </div>
//       <div className="p-4 bg-gray-50 border-t flex items-center gap-2">
//         <input
//           type="text"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           onKeyPress={(e) => e.key === 'Enter' && handleSend()}
//           placeholder="Type your message (e.g., 'Send a hi mail to mounikareddyboggari@gmail.com her name is Mounika')"
//           className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
//         />
//         <button
//           onClick={toggleVoiceInput}
//           className={`p-2 rounded-full ${isListening ? 'bg-red-500' : 'bg-blue-500'} text-white hover:opacity-80`}
//         >
//           <svg
//             className="w-6 h-6"
//             fill="none"
//             stroke="currentColor"
//             viewBox="0 0 24 24"
//             xmlns="http://www.w3.org/2000/svg"
//           >
//             <path
//               strokeLinecap="round"
//               strokeLinejoin="round"
//               strokeWidth="2"
//               d={isListening ? 'M6 18L18 6M6 6l12 12' : 'M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z'}
//             />
//           </svg>
//         </button>
//       </div>
//     </div>
//   );
// }

// export default Chat;









// // this UI for smtp


import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [screenshots, setScreenshots] = useState([]);
  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window) {
      recognitionRef.current = new window.webkitSpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        handleSend(transcript);
      };
      recognitionRef.current.onend = () => setIsListening(false);
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, screenshots]);

  const handleSend = async (text = input) => {
    if (!text.trim()) return;
    const userMessage = { text, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setScreenshots([]);

    try {
      const response = await axios.post('http://localhost:8000/chat', { message: text });
      const { reply, screenshots: newScreenshots } = response.data;
      setMessages((prev) => [...prev, { text: reply, sender: 'bot' }]);
      if (newScreenshots && Array.isArray(newScreenshots)) {
        setScreenshots((prev) => [...prev, ...newScreenshots.map(src => `/mock/${src}`)]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { text: '❌ Error: ' + (error.response?.data?.detail || error.message), sender: 'bot' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      setMessages((prev) => [...prev, { text: 'Voice input not supported.', sender: 'bot' }]);
      return;
    }
    if (isListening) recognitionRef.current.stop();
    else recognitionRef.current.start();
    setIsListening(!isListening);
  };

  return (
    <div className="flex flex-col h-[80vh] bg-white rounded-lg shadow-lg">
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-3 p-3 rounded-lg max-w-md ${msg.sender === 'user' ? 'bg-blue-500 text-white ml-auto' : 'bg-gray-200 text-black mr-auto'}`}>
            {msg.text.split('\n').map((line, i) => (
              <p key={i} className="break-words">{line}</p>
            ))}
          </div>
        ))}
        {isLoading && <div className="mb-3 p-3 rounded-lg max-w-md bg-gray-200 text-black mr-auto">Bot is thinking...</div>}
        {screenshots.map((src, idx) => (
          <div key={idx} className="mb-3 max-w-md mx-auto">
            <img src={src} alt={`Screenshot ${idx + 1}`} className="w-full h-auto rounded-lg shadow" />
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 bg-gray-50 border-t flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message (e.g., 'Send a leave application email' or 'Send email to hr@company.com for leave August 15-20')"
          className="flex-1 p-2 border rounded-lg"
        />
        <button onClick={toggleVoiceInput} className={`p-2 rounded-full ${isListening ? 'bg-red-500' : 'bg-blue-500'} text-white`}>
          🎤
        </button>
      </div>
    </div>
  );
}

export default Chat;


