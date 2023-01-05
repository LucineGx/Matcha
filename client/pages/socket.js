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
  socket.on("NewLike", message => {
    console.log("New like: ", message)
  })
  socket.on("LikeBack", message => {
    console.log("Like Back: ", message)
  })
  socket.on("LostLike", message => {
    console.log("Lost Like: ", message)
  })
  socket.on("NewVisit", message => {
    console.log("New Visit: ", message)
  })
  socket.on("NewMessage", message => {
    console.log("New Message: ", message)
  })
  return (
    <>
      hello
    </>
  )
}