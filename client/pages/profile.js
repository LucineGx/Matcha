import Head from 'next/head'
import Image from 'next/image'
import React from 'react'
import styles from '../styles/Home.module.css'
import { toast } from 'react-toastify'
const notify = (txt) => toast(txt)

let user

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
    borderRadius: '100vh',
    width: '20vh',
    marginRight: '15px',
    position: 'static',
    left: '30%',
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

/* @type {import('./type/userInfo').UserInfo} */

export default function Profile() {
  if (typeof window === "undefined") {
    //bypass ssr
    return null
  } else {
    user = JSON.parse(localStorage.getItem("userInfo"))
    if (!user){
      window.location.href = '/login'
      return null
    } else
      console.log(user)
    let lol = 0
    return (
      <div className={styles.container} style={{}}>
        <Head>
          <title>Pokélove</title>
          <meta name="description" content="Generated by a lot of redbull" />
          <link rel="icon" href="/logo.png" />
        </Head>
        <div className={styles.main}>
          <form style={jsxStyles.mainDiv}>
            <div style={jsxStyles.pictureNameTopRow}>
              <img src='carapuce.jpeg' style={jsxStyles.profilePicture}/>
              {user.username}
            </div>
            popularité
            <div style={{...jsxStyles.biography, ...((!user.short_bio) ? {color: 'grey'} : {color: 'inherit'})}}>
              {user.short_bio || 'écrire une description ...'}
            </div>
            <div>
              sex: {user.gender || 'inconnue'}
            </div>
            <div>
              recherche: {user.search_male ? "♂" : null} {user.search_female ? "♀" : null} {user.search_other ? "⚧" : null}
            </div>
            <div>
              inscit depuis: {user.created_on}
            </div>
            <div>
              tag
            </div>
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
