import io from 'socket.io-client'

export default function Socket() {
  const socket = io.connect('http://127.0.0.1:5000/', {
    reconnection: true,
  })
  socket.on("responseMessage", message => {
    console.log("responseMessage", message)
  })
  return (
    <>
      hello
    </>
  )
}