import React from 'react';
import Chat from './components/Chat';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 text-center shadow-md">
        <h1 className="text-2xl font-bold">Conversational Email Assistant</h1>
      </header>
      <main className="container mx-auto p-4">
        <Chat />
      </main>
    </div>
  );
}

export default App;