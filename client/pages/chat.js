import Head from 'next/head'
import { useRouter } from 'next/router'
import { toast } from 'react-toastify'
import styles from '../styles/Home.module.css'
import ChatPopup from './popupchat'

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
  const router = useRouter()
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
      if (res.status === 200) {
        const userinfo = await res.json()
        // debugger
        console.log('redirect to profile page', userinfo)
        if (typeof window !== "undefined"){
          localStorage.setItem('userInfo', JSON.stringify(userinfo))
          router.push('/profile')
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
        <ChatPopup/>
      </main>
    </div>
  )
}
