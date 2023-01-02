import { useEffect, useState } from 'react'

function ChatPopup() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')

  useEffect(() => {
    // Connect to the WebSocket server
    const ws = new WebSocket('ws://localhost:8080')

    // Add a message to the messages array when a message is received from the server
    ws.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data])
    }

    // Return a cleanup function that closes the WebSocket connection when the component unmounts
    return () => {
      ws.close()
    }
  }, [])

  // Handle the submit event for the chat form
  const handleSubmit = (event) => {
    event.preventDefault()

    // Send the input message to the WebSocket server
    ws.send(input)

    // Clear the input field
    setInput('')
  }

  return (
    <div style={{
      backgroundColor: 'blue'
    }}>
      {/* Display the chat messages */}
      <div>
        {messages.map((message) => (
          <div key={message}>{message}</div>
        ))}
      </div>

      {/* Set up the chat form */}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={(event) => setInput(event.target.value)} />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}

export default ChatPopup;