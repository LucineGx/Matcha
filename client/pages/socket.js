import io from 'socket.io-client'

export default function Socket() {
  const socket = io('http://127.0.0.1:5000/', {
    reconnection: true,
  })
  console.log("Connecting to socket")
  socket.connect()
  console.log("Socket connected")
  socket.on("HelloWorld", message => {
    console.log("HelloWorld", message)
  })
  return (
    <>
      hello
    </>
  )
}