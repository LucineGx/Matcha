import Head from 'next/head'
import Link from 'next/link'
import styles from '../styles/Home.module.css'

export default function Home() {
  if (typeof window !== "undefined"){
    return (
      <div className={styles.bgPicture}>
        <div className={styles.container} style={{opacity: '60%'}}>
          <Head>
            <title>Pokélove</title>
            <meta name="description" content="Generated by a lot of redbull" />
            <link rel="icon" href="/logo.png" />
          </Head>
          <main className={styles.main}>
            <h1 className={styles.title}>
              Welcome to Pokélove
            </h1>
            <div className={styles.grid}>
              <div className={styles.card}>
                <Link href="./register">
                  <h2>Inscription</h2>
                </Link>
              </div>
              <div className={styles.card}>
                <Link href="./login">
                  <p> Ce connecter </p>
                </Link>
              </div>
            </div>
          </main>
        </div>
      </div>
    )
  } else {
    return null
  }
}
