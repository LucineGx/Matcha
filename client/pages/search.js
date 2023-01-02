import Head from 'next/head'
import React, { useEffect, useState } from 'react'
import styles from '../styles/Home.module.css'
import stylesForCircle from '../styles/circle.module.css'
import { toast } from 'react-toastify'
import { pushRequest } from './api/apiUtils'
import { formatBase64Jpeg } from './api/formatBase64Jpeg'
import { useRouter } from 'next/router'
import { sleep } from './utils/sleep'
import SearchBar from '../components/sreachBar'

const notify = (txt) => toast(txt)
const logoutIcon = (logoutFn) => <img onClick={logoutFn} src='on-off-button.png' style={{
  height: '5vmin',
  margin: '1vmin',
  cursor: 'pointer',
}}/>
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
    width: '10vh',
    height: '10vh',
    margin: '15vh',
    position: 'fixed',
    zIndex: 100
  },
  profilePictureLoader: {
    backgroundColor: 'yellow',
    backgroundSize: 'cover',
    display:'flex'
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

/** @typedef {import('./type/userInfo').UserInfo} UserInfo*/

const useMountEffect = (fun) => useEffect(fun, [])

/** @param { number } vh */
const vhToPixel = vh => Math.round(window.innerHeight / (100 / vh))

export default function Profile() {
  const router = useRouter()
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
      router.push('/login')
    } catch (e) {
      console.error(e)
    }
  }
  /** @type {[UserInfo, import('react').Dispatch<import('react').SetStateAction<{}>>]} */
  const [user, setUser] = useState(/**@type {UserInfo}*/{})
  const [isLoaded, setisLoaded] = useState(false)
  const [people, setPeople] = useState(/**@type {UserInfo[]}*/[])

  const loadData = async () => {
    const curUser = await pushRequest('user/', 'GET')
    if (!curUser)
      router.push('/login')
    setUser(curUser)
    await sleep(2000)
    setisLoaded(true)
  }
  if (typeof window === "undefined") {
    //bypass ssr
    return null
  } else {
      useEffect( async () => {
        await loadData()
        return () => {}
      }, [] )
      if (!user && !user?.email)
        router.push('/login')
      if (user && user.picture) {
        user.picture = formatBase64Jpeg(user.picture)
      }
      if (isLoaded !== true) {
        return (
          <div className={styles.bgPicture}>
            <div className={styles.container} style={{}}>
              <Head>
                <title>Pokélove</title>
                <meta name="description" content="Generated by a lot of redbull" />
                <link rel="icon" href="/logo.png" />
              </Head>
              {logoutIcon(logout)}
              <main className={styles.main}>
              <p style={{color: 'white', position:'fixed', top: '1vmin'}}>looking for users...</p>
                {<img src={user?.picture} style={jsxStyles.profilePicture}/>}
                <div className={stylesForCircle.circle} style={{animationDelay: '0s'}}/>
                <div className={stylesForCircle.circle} style={{animationDelay: '1s'}}/>
                <div className={stylesForCircle.circle} style={{animationDelay: '2s'}}/>
                <div className={stylesForCircle.circle} style={{animationDelay: '3s'}}/>
              </main>
            </div>
          </div>
        )
      }
      return (
        <div className={styles.bgPicture}>
          <div className={styles.container}>
            <Head>
              <title>Pokélove</title>
              <meta name="description" content="Generated by a lot of redbull" />
              <link rel="icon" href="/logo.png" />
            </Head>
            {logoutIcon(logout)}
            <main className={styles.main}>
              <SearchBar/>
            </main>
            <button onClick={() => {setisLoaded(!isLoaded)}}>pouette</button>
          </div>
        </div>
      )
    }
  }
