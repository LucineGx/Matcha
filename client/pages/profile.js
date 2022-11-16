import Head from 'next/head'
import Image from 'next/image'
import React, { useEffect, useState } from 'react'
import styles from '../styles/Home.module.css'
import { toast } from 'react-toastify'
import Error from 'next/error'
import { pushRequest } from './api/apiUtils'
import { formatBase64Jpeg } from './api/formatBase64Jpeg'

const notify = (txt) => toast(txt)

/**
 * @type {{ [key:string]: React.CSSProperties }}
 */
const jsxStyles = {
  mainDiv: {
    border: 'solid',
    borderColor: 'green',
    backgroundColor: 'grey',
    borderRadius: '2rem',
    display: 'flex',
    flexDirection: 'column',
    minHeight: '60vh',
    minWidth: '40vw',
    alignItems: 'center',
    justifyContent: 'space-evenly'
  },
  pictureNameTopRow: {
    fontSize: '5vh',
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
  },
  profilePicture: {
    borderRadius: '100%',
    width: '20vh',
    margin: '15px',
    position: 'static',
  },
  biography: {
    border: 'solid',
    borderColor: 'white',
    backgroundColor: '#ffffff90',
    borderRadius: '2rem',
    padding: '10px',
    inlineSize: '30vw',
    overflow: 'hidden',
  }
}

const logout = async () => {
  const requestOption = {
    method: 'GET',
    // credentials: 'same-origin',
    credentials: 'include',
    mode: 'cors'
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/auth/logout', requestOption)
    notify(await response.text())
    localStorage.removeItem('userInfo')
    window.location.href = '/login'
  } catch (e) {
    console.error(e)
  }
}

/** @typedef {import('./type/userInfo').UserInfo} UserInfo*/

export default function Profile() {
  /**
   * @type {UserInfo}
   */
  let lol = {}
  /** @type {[UserInfo, import('react').Dispatch<import('react').SetStateAction<{}>>]} */
  const [user, setUser] = useState(/** @type {UserInfo}*/lol)
  if (typeof window === "undefined") {
    //bypass ssr
    return null
  } else {
      useEffect( () => {
        pushRequest('user/', 'GET')
          .then((data) => {
            setUser(data)
          })
      }, [] )
      if (!user)
        window.location.href = '/login'
      if (user && user.picture) {
        user.picture = formatBase64Jpeg(user.picture)
      }
      return (
        <div className={styles.container} style={{}}>
          <Head>
            <title>Pokélove</title>
            <meta name="description" content="Generated by a lot of redbull" />
            <link rel="icon" href="/logo.png" />
          </Head>
          <button onClick={logout}>
              logout
          </button>
          <div className={styles.main}>
            <form style={jsxStyles.mainDiv}>
              <div style={jsxStyles.pictureNameTopRow}>
                {/* <img src='carapuce.jpeg' style={jsxStyles.profilePicture}/> */}
                {<img src={user?.picture} style={jsxStyles.profilePicture}/>}
                {user?.username}
              </div>
              <div style={{...jsxStyles.biography, ...((!user?.short_bio) ? {color: 'grey'} : {color: 'inherit'})}}>
                {user?.short_bio || 'écrire une description ...'}
              </div>
              <div>
                sex: {user?.gender || 'inconnue'}
              </div>
              <div>
                recherche: {user?.search_male ? "♂" : null} {user?.search_female ? "♀" : null} {user?.search_other ? "⚧" : null}
              </div>
              <div>
                <p>
                  inscit depuis:
                  <>{user?.created_on}</>
                </p>
              </div>
              <div>
                tag
              </div>
              score de popularité: {user?.public_popularity ??= 'aucune visite sur votre profile pour le moment'}
              <button style={{
                borderRadius:'2vh',
                borderWidth:'0.1vh',
                textAlign:'center',
                paddingInline: '1vmax',
                padding: '2vmin',
              }} onClick={(event) => {
                event.preventDefault()
                window.location.href = '/updateProfile'
              }}>
                Modifier le profile🖊
              </button>
            </form>
          </div>
        </div>
      )
    }
  }
