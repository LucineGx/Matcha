import '../styles/globals.css'
import * as React from 'react'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

function MyApp({ Component, pageProps }) {
  return (
    <div>
      <Component {...pageProps} />
      <ToastContainer
          position="bottom-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnBottom={false}
          draggable={false}
          pauseOnVisibilityChange
          closeOnClick
          pauseOnHover
      />
    </div>
  )
}

export default MyApp
