import Head from 'next/head'
import Image from 'next/image'
import { useRouter } from 'next/router'
import { toast } from 'react-toastify'
import styles from '../styles/Home.module.css'

const notify = (txt) => toast(txt)

/**
 * @type {{ [key:string]: React.CSSProperties }}
 */
const jsxStyles = {
  base: {
    borderRadius:'5vh',
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
  const router = useRouter()
  if (typeof window === "undefined") {
    //bypass ssr
    return (
      <>
        <div className={styles.container}>
          caca
        </div>
      </>
    )
  }
  const connect = async event => {
    event.preventDefault()
    const { email, password } = event.target
    var formdata = new FormData()
    formdata.append('email', email.value)

    try {
      const res = await globalThis.fetch('http://127.0.0.1:5000/auth/forgot-password', {
        body: formdata,
        method: 'POST'
      })
      if (res.status === 200) {
        console.log('redirect to profile page')
        router.push('/login')
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
        <title>Pokélove - register</title>
        <meta name="description" content="Generated by a lot of redbull" />
        <link rel="icon" href="/logo.png" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Réinitialiser
        </h1>

        <form style={{
          justifyContent: 'space-evenly',
          display: 'flex',
          flexDirection: 'column',
          padding: '1vh'
        }} onSubmit={connect}>
          <input id="email" name="email" placeholder="email@exemple.com"
            size={vhToPixel(4.8)}
            style={{...jsxStyles.base, ...jsxStyles.input}}
            type="text" required/>
          <br/>
          <button type="submit" className={styles.card}
            style={{...jsxStyles.base, ...jsxStyles.button}}>
            Envoyer
          </button>
        </form>
      </main>
    </div>
  )
}
