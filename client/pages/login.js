import Head from 'next/head'
import Image from 'next/image'
import { toast } from 'react-toastify'
import styles from '../styles/Home.module.css'

const notify = (txt) => toast(txt)


export default function Login() {
  const connect = async event => {
    event.preventDefault()
    const { userName, password } = event.target
    var formdata = new FormData()
    formdata.append('userName', userName.value)
    formdata.append('password', password.value)

    try {
      const res = await globalThis.fetch('http://127.0.0.1:5000/auth/login', {
        body: formdata,
        method: 'POST'
      })
      if (res.status === 200) {
        console.log('redirect to profile page')
        window.location.href = '/profile'
      } else {
        notify(await res.text())
      }
    } catch (err) {
      throw Error(err)
    }

    // result.user => 'john Doe'
  }

  return (
    <div className={styles.container}>
      <Head>
        <title>Pokélove - register</title>
        <meta name="description" content="Generated by a lot of redbull" />
        <link rel="icon" href="/logo.png" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Connexion
        </h1>

        <form onSubmit={connect}>
          <input id="userName" name="userName" placeholder="Nom d'utilisateur"
            style={{borderRadius:'5vh', borderWidth:'0.1vh', textAlign:'center'}}
            type="text" required
          />
          <br/>
          <input id="password" name="password"
            type="password" placeholder="Mot de passe"
            style={{borderRadius:'5vh', borderWidth:'0.1vh', textAlign:'center'}}
            required
          />
          <br/>
          <button type="submit" className={styles.card}
            style={{borderRadius:'5vh', borderWidth:'0.1vh', textAlign:'center', color:'#cacaca'}}
          >
            Ce connecter
          </button>

        </form>

      </main>
    </div>
  )
}
