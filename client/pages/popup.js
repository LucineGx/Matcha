import React, { useState } from 'react'

const Popup = () => {
  const [isOpen, setIsOpen] = useState(false)

  const togglePopup = () => {
    setIsOpen(!isOpen)
  }

  return (
    <div>
      {isOpen && (
        <div className="popup">
          <div className="popup-top-row">
            <div className="popup-title">Chat</div>
            <div className="popup-close-button" onClick={togglePopup}>
              &times;
            </div>
          </div>
          <div className="popup-content">
            {/* Chat content goes here */}
          </div>
        </div>
      )}
      <button onClick={togglePopup}>Open Chat</button>
    </div>
  )
}

export default Popup
