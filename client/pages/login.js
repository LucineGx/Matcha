import Head from 'next/head'
import Image from 'next/image'
import { toast } from 'react-toastify'
import styles from '../styles/Home.module.css'

const notify = (txt) => toast(txt)

/**
 * @type {{ [key:string]: React.CSSProperties }}
 */
const jsxStyles = {
  base: {
    borderRadius:'2vh',
    borderWidth:'0.1vh',
    textAlign:'center',
    paddingInline: '10%'
  },
  input: {
    paddingInline: '1vh'
  },
  button: {
    color:'#cacaca',
    padding: '10%'
  }
}

export default function Login() {
  if (typeof window === "undefined") {
    //bypass ssr
    return (
      <>
      </>
    )
  }
  const connect = async event => {
    event.preventDefault()
    const { userName, password } = event.target
    var formdata = new FormData()
    formdata.append('username', userName.value)
    formdata.append('password', password.value)

    try {
      const res = await fetch('http://127.0.0.1:5000/auth/login', {
        body: formdata,
        method: 'POST',
        credentials: 'include',
        mode: 'cors'
      })
      // debugger
      if (res.status === 200) {
        const userinfo = await res.json()
        // debugger
        console.log('redirect to profile page', userinfo)
        if (typeof window !== "undefined"){
          localStorage.setItem('userInfo', JSON.stringify(userinfo))
          window.location.href = '/profile'
        }
      } else {
        notify(await res.text())
      }
    } catch (err) {
      console.error(err)
    }
  }
  /** @param { number } vh */
  const vhToPixel = vh => Math.round(window.innerHeight / (100 / vh))

  return (
    <div className={styles.container}>
      <Head>
        <title>Pokélove - login</title>
        <meta name="description" content="Generated by a lot of redbull" />
        <link rel="icon" href="/logo.png" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Connexion
        </h1>

        <form style={{
          justifyContent: 'space-evenly',
          display: 'flex',
          flexDirection: 'column',
          padding: '1vh'
        }} onSubmit={connect}>
          <input id="userName" name="userName" placeholder="Nom d'utilisateur"
            size={vhToPixel(4.8)}
            style={{...jsxStyles.base, ...jsxStyles.input}}
            type="text" required/>
          <br/>
          <input id="password" name="password" size={vhToPixel(5)}
            type="text" placeholder="Mot de passe"
            style={{...jsxStyles.base, ...jsxStyles.input}}
            required />
          <br/>
          <button type="submit" className={styles.card}
            style={{...jsxStyles.base, ...jsxStyles.button}}>
            Ce connecter
          </button>
        </form>
      </main>
    </div>
  )
}
