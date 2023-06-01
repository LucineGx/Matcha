import React, { useRef } from 'react'

const ScrollableTextBox = () => {
  const textBoxRef = useRef(null)

  const scrollToBottom = () => {
    textBoxRef.current.scrollTop = textBoxRef.current.scrollHeight
  }

  return (
    <div>
      <div ref={textBoxRef} className="scrollable-text-box">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </div>
      <button onClick={scrollToBottom}>Banana</button>
    </div>
  )
}

export default ScrollableTextBox
