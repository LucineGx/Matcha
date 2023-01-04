import stylesForCircle from '../styles/circle.module.css'
import styles from '../styles/Home.module.css'

export default function Loader (props) {
  const user = props.userPicture
  return (
    <main className={styles.main}>
      <p style={{color: 'white', position:'fixed', top: '1vmin'}}>looking for users...</p>
      {<img src={user?.picture} style={jsxStyles.profilePicture}/>}
      <div className={stylesForCircle.circle} style={{animationDelay: '0s'}}/>
      <div className={stylesForCircle.circle} style={{animationDelay: '1s'}}/>
      <div className={stylesForCircle.circle} style={{animationDelay: '2s'}}/>
      <div className={stylesForCircle.circle} style={{animationDelay: '3s'}}/>
    </main>
  )
}

/**
 * @type {{ [key:string]: React.CSSProperties }}
 */
const jsxStyles = {
  profilePicture: {
    borderRadius: '100%',
    width: '10vh',
    height: '10vh',
    margin: '15vh',
    position: 'fixed',
    zIndex: 100
  }
}